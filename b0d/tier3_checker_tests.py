#!/usr/bin/env python3
"""Planted-failure test suite for `tier3_checker.py`.

At least 18 cases per §7 C4 (B0m2 expansion):
  Golden path                                 — 1 case: exit 0.
  Check (i)   prompt hash tampered            — 3 cases
  Check (ii)  sample tampered                 — 3 cases
  Check (iii) blinded field leaked            — 3 cases
  Check (iv)  model revision drifted          — 3 cases
  Check (v)   response-id absent              — 1 case
  Check (v)   response-metadata hash drifted  — 1 case
  Check (vi.a) token absent                   — 1 case
  Check (vi.a) token count below N            — 1 case
  Check (vi.a) token count above N            — 1 case
  Check (vi.b) imprint drifted                — 1 case
  Check (vi.c) signature invalid              — 1 case
  Check (vii)  collapse-rule mismatch         — 3 cases:
      (a) aggregate verdict differs from the recomputed collapse;
      (b) one-of-three-parsing row published as the lone run's verdict
          instead of the default "trivial" (+ marker);
      (c) zero-parsing row published with a fabricated rationale instead
          of the empty string plus the default-no-contributing-run marker.
  Exit-code convention: malformed input       — 1 case (rc=1)

Total: 23 subprocess cases, plus the pure-function unit tests in
`CollapseRuleUnitTests` that pin every clause of the §6.3 collapse rule
(committed-N denominator, counts-against-the-threshold treatment of
unparseable runs, tie → "trivial", genTime ordering, envelope-hash
tie-break, no-contributing-run marker) against synthetic inputs — those
are non-circular: they do not touch the fixture builder below.

Each new (vi.*) case asserts the specific sub-boolean flipped and the
specific exit code — exercise-counted per the fire order. Each (vii)
case asserts `collapse_rule_match` flipped false for exactly the planted
seat, true for the other two, and exit 2.

Python stdlib only. The suite uses cached RFC-3161 tokens in
`scripts/b3/testdata/tokens/` (keyed by SHA-256 imprint) so it runs
hermetic after a one-shot bootstrap. On cache miss the bootstrap fetches
fresh tokens from the pinned TSAs and writes them to the cache directory
(that path is the ONLY place in the test suite that touches the network,
and it only runs when the cache is empty).

Run:
    python3 scripts/b3/tier3_checker_tests.py
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


HERE = os.path.dirname(os.path.abspath(__file__))
CHECKER_PATH = os.path.join(HERE, "tier3_checker.py")
TOKEN_CACHE_DIR = os.path.join(HERE, "testdata", "tokens")

sys.path.insert(0, HERE)
import panel_run_harness  # noqa: E402
import tier3_checker  # noqa: E402


# ---------------------------------------------------------------------------
# Token cache — hermetic-after-bootstrap.
# ---------------------------------------------------------------------------

# Non-pinned TSA endpoint used for the "signature invalid" case: we ask a
# TSA that is not in the pinned .pem set to sign a token, then verify it
# against the pinned primary .pem. It fails, which is exactly what the
# check should catch.
_UNPINNED_TSA_URL = "http://timestamp.sectigo.com"  # pinned as FALLBACK
_UNPINNED_TAG_AS_PRIMARY = True  # in the test we mislabel this as primary


def _cache_path(imprint_hex, identity):
    fname = "%s__%s.tsr" % (imprint_hex, identity)
    return os.path.join(TOKEN_CACHE_DIR, fname)


def _fetch_token(imprint_bytes, endpoint):
    """Fetch a fresh token from an endpoint. Only used to fill the cache."""
    tsq = panel_run_harness.build_tsq(imprint_bytes, cert_req=True)
    import urllib.request
    req = urllib.request.Request(
        endpoint, data=tsq, method="POST",
        headers={"Content-Type": "application/timestamp-query"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def _get_or_mint_token(envelope_bytes, identity):
    """Return the cached token bytes for this envelope+identity pair.

    On cache miss (first bootstrap), fetch from the corresponding TSA and
    write to the cache directory. All subsequent test runs are hermetic.
    """
    imprint = hashlib.sha256(envelope_bytes).hexdigest()
    path = _cache_path(imprint, identity)
    if os.path.isfile(path):
        with open(path, "rb") as fh:
            return fh.read()
    endpoint = {
        "primary": panel_run_harness.TSA_PRIMARY["endpoint"],
        "fallback": panel_run_harness.TSA_FALLBACK["endpoint"],
        "unpinned": _UNPINNED_TSA_URL,
    }[identity]
    imprint_bytes = bytes.fromhex(imprint)
    tsr = _fetch_token(imprint_bytes, endpoint)
    os.makedirs(TOKEN_CACHE_DIR, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(tsr)
    return tsr


def _make_notarize_fn(identity="primary"):
    """Return a notarize_fn injectable for publish_panel_checker_artifacts.

    Reads/writes the on-disk cache. The default identity is 'primary';
    tests that want fallback-identity tokens override.
    """
    def _fn(envelope_canonical_bytes):
        tsr = _get_or_mint_token(envelope_canonical_bytes, identity)
        return tsr, identity
    return _fn


# ---------------------------------------------------------------------------
# Fixture builder — the golden-path panel-run state every test starts from.
# ---------------------------------------------------------------------------

SAMPLE_BYTES = json.dumps(
    [{"property_id": "anchor-%04d" % i,
      "visible_field": "predicate-%d" % i}
     for i in range(1, 9)],
    ensure_ascii=False, sort_keys=True, separators=(",", ":"),
).encode("utf-8")

BLINDED_FIELDS = [
    "SECRET_PROVIDER_TOKEN_alpha",
    "SECRET_PROVIDER_TOKEN_bravo",
]


def _adj_prompts(adj):
    """Golden system + user-template + actual-user bytes for one adjudicator."""
    system = (
        "You are Tier-3 panel scorer %s. Score each row as trivial or "
        "non-trivial. Return JSON.\n" % adj
    ).encode("utf-8")
    template = (
        "Score the following blind sample rows:\n{BLIND_SAMPLE_ROWS}\n"
    ).encode("utf-8")
    actual = template.replace(b"{BLIND_SAMPLE_ROWS}", SAMPLE_BYTES)
    return system, template, actual


# Per-seat fixtures. Each seat gets N=3 runs, each with a distinct
# response_id and slightly-varying usage counts so the envelope hashes
# differ across runs (which is what happens in reality — usage totals
# rarely repeat across independent invocations).
_SEAT_FIXTURES = {
    "A1": {
        "provider": "OpenAI",
        "api_model_identifier": "gpt-5.6-sol",
        "pinned_model_revision": "gpt-5.6-sol",
        "runs": [
            {"response_id": "resp_A1_run0_abc",
             "usage_in": 4321, "usage_out": 199,
             "fp": "fp_a1_00000000"},
            {"response_id": "resp_A1_run1_def",
             "usage_in": 4322, "usage_out": 200,
             "fp": "fp_a1_11111111"},
            {"response_id": "resp_A1_run2_ghi",
             "usage_in": 4323, "usage_out": 201,
             "fp": "fp_a1_22222222"},
        ],
    },
    "A2": {
        "provider": "Fireworks",
        "api_model_identifier": "accounts/fireworks/models/deepseek-v4-pro",
        "pinned_model_revision":
            "deepseek-ai/DeepSeek-V4-Pro@rev_1234567890abcdef",
        "runs": [
            {"response_id": "fw-msg-a2-run0",
             "usage_in": 4400, "usage_out": 220, "fp": None},
            {"response_id": "fw-msg-a2-run1",
             "usage_in": 4401, "usage_out": 221, "fp": None},
            {"response_id": "fw-msg-a2-run2",
             "usage_in": 4402, "usage_out": 222, "fp": None},
        ],
    },
    "A3": {
        "provider": "Anthropic",
        "api_model_identifier": "claude-opus-5",
        "pinned_model_revision": "claude-opus-5",
        "runs": [
            {"response_id": "msg_run0_CdWjMejrrdhoXtQxN7k4R",
             "usage_in": 4500, "usage_out": 240, "fp": None},
            {"response_id": "msg_run1_CdWjMejrrdhoXtQxN7k4R",
             "usage_in": 4501, "usage_out": 241, "fp": None},
            {"response_id": "msg_run2_CdWjMejrrdhoXtQxN7k4R",
             "usage_in": 4502, "usage_out": 242, "fp": None},
        ],
    },
}


def _golden_per_scorer():
    per = {}
    for adj, cfg in _SEAT_FIXTURES.items():
        sys_bytes, tmpl_bytes, actual_bytes = _adj_prompts(adj)
        runs = []
        for r in cfg["runs"]:
            resp = {
                "id": r["response_id"],
                "model": cfg["api_model_identifier"],
                "type": "message" if adj == "A3" else "chat.completion",
                "stop_reason": "end_turn" if adj != "A1" else "stop",
                "usage": {"input_tokens": r["usage_in"],
                          "output_tokens": r["usage_out"]},
                "content": [{"type": "text", "text": "<message body>"}],
            }
            if r["fp"]:
                resp["system_fingerprint"] = r["fp"]
            runs.append({
                "provider": cfg["provider"],
                "api_model_identifier": cfg["api_model_identifier"],
                "pinned_model_revision": cfg["pinned_model_revision"],
                "response_id": r["response_id"],
                "system_prompt_bytes": sys_bytes,
                "user_prompt_template_bytes": tmpl_bytes,
                "user_prompt_actual_bytes": actual_bytes,
                "raw_response": resp,
            })
        per[adj] = {
            "commit": {
                "provider": cfg["provider"],
                "api_model_identifier": cfg["api_model_identifier"],
                "pinned_model_revision": cfg["pinned_model_revision"],
                "system_prompt_sha256":
                    tier3_checker.canonical_hash(sys_bytes),
                "user_prompt_template_sha256":
                    tier3_checker.canonical_hash(tmpl_bytes),
            },
            "runs": runs,
        }
    return per


def _publish(panel_dir, per_scorer=None, sample=None, blinded=None,
             notarize_fn=None):
    if notarize_fn is None:
        notarize_fn = _make_notarize_fn("primary")
    return panel_run_harness.publish_panel_checker_artifacts(
        panel_dir=panel_dir,
        per_scorer=per_scorer if per_scorer is not None else _golden_per_scorer(),
        sample_bytes=sample if sample is not None else SAMPLE_BYTES,
        blinded_field_values=blinded if blinded is not None else BLINDED_FIELDS,
        notarize_fn=notarize_fn,
    )


# ---------------------------------------------------------------------------
# Check (vii) fixtures — per-run outputs + published aggregate.
#
# No live panel run exists yet (B3 has not fired), so these fixtures DEFINE
# the artifact shape check (vii) consumes: one `run-output.json` per run dir
# (the scorer's raw per-row JSON output, an array of
# {property_id, verdict, rationale} objects) and `panel/aggregate.json` per
# §6.3 (the three count fields, section3 count, and panel_disagreement_rows
# entries shaped {property_id, seats: {A1|A2|A3: {verdict, rationale
# [, marker]}}}).
#
# Golden verdict design: A1/A3 vote non-trivial on anchor-0001 only; A2 on
# anchor-0001 and anchor-0002. All three runs of every seat agree, so the
# golden collapse is a clean 3-of-3 everywhere, the majority and unanimous
# counts are both 1 (anchor-0001), and anchor-0002 is the one disagreement
# row (A2 non-trivial vs A1/A3 trivial).
#
# The golden aggregate is built by running the checker's OWN recomputation
# over the golden run artifacts (so the rationale selection — earliest
# cached-token genTime, envelope-hash tie-break — is exactly what the rule
# produces; the cached tokens carry second-precision genTimes with real
# ties, so the tie-break path is live). That construction is deliberately
# circular for the golden path; the NON-circular verification of the rule
# itself lives in CollapseRuleUnitTests, and the three planted cases mutate
# away from the golden aggregate and must be caught.
# ---------------------------------------------------------------------------

GOLDEN_NONTRIVIAL = {
    "A1": {"anchor-0001"},
    "A2": {"anchor-0001", "anchor-0002"},
    "A3": {"anchor-0001"},
}

ALL_ROW_IDS = ["anchor-%04d" % i for i in range(1, 9)]


def _golden_run_output_rows(adj, run_idx):
    rows = []
    for pid in ALL_ROW_IDS:
        verdict = ("non-trivial" if pid in GOLDEN_NONTRIVIAL[adj]
                   else "trivial")
        rows.append({
            "property_id": pid,
            "verdict": verdict,
            "rationale": "rationale %s run-%d %s" % (adj, run_idx, pid),
        })
    return rows


def _run_output_path(panel_dir, adj, run_idx):
    return os.path.join(panel_dir,
                        "checker-inputs/%s/run-%d/run-output.json"
                        % (adj, run_idx))


def _write_run_outputs(panel_dir):
    for adj in ("A1", "A2", "A3"):
        for i in range(3):
            raw = json.dumps(_golden_run_output_rows(adj, i),
                             ensure_ascii=False, indent=2)
            with open(_run_output_path(panel_dir, adj, i), "w",
                      encoding="utf-8") as fh:
                fh.write(raw + "\n")


def _recompute_all(panel_dir):
    """The checker's own collapse recomputation over the panel on disk."""
    top = tier3_checker.load_checker_input(panel_dir)
    sample_ids = tier3_checker._load_sample_row_ids(panel_dir, top)
    return sample_ids, {
        adj: tier3_checker.recompute_seat_collapse(
            panel_dir, top["adjudicators"][adj], top["committed_n"],
            sample_ids)
        for adj in ("A1", "A2", "A3")
    }


def _aggregate_from_recompute(sample_ids, rec):
    adjs = ("A1", "A2", "A3")
    per_adj = {
        a: sum(1 for pid in sample_ids
               if rec[a][pid]["verdict"] == "non-trivial")
        for a in adjs
    }
    majority = 0
    unanimous = 0
    for pid in sample_ids:
        nt = sum(1 for a in adjs
                 if rec[a][pid]["verdict"] == "non-trivial")
        if nt >= 2:
            majority += 1
        if nt == 3:
            unanimous += 1
    disagreement = []
    for pid in sample_ids:
        verdicts = {rec[a][pid]["verdict"] for a in adjs}
        any_marker = any(rec[a][pid]["no_contributing_run"] for a in adjs)
        if len(verdicts) > 1 or any_marker:
            seats = {}
            for a in adjs:
                entry = {"verdict": rec[a][pid]["verdict"],
                         "rationale": rec[a][pid]["rationale"]}
                if rec[a][pid]["no_contributing_run"]:
                    entry["marker"] = "default-no-contributing-run"
                seats[a] = entry
            disagreement.append({"property_id": pid, "seats": seats})
    return {
        "panel_nontrivial_count_per_adjudicator": per_adj,
        "panel_nontrivial_count_majority": majority,
        "panel_nontrivial_count_unanimous": unanimous,
        "section3_nontrivial_count_on_sample": 1,
        "panel_disagreement_rows": disagreement,
    }


def _write_aggregate(panel_dir, aggregate):
    path = os.path.join(panel_dir, "aggregate.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(aggregate, fh, ensure_ascii=False, indent=2,
                  sort_keys=True)
        fh.write("\n")


def _write_true_aggregate(panel_dir):
    """Publish the aggregate the §6.3 rule actually produces from disk."""
    sample_ids, rec = _recompute_all(panel_dir)
    _write_aggregate(panel_dir, _aggregate_from_recompute(sample_ids, rec))


def _mutate_run_output(panel_dir, adj, run_idx, mutator):
    path = _run_output_path(panel_dir, adj, run_idx)
    with open(path, "r", encoding="utf-8") as fh:
        rows = json.load(fh)
    rows = mutator(rows) or rows
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def _mutate_aggregate(panel_dir, mutator):
    path = os.path.join(panel_dir, "aggregate.json")
    with open(path, "r", encoding="utf-8") as fh:
        agg = json.load(fh)
    mutator(agg)
    _write_aggregate(panel_dir, agg)


def _disagreement_entry(aggregate, pid):
    for row in aggregate["panel_disagreement_rows"]:
        if row["property_id"] == pid:
            return row
    raise AssertionError("no disagreement row for %s" % pid)


def _run_checker(panel_dir):
    """Invoke tier3_checker.py as a subprocess. Returns (rc, stdout, stderr)."""
    proc = subprocess.run(
        [sys.executable, CHECKER_PATH, "--panel-dir", panel_dir],
        capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _parse_records(stdout):
    recs = {}
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        recs[rec["adjudicator"]] = rec
    return recs


def _mutate_checker_json(panel_dir, mutator):
    path = os.path.join(panel_dir, "checker.json")
    with open(path, "r", encoding="utf-8") as fh:
        top = json.load(fh)
    mutator(top)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(top, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")


def _mutate_file_bytes(panel_dir, relpath, mutator):
    path = os.path.join(panel_dir, relpath)
    with open(path, "rb") as fh:
        raw = fh.read()
    with open(path, "wb") as fh:
        fh.write(mutator(raw))


# ---------------------------------------------------------------------------
# Test class.
# ---------------------------------------------------------------------------

class Tier3CheckerTests(unittest.TestCase):
    """20 planted-failure cases per §7 C4 (B0m2 expansion)."""

    # Class-level golden panel so we bootstrap tokens exactly once. Each
    # test's setUp copies the golden panel to a fresh tmp dir and mutates.
    _CLASS_TMP = None
    _GOLDEN_PANEL = None

    @classmethod
    def setUpClass(cls):
        cls._CLASS_TMP = tempfile.mkdtemp(prefix="p032_tier3_golden_")
        cls._GOLDEN_PANEL = os.path.join(cls._CLASS_TMP, "panel")
        # This _publish call is what triggers any needed token minting
        # against the pinned TSAs (only on cache miss). Once the cache is
        # populated it runs offline.
        _publish(cls._GOLDEN_PANEL)
        # Check (vii) fixtures: per-run outputs, then the aggregate the
        # §6.3 collapse rule produces from them.
        _write_run_outputs(cls._GOLDEN_PANEL)
        _write_true_aggregate(cls._GOLDEN_PANEL)

    @classmethod
    def tearDownClass(cls):
        if cls._CLASS_TMP:
            shutil.rmtree(cls._CLASS_TMP, ignore_errors=True)

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="p032_tier3_test_")
        self.panel = os.path.join(self.tmp, "panel")
        shutil.copytree(self._GOLDEN_PANEL, self.panel)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # -- Golden path ------------------------------------------------------

    def test_00_golden_path(self):
        """All seven checks pass for A1, A2, A3 — exit 0, all booleans true."""
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 0, msg="stderr: %s\nstdout: %s" % (err, out))
        recs = _parse_records(out)
        for adj in ("A1", "A2", "A3"):
            for b in tier3_checker.CHECK_BOOLS:
                self.assertTrue(recs[adj][b],
                                msg="%s.%s should be true (rec=%r)"
                                    % (adj, b, recs[adj]))
            self.assertEqual(recs[adj]["notarization_token_count"], 3)
            self.assertEqual(recs[adj]["failure_reason"], "")

    # -- Check (i): prompt hash tampered (3 cases) ------------------------

    def test_01_i_system_prompt_bytes_tampered(self):
        """A1 system-prompt bytes mutated on disk vs. committed hash."""
        _mutate_file_bytes(
            self.panel, "checker-inputs/A1-system-prompt.txt",
            lambda b: b + b"trailing tamper\n",
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A1"]["prompt_hash_match"])
        self.assertIn("prompt_hash", recs["A1"]["failure_reason"])
        self.assertTrue(recs["A2"]["prompt_hash_match"])
        self.assertTrue(recs["A3"]["prompt_hash_match"])

    def test_02_i_user_template_bytes_tampered(self):
        """A2 user-prompt-template bytes mutated on disk."""
        _mutate_file_bytes(
            self.panel, "checker-inputs/A2-user-prompt-template.txt",
            lambda b: b.replace(b"{BLIND_SAMPLE_ROWS}", b"{OTHER_PLACEHOLDER}"),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A2"]["prompt_hash_match"])
        self.assertIn("user_prompt_template", recs["A2"]["failure_reason"])

    def test_03_i_committed_hash_drift(self):
        """A3 committed system-prompt hash mutated (commit drift, not bytes)."""
        _mutate_checker_json(
            self.panel,
            lambda top: top["adjudicators"]["A3"]["commit"].__setitem__(
                "system_prompt_sha256", "0" * 64),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A3"]["prompt_hash_match"])

    # -- Check (ii): sample tampered (3 cases) ----------------------------

    def test_04_ii_sample_bytes_mutated(self):
        _mutate_file_bytes(
            self.panel, "checker-inputs/blind-sample.json",
            lambda b: b.replace(b"anchor-0001", b"anchor-9999"),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        for adj in ("A1", "A2", "A3"):
            self.assertFalse(recs[adj]["sample_match"])

    def test_05_ii_sample_not_in_actual_user_prompt(self):
        _mutate_file_bytes(
            self.panel, "checker-inputs/A1-user-prompt-actual.txt",
            lambda b: b.replace(SAMPLE_BYTES, b"[REDACTED]"),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A1"]["sample_match"])
        self.assertTrue(recs["A2"]["sample_match"])
        self.assertTrue(recs["A3"]["sample_match"])

    def test_06_ii_committed_sample_hash_drift(self):
        _mutate_checker_json(
            self.panel,
            lambda top: top["sample"].__setitem__("sha256_committed", "0" * 64),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        for adj in ("A1", "A2", "A3"):
            self.assertFalse(recs[adj]["sample_match"])

    # -- Check (iii): blinded field leaked (3 cases) ----------------------

    def test_07_iii_blinded_leak_A1(self):
        _mutate_file_bytes(
            self.panel, "checker-inputs/A1-user-prompt-actual.txt",
            lambda b: b + b"\nleaked: " + BLINDED_FIELDS[0].encode("utf-8"),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A1"]["blinding_preserved"])
        self.assertTrue(recs["A2"]["blinding_preserved"])
        self.assertTrue(recs["A3"]["blinding_preserved"])

    def test_08_iii_blinded_leak_A2_case_insensitive(self):
        _mutate_file_bytes(
            self.panel, "checker-inputs/A2-user-prompt-actual.txt",
            lambda b: b + b"\nleak: " + BLINDED_FIELDS[1].upper().encode("utf-8"),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A2"]["blinding_preserved"])

    def test_09_iii_blinded_leak_A3(self):
        _mutate_file_bytes(
            self.panel, "checker-inputs/A3-user-prompt-actual.txt",
            lambda b: BLINDED_FIELDS[0].encode("utf-8") + b"\n" + b,
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A3"]["blinding_preserved"])

    # -- Check (iv): model revision drifted (3 cases) ---------------------

    def test_10_iv_provider_drift(self):
        """A1 runs[0].provider drifts from commit.provider."""
        _mutate_checker_json(
            self.panel,
            lambda top: top["adjudicators"]["A1"]["runs"][0].__setitem__(
                "provider", "OpenAI-mirror"),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A1"]["model_revision_match"])
        self.assertIn("provider", recs["A1"]["failure_reason"])

    def test_11_iv_api_model_identifier_drift(self):
        _mutate_checker_json(
            self.panel,
            lambda top: top["adjudicators"]["A2"]["runs"][1].__setitem__(
                "api_model_identifier",
                "accounts/fireworks/models/deepseek-v4-mini"),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A2"]["model_revision_match"])
        self.assertIn("api_model_identifier", recs["A2"]["failure_reason"])

    def test_12_iv_pinned_revision_drift(self):
        _mutate_checker_json(
            self.panel,
            lambda top: top["adjudicators"]["A3"]["runs"][2].__setitem__(
                "pinned_model_revision", "claude-opus-4.6-20250514"),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A3"]["model_revision_match"])
        self.assertIn("pinned_model_revision", recs["A3"]["failure_reason"])

    # -- Check (v): response-id + metadata hash (2 cases) -----------------

    def test_13_v_response_id_absent(self):
        _mutate_checker_json(
            self.panel,
            lambda top: top["adjudicators"]["A2"]["runs"][1].__setitem__(
                "response_id", ""),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A2"]["response_id_present"])
        self.assertIn("response_id", recs["A2"]["failure_reason"])
        self.assertTrue(recs["A2"]["response_metadata_hash_match"])
        self.assertTrue(recs["A1"]["response_id_present"])
        self.assertTrue(recs["A3"]["response_id_present"])

    def test_14_v_response_metadata_hash_drift(self):
        # Mutate A3 run-0 envelope on disk so its recomputed hash drifts.
        _mutate_file_bytes(
            self.panel, "checker-inputs/A3/run-0/response-metadata.json",
            lambda b: b.replace(b'"end_turn"', b'"tampered_stop_reason"'),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A3"]["response_metadata_hash_match"])
        self.assertIn("response_metadata", recs["A3"]["failure_reason"])
        self.assertTrue(recs["A3"]["response_id_present"])
        self.assertTrue(recs["A1"]["response_metadata_hash_match"])
        self.assertTrue(recs["A2"]["response_metadata_hash_match"])

    # -- Check (vi): notarization (5 new cases per fire order) ------------

    def test_15_vi_a_token_absent(self):
        """A1 run-1 notarization_token.tsr file deleted from disk.

        Exercise-counts: notarization_imprint_match flips false (can't
        parse a missing token), notarization_signature_valid flips false,
        notarization_token_count drops from 3 to 2, exit 2.
        """
        tok = os.path.join(self.panel,
                           "checker-inputs/A1/run-1/notarization_token.tsr")
        os.remove(tok)
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertEqual(recs["A1"]["notarization_token_count"], 2)
        self.assertFalse(recs["A1"]["notarization_imprint_match"])
        self.assertFalse(recs["A1"]["notarization_signature_valid"])
        self.assertIn("token file absent", recs["A1"]["failure_reason"])
        # Other seats unaffected.
        for adj in ("A2", "A3"):
            self.assertEqual(recs[adj]["notarization_token_count"], 3)
            self.assertTrue(recs[adj]["notarization_imprint_match"])
            self.assertTrue(recs[adj]["notarization_signature_valid"])

    def test_16_vi_a_token_count_below_N(self):
        """A2 declares only 2 runs (below committed N=3) after mutating the
        JSON to drop one run record; also physically removes the file.

        Exercise-counts: notarization_token_count = 2 vs committed_n = 3,
        exit 2, failure_reason names the count mismatch.
        """
        _mutate_checker_json(
            self.panel,
            lambda top: top["adjudicators"]["A2"]["runs"].pop(2),
        )
        # Also remove the on-disk file so a directory scan does not see it.
        shutil.rmtree(os.path.join(self.panel, "checker-inputs/A2/run-2"))
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertEqual(recs["A2"]["notarization_token_count"], 2)
        self.assertIn("notarization_token_count", recs["A2"]["failure_reason"])
        self.assertIn("committed N=3", recs["A2"]["failure_reason"])

    def test_17_vi_a_token_count_above_N(self):
        """A3 gets a spurious extra .tsr file added to a new run-3 subdir.

        Exercise-counts: notarization_token_count = 4 vs committed_n = 3,
        exit 2. The spurious file is not in the run records so the
        seat-directory sweep in check_notarization detects it.
        """
        extra_dir = os.path.join(self.panel, "checker-inputs/A3/run-3")
        os.makedirs(extra_dir)
        # Copy an existing token in as the "extra" — content doesn't matter
        # for the count check.
        src = os.path.join(self.panel,
                           "checker-inputs/A3/run-0/notarization_token.tsr")
        shutil.copy(src, os.path.join(extra_dir, "notarization_token.tsr"))
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertEqual(recs["A3"]["notarization_token_count"], 4)
        self.assertIn("notarization_token_count", recs["A3"]["failure_reason"])
        # The declared tokens are still fine, so signature+imprint stay ok.
        self.assertTrue(recs["A3"]["notarization_imprint_match"])
        self.assertTrue(recs["A3"]["notarization_signature_valid"])

    def test_18_vi_b_imprint_drifted(self):
        """A1 run-2 envelope mutated on disk AFTER the token was issued —
        the token's imprint no longer matches the recomputed envelope hash.

        Exercise-counts: notarization_imprint_match flips false, exit 2.
        Signature verification still passes (token itself is intact and
        binds to its ORIGINAL imprint), but the runner-published envelope
        drifted from what was notarized.
        """
        _mutate_file_bytes(
            self.panel, "checker-inputs/A1/run-2/response-metadata.json",
            lambda b: b.replace(b'"input_tokens":4323',
                                b'"input_tokens":9999'),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A1"]["notarization_imprint_match"])
        self.assertIn("imprint mismatch", recs["A1"]["failure_reason"])
        # Metadata-hash check (v) also fails, but that is not what THIS
        # test asserts against — the specific sub-boolean the fire order
        # wants exercised here is notarization_imprint_match.
        # Signature verification against the pinned pem still succeeds
        # because the token itself is untouched and its embedded imprint
        # is what we feed openssl for the -digest arg.
        self.assertTrue(recs["A1"]["notarization_signature_valid"])
        # Count is unchanged; three files are still on disk.
        self.assertEqual(recs["A1"]["notarization_token_count"], 3)

    def test_19_vi_c_signature_invalid(self):
        """A2 run-0 token replaced with a token issued by an UNPINNED TSA
        (not the pinned primary DigiCert cert). Verification against the
        pinned primary .pem fails.

        Exercise-counts: notarization_signature_valid flips false, exit 2.
        The imprint match still passes because the alien token binds to
        the same envelope hash.
        """
        # Build a valid envelope from the golden per_scorer for A2 run 0,
        # then get a token from a NON-pinned TSA (via the token cache
        # helper). We fetch/cache an "unpinned"-identity token for the
        # same imprint as the golden A2 run-0 envelope.
        env_path = os.path.join(self.panel,
                                "checker-inputs/A2/run-0/response-metadata.json")
        with open(env_path, "rb") as fh:
            env_bytes = fh.read()
        # Fetch a token from an unpinned endpoint for THIS imprint. Even
        # though the endpoint is Sectigo (which IS pinned as fallback),
        # the harness recorded this run as issued by PRIMARY, so
        # verification against the primary DigiCert pem fails —
        # signature-invalid case per the fire order.
        alien_token = _get_or_mint_token(env_bytes, "unpinned")
        tok_path = os.path.join(self.panel,
                                "checker-inputs/A2/run-0/notarization_token.tsr")
        with open(tok_path, "wb") as fh:
            fh.write(alien_token)
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        # Imprint match still true — the alien token was minted for the
        # SAME imprint. It's the signature that fails.
        self.assertTrue(recs["A2"]["notarization_imprint_match"])
        self.assertFalse(recs["A2"]["notarization_signature_valid"])
        self.assertIn("signature invalid", recs["A2"]["failure_reason"])
        self.assertEqual(recs["A2"]["notarization_token_count"], 3)

    # -- Check (vii): collapse-rule recomputation (3 planted cases) -------

    def test_20_vii_aggregate_verdict_differs(self):
        """(a) Published aggregate verdict differs from the recomputed
        collapse: the anchor-0002 disagreement entry publishes A2's verdict
        as "trivial" while all three of A2's runs returned "non-trivial".

        Exercise-counts: collapse_rule_match flips false for A2 only,
        exit 2, failure_reason names the row and both verdicts.
        """
        def plant(agg):
            entry = _disagreement_entry(agg, "anchor-0002")
            entry["seats"]["A2"]["verdict"] = "trivial"
        _mutate_aggregate(self.panel, plant)
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A2"]["collapse_rule_match"])
        self.assertIn("collapse_rule", recs["A2"]["failure_reason"])
        self.assertIn("anchor-0002", recs["A2"]["failure_reason"])
        self.assertTrue(recs["A1"]["collapse_rule_match"])
        self.assertTrue(recs["A3"]["collapse_rule_match"])
        self.assertEqual(recs["A1"]["failure_reason"], "")
        self.assertEqual(recs["A3"]["failure_reason"], "")

    def test_21_vii_lone_parsing_run_published_as_its_verdict(self):
        """(b) One-of-three-parsing row published as the lone run's verdict
        instead of the default "trivial": A1's run-1 and run-2 outputs on
        anchor-0003 are mutated to the non-literal verdict "indeterminate"
        (contributes nothing, still counts against the committed-N
        threshold), and run-0 — the lone run that parses — votes
        "non-trivial". One non-trivial vote out of the committed N=3 is
        not more than N/2, and no run returned the default "trivial", so
        the rule collapses A1/anchor-0003 to "trivial" with the empty
        rationale and the default-no-contributing-run marker. The planted
        aggregate instead publishes the lone parsing run's "non-trivial"
        with its rationale, no marker, and bumps A1's non-trivial count
        to match the lie.

        Exercise-counts: collapse_rule_match flips false for A1 only
        (count mismatch + verdict mismatch + rationale mismatch + marker
        mismatch), exit 2.
        """
        def lone_nontrivial(rows):
            for r in rows:
                if r["property_id"] == "anchor-0003":
                    r["verdict"] = "non-trivial"
            return rows
        def corrupt(rows):
            for r in rows:
                if r["property_id"] == "anchor-0003":
                    r["verdict"] = "indeterminate"
            return rows
        _mutate_run_output(self.panel, "A1", 0, lone_nontrivial)
        _mutate_run_output(self.panel, "A1", 1, corrupt)
        _mutate_run_output(self.panel, "A1", 2, corrupt)
        # The TRUE aggregate for the mutated panel (carries the marker row).
        sample_ids, rec = _recompute_all(self.panel)
        agg = _aggregate_from_recompute(sample_ids, rec)
        # Sanity on the plant's premise: the rule really does collapse
        # A1/anchor-0003 to default-"trivial" + marker.
        self.assertEqual(rec["A1"]["anchor-0003"]["verdict"], "trivial")
        self.assertEqual(rec["A1"]["anchor-0003"]["rationale"], "")
        self.assertTrue(rec["A1"]["anchor-0003"]["no_contributing_run"])
        # Plant: publish the lone run-0 verdict instead.
        entry = _disagreement_entry(agg, "anchor-0003")
        entry["seats"]["A1"] = {
            "verdict": "non-trivial",
            "rationale": "rationale A1 run-0 anchor-0003",
        }
        agg["panel_nontrivial_count_per_adjudicator"]["A1"] += 1
        _write_aggregate(self.panel, agg)
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A1"]["collapse_rule_match"])
        self.assertIn("collapse_rule", recs["A1"]["failure_reason"])
        self.assertIn("anchor-0003", recs["A1"]["failure_reason"])
        self.assertIn("default-no-contributing-run",
                      recs["A1"]["failure_reason"])
        self.assertTrue(recs["A2"]["collapse_rule_match"])
        self.assertTrue(recs["A3"]["collapse_rule_match"])
        self.assertEqual(recs["A2"]["failure_reason"], "")
        self.assertEqual(recs["A3"]["failure_reason"], "")

    def test_22_vii_zero_parsing_row_fabricated_rationale(self):
        """(c) Zero-parsing row published with a fabricated rationale
        instead of the empty string plus marker: every A3 run's output
        drops its anchor-0004 entry (no run contributes a verdict), so the
        rule collapses A3/anchor-0004 to "trivial", empty rationale,
        default-no-contributing-run marker. The planted aggregate keeps
        the "trivial" verdict but attaches a fabricated rationale and no
        marker.

        Exercise-counts: collapse_rule_match flips false for A3 only
        (rationale mismatch + marker mismatch; counts unchanged), exit 2.
        """
        def drop(rows):
            return [r for r in rows if r["property_id"] != "anchor-0004"]
        for i in range(3):
            _mutate_run_output(self.panel, "A3", i, drop)
        sample_ids, rec = _recompute_all(self.panel)
        agg = _aggregate_from_recompute(sample_ids, rec)
        self.assertEqual(rec["A3"]["anchor-0004"]["verdict"], "trivial")
        self.assertEqual(rec["A3"]["anchor-0004"]["rationale"], "")
        self.assertTrue(rec["A3"]["anchor-0004"]["no_contributing_run"])
        entry = _disagreement_entry(agg, "anchor-0004")
        entry["seats"]["A3"] = {
            "verdict": "trivial",
            "rationale": "fabricated: obviously fine on inspection",
        }
        _write_aggregate(self.panel, agg)
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 2, msg="stderr: %s" % err)
        recs = _parse_records(out)
        self.assertFalse(recs["A3"]["collapse_rule_match"])
        self.assertIn("collapse_rule", recs["A3"]["failure_reason"])
        self.assertIn("anchor-0004", recs["A3"]["failure_reason"])
        self.assertTrue(recs["A1"]["collapse_rule_match"])
        self.assertTrue(recs["A2"]["collapse_rule_match"])
        self.assertEqual(recs["A1"]["failure_reason"], "")
        self.assertEqual(recs["A2"]["failure_reason"], "")

    # -- Exit-code convention: malformed input → exit 1 -------------------

    def test_99_malformed_checker_json_exits_1(self):
        """Missing top-level key in checker.json → exit 1 (not 2)."""
        _mutate_checker_json(
            self.panel, lambda top: top.pop("blinded_field_values"),
        )
        rc, out, err = _run_checker(self.panel)
        self.assertEqual(rc, 1)
        self.assertEqual(out, "")
        self.assertIn("blinded_field_values", err)


# ---------------------------------------------------------------------------
# Non-circular unit tests for the §6.3 collapse rule itself.
#
# The golden aggregate above is built with the checker's own recomputation,
# which is fine for detecting drift but proves nothing about the rule. These
# tests pin every clause of `tier3_checker.collapse_votes` (and the genTime
# parser) against hand-computed synthetic inputs, no files involved.
# ---------------------------------------------------------------------------

def _vote(verdict, rationale="r", key=(0, (2026, 7, 30, 14, 55, 21,
                                           "000000000"), "aa" * 32)):
    return {"verdict": verdict, "rationale": rationale, "sort_key": key}


def _key(sec, env_hex):
    return (0, (2026, 7, 30, 14, 55, sec, "000000000"), env_hex)


class CollapseRuleUnitTests(unittest.TestCase):
    """§6.3 collapse rule, clause by clause, synthetic inputs."""

    def test_majority_two_of_three(self):
        out = tier3_checker.collapse_votes(
            [_vote("non-trivial", "a", _key(1, "aa" * 32)),
             _vote("non-trivial", "b", _key(2, "bb" * 32)),
             _vote("trivial", "c", _key(3, "cc" * 32))], 3)
        self.assertEqual(out["verdict"], "non-trivial")
        self.assertEqual(out["rationale"], "a")
        self.assertFalse(out["no_contributing_run"])

    def test_rationale_is_earliest_gentime_contributing_run(self):
        # Latest-listed run has the earliest genTime; ordering must follow
        # genTime, not list position.
        out = tier3_checker.collapse_votes(
            [_vote("trivial", "late", _key(9, "aa" * 32)),
             _vote("trivial", "mid", _key(5, "bb" * 32)),
             _vote("trivial", "early", _key(1, "cc" * 32))], 3)
        self.assertEqual(out["rationale"], "early")

    def test_gentime_tie_broken_by_ascending_envelope_hash(self):
        out = tier3_checker.collapse_votes(
            [_vote("trivial", "hash-ff", _key(1, "ff" * 32)),
             _vote("trivial", "hash-0a", _key(1, "0a" * 32)),
             _vote("trivial", "hash-bb", _key(1, "bb" * 32))], 3)
        self.assertEqual(out["rationale"], "hash-0a")

    def test_one_parsing_of_three_defaults_trivial_with_marker(self):
        # H13 clause (i): one contributing run out of three is NOT a
        # collapse — the two unparseable runs count against the threshold
        # instead of shrinking the denominator to 1.
        out = tier3_checker.collapse_votes(
            [_vote("non-trivial", "lone", _key(1, "aa" * 32)),
             _vote(None, "", _key(2, "bb" * 32)),
             _vote(None, "", _key(3, "cc" * 32))], 3)
        self.assertEqual(out["verdict"], "trivial")
        self.assertEqual(out["rationale"], "")
        self.assertTrue(out["no_contributing_run"])

    def test_zero_parsing_defaults_trivial_with_marker(self):
        # H13 clause (ii): zero contributing runs → "trivial", empty
        # rationale, default-no-contributing-run marker.
        out = tier3_checker.collapse_votes(
            [_vote(None, "", _key(1, "aa" * 32)),
             _vote(None, "", _key(2, "bb" * 32)),
             _vote(None, "", _key(3, "cc" * 32))], 3)
        self.assertEqual(out["verdict"], "trivial")
        self.assertEqual(out["rationale"], "")
        self.assertTrue(out["no_contributing_run"])

    def test_one_one_split_with_unparseable_defaults_trivial_no_marker(self):
        # 1 non-trivial, 1 trivial, 1 unparseable: nothing clears >N/2, so
        # default "trivial" — but a run DID return "trivial", so its
        # rationale publishes and no marker applies.
        out = tier3_checker.collapse_votes(
            [_vote("non-trivial", "nt", _key(1, "aa" * 32)),
             _vote("trivial", "the-trivial-run", _key(2, "bb" * 32)),
             _vote(None, "", _key(3, "cc" * 32))], 3)
        self.assertEqual(out["verdict"], "trivial")
        self.assertEqual(out["rationale"], "the-trivial-run")
        self.assertFalse(out["no_contributing_run"])

    def test_denominator_is_committed_n_not_published_run_count(self):
        # The H13 denominator clause: with only ONE published run record
        # and committed N = 3, the lone run's verdict does not clear the
        # threshold (1 is not > 3/2). A recomputation that shrank the
        # denominator to the published subset would return "non-trivial".
        out = tier3_checker.collapse_votes(
            [_vote("non-trivial", "lone", _key(1, "aa" * 32))], 3)
        self.assertEqual(out["verdict"], "trivial")
        self.assertTrue(out["no_contributing_run"])
        # Two published runs agreeing DO clear it (2 > 3/2).
        out = tier3_checker.collapse_votes(
            [_vote("non-trivial", "a", _key(1, "aa" * 32)),
             _vote("non-trivial", "b", _key(2, "bb" * 32))], 3)
        self.assertEqual(out["verdict"], "non-trivial")
        self.assertEqual(out["rationale"], "a")

    def test_unanimous_trivial(self):
        out = tier3_checker.collapse_votes(
            [_vote("trivial", "a", _key(1, "aa" * 32)),
             _vote("trivial", "b", _key(2, "bb" * 32)),
             _vote("trivial", "c", _key(3, "cc" * 32))], 3)
        self.assertEqual(out["verdict"], "trivial")
        self.assertEqual(out["rationale"], "a")
        self.assertFalse(out["no_contributing_run"])

    def test_parse_gen_time_second_precision(self):
        t = tier3_checker.parse_gen_time(
            "Some header\nTime stamp: Jul 30 14:55:21 2026 GMT\nAccuracy:")
        self.assertEqual(t, (2026, 7, 30, 14, 55, 21, "000000000"))

    def test_parse_gen_time_fractional_seconds_sort_before_next_second(self):
        t_frac = tier3_checker.parse_gen_time(
            "Time stamp: Jul 30 14:55:21.123 2026 GMT")
        t_next = tier3_checker.parse_gen_time(
            "Time stamp: Jul 30 14:55:22 2026 GMT")
        self.assertEqual(t_frac, (2026, 7, 30, 14, 55, 21, "123000000"))
        self.assertLess(t_frac, t_next)

    def test_parse_gen_time_absent_returns_none(self):
        self.assertIsNone(tier3_checker.parse_gen_time("no timestamp here"))


# ---------------------------------------------------------------------------
# Runner.
# ---------------------------------------------------------------------------

def _make_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(Tier3CheckerTests))
    suite.addTests(loader.loadTestsFromTestCase(CollapseRuleUnitTests))
    return suite


def main():
    suite = _make_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())

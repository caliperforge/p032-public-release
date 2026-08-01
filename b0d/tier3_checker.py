#!/usr/bin/env python3
"""P032 Tier-3 panel checker (§7 C4).

Verifies per-scorer commitments in `panel/checker.json` against the actual
prompt bytes, sample bytes, blinded field values, provider response
metadata, and RFC-3161 notarization tokens published under
`panel/checker-inputs/`. Also verifies, per check (vii), that the verdict
and rationale fed into `panel/aggregate.json` are the verdict and rationale
the §6.3 collapse rule produces from the published run artifacts. Emits one
JSON record per scorer to stdout and exits per the C4 convention:

    exit 0 — all seven checks passed for all three scorers
    exit 1 — the checker input was malformed
    exit 2 — at least one check failed for at least one scorer

Python standard library only for hashing, JSON, and I/O. Per the T-B0m2
ruling on the C4 invariant, `openssl ts -verify` is invoked via
`subprocess.run` against the pinned .pem trust anchor for check (vi.c)
signature verification — this is deterministic, offline, and uses only
local files. NO network call, NO LLM call, NO external service call is
issued from this script's execution path. C4 requires this; grep the
imports to verify.

Usage:
    python3 tier3_checker.py --panel-dir /path/to/panel [--out /path/to/log]

The seven checks (booleans per scorer per check):
    (i)   prompt_hash_match         — system + user-template bytes hash to
                                      the SHA-256 committed at B0d.
    (ii)  sample_match              — sample bytes on disk hash to the
                                      SHA-256 committed at B0d and the sample
                                      bytes appear verbatim in the actual
                                      user-prompt bytes each scorer received.
    (iii) blinding_preserved        — for each blinded field value V,
                                      V.lower() does not appear in the
                                      lower-cased UTF-8 user-prompt bytes.
    (iv)  model_revision_match      — the per-run provider, API model
                                      identifier, and pinned model revision
                                      equal the strings committed at B0d
                                      (all N runs).
    (v)   response_id_present +     — for all N runs: response_id is a
          response_metadata_hash_match  non-empty string, and the SHA-256 of
                                      the JCS-canonicalized response-
                                      metadata blob on disk equals the
                                      SHA-256 committed at B0d for that run.
    (vi)  notarization_token_count  — for each seat, exactly `committed_n`
                                      valid distinct RFC-3161 tokens exist
                                      under checker-inputs/<seat>/run-<i>/
                                      notarization_token.tsr.
          notarization_imprint_match — each token's message imprint equals
                                      SHA-256 of the JCS-canonical response
                                      envelope for that run.
          notarization_signature_valid — each token verifies via
                                      `openssl ts -verify` against the
                                      pinned .pem for the recorded TSA
                                      identity (primary or fallback).
    (vii) collapse_rule_match       — for each seat and each row of the
                                      blind sample, the checker recomputes
                                      the §6.3 collapse rule from the
                                      published per-run outputs (verdict
                                      returned by more than `N/2` of the
                                      committed `N` runs, denominator the
                                      committed `N` in every case;
                                      unparseable or non-literal `verdict`
                                      contributes nothing and counts
                                      against the threshold; no such
                                      verdict → `"trivial"`; rationale =
                                      earliest contributing run by
                                      RFC-3161 token `genTime`, ties by
                                      ascending SHA-256 of the
                                      JCS-canonicalized response envelope;
                                      no contributing run → empty
                                      rationale plus a
                                      `default-no-contributing-run` marker
                                      in `panel_disagreement_rows`), and
                                      asserts equality with every
                                      collapse-derived field published in
                                      `panel/aggregate.json`: the per-seat
                                      non-trivial counts, the majority and
                                      unanimous counts, and the
                                      membership, per-seat verdicts,
                                      rationales, and markers of
                                      `panel_disagreement_rows`.
                                      `section3_nontrivial_count_on_sample`
                                      is Tier 1's output, not a function
                                      of the collapse, and is outside
                                      check (vii).

Input layout (see `panel/checker.json.schema.md` for the full shape):

    panel/
      checker.json                             commitment + run records
      aggregate.json                           published aggregation (§6.3),
                                               consumed by check (vii)
      checker-inputs/
        A1-system-prompt.txt                   bytes sent as system role
        A1-user-prompt-template.txt            user-prompt template
        A1-user-prompt-actual.txt              user-prompt bytes actually sent
        A1/run-0/response-metadata.json        provider envelope minus content
        A1/run-0/notarization_token.tsr        DER-encoded RFC-3161 TSR
        A1/run-0/run-output.json               scorer's raw per-row JSON
                                               output for this run (C3),
                                               consumed by check (vii)
        A1/run-1/...                           (same shape, N runs per seat)
        A1/run-2/...
        A2/... A3/...                          (same set per seat)
        blind-sample.json                      deterministic blind sample
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata


ADJUDICATORS = ("A1", "A2", "A3")

# Ordered list of C4 booleans emitted per scorer. Order is stable so the
# JSON records are diff-friendly.
CHECK_BOOLS = (
    "prompt_hash_match",
    "sample_match",
    "blinding_preserved",
    "model_revision_match",
    "response_id_present",
    "response_metadata_hash_match",
    "notarization_imprint_match",
    "notarization_signature_valid",
    "collapse_rule_match",
)

# The only two verdict strings the §6.3 collapse rule accepts. A run whose
# `verdict` field is not EXACTLY one of these two literals contributes no
# verdict to the collapse (and still counts against the threshold, because
# the denominator is the committed N in every case).
VERDICT_LITERALS = ("trivial", "non-trivial")

# Path (relative to repo root) to the pinned TSA trust-anchor .pem files.
# The checker.json's `tsa.<identity>.pin_pem` field carries the same
# strings; we accept them from the JSON so a re-runner rooted elsewhere
# can override, but default to the pinned locations for defense in depth.
PINNED_TSA_PEM = {
    "primary": "ops/projects/P032/B0/tsa/digicert_primary.pem",
    "fallback": "ops/projects/P032/B0/tsa/sectigo_fallback.pem",
}


# ---------------------------------------------------------------------------
# Hashing helpers. Stdlib only.
# ---------------------------------------------------------------------------

def canonical_hash(raw_bytes):
    """SHA-256 of UTF-8-no-BOM, LF, NFC-normalized text bytes.

    Matches the C2 convention used by the emitter (`experiments/p032-emitter/
    emitter.py::canonical_hash`) so committed prompt hashes line up.
    """
    text = raw_bytes.decode("utf-8")
    if text.startswith("﻿"):
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = unicodedata.normalize("NFC", text)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def raw_sha256(raw_bytes):
    """SHA-256 of raw bytes with no normalization."""
    return hashlib.sha256(raw_bytes).hexdigest()


def jcs_canonicalize(obj):
    """Best-effort RFC 8785 JSON Canonicalization Scheme serializer.

    Stdlib only. Sufficient for provider response-metadata envelopes, which
    contain only strings, integers, booleans, nulls, arrays, and nested
    objects. Sorts object keys, uses the compact `,`/`:` separators, and
    ensure_ascii=False so non-ASCII strings serialize as the raw code points
    (RFC 8785 §3.2.2.2). Rejects floats and non-serializable types so a
    caller mis-using the checker fails loudly rather than silently drifting.
    """
    _reject_floats(obj)
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _reject_floats(obj):
    if isinstance(obj, float):
        raise ValueError(
            "jcs_canonicalize rejects floats: response-metadata envelopes "
            "must serialize as ints/strings/bools/nulls only. Got %r." % obj
        )
    if isinstance(obj, dict):
        for v in obj.values():
            _reject_floats(v)
    elif isinstance(obj, list):
        for v in obj:
            _reject_floats(v)


# ---------------------------------------------------------------------------
# Input loading.
# ---------------------------------------------------------------------------

def _read_bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


def load_checker_input(panel_dir):
    """Load and shallow-validate panel/checker.json.

    Returns the parsed JSON. Raises ValueError on structural malformation
    (missing adjudicator, missing required commitment field, etc.) — the
    caller maps ValueError to exit code 1 per the C4 convention.
    """
    checker_json_path = os.path.join(panel_dir, "checker.json")
    if not os.path.isfile(checker_json_path):
        raise ValueError("checker.json not found at %s" % checker_json_path)
    with open(checker_json_path, "rb") as fh:
        raw = fh.read()
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("checker.json parse failed: %s" % exc)
    for key in ("adjudicators", "sample", "blinded_field_values",
                "committed_n"):
        if key not in data:
            raise ValueError("checker.json missing top-level key: %s" % key)
    if not isinstance(data["adjudicators"], dict):
        raise ValueError("checker.json 'adjudicators' must be an object")
    if not isinstance(data["committed_n"], int) or data["committed_n"] < 1:
        raise ValueError(
            "checker.json 'committed_n' must be a positive integer"
        )
    for adj in ADJUDICATORS:
        if adj not in data["adjudicators"]:
            raise ValueError("checker.json missing adjudicator: %s" % adj)
        block = data["adjudicators"][adj]
        if "commit" not in block or not isinstance(block["commit"], dict):
            raise ValueError(
                "checker.json adjudicator %s missing commit block" % adj
            )
        if "runs" not in block or not isinstance(block["runs"], list):
            raise ValueError(
                "checker.json adjudicator %s missing runs list" % adj
            )
        for rel_key in ("system_prompt_relpath",
                        "user_prompt_template_relpath",
                        "user_prompt_actual_relpath"):
            if rel_key not in block:
                raise ValueError(
                    "checker.json adjudicator %s missing %s" % (adj, rel_key)
                )
    if not isinstance(data["sample"], dict):
        raise ValueError("checker.json 'sample' must be an object")
    for key in ("sha256_committed", "relpath"):
        if key not in data["sample"]:
            raise ValueError("checker.json sample missing key: %s" % key)
    if not isinstance(data["blinded_field_values"], list):
        raise ValueError("checker.json 'blinded_field_values' must be a list")
    return data


# ---------------------------------------------------------------------------
# Per-check helpers. Each returns (bool, reason_string_if_false).
# ---------------------------------------------------------------------------

def _resolve(panel_dir, relpath):
    """Resolve a checker-inputs path and reject escape attempts.

    A malformed relpath (absolute, or one that walks outside panel_dir) is a
    checker-input malformation, not a check failure — it exits 1 upstream.
    """
    if os.path.isabs(relpath):
        raise ValueError("checker.json relpath must be relative: %s" % relpath)
    full = os.path.normpath(os.path.join(panel_dir, relpath))
    panel_abs = os.path.abspath(panel_dir)
    full_abs = os.path.abspath(full)
    if not (full_abs == panel_abs or full_abs.startswith(panel_abs + os.sep)):
        raise ValueError("checker.json relpath escapes panel dir: %s" % relpath)
    if not os.path.isfile(full_abs):
        raise ValueError("checker-inputs file missing: %s" % relpath)
    return full_abs


def check_prompt_hash(panel_dir, block):
    """(i) prompt_hash_match — system + user-template canonical hashes."""
    commit = block["commit"]
    for role, sha_key, rel_key in (
        ("system_prompt", "system_prompt_sha256", "system_prompt_relpath"),
        ("user_prompt_template", "user_prompt_template_sha256",
         "user_prompt_template_relpath"),
    ):
        expected = commit.get(sha_key)
        if not expected:
            return False, "prompt_hash: commit missing %s" % sha_key
        rel = block.get(rel_key)
        if not rel:
            return False, "prompt_hash: block missing %s" % rel_key
        got = canonical_hash(_read_bytes(_resolve(panel_dir, rel)))
        if got != expected:
            return False, (
                "prompt_hash: %s canonical sha256 mismatch (expected %s, got %s)"
                % (role, expected, got)
            )
    return True, ""


def check_sample(panel_dir, top, block):
    """(ii) sample_match — sample bytes hash + appear-in-actual-user-prompt."""
    expected = top["sample"]["sha256_committed"]
    sample_path = _resolve(panel_dir, top["sample"]["relpath"])
    sample_bytes = _read_bytes(sample_path)
    got = raw_sha256(sample_bytes)
    if got != expected:
        return False, (
            "sample: sample bytes sha256 mismatch (expected %s, got %s)"
            % (expected, got)
        )
    actual_rel = block.get("user_prompt_actual_relpath")
    if not actual_rel:
        return False, "sample: block missing user_prompt_actual_relpath"
    actual_bytes = _read_bytes(_resolve(panel_dir, actual_rel))
    if sample_bytes not in actual_bytes:
        return False, (
            "sample: committed sample bytes do not appear verbatim in the "
            "actual user prompt bytes sent to the scorer"
        )
    return True, ""


def check_blinding(panel_dir, top, block):
    """(iii) blinding_preserved — no blinded value in actual user prompt."""
    actual_rel = block.get("user_prompt_actual_relpath")
    if not actual_rel:
        return False, "blinding: block missing user_prompt_actual_relpath"
    actual_bytes = _read_bytes(_resolve(panel_dir, actual_rel))
    lowered = actual_bytes.lower()
    for v in top["blinded_field_values"]:
        if not isinstance(v, str):
            return False, "blinding: blinded_field_values entries must be strings"
        v_bytes = v.encode("utf-8").lower()
        if not v_bytes:
            # An empty blinded value is a malformed input, not a leak.
            continue
        if v_bytes in lowered:
            return False, "blinding: blinded value leaked in actual user prompt: %r" % v
    return True, ""


def check_model_revision(block):
    """(iv) model_revision_match — provider + model id + pinned revision.

    Verifies for every run in block['runs']. Fails if any run drifts.
    """
    commit = block["commit"]
    for r in block["runs"]:
        for field in ("provider", "api_model_identifier",
                      "pinned_model_revision"):
            e = commit.get(field)
            g = r.get(field)
            if e is None or g is None:
                return False, ("model_revision: run %d missing field %s"
                               % (r.get("run_index", -1), field))
            if e != g:
                return False, (
                    "model_revision: run %d %s mismatch (committed %r, run %r)"
                    % (r.get("run_index", -1), field, e, g)
                )
    return True, ""


def check_response_v(panel_dir, block):
    """(v) response_id_present + response_metadata_hash_match.

    Verifies for every run in block['runs']. Returns
    (id_ok, id_reason, hash_ok, hash_reason) aggregated across runs.
    """
    id_ok = True
    id_reason = ""
    hash_ok = True
    hash_reason = ""

    for r in block["runs"]:
        idx = r.get("run_index", -1)
        rid = r.get("response_id")
        if not (isinstance(rid, str) and rid != ""):
            id_ok = False
            id_reason = "response_id: run %d missing or empty" % idx
            # Continue looping so later runs can still be checked for hash.

        expected = r.get("response_metadata_sha256")
        rel = r.get("response_metadata_relpath")
        if not expected:
            hash_ok = False
            hash_reason = ("response_metadata: run %d missing "
                           "response_metadata_sha256" % idx)
            continue
        if not rel:
            hash_ok = False
            hash_reason = ("response_metadata: run %d missing "
                           "response_metadata_relpath" % idx)
            continue
        try:
            blob_bytes = _read_bytes(_resolve(panel_dir, rel))
        except ValueError as exc:
            hash_ok = False
            hash_reason = "response_metadata: run %d %s" % (idx, exc)
            continue
        if not blob_bytes:
            hash_ok = False
            hash_reason = ("response_metadata: run %d on-disk blob is empty"
                           % idx)
            continue
        try:
            blob_obj = json.loads(blob_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            hash_ok = False
            hash_reason = ("response_metadata: run %d on-disk blob is not "
                           "valid UTF-8 JSON: %s" % (idx, exc))
            continue
        if not isinstance(blob_obj, dict) or not blob_obj:
            hash_ok = False
            hash_reason = ("response_metadata: run %d on-disk blob is not "
                           "a non-empty JSON object" % idx)
            continue
        got = raw_sha256(jcs_canonicalize(blob_obj))
        if got != expected:
            hash_ok = False
            hash_reason = (
                "response_metadata: run %d JCS-canonicalized sha256 mismatch "
                "(expected %s, got %s)" % (idx, expected, got)
            )

    return id_ok, id_reason, hash_ok, hash_reason


# ---------------------------------------------------------------------------
# Check (vi): notarization — count, imprint, signature.
# ---------------------------------------------------------------------------

# Parse `openssl ts -reply -in <token>.tsr -text` output for the message
# imprint hex string, which appears on a line like:
#   Message data:
#       0000 - de ad be ef ...
# or (more usefully for us) the summary line:
#   Hash Algorithm: sha256
#   Message data:
#       ...
# openssl prints an easier-to-parse hex on the token TST info under the
# "Message data:" line as a hexdump. But the modern openssl also emits a
# top-level "Message data:" line preceded by "TST info:". We extract by
# reading the token TST fields.
#
# Simpler and more robust: use `openssl ts -reply -token_in <token>.tsr
# -token_out` to get the embedded PKCS7 token bytes, then parse. That
# indirection is fragile too. The most portable path is:
#   openssl ts -reply -in <token>.tsr -text
# and to scrape the "Message data:" hex bytes section.

_MSG_DATA_HEXDUMP = re.compile(
    r"Message data:\s*\n((?:\s+[0-9a-f]{4} - [0-9a-f]{2}(?: [0-9a-f]{2})*"
    r"(?:-[0-9a-f]{2})?(?: [0-9a-f]{2})*"
    r"(?:\s+[!-~\.]+)?\s*\n)+)",
    re.IGNORECASE,
)


def _extract_imprint_from_ts_reply(ts_reply_text):
    """Pull the Message data hex bytes from `openssl ts -reply -text` output.

    Returns the imprint bytes as `bytes`. Raises ValueError if the section
    is missing or unparseable.
    """
    # Locate the "Message data:" block. openssl formats hex dumps like:
    #   Message data:
    #       0000 - 53 ad e5 df 0e 78 79 f3-2c 8e 35 8a 5d 69 41 b9
    #       0010 - ab c9 9a 4c b8 65 00 5b-d8 50 f3 27 d4 28 4f 29
    idx = ts_reply_text.find("Message data:")
    if idx < 0:
        raise ValueError("openssl ts -reply output has no 'Message data:'")
    tail = ts_reply_text[idx:]
    lines = tail.splitlines()
    # Skip the "Message data:" line itself.
    bytes_hex = []
    for line in lines[1:]:
        stripped = line.strip()
        if not stripped:
            break
        # Continue while lines look like hexdump lines. A hexdump line has
        # the pattern "OFFSET - HH HH ... - HH HH HH  ASCII".
        m = re.match(
            r"^([0-9a-f]{4})\s*-\s*([0-9a-f]{2}(?:[\s\-][0-9a-f]{2})*)",
            stripped, re.IGNORECASE,
        )
        if not m:
            break
        hex_part = m.group(2)
        # Replace separators with spaces and split.
        cleaned = re.sub(r"[\-\s]+", " ", hex_part).strip()
        for tok in cleaned.split():
            if len(tok) == 2 and re.match(r"^[0-9a-f]{2}$", tok, re.IGNORECASE):
                bytes_hex.append(tok)
    if not bytes_hex:
        raise ValueError("could not extract Message data hex bytes")
    return bytes.fromhex("".join(bytes_hex))


def _openssl_ts_reply_text(token_path):
    """Run `openssl ts -reply -in <token>.tsr -text`. Returns stdout string."""
    proc = subprocess.run(
        ["openssl", "ts", "-reply", "-in", token_path, "-text"],
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        raise ValueError(
            "openssl ts -reply failed for %s: rc=%d stderr=%s"
            % (token_path, proc.returncode, proc.stderr.strip())
        )
    return proc.stdout


def _openssl_ts_verify(token_path, imprint_hex, ca_pem_path):
    """Run `openssl ts -verify -digest <hex> -in <token>.tsr -CAfile <pem>`.

    Returns (ok, stderr) where ok is True iff verification succeeded.
    Uses only local files: the token path and the pinned .pem. No network.
    """
    cmd = [
        "openssl", "ts", "-verify",
        "-digest", imprint_hex,
        "-in", token_path,
        "-CAfile", ca_pem_path,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode == 0 and "Verification: OK" in proc.stdout:
        return True, ""
    err = (proc.stderr.strip() or proc.stdout.strip()
           or "openssl ts -verify returned rc=%d" % proc.returncode)
    return False, err


def _repo_relative_pem(top, identity, panel_dir):
    """Resolve the pinned .pem path for a given TSA identity.

    Prefers `checker.json`'s tsa block if present (allowing the re-runner to
    override); otherwise falls back to the module-level pinned map. All paths
    are resolved relative to CWD (the runner is expected to be launched from
    repo root, per protocol §6.2 publishing conventions).
    """
    tsa_block = top.get("tsa") or {}
    entry = tsa_block.get(identity) or {}
    pem = entry.get("pin_pem") or PINNED_TSA_PEM.get(identity)
    if not pem:
        raise ValueError("no pinned .pem for TSA identity %r" % identity)
    # Accept absolute paths as-is; resolve relative paths against CWD.
    if not os.path.isabs(pem):
        pem = os.path.abspath(pem)
    if not os.path.isfile(pem):
        raise ValueError(
            "pinned TSA pem missing for identity %r at %s" % (identity, pem)
        )
    return pem


def check_notarization(panel_dir, top, block):
    """(vi.a/b/c) — count, imprint, signature per token.

    Returns
    -------
    (count_int, imprint_ok, imprint_reason,
     sig_ok, sig_reason)

    count_int is the number of tokens actually present on disk for this
    seat. The caller compares to `top['committed_n']` to compute the
    notarization_token_count field and to derive the C4 outcome.
    """
    runs = block["runs"]
    committed_n = top["committed_n"]

    # (vi.a) count tokens actually present on disk for this seat.
    token_count = 0
    for r in runs:
        rel = r.get("notarization_token_relpath")
        if not rel:
            continue
        full = os.path.normpath(os.path.join(panel_dir, rel))
        if os.path.isfile(full):
            token_count += 1

    # Also scan the seat directory for any spurious extra .tsr files that
    # the run records did not enumerate — surplus tokens are also a C2(f)
    # violation. The seat directory is inferred from run 0's relpath.
    if runs:
        first_rel = runs[0].get("notarization_token_relpath") or ""
        seat_root = os.path.dirname(os.path.dirname(first_rel))
        if seat_root:
            seat_full = os.path.normpath(os.path.join(panel_dir, seat_root))
            if os.path.isdir(seat_full):
                found = []
                for entry in sorted(os.listdir(seat_full)):
                    entry_full = os.path.join(seat_full, entry)
                    if not os.path.isdir(entry_full):
                        continue
                    for f in sorted(os.listdir(entry_full)):
                        if f.endswith(".tsr"):
                            found.append(os.path.join(seat_root, entry, f))
                # Add any file not already accounted for by a run record.
                declared = {r.get("notarization_token_relpath") for r in runs}
                for f in found:
                    if f not in declared:
                        token_count += 1

    imprint_ok = True
    imprint_reason = ""
    sig_ok = True
    sig_reason = ""

    for r in runs:
        idx = r.get("run_index", -1)
        rel = r.get("notarization_token_relpath")
        env_rel = r.get("response_metadata_relpath")
        tsa_identity = r.get("notarization_tsa_identity")

        if not rel:
            imprint_ok = False
            imprint_reason = ("notarization: run %d missing "
                              "notarization_token_relpath" % idx)
            sig_ok = False
            sig_reason = imprint_reason
            continue

        token_full = os.path.normpath(os.path.join(panel_dir, rel))
        if not os.path.isfile(token_full):
            imprint_ok = False
            imprint_reason = ("notarization: run %d token file absent: %s"
                              % (idx, rel))
            sig_ok = False
            sig_reason = imprint_reason
            continue

        # (vi.b) imprint match: extract the token's message imprint and
        # compare to the SHA-256 of the on-disk envelope bytes.
        try:
            reply_text = _openssl_ts_reply_text(token_full)
            token_imprint = _extract_imprint_from_ts_reply(reply_text)
        except ValueError as exc:
            imprint_ok = False
            imprint_reason = ("notarization: run %d openssl ts -reply "
                              "failed: %s" % (idx, exc))
            # Signature check requires the imprint hex, so cascade the fail.
            sig_ok = False
            sig_reason = imprint_reason
            continue

        try:
            env_full = _resolve(panel_dir, env_rel)
        except ValueError as exc:
            imprint_ok = False
            imprint_reason = ("notarization: run %d envelope path invalid: %s"
                              % (idx, exc))
            sig_ok = False
            sig_reason = imprint_reason
            continue

        envelope_bytes = _read_bytes(env_full)
        recomputed = hashlib.sha256(envelope_bytes).digest()
        if token_imprint != recomputed:
            imprint_ok = False
            imprint_reason = (
                "notarization: run %d imprint mismatch (token=%s, "
                "recomputed=%s)"
                % (idx, token_imprint.hex(), recomputed.hex())
            )

        # (vi.c) signature verification against the pinned .pem for the
        # TSA identity recorded on this run.
        if tsa_identity not in ("primary", "fallback"):
            sig_ok = False
            sig_reason = ("notarization: run %d has invalid TSA identity: %r"
                          % (idx, tsa_identity))
            continue
        try:
            pem = _repo_relative_pem(top, tsa_identity, panel_dir)
        except ValueError as exc:
            sig_ok = False
            sig_reason = "notarization: run %d %s" % (idx, exc)
            continue
        # Feed the token's own imprint bytes to openssl (not the recomputed
        # envelope hash) so signature verification is independent of the
        # (vi.b) imprint-match outcome; a signature-invalid token still
        # flags check (vi.c) even if the imprint is also mutated.
        ok, err = _openssl_ts_verify(token_full, token_imprint.hex(), pem)
        if not ok:
            sig_ok = False
            sig_reason = ("notarization: run %d signature invalid vs %s "
                          "pem: %s" % (idx, tsa_identity, err))

    return token_count, imprint_ok, imprint_reason, sig_ok, sig_reason


# ---------------------------------------------------------------------------
# Check (vii): collapse-rule recomputation (§6.3, H13 clause (iii)).
#
# The §6.3 collapse rule, restated exactly as the checker applies it, for a
# given seat and a given row:
#
#   1. The seat's verdict for the row is the verdict returned by MORE THAN
#      N/2 of the committed N runs (N from checker.json `committed_n` per
#      C2(f)). The denominator is the committed N in every case, never the
#      number of runs that contributed a verdict — a run that contributes
#      nothing counts against the threshold rather than shrinking it.
#   2. A run whose published output does not parse per the committed output
#      format, or whose `verdict` field is not exactly one of the two
#      literal values "trivial" / "non-trivial", contributes no verdict.
#   3. If no verdict clears the more-than-N/2 threshold (tie, or too few
#      parsed runs), the seat's verdict for the row is "trivial".
#   4. The published rationale is the rationale from the earliest of the
#      seat's runs whose verdict equals the collapsed verdict, ordered by
#      the RFC-3161 token `genTime` recorded for that run under C2(g), ties
#      broken by ascending hexadecimal-lowercase SHA-256 of the
#      JCS-canonicalized response envelope for that run.
#   5. If no run of the seat on the row returned the collapsed verdict, the
#      published rationale is the empty string and the seat's collapse for
#      the row is recorded in `panel_disagreement_rows` with the marker
#      `default-no-contributing-run`.
#
# Everything is recomputed from the published artifacts — per-run outputs,
# tokens, envelopes — and never taken from a stored aggregate value. The
# `genTime` read uses the same `openssl ts -reply -text` invocation as
# check (vi.b) (deterministic, offline, local files only, per the T-B0m2
# ruling on the C4 invariant). No network, no LLM.
# ---------------------------------------------------------------------------

_DISAGREEMENT_MARKER = "default-no-contributing-run"

_GENTIME_MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}

# `openssl ts -reply -text` prints the token's genTime as e.g.
#   Time stamp: Jul 30 14:55:21 2026 GMT
# optionally with fractional seconds ("14:55:21.123 2026 GMT"). openssl
# emits C-locale English month abbreviations regardless of environment, so
# the month map above is deterministic.
_GENTIME_RE = re.compile(
    r"Time stamp:\s*([A-Z][a-z]{2})\s+(\d{1,2})\s+"
    r"(\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?\s+(\d{4})\s+GMT"
)


def parse_gen_time(reply_text):
    """Extract a sortable genTime tuple from `openssl ts -reply -text` output.

    Returns (year, month, day, hour, minute, second, frac_str) where
    frac_str is the fractional-seconds digits right-padded to 9 places so
    lexicographic comparison equals numeric comparison. Returns None if the
    output carries no parseable "Time stamp:" line.
    """
    m = _GENTIME_RE.search(reply_text)
    if not m:
        return None
    month = _GENTIME_MONTHS.get(m.group(1))
    if month is None:
        return None
    frac = (m.group(6) or "").ljust(9, "0")
    return (int(m.group(7)), month, int(m.group(2)), int(m.group(3)),
            int(m.group(4)), int(m.group(5)), frac)


def _envelope_tiebreak_hash(panel_dir, run):
    """SHA-256 (lowercase hex) of the run's JCS-canonicalized envelope.

    Recomputed from the on-disk envelope bytes — never taken from the
    stored `response_metadata_sha256` field, so a stored-value lie cannot
    steer the tie-break. Falls back to the raw byte hash if the on-disk
    blob does not parse (check (v) flags that separately), and to the hash
    of the empty byte string if the file is absent (check (vi)/(v) flag
    that separately). Deterministic in every branch.
    """
    rel = run.get("response_metadata_relpath")
    if rel and not os.path.isabs(rel):
        full = os.path.normpath(os.path.join(panel_dir, rel))
        if os.path.isfile(full):
            raw = _read_bytes(full)
            try:
                obj = json.loads(raw.decode("utf-8"))
                return raw_sha256(jcs_canonicalize(obj))
            except (ValueError, UnicodeDecodeError):
                return raw_sha256(raw)
    return raw_sha256(b"")


def _run_sort_key(panel_dir, run):
    """Ordering key for rationale selection per §6.3.

    Primary: RFC-3161 token genTime (earlier first). Ties: ascending
    hexadecimal-lowercase SHA-256 of the JCS-canonicalized envelope. A run
    whose token is absent or unparseable has no genTime and orders after
    every run with one (its token problem is check (vi)'s finding; the
    ordering here just stays total and deterministic).
    """
    gen_time = None
    rel = run.get("notarization_token_relpath")
    if rel and not os.path.isabs(rel):
        full = os.path.normpath(os.path.join(panel_dir, rel))
        if os.path.isfile(full):
            try:
                gen_time = parse_gen_time(_openssl_ts_reply_text(full))
            except ValueError:
                gen_time = None
    env_hash = _envelope_tiebreak_hash(panel_dir, run)
    if gen_time is None:
        return (1, (), env_hash)
    return (0, gen_time, env_hash)


def _run_output_relpath(run):
    env_rel = run.get("response_metadata_relpath")
    if not env_rel:
        raise ValueError(
            "run record missing response_metadata_relpath; cannot locate "
            "the run-output artifact for check (vii)"
        )
    return os.path.dirname(env_rel) + "/run-output.json"


def _run_output_verdicts(panel_dir, run, sample_ids):
    """Parse one run's published output into {property_id: (verdict, rationale)}.

    The committed output format is a JSON array of row objects, each with a
    string `property_id`, a `verdict`, and a `rationale`. Per §6.3:
    - a run whose output does not parse per that format (not UTF-8, not
      JSON, not an array of objects with string property ids) contributes
      no verdict on ANY row: every row maps to (None, "");
    - a row entry whose `verdict` is not exactly "trivial" or "non-trivial"
      contributes no verdict on THAT row;
    - a row absent from the output, or duplicated in it, contributes no
      verdict on that row;
    - a missing or non-string `rationale` on a contributing entry is
      treated as the empty string.

    A MISSING run-output.json file is a malformed checker input (C3 obliges
    publication of every run's raw outputs), raised as ValueError → exit 1,
    consistent with every other enumerated artifact.
    """
    rel = _run_output_relpath(run)
    raw = _read_bytes(_resolve(panel_dir, rel))
    nothing = {pid: (None, "") for pid in sample_ids}
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return nothing
    if not isinstance(parsed, list):
        return nothing
    seen = {}
    duplicated = set()
    for entry in parsed:
        if not isinstance(entry, dict):
            return nothing
        pid = entry.get("property_id")
        if not isinstance(pid, str):
            return nothing
        if pid in seen:
            duplicated.add(pid)
        seen[pid] = entry
    rows = {}
    for pid in sample_ids:
        if pid not in seen or pid in duplicated:
            rows[pid] = (None, "")
            continue
        verdict = seen[pid].get("verdict")
        if verdict not in VERDICT_LITERALS:
            rows[pid] = (None, "")
            continue
        rationale = seen[pid].get("rationale")
        if not isinstance(rationale, str):
            rationale = ""
        rows[pid] = (verdict, rationale)
    return rows


def collapse_votes(per_run_rows, committed_n):
    """Apply the §6.3 collapse rule to one seat's runs on one row. Pure.

    per_run_rows: list of dicts, one per published run, each with
        "verdict"   — "trivial" / "non-trivial", or None if the run
                      contributed no verdict on this row;
        "rationale" — the run's rationale string for this row;
        "sort_key"  — the run's ordering key per `_run_sort_key`.
    committed_n: the committed N from C2(f). ALWAYS the denominator; the
        threshold is more-than-N/2 regardless of how many runs were
        published or how many parsed.

    Returns {"verdict", "rationale", "no_contributing_run"}.
    """
    tallies = {}
    for r in per_run_rows:
        v = r["verdict"]
        if v in VERDICT_LITERALS:
            tallies[v] = tallies.get(v, 0) + 1
    collapsed = None
    for v in VERDICT_LITERALS:
        # more than N/2, integer arithmetic (2*count > N). At most one
        # literal can clear the threshold.
        if tallies.get(v, 0) * 2 > committed_n:
            collapsed = v
            break
    if collapsed is None:
        # Tie, or too few contributing runs: default "trivial" (§6.3 fixes
        # the tie direction against the publisher's own headline measure).
        collapsed = "trivial"
    contributing = [r for r in per_run_rows if r["verdict"] == collapsed]
    if not contributing:
        return {"verdict": collapsed, "rationale": "",
                "no_contributing_run": True}
    winner = min(contributing, key=lambda r: r["sort_key"])
    return {"verdict": collapsed, "rationale": winner["rationale"],
            "no_contributing_run": False}


def recompute_seat_collapse(panel_dir, block, committed_n, sample_ids):
    """Recompute one seat's collapsed verdict + rationale for every row.

    Reads the seat's published run artifacts (run-output.json, RFC-3161
    token for genTime, response envelope for the tie-break hash) and
    applies `collapse_votes`. Returns {property_id: {"verdict",
    "rationale", "no_contributing_run"}}.
    """
    per_run = []
    for run in (block.get("runs") or []):
        rows = _run_output_verdicts(panel_dir, run, sample_ids)
        per_run.append({"rows": rows,
                        "sort_key": _run_sort_key(panel_dir, run)})
    out = {}
    for pid in sample_ids:
        votes = [{"verdict": pr["rows"][pid][0],
                  "rationale": pr["rows"][pid][1],
                  "sort_key": pr["sort_key"]} for pr in per_run]
        out[pid] = collapse_votes(votes, committed_n)
    return out


def load_aggregate(panel_dir):
    """Load and shallow-validate panel/aggregate.json for check (vii).

    Raises ValueError on absence or structural malformation (exit 1 per
    the C4 convention). Value-level disagreement with the recomputation is
    a check (vii) FAILURE (exit 2), not a malformation.
    """
    path = os.path.join(panel_dir, "aggregate.json")
    if not os.path.isfile(path):
        raise ValueError(
            "aggregate.json not found at %s (check (vii) verifies the "
            "published aggregate against the collapse-rule recomputation "
            "and cannot run without it)" % path
        )
    with open(path, "rb") as fh:
        raw = fh.read()
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("aggregate.json parse failed: %s" % exc)
    if not isinstance(data, dict):
        raise ValueError("aggregate.json must be a JSON object")
    for key in ("panel_nontrivial_count_per_adjudicator",
                "panel_nontrivial_count_majority",
                "panel_nontrivial_count_unanimous",
                "panel_disagreement_rows"):
        if key not in data:
            raise ValueError("aggregate.json missing key: %s" % key)
    per_adj = data["panel_nontrivial_count_per_adjudicator"]
    if not isinstance(per_adj, dict):
        raise ValueError(
            "aggregate.json panel_nontrivial_count_per_adjudicator must "
            "be an object"
        )
    for adj in ADJUDICATORS:
        v = per_adj.get(adj)
        if not isinstance(v, int) or isinstance(v, bool):
            raise ValueError(
                "aggregate.json panel_nontrivial_count_per_adjudicator "
                "missing integer for %s" % adj
            )
    for key in ("panel_nontrivial_count_majority",
                "panel_nontrivial_count_unanimous"):
        v = data[key]
        if not isinstance(v, int) or isinstance(v, bool):
            raise ValueError("aggregate.json %s must be an integer" % key)
    rows = data["panel_disagreement_rows"]
    if not isinstance(rows, list):
        raise ValueError("aggregate.json panel_disagreement_rows must be a list")
    for row in rows:
        if not isinstance(row, dict) \
                or not isinstance(row.get("property_id"), str) \
                or not isinstance(row.get("seats"), dict):
            raise ValueError(
                "aggregate.json panel_disagreement_rows entries must be "
                "objects with a string property_id and a seats object"
            )
    return data


def _load_sample_row_ids(panel_dir, top):
    """Ordered property ids of the blind sample rows. ValueError → exit 1."""
    raw = _read_bytes(_resolve(panel_dir, top["sample"]["relpath"]))
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("blind sample is not valid UTF-8 JSON: %s" % exc)
    if not isinstance(parsed, list) or not parsed:
        raise ValueError("blind sample must be a non-empty JSON array")
    ids = []
    for entry in parsed:
        if not isinstance(entry, dict) \
                or not isinstance(entry.get("property_id"), str):
            raise ValueError(
                "blind sample rows must be objects with a string property_id"
            )
        ids.append(entry["property_id"])
    if len(ids) != len(set(ids)):
        raise ValueError("blind sample carries duplicate property_id values")
    return ids


def _recompute_all_seats(panel_dir, top, sample_ids):
    return {
        adj: recompute_seat_collapse(
            panel_dir, top["adjudicators"][adj], top["committed_n"],
            sample_ids)
        for adj in ADJUDICATORS
    }


def _expected_disagreement_ids(recomputed_all, sample_ids):
    """Rows that must appear in panel_disagreement_rows per §6.3 `:418`:
    non-unanimous rows, plus any row where a seat's collapse carries the
    default-no-contributing-run marker (whether or not the seats agreed).
    """
    ids = set()
    for pid in sample_ids:
        verdicts = {recomputed_all[a][pid]["verdict"] for a in ADJUDICATORS}
        any_marker = any(recomputed_all[a][pid]["no_contributing_run"]
                         for a in ADJUDICATORS)
        if len(verdicts) > 1 or any_marker:
            ids.add(pid)
    return ids


def _panel_level_mismatch(recomputed_all, aggregate, sample_ids):
    """Cross-seat aggregate fields vs. the recomputation. Returns a reason
    string, empty when everything matches. A mismatch here is not
    attributable to a single scorer, so the caller applies it to every
    seat's collapse_rule_match.
    """
    reasons = []
    majority = 0
    unanimous = 0
    for pid in sample_ids:
        nt = sum(1 for a in ADJUDICATORS
                 if recomputed_all[a][pid]["verdict"] == "non-trivial")
        if nt >= 2:
            majority += 1
        if nt == 3:
            unanimous += 1
    if aggregate["panel_nontrivial_count_majority"] != majority:
        reasons.append(
            "panel_nontrivial_count_majority published %d, recomputed %d"
            % (aggregate["panel_nontrivial_count_majority"], majority)
        )
    if aggregate["panel_nontrivial_count_unanimous"] != unanimous:
        reasons.append(
            "panel_nontrivial_count_unanimous published %d, recomputed %d"
            % (aggregate["panel_nontrivial_count_unanimous"], unanimous)
        )
    published_ids = [row["property_id"]
                     for row in aggregate["panel_disagreement_rows"]]
    if len(published_ids) != len(set(published_ids)):
        reasons.append("panel_disagreement_rows carries duplicate rows")
    expected_ids = _expected_disagreement_ids(recomputed_all, sample_ids)
    if set(published_ids) != expected_ids:
        missing = sorted(expected_ids - set(published_ids))
        surplus = sorted(set(published_ids) - expected_ids)
        reasons.append(
            "panel_disagreement_rows membership mismatch "
            "(missing per recomputation: %s; surplus: %s)"
            % (missing, surplus)
        )
    return "; ".join(reasons)


def check_collapse_rule(panel_dir, block, top=None, adjudicator=None,
                        aggregate=None, recomputed_all=None):
    """(vii) collapse_rule_match — §6.3 collapse recomputed vs. published.

    Recomputes, for this seat and every row of the blind sample, the
    collapsed verdict and rationale from the seat's N published run
    artifacts, and asserts equality with everything `panel/aggregate.json`
    publishes as a function of the collapse. Returns (bool, reason).

    Callable standalone as check_collapse_rule(panel_dir, block): the
    remaining context (checker.json top-level, seat identity, aggregate,
    sibling-seat recomputations for the cross-seat fields) is loaded /
    derived when not passed. `check_all` passes everything explicitly so
    the recomputation runs once per panel, not once per seat.
    """
    if top is None:
        top = load_checker_input(panel_dir)
    if aggregate is None:
        aggregate = load_aggregate(panel_dir)
    if adjudicator is None:
        for adj in ADJUDICATORS:
            if top["adjudicators"].get(adj) is block \
                    or top["adjudicators"].get(adj) == block:
                adjudicator = adj
                break
        if adjudicator is None:
            raise ValueError(
                "check_collapse_rule: block matches no adjudicator in "
                "checker.json"
            )
    sample_ids = _load_sample_row_ids(panel_dir, top)
    if recomputed_all is None:
        recomputed_all = _recompute_all_seats(panel_dir, top, sample_ids)

    reasons = []
    panel_reason = _panel_level_mismatch(recomputed_all, aggregate,
                                         sample_ids)
    if panel_reason:
        reasons.append("collapse_rule: %s" % panel_reason)

    mine = recomputed_all[adjudicator]
    published_count = \
        aggregate["panel_nontrivial_count_per_adjudicator"][adjudicator]
    recomputed_count = sum(1 for pid in sample_ids
                           if mine[pid]["verdict"] == "non-trivial")
    if published_count != recomputed_count:
        reasons.append(
            "collapse_rule: %s non-trivial count published %d, "
            "recomputed %d"
            % (adjudicator, published_count, recomputed_count)
        )

    for row in aggregate["panel_disagreement_rows"]:
        pid = row["property_id"]
        if pid not in mine:
            # Row is not a sample row; membership mismatch is already a
            # panel-level reason. Nothing seat-specific to compare.
            continue
        seat_entry = row["seats"].get(adjudicator)
        if not isinstance(seat_entry, dict):
            reasons.append(
                "collapse_rule: disagreement row %s carries no entry for "
                "seat %s" % (pid, adjudicator)
            )
            continue
        rec = mine[pid]
        if seat_entry.get("verdict") != rec["verdict"]:
            reasons.append(
                "collapse_rule: row %s %s verdict published %r, "
                "recomputed %r"
                % (pid, adjudicator, seat_entry.get("verdict"),
                   rec["verdict"])
            )
        if seat_entry.get("rationale") != rec["rationale"]:
            reasons.append(
                "collapse_rule: row %s %s rationale published %r, "
                "recomputed %r"
                % (pid, adjudicator, seat_entry.get("rationale"),
                   rec["rationale"])
            )
        published_marker = (seat_entry.get("marker") == _DISAGREEMENT_MARKER)
        if published_marker != rec["no_contributing_run"]:
            reasons.append(
                "collapse_rule: row %s %s %s marker published %s, "
                "recomputation says %s"
                % (pid, adjudicator, _DISAGREEMENT_MARKER,
                   published_marker, rec["no_contributing_run"])
            )

    return (not reasons), "; ".join(reasons)


# ---------------------------------------------------------------------------
# Driver.
# ---------------------------------------------------------------------------

def check_all(panel_dir):
    """Return (records, any_failure).

    records is a list of one dict per adjudicator with the CHECK_BOOLS fields
    and a `failure_reason` string. any_failure is True if any check failed
    for any scorer.
    """
    top = load_checker_input(panel_dir)
    committed_n = top["committed_n"]
    # Check (vii) context, loaded once per panel: the published aggregate,
    # the sample row ids, and the collapse recomputation for all three
    # seats (the cross-seat aggregate fields need every seat's collapse).
    # Absence or structural malformation of any of these raises ValueError
    # → exit 1 per the C4 convention, same as checker.json itself.
    aggregate = load_aggregate(panel_dir)
    sample_ids = _load_sample_row_ids(panel_dir, top)
    recomputed_all = _recompute_all_seats(panel_dir, top, sample_ids)
    records = []
    any_failure = False
    for adj in ADJUDICATORS:
        block = top["adjudicators"][adj]
        reasons = []

        i_ok, i_reason = check_prompt_hash(panel_dir, block)
        if not i_ok:
            reasons.append(i_reason)

        ii_ok, ii_reason = check_sample(panel_dir, top, block)
        if not ii_ok:
            reasons.append(ii_reason)

        iii_ok, iii_reason = check_blinding(panel_dir, top, block)
        if not iii_ok:
            reasons.append(iii_reason)

        iv_ok, iv_reason = check_model_revision(block)
        if not iv_ok:
            reasons.append(iv_reason)

        v_id_ok, v_id_reason, v_hash_ok, v_hash_reason = check_response_v(
            panel_dir, block)
        if not v_id_ok:
            reasons.append(v_id_reason)
        if not v_hash_ok:
            reasons.append(v_hash_reason)

        (token_count, vi_imprint_ok, vi_imprint_reason,
         vi_sig_ok, vi_sig_reason) = check_notarization(panel_dir, top, block)
        count_ok = (token_count == committed_n)
        if not count_ok:
            reasons.append(
                "notarization_token_count: got %d, committed N=%d"
                % (token_count, committed_n)
            )
        if not vi_imprint_ok:
            reasons.append(vi_imprint_reason)
        if not vi_sig_ok:
            reasons.append(vi_sig_reason)

        vii_ok, vii_reason = check_collapse_rule(
            panel_dir, block, top=top, adjudicator=adj,
            aggregate=aggregate, recomputed_all=recomputed_all)
        if not vii_ok:
            reasons.append(vii_reason)

        rec = {
            "adjudicator": adj,
            "prompt_hash_match": i_ok,
            "sample_match": ii_ok,
            "blinding_preserved": iii_ok,
            "model_revision_match": iv_ok,
            "response_id_present": v_id_ok,
            "response_metadata_hash_match": v_hash_ok,
            "notarization_token_count": token_count,
            "notarization_imprint_match": vi_imprint_ok,
            "notarization_signature_valid": vi_sig_ok,
            "collapse_rule_match": vii_ok,
            "failure_reason": "; ".join(reasons),
        }
        records.append(rec)
        # Any of: reasons list non-empty, or the token count doesn't equal
        # committed_n (already captured in reasons), is a failure.
        if reasons:
            any_failure = True
    return records, any_failure


def main(argv=None):
    ap = argparse.ArgumentParser(description="P032 Tier-3 panel checker (§7 C4).")
    ap.add_argument("--panel-dir", required=True,
                    help="path to the panel/ directory containing checker.json "
                         "and checker-inputs/")
    ap.add_argument("--out", default=None,
                    help="optional path to write per-scorer JSON records (one "
                         "per line, JCS-canonical). Defaults to stdout.")
    args = ap.parse_args(argv)

    try:
        records, any_failure = check_all(args.panel_dir)
    except ValueError as exc:
        sys.stderr.write("checker input malformed: %s\n" % exc)
        return 1

    out_fh = None
    try:
        if args.out:
            out_fh = open(args.out, "w", encoding="utf-8")
            sink = out_fh
        else:
            sink = sys.stdout
        for rec in records:
            sink.write(jcs_canonicalize(rec).decode("utf-8"))
            sink.write("\n")
        if out_fh is not None:
            out_fh.flush()
    finally:
        if out_fh is not None:
            out_fh.close()

    return 2 if any_failure else 0


if __name__ == "__main__":
    sys.exit(main())

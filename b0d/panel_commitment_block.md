# Panel commitment block (C2) — human-readable summary

Ticket: `T-P032-B0d-panel-commitment-hash-2026-07-31`
(supersedes `T-P032-B0d-panel-commitment-block-2026-07-31`)
Produced by: `backend_devops_eng`
Machine-readable source of truth: `panel_commitment_block.json` (same directory).
Shape of record: mirrors `B1_emitter_commitment_block.{json,md}` — same schema style, same
normalization statements, same base64 embedding discipline, same independent-recomputation
discipline. Three seats instead of one.

Authority: `ops/projects/P032_B0_BENCHMARK_PROTOCOL.md` §7 C2(a)–(e);
`D-P032-panel-composition-2026-07-28` (CEO);
`D-P032-B0d-a1-openai-probe-followup-2026-07-30` (COO-ruled 2026-07-31);
`D-P032-B0d-a2-provider-and-missing-key-2026-07-31` (COO) — settled POSITIVE by the probe;
`D-P032-B0d-system-fingerprint-present-but-null-2026-07-31` (COO ruling, 2026-07-31);
`D-P032-B0d-h12-diagnostic-moves-to-unanimity-2026-07-31`;
fire order `T-COO-P032-hash-and-gates-fireorder-2026-07-31` W2.3 — HASH AUTHORISED.

---

## 0. Publish gate — read this first

**`publish_ready` = `true`. `publish_blocking_pending_fields` = `[]`.**

Zero fields read `pending`. The four A2 fields that were `pending` on the previous pass
(provider, identifier as sent, pinned revision as returned, C2(d) blob) are filled from the
POSITIVE DeepSeek probe of record, `A2_deepseek_probe_2026-07-31.{json,md}`. A3's
`c2d_response_metadata_blob.status` of `not-committed-at-B0d` is a defined non-applicability
(the blob is a per-scorer-run artifact and no A3 envelope exists before B3), not an unfilled
value; it does not block publish.

---

## 1. What this is, and what changed since the previous block

C2 requires a per-scorer commitment recorded in the B0d publication ticket for each of A1, A2,
A3, **before any B1 output exists**. This block is that commitment, hashed against the **frozen**
prompt tree: H11 `LANDS_CLEAN`; H12–H15 closed at the re-attack; H16 and H17 closed on disk
under `T-P032-B0d-h16h17-2026-07-31`; the lens amendment landed. No further prompt or protocol
edit is scheduled before publish.

**Every digest was recomputed from the bytes currently on disk.** Nothing was carried forward
from the previous block. Changed-vs-held, per seat, versus
`T-P032-B0d-panel-commitment-block-2026-07-31`:

| Seat | 5 system prompt | 6 user template | 7 tool manifest | 8 parameter manifest |
|------|-----------------|-----------------|-----------------|----------------------|
| A1 | **changed** | **changed** | held | held |
| A2 | **changed** | **changed** | held | **changed** |
| A3 | **changed** | **changed** | held | held |

All six prompt files moved under the H11/H12–H15/H16–H17 + lens fix cycle. The three
tool-availability manifests (the 2-byte literal `[]`) held. A2's parameter manifest changed
because the fix cycle replaced the Fireworks model path with `deepseek-v4-pro` (see §6). A1's
and A3's parameter manifests held. The previous digest for every field is recorded alongside
the new one in the JSON (`previous_block_sha256`).

**No scorer run exists yet, for any seat.** Panel scorer runs happen at B3. C4 check (iv) is
what verifies these commitments against the actual scorer runs at B3. Every field-2/3/4 value
below carries a named provenance describing what evidence it *actually* came from.

This ticket is unmetered: local bytes plus already-captured probe JSON. No provider API was
called.

---

## 2. The eight fields, plus two, per seat

Digests are SHA-256, lower-case hex. Full base64 of raw and canonical bytes for every hashed
input lives in the JSON under `seats.<seat>.hashed_input_evidence`, so a reader can re-derive
every digest without access to this repo.

### A1 — GPT-5.6 Sol

| # | Field | Value |
|---|-------|-------|
| 1 | Base model | GPT-5.6 Sol |
| 2 | Provider | OpenAI direct API |
| 3 | API model identifier as sent | `gpt-5.6-sol` |
| 4 | Pinned model revision as returned | `gpt-5.6-sol` |
| 5 | System-prompt SHA-256 | `475a52d55778ab64a06c904a17d64240d59dbcc04f493d1d4e4fdbfdf788793d` |
| 6 | User-template SHA-256 | `099560dba863a424532e05e9dfbc67c26d98211a9a1a0d3d24b68fd3e1290ec5` |
| 7 | Tool-availability manifest (`[]`) SHA-256 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |
| 8 | Parameter manifest SHA-256 (JCS→SHA-256) | `93ef8a215b4df8f5d16842fb5729955bc559704a4252744c2bd4b3d6cc9a78be` |
| 9 | Harness system-prompt version | `literal-system-prompt-per-(a)` |

Parameter manifest canonical JSON: `{"max_completion_tokens":16000,"model":"gpt-5.6-sol"}`

**Fields 2/3/4 provenance:** the W1.1 A1 probe (`A1_openai_probe_2-2026-07-31.json`, ticket
`T-P032-B0d-a1-openai-probe-2-2026-07-31`), an HTTP 200 success envelope from
`https://api.openai.com/v1/chat/completions`, response id
`chatcmpl-E7mG38ld2ZqElv5QdLzsxD0LJwlLa`. A one-token liveness call, **not** a scorer run.
Values read from the probe JSON, not from ticket prose. Fields 3 and 4 carrying the same string
is the expected and satisfying case under C2(d)'s dateless-pinned-snapshot paragraph — not a
defect.

### A2 — DeepSeek-V4-Pro

| # | Field | Value |
|---|-------|-------|
| 1 | Base model | DeepSeek-V4-Pro |
| 2 | Provider | DeepSeek first-party API |
| 3 | API model identifier as sent | `deepseek-v4-pro` |
| 4 | Pinned model revision as returned | `fp_9954b31ca7_prod0820_fp8_kvcache_20260402` |
| 5 | System-prompt SHA-256 | `824d1ee8722f29c2350c0e8bb208a1fdb1253566ab22fe3d348195648874d525` |
| 6 | User-template SHA-256 | `78e07136c2378c4d7f25fc3bdbe819e3342c44b08580ba4efae84382d446b2e3` |
| 7 | Tool-availability manifest (`[]`) SHA-256 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |
| 8 | Parameter manifest SHA-256 (JCS→SHA-256) | `8b5e54ef074ea291711c49ff8077c1d1c348319e5cdcb4c0a63e3f43b2a7f074` |
| 9 | Harness system-prompt version | `literal-system-prompt-per-(a)` |

Parameter manifest canonical JSON: `{"max_tokens":16000,"model":"deepseek-v4-pro"}`

Plus the A2-only Hugging Face pair (source of record `A2_hf_revision_2026-07-31.json`, read
from the JSON, not from ticket prose; the JSON agrees with the dispatching ticket's strings;
corroborated across three independent unauthenticated surfaces; captured 2026-07-31T18:26:16Z):

- `repo_id` = `deepseek-ai/DeepSeek-V4-Pro`
- `revision_sha` = `b5968e9190ef611bbf34a7229255be88a0e937c1`

**Fields 2/3/4 provenance:** the A2 provider probe
(`A2_deepseek_probe_2026-07-31.json`, ticket `T-P032-B0d-a2-deepseek-probe-2026-07-31`),
an HTTP 200 success envelope from `https://api.deepseek.com/v1/chat/completions`, response id
`f1181e8a-3e89-4f39-ab95-8070ccd2af9c`, verdict **POSITIVE**. Values read from the probe JSON,
not from ticket prose.

**Field 4 is `system_fingerprint`, not `model`.** The pinnable value on DeepSeek is the
envelope's `system_fingerprint`. The API accepts only two undated names (`deepseek-v4-pro` /
`deepseek-v4-flash`) — the probe's negative control confirmed a dated variant is rejected with
HTTP 400 — so the returned `model` string (`deepseek-v4-pro`) does not pin a revision and is
**not** used as field 4.

**Prior field-2 deviation closed.** The previous pass set field 2 to `pending` against the fire
order because the probe had not yet decided between DeepSeek first-party and Fireworks. The
probe decided: DeepSeek first-party, POSITIVE, Fireworks not taken and not contacted. Field 2
is now an observation, not an expectation — the deviation is closed by evidence, not by
instruction.

### A3 — Claude Opus 5

| # | Field | Value |
|---|-------|-------|
| 1 | Base model | Claude Opus 5 |
| 2 | Provider | Anthropic direct API |
| 3 | API model identifier as sent | `claude-opus-5` |
| 4 | Pinned model revision as returned | `claude-opus-5` |
| 5 | System-prompt SHA-256 | `fd7d7a04f2a249ce1d3a631613c00d7725610694ccba69b21698e04460b9dad8` |
| 6 | User-template SHA-256 | `cc47532ba1085adeaa1b902b3af7de6f9fb54e4744172a7785d03e46d6c0ef54` |
| 7 | Tool-availability manifest (`[]`) SHA-256 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |
| 8 | Parameter manifest SHA-256 (JCS→SHA-256) | `deaaed58f4444b9dba4d671d07bddd00b319f131f902bec7e4eac802b22ad5c2` |
| 9 | Harness system-prompt version | `literal-system-prompt-per-(a)` |

Parameter manifest canonical JSON: `{"max_tokens":16000,"model":"claude-opus-5"}`

**Fields 2/3/4 provenance — stated on the face of the block:** A3's field 4 is evidenced by the
**2026-07-29 B1 emitter success envelope** on the same provider, same identifier, same call
shape — `claude-opus-5` sent, `claude-opus-5` returned, response id
`msg_011CdWjMejrrdhoXtQxN7k4R`. Source of record
`experiments/p032-emitter/out/anchor-run-metadata.json` (read-only; the emitter tree is
frozen); tickets `T-P032-B1f-live-end-to-end-basic-0-2026-07-29` (retry pass B1f2) /
`T-P032-B1g-c2-block-fill-from-live-run-2026-07-29`. **This is an emitter-envelope source, not
a scorer run.** No panel invocation of A3 has ever happened, and none is claimed. No scorer run
exists before B3; C4 check (iv) verifies this commitment at B3.

---

## 3. The C2(d) response-metadata blob rule — RULED, published alongside the digest

Decision row: `D-P032-B0d-system-fingerprint-present-but-null-2026-07-31` (COO, 2026-07-31,
`ops/decisions.md`). A digest without its rule is an unverifiable number, so the rule is stated
here in executable form:

1. Take the provider's response body as returned, parsed as JSON, at the top level.
2. **Retain every top-level key except the message-content carrier `choices`.** The retained
   key set is whatever the provider's envelope actually carries; it is not a fixed list.
   Observed: OpenAI/A1 → `created`, `id`, `model`, `object`, `service_tier`,
   `system_fingerprint`, `usage`; DeepSeek/A2 → `created`, `id`, `model`, `object`,
   `system_fingerprint`, `usage`.
3. **Drop `choices` in full** — the entire array, not only its message-content leaves.
4. Retain a key whose value is `null` **as a present key with a null value**. `system_fingerprint`
   on the A1 envelope is exactly that case, and the builder trips a halt if canonicalization
   drops it (it did not: the A1 canonical form carries `"system_fingerprint":null`).
5. Do not coerce, reorder, round, or re-type any retained value.
6. Canonicalize what remains per JCS (RFC 8785).
7. SHA-256 (FIPS 180-4) over the UTF-8 bytes of the canonicalized string. **That digest is the
   C2(d) commitment.**

The **§4b form** (`choices` dropped entirely) **is** the commitment — the redaction-independent
reading, so the digest encodes nobody's judgment call about what counts as message content.
Dropping `choices` in full removes `finish_reason` from the committed surface; a known and
accepted cost of the ruling, not an oversight. The §4a form (`choices` retained with assistant
message content keys omitted) is recorded per seat as the non-committed alternate reading, not
deleted.

### Per-seat digests

| Seat | Committed (§4b) | Alternate (§4a, not committed) |
|------|-----------------|--------------------------------|
| A1 | `448864e6d23dc288af475ac0c93bc433f05e159a8794bcc54566c5d618a37260` | `40aa82fc9cedb50837b660561ecefae973eb869524f9932e5edd9880a2603b99` |
| A2 | `364bd601a9eee61eab44304b75cd834dfa8c03c1d6d406a0d2cc1775ac4a1216` | `7ad7cc7f2761d657f525702c9e66188157dfe0f5b9a078235b1b52a8efb8662d` |
| A3 | not committed at B0d — per-scorer-run artifact; no A3 envelope exists before B3 | — |

Both A1 and A2 digests were recomputed here from the probe envelopes and match the
probe-published values (`recomputed_here_matches_probe_published: true` in the JSON; a mismatch
was a halt condition).

### Provider-shape transfer to the DeepSeek envelope — stated, not silently generalised

The rule transfers to A2's envelope with these differences, stated so it stays executable by a
stranger against each provider's actual envelope:

- DeepSeek's envelope carries **no `service_tier` key**; every other retained key is common to
  both providers.
- DeepSeek's `system_fingerprint` is a **non-null string**
  (`fp_9954b31ca7_prod0820_fp8_kvcache_20260402`) where OpenAI's came back present-but-`null`.
- DeepSeek's `usage` object additionally carries `prompt_cache_hit_tokens` and
  `prompt_cache_miss_tokens`, retained as returned per step 2 — the rule retains whatever the
  envelope carries outside `choices`.

On the previous pass A2's blob read `pending` because no A2 envelope existed. One now does; the
published rule was applied to it unchanged.

---

## 4. Normalization — stated so a reader can re-derive every digest

- **Fields 5, 6, 7:** UTF-8 bytes, BOM stripped if present, CRLF and CR normalized to LF,
  Unicode NFC, SHA-256 per FIPS 180-4.
- **Field 8 and the C2(d) blobs:** JCS (RFC 8785) canonicalization, then SHA-256 (FIPS 180-4)
  over the UTF-8 bytes of the canonicalized string.
- JCS caveat: RFC 8785 specifies UTF-16 code-unit key ordering; the serializer here sorts by
  Unicode code point. Every key in every hashed object is ASCII, where the two orderings are
  identical; the builder asserts ASCII-only keys and halts otherwise. No hashed object contains
  a floating-point number, so RFC 8785's number-formatting rules are not load-bearing.

Raw and canonical bytes of every hashed input are embedded as base64 in the JSON. All six
prompt files are BOM-free, LF-only and NFC-normalized on disk, so normalization was a no-op for
each (both encodings embedded anyway, per the emitter block's discipline).

---

## 5. Independent recomputation discipline

Every digest in this block was computed twice by independent paths, both results recorded
alongside it in the JSON: **path 1** a separately spawned `python3 -c` process using
`hashlib.sha256`; **path 2** the `sha256sum` binary at `/sbin/sha256sum`. A third in-process
read acts as a tripwire on the temp-file plumbing. All paths agreed for every digest; a
disagreement was a halt condition, not a footnote.

---

## 6. Prior contingency — A2's Fireworks parameter manifest — resolved on disk

The previous block flagged `experiments/p032-panel/manifests/A2_parameters.json` as carrying a
Fireworks model path (`accounts/fireworks/models/deepseek-v4-pro`), contingent on the A2
provider probe. **Verified on disk before hashing this pass:** the manifest now reads
`{"max_tokens":16000,"model":"deepseek-v4-pro"}` — the spec_writer fix cycle folded the
correction in. The manifest's `model` value agrees with the probe-settled field-2/3 values, so
the bytes hashed and the fields written no longer disagree; had they still disagreed, this pass
would have halted, not patched. A2 field 8 reads `changed` versus the previous block for
exactly this reason. The `contingent_fields_not_pending_but_not_settled` list is now empty.

The tool-availability observation from the previous block still holds: the three panel
manifests are the 2-byte literal `[]` with no trailing newline, so the field-7 digest differs
from the B1 emitter block's (`[]\n`, 3 bytes) for the trailing-newline reason alone. Not a
defect; C2(c) commits the literal string `[]`.

---

## 7. What this ticket did not do

- Did not author, edit or repair any prompt or manifest under `experiments/p032-panel/`
  (spec_writer's bytes, gated by adversarial_research_lead). It hashed what was on disk.
- Did not write to `experiments/p032-emitter/`; `out/anchor-run-metadata.json` was read only.
- Did not edit `ops/projects/P032_B0_BENCHMARK_PROTOCOL.md`.
- Did not call any provider API. Unmetered; local bytes plus already-captured probe JSON.
- Did not read any credential; no file under `scripts/.env` was opened. Both output files grep
  clean for the three credential prefixes named in the ticket hard rails (zero hits).
- Did not re-open, weigh, or escalate the C2(d) blob ruling; it is applied as ruled.
- Did not run `git commit`. The Director lands.

# B1 emitter commitment block — human-readable summary

Ticket: T-P032-B1d-c2-freeze-2026-07-28
Corrected: T-P032-B1e-parameter-manifest-correct-and-refreeze-2026-07-29
(field 8 only; see "B1e correction" below)
Corrected: T-P032-B1e2-drop-deprecated-parameters-2026-07-29
(field 8 only; see "B1e2 correction" below)
Filled: T-P032-B1g-c2-block-fill-from-live-run-2026-07-29
(fields 3 and 4 from the live run; see "B1g fill" below)
Machine-readable source of truth: `B1_emitter_commitment_block.json` (same directory).

Per `ops/projects/P032_B0_BENCHMARK_PROTOCOL.md` §6.3 Emitter-panel isolation
(C2(a)–C2(e) analog for the emitter). The COO pastes the JSON block into the
B0d publication ticket unmodified. Any change to the emitter after B0d
publication is a new B0-revision.

## The eight fields

| # | Field | Value |
|---|-------|-------|
| 1 | Base model | Claude Opus 5 |
| 2 | Provider | Anthropic direct API |
| 3 | API model identifier | `claude-opus-5` |
| 4 | Pinned model revision | `claude-opus-5` |
| 5 | System-prompt SHA-256 | (see JSON — `fields.5_system_prompt_sha256`) |
| 6 | User-prompt template SHA-256 | (see JSON — `fields.6_user_template_sha256`) |
| 7 | Tool-availability manifest SHA-256 | (see JSON — `fields.7_tool_availability.sha256`); manifest value: `[]` (literal empty JSON array) |
| 8 | Parameter manifest SHA-256 | (see JSON — `fields.8_parameter_manifest.sha256`); canonical form: JCS per RFC 8785, published inline in `parameter_manifest_canonical_json` |

## Hash normalization

- Fields 5, 6, 7: UTF-8 bytes, BOM stripped if present, CRLF/CR normalized to LF,
  Unicode NFC, SHA-256 (FIPS 180-4).
- Field 8: JCS (RFC 8785) canonicalization of the parameter object, then SHA-256
  (FIPS 180-4) over the UTF-8 bytes of the canonicalized string.

## Pending

None. All eight fields carry final values as of
T-P032-B1g-c2-block-fill-from-live-run-2026-07-29. See "B1g fill" below.

## Source paths

- System prompt: `experiments/p032-emitter/prompts/emitter_system.txt`
- User template: `experiments/p032-emitter/prompts/emitter_user_template.txt`
- Tool-availability manifest: `experiments/p032-emitter/manifests/tool_availability.json`
- Parameter manifest: `experiments/p032-emitter/manifests/parameters.json`

Prompt and tool-availability mtimes precede this ticket (set by B1b on
2026-07-28 at 11:14:57 to 11:15:45 local, per `stat -f '%Sm'`); those three
files are untouched since B1b. The parameter manifest was re-frozen by B1e on
2026-07-29 (see below).

## B1e correction (2026-07-29)

The B1d block hash-committed `api_model_identifier` value
`claude-opus-5-20260714`, which returns 404 (`not_found_error`) against the
metered account. Per D-P032-B1-emitter-model-id-is-dateless-claude-opus-5-2026-07-29,
ticket T-P032-B1e changed that one value in
`experiments/p032-emitter/manifests/parameters.json` to `claude-opus-5` and
recomputed field 8:

- Old field 8 SHA-256: `7739be149946359f28561e69f16d7ac75b6a5bcb427509fa8a3499e339088323`
- New field 8 SHA-256: `04ab29402682bc57f28deddfc395c5a9cb55bbc5cf44ad713a708aa0132443a2`

Fields 1, 2, 5, 6, 7 are byte-identical to B1d. Fields 3 and 4 remain pending
and fill in T-B1g from the live run's own response metadata. No emitter
execution occurred under B1e.

## B1e2 correction (2026-07-29)

The B1f live run halted at HTTP 400: Anthropic rejects the `temperature`
parameter on this model (request id `req_011CdWibRbN1ihWSsBVPj3kg`). Per
D-P032-B1-emitter-parameters-drop-deprecated-2026-07-29, ticket T-P032-B1e2
removed the `temperature` and `top_p` keys from
`experiments/p032-emitter/manifests/parameters.json`, removed the two
corresponding reads from `call_anthropic()` in
`experiments/p032-emitter/emitter.py`, and recomputed field 8:

- B1d field 8 SHA-256: `7739be149946359f28561e69f16d7ac75b6a5bcb427509fa8a3499e339088323`
- B1e field 8 SHA-256: `04ab29402682bc57f28deddfc395c5a9cb55bbc5cf44ad713a708aa0132443a2`
- B1e2 field 8 SHA-256: `5d8907c3ae2ea95c85fe571d1ac4b0ccb4eb3e3162210718358397a26754524c`

The manifest now carries six keys: `provider`, `api_model_identifier`,
`max_tokens`, `system_prompt_source`, `user_template_source`,
`user_template_placeholder`. All six values are byte-identical to their B1e
state. Fields 1, 2, 5, 6, 7 are byte-identical to B1d. Fields 3 and 4 remain
pending and fill in T-B1g from the retry's live run. No emitter execution
occurred under B1e2.

## B1g fill (2026-07-29)

Fields 3 and 4 were filled by T-P032-B1g-c2-block-fill-from-live-run-2026-07-29
from the successful live emitter run (target label `anchor`, ticket
T-P032-B1f-live-end-to-end-basic-0-2026-07-29, retry pass B1f2). Source of
record: `experiments/p032-emitter/out/anchor-run-metadata.json`.

- Field 3 = `api_model_identifier_sent` = `claude-opus-5`
- Field 4 = `api_model_field_returned` = `claude-opus-5`
- `api_response_id` = `msg_011CdWjMejrrdhoXtQxN7k4R`
- The run metadata records no request_id field, so none is quoted.

Fields 3 and 4 both read `claude-opus-5`. This is correct under dateless
pinned-snapshot IDs (Anthropic 4.6+); the pinning argument is defended inline
in the protocol per T-B0h, and independently attacked by T-B0i. Field 8
remains at the B1e2 value
`5d8907c3ae2ea95c85fe571d1ac4b0ccb4eb3e3162210718358397a26754524c`;
`parameters.json` was not touched by B1g. No field remains pending.

## Verification

The JSON block is fully self-contained: it embeds the raw and canonical bytes of
each hashed input as base64 under `prompt_files_base64`, and the JCS
canonical form of the parameter manifest as a string under
`parameter_manifest_canonical_json`. A reader can decode the base64, re-run the
normalization, re-hash, and confirm every digest independently. Both the primary
(in-script) and independent (`sha256sum` / `python3 -c`) recomputations were
performed at freeze time and are recorded in the ticket handoff.

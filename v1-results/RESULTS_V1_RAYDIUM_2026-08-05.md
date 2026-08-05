# P032 Results v1 — Raydium CP-Swap

**Target:** Raydium CP-Swap, mainnet program ID `CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C`, source pinned at commit `78f254e1023751e706df7dc15c453fc3e046697c` (protocol §1.1).
**Emitter run:** 2026-08-05.
**Measured against:** the pre-registered benchmark protocol published 2026-08-01.
**Result:** `trivial_rate_emitted` = 74 / 74 = 1.00. `section3_nontrivial_count_on_sample` = 0. `C_total` is not computable.

---

## 1. What this document is, and what it is not

This is a results report against a pre-registration. The protocol it is measured against was published on 2026-08-01 at
`https://github.com/caliperforge/solana-property-benchmark`, commit `e95467359cb7cc03ebd3583b3f9807f87fb1dd85`, before
any result existed. The push is recorded at 2026-08-01T14:05:49Z (GitHub server-side `pushed_at`), and the emitter run
reported here fired on 2026-08-05.

The protocol document published at that commit is `b0d/P032_B0_BENCHMARK_PROTOCOL.md`, sha256
`9862b050ff93ee1e65633e2e274e13ec38672e736b010394bbb47b79c8d9e1d3`. Twelve further pre-registration artifacts published
in the same commit, including the emitter and panel commitment blocks that hash-commit the emitter configuration used in
the run below.

This document reports a measurement. It does not change the measure. The 2026-08-01 files are untouched by this
publication. Nothing in §2, §3, §4 or §7 of the protocol is amended, restated in a way that alters it, or reinterpreted
here. Where this document needs a definition, it quotes the published text. This is an additive commit.

This document is not a claim about the technique in general, not a head-to-head result, and not an evaluation of the §7
kill statement. See §4 and §8.

**Sources for this section:** `ops/projects/P032/B0/PUBLICATION_RECORD_2026-08-01.md` (repository, commit, `pushed_at`
anchor, published file set and digests, rename record); `ops/projects/P032_B0_BENCHMARK_PROTOCOL.md` §1.1 (target pin).

---

## 2. The B1 emission

**74 raw properties** were emitted on Raydium CP-Swap. That is the full pre-filter candidate set: the record count of the
emitted-set JSON, the line count of the candidates log, and the `candidate_count_in_log` field of the run metadata all
read 74. No filter, no deduplication, no confidence threshold was applied; protocol §4.1 bars any pre-emit filter, and
the emitter applies none by construction.

**One live run. Zero deviations from the pinned run plan.** One API call, exit 0, `stop_reason` `end_turn`, no retry and
no variation. All four hash-committed emitter configuration fields (system prompt, user template, tool availability,
parameter manifest) were re-verified against the C2 commitment block before the call, by two independent hashing paths,
and all four matched. The run artifact records the deviation count as zero and lists every frozen file as unchanged
post-run.

Run envelope, read from the response metadata:

| Field | Value |
|---|---|
| `api_model_identifier_sent` / `api_model_field_returned` | `claude-opus-5` / `claude-opus-5` |
| `api_response_id` | `msg_011CdkEANShkBCqmV7EF5fKW` |
| `api_stop_reason` | `end_turn` |
| `api_usage_input_tokens` | 382,038 |
| `api_usage_output_tokens` | 14,154 |
| `parse_error` | none |
| Records failing the §4.6 schema check | 0 of 74 |

`stop_reason` is `end_turn` rather than `max_tokens`, so the response was not truncated against the frozen 16,000-token
output cap.

### 2.1 Cost

| Figure | Value | What it is |
|---|---|---|
| Projection | **$6.93057** | Pre-flight ceiling, recorded before the call. Assumes the response saturates the frozen 16,000-token output cap. |
| Actual | **$6.79212** | Computed from the billed `usage` figures in the response envelope. |
| Delta | **-$0.13845** (-1.998%) | Actual under projection. |

The pre-flight token measurement (382,038, via the provider's `count_tokens` endpoint) and the billed
`usage.input_tokens` agree exactly, so the entire delta is on the output side: 14,154 tokens used of the 16,000-token
cap.

Both figures use per-token rates of $15 per MTok input and $75 per MTok output. Those rates are back-solved from one
prior 39,961-token call on the same lane; they are not read off a price list. The run artifact records a hedge: if a
long-context premium applies above 200K input tokens, the projected ceiling would instead be $13.26. The hedge can be
neither confirmed nor refuted from the response envelope, which reports tokens and not dollars. The dollar figures above
are therefore derived from token counts, not billed amounts.

### 2.2 Artifact digests

| Artifact | sha256 |
|---|---|
| Emitted set, 74 records (`raydium-cp-swap.json`) | `d78c131cafc9e32516323b2bb8f3dc92b8ae73d7b238be591ac0a5e00ad180da` |
| Full pre-filter candidate log, 74 lines (`raydium-cp-swap-candidates.log`) | `e3f9a174b6820e4fd2b3fd3d33af4410a4008be6464c8a0925d8883dc9f3f14e` |
| Run metadata (`raydium-cp-swap-run-metadata.json`) | `57ec011708777d04898c8d3ca2dd23b698b50ee5b025bdd97afff02be20d82b0` |
| Raw model response (`raydium-cp-swap-raw-response.txt`) | `1e73b11327b4ccc589bcbba7f0758c9eb3ea5b3d42b76e0970a39321e3b3f488` |
| Expanded-source bundle sent to the emitter (`bundle.txt`, 1,239,890 bytes) | `e0829a71297058a622537e76a1d5c88d8ba69abe0ccbc33bf226fbc5fe635353` |

Emitter class distribution across the 74 records, per the `emitter_class` field: `pubkey_bindings` 51,
`access_control` 21, `fee_monotonicity` 2, `supply_vs_mint_agreement` 0, `vault_bindings` 0, `mint_authority` 0.

**Sources for this section:** `ops/projects/P032/B1/RUN_ARTIFACT_RAYDIUM_2026-08-05.md` §1 (halt gates), §2 (C2 hash
re-verification), §4 and §4.1 and §4.2 (count, envelope, class distribution), §5.1 through §5.7 (cost), §6 (zero
deviations), §7.1 (artifact digests); `ops/projects/P032/B1/raydium-cp-swap/raydium-cp-swap-run-metadata.json`.

---

## 3. The B2 result against the frozen §3

Protocol §3 fixes the definition of "trivial" in advance. It was applied as written to the 74 emitted records by a
deterministic pattern match, with no model in the classification path.

- **`trivial_rate_emitted` (§4.3) = 74 / 74 = 1.00.** Numerator: emitted properties classified trivial per §3.
  Denominator: `|E|` = 74. §4.3 fixes this rate on the emitted set, which is what B1 produced.
- **`section3_nontrivial_count_on_sample` = 0.**
- Unclassified per §3: 0.
- **`api_spend_usd` for the B2 leg: $0.00.** No model call was made; the classification is deterministic.

**All 74 were decided by the same clause, §3.2 T3.** §3.1 fixes §3.2 and §3.3 as mutually exclusive ("No property is
both") and fixes §3.4 as the residual for predicates that appear to fall in neither list. It fixes no precedence between
§3.2 and §3.3, and none was assumed here: every record was checked against both lists. §3.2 T3 matched all 74, §3.3 was
independently checked and excluded for all 74 (see 3.1 of this document), and §3.4 was therefore not reached. §3.2 T3,
verbatim from the published protocol:

> **T3 - Redundant Anchor-constraint re-statement.** A property whose predicate is a direct re-assertion of an Anchor
> `has_one`, `constraint`, `seeds`, `bump`, `owner`, or `signer` clause that the Anchor framework's `try_accounts`
> machinery already enforces at instruction entry. Rationale: the framework rejects the transaction before the handler
> runs if the constraint fails; a property re-asserting the same predicate post-handler is not measuring anything the
> framework did not.

The Anchor clause each predicate re-asserts, by count:

| Anchor clause the predicate re-asserts | Count |
|---|---|
| `constraint = <expr>` | 24 |
| `seeds = [...], bump` | 23 |
| `signer` / `<account>: Signer<'info>` | 21 |
| `has_one = authority` | 4 |
| `owner = token_2022::ID` | 2 |
| **Total** | **74** |

Every record in the emitted set carries a `justification_constraint` field holding the Anchor clause the emitter derived
it from, and in all 74 cases the predicate is that clause's expression after variable substitution.

### 3.1 The classifier was controlled

A classifier that returned "trivial" for everything would produce the same headline table. It does not. The classifier
was negative-controlled against the protocol's own §3.3 worked examples, which it must return non-trivial for, and
against a §3.2 worked example, which it must return trivial for:

| Protocol worked example | Returned |
|---|---|
| N2.a `pool_state.token_a_reserve.checked_add(swap_amount) != None` | non-trivial (§3.3 N2) |
| N2.b `escrow.claimed.checked_add(claim_amount) <= escrow.total` | non-trivial (§3.3 N2) |
| N2.c `pool_state.k_last <= …checked_mul(…)` | non-trivial (§3.3 N2) |
| N3.a `cpi_target_program.key() == spl_token::ID` | non-trivial (§3.3 N3) |
| N3.b `payer.key() != recipient.key()` | non-trivial (§3.3 N3) |
| T1.a `pool_state.bump_after == pool_state.bump_before` | trivial (§3.2 T1) |

The classifier returns non-trivial when the predicate shape warrants. The 74/74 result is a property of the Raydium
emitted set under §3, not an artifact of a matcher that returns one answer. The Raydium set contains no predicate of any
§3.3 shape: no `checked_*` or `saturating_*` call site appears in any of the 74 predicates, and no CPI-target equality
appears.

Two families were checked by hand against §3.3 N3 because they resemble it in shape, and both are excluded by N3's own
text. Records `0040` and `0044` assert `*token_mint.to_account_info().owner == token_2022::ID`; N3.c requires that the
owning-program equality not be declared by `#[account(owner = …)]`, and here it is declared. Records `0062`, `0065`,
`0067`, `0071` and `0074` assert `authority.key != &ERASED_AUTHORITY`; N3 requires a distinctness predicate that no
Anchor `has_one` / `constraint` / `owner` clause covers, and here a `constraint =` clause covers it exactly.

### 3.2 Two matcher defects, found and fixed during the run

The first execution of the classifier returned 68 trivial and 6 unclassified. Both causes were defects in the
implementation's text normalizer, not §3 outcomes. A `str.strip("()")` was consuming the trailing `()` of
`authority.key()`, corrupting 4 `has_one` predicates; and the `owner` clause matcher required `==` where the Anchor
clause carries a single `=`, failing 2 `owner` records. After the fix those 6 land as trivial via §3.2 T3, giving 74/74.
Both fixes make the matcher read the declared text correctly. Neither adds, relaxes, or reorders a §3 rule.

### 3.3 Reproducibility note on the 74

An internal hand triage of the same 74 records, performed separately and not used as an input to the classifier,
returned 58 trivial rather than 74. The two counts agree exactly on the signer family (21) and the PDA-derivation family
(23) and diverge on the third: the hand read counted 14 `has_one` restatements and set the remaining 16 aside as
duplicates or as properties attaching to Anchor's generated IDL-account instructions. §3 has no duplicate exemption and
no generated-instruction exemption. It classifies on predicate shape, and each of those 16 carries a `constraint =` or
`owner =` clause that its predicate restates verbatim, which is §3.2 T3.

This is recorded because a third party hand-classifying the published emitted set is likely to reach the same 16
records and needs to know that §3 as written admits no such exemption. The agreement on the other 44 records is not
independent corroboration of the classifier; it is two methods matching on the two families whose shape is least
ambiguous.

**Sources for this section:** `agents/audit_engineer/outbox/T-P032-B2-certify-raydium-section3-2026-08-05_result.md`
§2 (verdict table, clause counts), §2.1 (control table, N3 exclusions), §2.2 (matcher defects), §8 (74-vs-58 delta),
§9 (API spend); `ops/projects/P032_B0_BENCHMARK_PROTOCOL.md` §3.1, §3.2 T3, §3.3, §4.3;
`ops/projects/P032/B2/tier1-raydium.json` (74 records, all `trivial`).

---

## 4. `C_total` is not computable. It is not zero.

Protocol §4.2 defines certification. Verbatim:

> A property is **certified** if it clears all three B2 checks: (i) compiles into the Crucible harness fixture, (ii) is
> non-vacuous per B2's per-property execution-counter instrumentation (execution count > 0), (iii) fires when a
> third-party mutation-engine-produced mutant of its class is injected.

**None of the three checks has been run on this target by anyone.** `ops/projects/P032/B2/` was empty at B2 dispatch.
The B1 artifact carries the §4.1 emitted-set fields only: no compile result, no execution counter, no mutation-kill
verdict. No property on this target is certified within the meaning of §4.2.

Therefore, on this target:

| Quantity | Value |
|---|---|
| `C_total` | not computable — the certified set does not exist |
| `C_baseline` | not computable — requires both the certified set (absent) and the §2.13 bucket assignment (empty) |
| `C_baseline / C_total` | not computable — both terms undefined |
| The §7.2 read | not computable |

**No `null` is a `false`.** Six of the §6.1 mechanical fields were emitted `null` on all 74 records, each carrying an
explicit `unavailable_reason`: `compiles`, `non_vacuous`, `mutant_kills`, `radar_flags_same_predicate`,
`xray_flags_same_predicate`, and `landscape_class_bucket`. The derived rates that depend on them —
`certification_pass_rate`, `certified_class_distribution`, `above_baseline_count`, `C_total_this_target` — are likewise
`null` with reasons. A `null` on `landscape_class_bucket` does not mean "bucketed and found not above baseline". A
`null` on `radar_flags_same_predicate` does not mean Radar reported nothing; the Radar and X-Ray legs are B3 inputs and
have not run. **No proxy was substituted for any of them.** Neither the §3 non-trivial count nor `|E|` was used to stand
in for the certified count.

The only thing derivable about `C_total` without judgement is the §4.2 containment `C ⊆ E`, giving
`0 ≤ C_raydium ≤ 74`. That is a direct consequence of §4.2's own text. It is not an estimate and it narrows nothing.

**§3 triviality and §4.2 certification are independent quantities.** A trivial property can certify cleanly: a signer
check compiles, executes, and would fire against a mutant that removes the signer check. A non-trivial property can fail
to certify. The 74/74 trivial rate of §3 above therefore implies nothing about the certified count, and zero non-trivial
properties does not mean zero certified properties.

### 4.1 Nothing here is the §7 gate firing

The pre-committed kill statement, verbatim from the published protocol:

> **If certified properties land predominantly in classes the existing analyzers already flag, we stop and publish that
> result.**

§7.2 defines the terms: `C_baseline` is the count of certified properties **across both targets** whose landscape-class
bucket falls in the §7.1 already-flagged set; `C_total` is `|C_raydium| + |C_meteora|`; and "predominantly" means
`C_baseline / C_total >= 0.70`. §7.2 also carries a minimum-`C_total` branch that fires the kill by construction when
`C_total < 5`.

Neither branch is evaluated here, and neither can be. `C_total` is not computable on Raydium because no §4.2
certification has been run on this target, and independently of that, §7.2 is defined over both targets: Meteora Alpha
Vault has not been emitted at all, let alone certified. Whether the `C_total < 5` branch is met cannot be determined,
because the count it tests does not exist.

The §7.1 already-flagged set is likewise not determined. §7.1 defines it as `{2, 7} ∪ {classes reported by Radar} ∪
{classes reported by X-Ray}`. Classes 2 and 7 are the construction-flagged floor; the two analyzer legs are B3 inputs
that have not run, so the set can only be stated as that floor and can only grow.

**The kill statement is neither fired nor not-fired by this document.** §7 is not evaluable on either target until §4.2
certification records exist for both, and the protocol decides at B3.

**Sources for this section:** `ops/projects/P032_B0_BENCHMARK_PROTOCOL.md` §4.1, §4.2, §6.1, §7 (kill statement), §7.1,
§7.2; `agents/audit_engineer/outbox/T-P032-B2-certify-raydium-section3-2026-08-05_result.md` §3, §4, §5, §6 finding 5,
§7; `agents/audit_engineer/escalations/E-P032-B2-protocol-application-2026-08-05.md` Item 2.

---

## 5. Post-hoc diagnosis — formed after the result, not pre-registered

**Everything in this section is post hoc.** It was formed after the 74/74 result was known. It is a hypothesis, it is
not evidence, and nothing in it was registered in advance. It is recorded here because a reader is entitled to the
authors' reading of why the number came out this way, clearly marked as what it is. Testing it requires a new run under
a new registration.

### 5.1 The post-hoc hypothesis, in one line

The set of evidence the emitter was permitted to use and the set of properties §3 counts as non-trivial have an empty
intersection by construction.

### 5.2 What the frozen emitter was permitted to read (this part is not post hoc)

The emitter system prompt is frozen and hash-committed. Its sha256 is
`8c509d421b2b5f9bb1eb706b42d9f8a383893f2355500c92b8bb762595222584`, committed before the run as field
`5_system_prompt_sha256` of the B1 emitter commitment block, and re-verified against that commitment by two independent
hashing paths at run time.

That prompt admits evidence exclusively from six Anchor clause types, listed in it as:

> 1. has_one = <field>
> 2. seeds = [<expr>, ...]
> 3. bump (paired with seeds)
> 4. owner = <program_id>
> 5. signer (or a field whose type is Signer<'info>)
> 6. constraint = <expression>

It states, verbatim:

> No other source of evidence is admissible.

and, verbatim:

> The identifier of a field carries no meaning to you.

### 5.3 What §3 counts as trivial (this part is not post hoc)

§3.2 T3, quoted in full in §3 above, defines a property whose predicate re-asserts an Anchor `has_one`, `constraint`,
`seeds`, `bump`, `owner`, or `signer` clause as trivial, because the framework already enforces it at instruction entry.
That is the same six-clause set.

### 5.4 The post-hoc reading

The six clause types the emitter may read are the six clause types §3.2 T3 names as framework-enforced. On this
post-hoc reading, an emitter restricted to that evidence set can only produce restatements of framework-enforced
constraints, and every such restatement is trivial by §3.2 T3. The observed result is 74 of 74 decided at §3.2 T3, all
tracing to a `justification_constraint` field naming one of those six clauses.

### 5.5 The bundle did contain the economic machinery (post-hoc observation)

The expanded-source bundle sent to the emitter, sha256
`e0829a71297058a622537e76a1d5c88d8ba69abe0ccbc33bf226fbc5fe635353`, 1,239,890 bytes, contains the program's economic
code. Raw substring occurrence counts over that file, by `grep -o <token> | wc -l`:

| Token | Occurrences in the bundle |
|---|---|
| `CurveCalculator` | 26 |
| `checked_mul` | 19 |
| `fee_rate` | 187 |

The `fee_rate` count is of the substring, and every occurrence sits inside a longer identifier. The decomposition below
uses a second counting method, longest-identifier match: each occurrence is attributed only to the full identifier
surrounding it, so an occurrence nested inside an `update_` or `adjust_` variant counts against that variant and not
against the shorter name. It reproduces on the bundle at the recorded digest with
`grep -o '[A-Za-z0-9_]*fee_rate[A-Za-z0-9_]*' <bundle> | sort | uniq -c`:

```
 48 creator_fee_rate         46 trade_fee_rate             41 protocol_fee_rate
 41 fund_fee_rate             3 adjust_creator_fee_rate     2 update_creator_fee_rate
  2 update_trade_fee_rate     2 update_protocol_fee_rate    2 update_fund_fee_rate
```

The four base identifiers and the five `update_`/`adjust_` variants partition the 187 occurrences with no overlap:
48 + 46 + 41 + 41 + 3 + 2 + 2 + 2 + 2 = 187.

The two methods are not interchangeable and do not agree on the four base identifiers. Run against the same bundle,
`grep -o creator_fee_rate | wc -l` returns 53, `trade_fee_rate` 48, `protocol_fee_rate` 43 and `fund_fee_rate` 43,
because that method also matches inside the longer variants; those four figures double-count the nested occurrences and
do not partition 187. The `grep -o <token> | wc -l` attribution stated for the three-row table above is correct for
those three tokens, none of which is nested inside another. The bare identifier `fee_rate` does not occur:
`grep -ow fee_rate` returns 0. The counts are raw text occurrences, not distinct code sites, and both methods are named
so a reader can reproduce every figure in this section against the recorded digest.

The emitter was barred from deriving properties from any of it. None of these appears in an admissible clause, and the
prompt states the identifier of a field carries no meaning to the emitter. The material was in the input and the
instrument could not read it as evidence.

### 5.6 The one channel that could have carried arithmetic, and what it actually carried (post-hoc observation)

`constraint = <expr>` is the one admissible clause type that can carry arbitrary arithmetic. Two of the 74 records
carry the emitter class `fee_monotonicity`, and both came through that clause type. Their content:

| Record | Predicate | `justification_constraint` | Instruction |
|---|---|---|---|
| `raydium-cp-swap-0007` | `token_0_mint.key() < token_1_mint.key()` | `constraint = token_0_mint.key()<token_1_mint.key()` | `Initialize` |
| `raydium-cp-swap-0048` | `token_0_mint.key() < token_1_mint.key()` | `constraint = token_0_mint.key()<token_1_mint.key()` | `InitializeWithPermission` |

The predicate is a mint-address ordering comparison. It carries no economic content. The class label is assigned
mechanically and does not describe the predicate's subject: the frozen user template (sha256
`edd99e4bb987ff133ef2938f73604e429bf1a4f968a5bd9b02005d80cc3439ea`, committed as C2 field `6_user_template_sha256`)
rule 5c assigns `fee_monotonicity` to any `constraint` expression that is an inequality between two operands, and the
system prompt states that the class strings are opaque enum labels assigned by mechanical rule rather than by reasoning
about what the labels mean.

**These two records do not confirm the post-hoc hypothesis in §5.1.** The channel that could have carried the program's
economics carried no economic predicate in this run. Whether the economics would come through that channel under a
different instrument is untested.

### 5.7 Status of this section: post hoc, untested

The whole of §5 is a hypothesis formed after seeing the result. It is not evidence for or against the technique. It has
not been tested. Testing it means changing the instrument and running again, which under §7 below is a new
registration.

**Sources for this section:** `experiments/p032-emitter/prompts/emitter_system.txt` (sha256 `8c509d42…2584`, verified);
`experiments/p032-emitter/prompts/emitter_user_template.txt` (sha256 `edd99e4b…39ea`, verified);
`ops/projects/P032/B0/B1_emitter_commitment_block.json` field `5_system_prompt_sha256`;
`ops/projects/P032/B1/RUN_ARTIFACT_RAYDIUM_2026-08-05.md` §2 (C2 re-verification), §3.5 (bundle digest and size);
`ops/projects/P032/B1/raydium-cp-swap/raydium-cp-swap.json` (the two `fee_monotonicity` records);
`experiments/p032-emitter/out/raydium-cp-swap/bundle.txt` at the recorded digest (occurrence counts);
`ops/projects/P032_B0_BENCHMARK_PROTOCOL.md` §3.2 T3.

---

## 6. Three open application questions, unresolved at publication

The audit seat that applied §3 raised three questions about how the published protocol applies to this data. It
escalated all three rather than resolving any of them, and all three are open at the time this document publishes. They
are stated here as questions. This document does not resolve any of them, states no preference between the available
readings, and no reading has been applied to any number above.

### 6.1 Item 1 — §2.7 and §2.3 both reach the same 23 PDA predicates

This is the item that moves a number in our favour on one of its two readings, which is why it is stated in full.

§2.7 (Landscape Class 7, bucket **(a) subsumed**, which is baseline coverage and does not count as above-baseline),
verbatim:

> Coverage rule: any certified P032 property whose predicate asserts
> `<account>.key() == find_program_address(<seeds>, <program_id>)` where `<seeds>` includes the canonical bump byte from
> the Anchor `bump` clause counts as covering Class 7.

§2.3 (Landscape Class 3, bucket **(b) partial**, which can yield `b-with-rule-pass`, i.e. above baseline), verbatim:

> Coverage rule: a P032 property counts as covering Class 3 if and only if its predicate reduces to
> `<account>.key() == find_program_address(<seed_expr>, <program_id>)` and every symbol in `<seed_expr>` resolves to a
> field that appears in the same instruction's account context.

23 of the 74 emitted records have this shape. One of them, `raydium-cp-swap-0002`, has predicate
`authority.key() == Pubkey::find_program_address(&[crate::AUTH_SEED.as_bytes()], program_id).0` and
`justification_constraint` `seeds = [crate::AUTH_SEED.as_bytes()], bump`.

The tiebreak turns on a Rust API detail. `find_program_address` derives the canonical bump and returns it as tuple
element `.1`; it does not consume a bump byte as an input seed. The function that consumes a bump in its seed array is
`create_program_address`. On a literal read of §2.7, the argument `&[crate::AUTH_SEED.as_bytes()]` does not include the
canonical bump byte, §2.7 does not match, §2.13's precedence order falls through to §2.3, and the 23 records bucket as
Class 3 `(b) partial`. On the other read, the Anchor `bump` clause is present in the declaration and the canonical bump
is what `find_program_address` returns, so §2.7 matches and the 23 records bucket as Class 7 `(a) subsumed`.

**What turns on it.** Classes 2 and 7 are exactly the two classes §7.1 counts as already flagged by construction. On the
first read, 23 of 74 records move out of the §7.1 already-flagged set and become eligible for above-baseline credit. On
the second, they stay inside it. That directly moves the `C_baseline / C_total` ratio that §7.2 tests against 0.70, in
the direction that favours the tool on the first read. This is not a presentational question.

The audit seat noted, without applying it, that §2.7's own text refers to the earlier "23-of-25-trivial finding on
Raydium" being "dominated by bump-seed conservation properties", which is context and not a resolution.

The question is unresolved. It is with the COO, who decides whether it requires a B0-revision re-publication. No reading
has been applied to any number in this document.

### 6.2 Item 2 — the §4.2 certified set does not exist

This is the same fact reported in §4 above: none of the three §4.2 checks has been run on this target, so `C_total` is
not computable. It is escalated as an open question about whether a separate certification leg is dispatched. See §4.

### 6.3 Item 3 — §2.3 and §3.4 Step 2 read input the B1 artifact does not carry

§2.3's Class-3 coverage rule requires that every symbol in `<seed_expr>` resolve to a field that appears in the same
instruction's account context. §3.4 Step 2 clause (2c) likewise requires reading whether an account declaration carries
`mut`, `init`, `init_if_needed`, `realloc`, or `close`. Both read the instruction's account context. The B1 emitted-set
artifact records the originating constraint clause but not the account-context field list or its writability markers,
so neither rule is fully computable from that artifact alone.

This is a question about the emitter artifact's schema, not about the protocol text. It did not bite at B2: all 74
records were decided at §3.2 T3, so §3.4 Step 2 was never reached. It binds at B3 for any record that does reach §3.4
Step 2. Unresolved.

**Sources for this section:** `agents/audit_engineer/escalations/E-P032-B2-protocol-application-2026-08-05.md` Items 1,
2 and 3, attributed to the audit seat; `ops/projects/P032_B0_BENCHMARK_PROTOCOL.md` §2.3, §2.7, §2.13, §3.4, §4.2,
§7.1.

---

## 7. What comes next

Any follow-up that changes the instrument is a new registration rather than an amendment to this one, and it will be
published before it is run.

---

## 8. Scope and limits

One live run, one target, one emitter configuration. This is not a claim about the technique in general.

- **One target of two.** The protocol pins two targets (§1). Meteora Alpha Vault has not been emitted. Every number here
  is Raydium CP-Swap only, and §7.2's terms are defined over both targets.
- **One run.** A single API call, not a repeated measurement. No variance estimate exists and none is offered.
- **One emitter configuration.** The result is a measurement of the frozen configuration hash-committed before
  publication, not of any other configuration.
- **Emitted set only.** §4.3 measures the trivial rate on the emitted set. No certified set exists on this target, so
  the certification pass rate (§4.4), the certified class distribution (§4.5) and the above-baseline counts (§2.13) are
  not reported.
- **No head-to-head.** The Radar and Sec3 X-Ray legs (protocol §5) are B3 inputs and have not run. No coverage map is
  reported.
- **No panel.** The Tier 3 scorer panel (protocol §6.3) is a B3 procedure and has not run. Every classification here is the
  mechanical Tier 1 §3 rubric.
- **Three protocol-application questions are open**, one of which (§6.1 above) moves a number in the tool's favour on
  one of its two readings. None is resolved here.
- **Target-scope observation, recorded and not acted on.** 17 of the 74 records attach to Anchor's generated IDL
  instructions (`IdlCreateAccounts`, `IdlAccounts`, `IdlResizeAccount`, `IdlCreateBuffer`, `IdlSetBuffer`,
  `IdlCloseAccount`) rather than to Raydium's own instruction set. §3 classified them on predicate shape exactly as it
  classified the rest, and their provenance changed no verdict. Whether framework-generated instructions belong in the
  emitted set is a question about the emitter's scope, not about §3, and it is unresolved.
- **Cost figures are derived from token counts**, not from billed amounts, at back-solved per-token rates. See §2.1.

**Sources for this section:** `ops/projects/P032_B0_BENCHMARK_PROTOCOL.md` §1, §2.13, §4.3, §4.4, §4.5, §5, §6.3, §7.2;
`agents/audit_engineer/outbox/T-P032-B2-certify-raydium-section3-2026-08-05_result.md` §6 finding 6 (the 17 records),
§7; `ops/projects/P032/B1/RUN_ARTIFACT_RAYDIUM_2026-08-05.md` §5.2 and §5.7.

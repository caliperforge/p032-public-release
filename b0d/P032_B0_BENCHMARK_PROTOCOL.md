# P032 B0 - Pre-Registered Benchmark Protocol

**Project:** P032 (Solana tool, build-to-win shape).
**Sprint:** B0-revision (pre-registration). Nothing in B1 fires until this document is published.
**Draft by:** spec_writer. **Ticket:** T-P032-B0a-benchmark-protocol-draft-2026-07-27.
**Drafted:** 2026-07-27. **Fix-pass:** 2026-07-27 (ticket T-P032-B0a-fix-pass-2026-07-27; closes ten holes from T-P032-B0b-gameability-review-2026-07-27). **Revision-pass:** 2026-07-28 (ticket T-P032-B0e-section6-rewrite-2026-07-28; rewrites §6 to a pre-committed agent panel per CEO ruling). **Revision-pass fix cycle:** 2026-07-28 (ticket T-P032-B0e2-section6-hole-fix-2026-07-28; closes six holes H1..H6 from T-P032-B0f-gameability-rereview-2026-07-28). **Panel-composition amendment:** 2026-07-28 (ticket T-P032-B0e3-section6-panel-composition-amendment-2026-07-28; amends §6 to the CEO's option-C cross-lab scorer panel per `D-P032-panel-composition-2026-07-28`, panel becomes GPT-5.6 Sol · DeepSeek-V4-Pro · Claude Opus 5 as standalone scorer configurations rather than CaliperForge seats; §1–§5, §7, §6.1, §6.2 substance unchanged). **Register re-check on the panel amendment:** 2026-07-28 (tickets T-P032-B0g2-section6-4a-recheck-panel-amendment-2026-07-28 and T-P032-B0g2-rerun-panel-amendment-2026-07-28; §4a re-check and re-run over the amended §6 text). **C2(d) identifier pass:** 2026-07-29 (ticket T-P032-B0h-protocol-c2d-model-id-and-dateless-citation-2026-07-29; corrects the A1 and A3 API model identifiers in C2(d) and adds the dateless-pinned-snapshot citations). **Gameability re-review on C2(d) dateless pinning:** 2026-07-29 (review ticket T-P032-B0i-gameability-rereview-c2d-dateless-pinning-2026-07-29; verdict PARTIALLY LANDS, routed into the B0k fix cycle below). **Register pass on the B0h text:** 2026-07-29 (review ticket T-P032-B0j-anti-ai-ism-4a-on-b0h-2026-07-29). **C2(d) and C4 wire-level tightening:** 2026-07-29 (tickets T-B0k1-protocol-c2d-c4-wire-level-tightening-2026-07-29 and T-B0k1-fix-candor-amendment-2026-07-29; adds the per-run provider response identifier and response-metadata blob commitments to C2(d) and check (v) to C4, and states in the text what those commitments do not verify; checker and tests under T-B0k2-checker-harness-check-v-2026-07-29 and T-B0k3-4b-checker-and-tests-2026-07-29; re-attacked under T-B0k4-rereview-c2d-c4-pinning-attack-2026-07-29 and T-B0k4-rerun-c2d-c4-pinning-attack-2026-07-29). **Notarization pass, sealed 2026-07-30:** 2026-07-30 (TSA probe T-B0m0-rfc3161-tsa-probe-2026-07-30; protocol edits T-B0m1-protocol-c2-c4-notarization-2026-07-30 with T-B0m1-fix-candor-extension-2026-07-30 and T-B0m1-fix2-system-fingerprint-hedge-2026-07-30; adds C2(f) committed scorer-run count `N`, C2(g) RFC-3161 notarization with pinned primary and fallback TSAs, and check (vi) to C4; harness and tests under T-B0m2-harness-checker-check-vi-2026-07-30 and T-B0m3-4b-checker-and-tests-2026-07-30; re-attack T-B0m4-rerun-attack-amended-candor-2026-07-30 LANDS_CLEAN; §4a T-B0m5-4a-on-changed-text-2026-07-30 PASS; §4c T-B0m6-4c-on-changed-text-2026-07-30 and T-B0m6-rerun-system-fingerprint-hedge-2026-07-30 PASS). **B0d panel prompts:** 2026-07-31 (tickets T-P032-B0d-panel-prompts-2026-07-31 and T-P032-B0d-panel-prompts-fix1-2026-07-31, gate T-P032-B0d-panel-prompt-gameability-2026-07-31; authors the three committed scorer prompts that C2(a) and C2(b) hash, held outside this document and committed in the B0d publication ticket). **§6.3 lens amendment:** 2026-07-31 (ticket T-P032-B0d-lens-amendment-2026-07-31 under `D-P032-B0d-panel-lens-overlap-amend-not-concede-2026-07-31`; replaces A1's refutation lens with the falsification-witness lens and moves the Section 3 under-tuning diagnostic from majority to unanimity, closing `H7-A1-AND-A2-ARE-ONE-LENS` and `H8-SECTION-3-GRADES-ITSELF`; re-attack T-P032-B0d-lens-reattack-2026-07-31). **H11 user-template fix:** 2026-07-31 (ticket T-P032-B0d-h11-user-template-2026-07-31, recheck T-P032-B0d-h11-recheck-2026-07-31; changes A1's committed user-prompt template only and does not touch this document). **H12 through H15 pass:** 2026-07-31 (ticket T-P032-B0d-h12h15-protocol-pass-2026-07-31; §3.4 and §6.3 edits, including the stated residual overlap `H12-OVERLAP-MOVED-TO-A1-A3-NOT-CLOSED`; re-attack T-P032-B0d-h12h15-reattack-2026-07-31). **H16 and H17 pass:** 2026-07-31 (ticket T-P032-B0d-h16h17-2026-07-31; the §3.4 (2c) rule and its rationale, and the C4 test-suite counts in §6.3). **C4 check (vii):** 2026-07-31 (ticket T-P032-B0d-c4-check-vii-2026-07-31, with T-P032-B0d-checker-json-committed-n-2026-07-31 on the committed-`N` record; adds the collapse-rule recomputation check and the `collapse_rule_match` field to C4). **Publish-runway defect pass:** 2026-07-31 (ticket T-P032-B0y-defects-and-outreach-2026-07-31; corrects this Status line and this drafting chain, and re-seats A2 on the DeepSeek first-party API in §6.3 and C2(d) per `ops/projects/P032/B0/A2_deepseek_probe_2026-07-31.md`).
**Authority:** shape lock `D-P032-shape-locked-post-s5b-kill-2026-07-27`; framing `D-P032-headtohead-coverage-map-2026-07-27`; sequence `D-P032-sequence-kill-gate-before-ludo-2026-07-27`; renaming `D-P032-sprint-renaming-B0-B5-2026-07-27`; §6 adjudication `D-P032-B0-section6-agent-panel-reverted-2026-07-27` (CEO, resolved 2026-07-28); §6 panel composition `D-P032-panel-composition-2026-07-28` (CEO, option C, decided 2026-07-28).
**Status:** SEALED for B0d publication. The §6-panel-composition-amendment adversarial re-review (T-P032-B0f3-gameability-review-panel-amendment-2026-07-28) returned PASS on 2026-07-28; every revision after it is recorded in the drafting chain above, through the publish-runway defect pass of 2026-07-31. No section of this document is open for further edit: any change after B0d publish requires re-publishing the protocol as a new B0-revision.

## Purpose (read this first)

This document records, in advance and in public, how the P032 tool will be judged. It is written before any B1 build fires and before any result exists. The point of pre-registration is to name the failure condition before we have seen the answer. If any section leaves discretion to the person running the gate, that discretion is a defect and the section is rewritten until the defect is gone.

The document is measurement-only. It describes what will be measured, how, on what, by whom, and how ties get broken. It does not describe the tool's implementation and it does not describe the harness. B1 through B5 build. B0 measures.

## Sections

1. Targets, pinned.
2. Classification rubric - mapping the six baseline classes onto the twelve Solana vulnerability classes, with the definition of "above baseline" fixed in advance.
3. The definition of "trivial", fixed in advance.
4. What gets measured - numerators and denominators, unambiguously.
5. Head-to-head design - coverage map, not scoreboard.
6. The adjudication rule - four tiers, in this order.
7. The pre-committed kill statement.

---

## Section 1 - Targets, pinned

Two on-chain programs. No third target may be added after this document is published. Each target is pinned by mainnet program ID plus the source artifact and SHA used for property authoring and for benchmark comparison. The IDL fetch method and fetch date are recorded so a third party can reproduce the input set.

### 1.1 - Raydium CP-Swap

- **Program ID (mainnet-beta):** `CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C`.
- **Source repository:** `https://github.com/raydium-io/raydium-cp-swap`.
- **Pinned commit SHA:** `78f254e1023751e706df7dc15c453fc3e046697c` (HEAD of `master` at 2026-06-12T02:08:51Z, verified via `api.github.com/repos/raydium-io/raydium-cp-swap/branches/master` on 2026-07-28).
- **License:** Apache-2.0.
- **IDL fetch method:** fetched from mainnet against program ID `CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C`, per the P032 baseline (`ops/projects/P032_BASELINE_BRIEF.md` §"What it has actually produced").
- **IDL fetch date (baseline reference):** IDL used in B1 will be re-fetched on the day B1 fires and its fetch timestamp recorded in the B1 run artifact.

### 1.2 - Meteora Alpha Vault

- **Program ID (mainnet-beta):** `vaU6kP7iNEGkbmPkLmZfGwiGxd4Mob24QQCie5R9kd2` (per `MeteoraAg/alpha-vault-sdk` constant `PROGRAM_ID["mainnet-beta"]` at `ts-client/src/alpha-vault/constant.ts`, verified 2026-07-28).
- **On-chain program source:** not published as an open-source repository. `MeteoraAg` publishes an SDK, not the on-chain program crate. Property authoring works from the SDK-shipped IDL plus the deployed bytecode, not from a source clone.
- **IDL source repository:** `https://github.com/MeteoraAg/alpha-vault-sdk` (ships `ts-client/src/alpha-vault/alpha_vault.json`).
- **Pinned SDK commit SHA:** `7ab389d97db1ad3b4e1889b38487f54ba0ed2a67` (HEAD of `main` at 2026-03-26T09:09:00Z, verified via `api.github.com/repos/MeteoraAg/alpha-vault-sdk/branches/main` on 2026-07-28).
- **SDK repository license:** the repository ships no LICENSE file (SPDX `null` per GitHub API). The IDL JSON is a machine-readable interface description consumed as data, not as licensed source; if downstream distribution of the IDL becomes contested, this document's public copy carries no rehost of the IDL and links to the upstream file instead. Flagged for spec awareness; not a gate.
- **IDL fetch method:** IDL used in B1 will be read from the pinned SDK commit at `ts-client/src/alpha-vault/alpha_vault.json`. If the IDL also verifies against mainnet by direct on-chain fetch on B1 fire day, that mainnet fetch is recorded alongside.
- **IDL fetch date (baseline reference):** IDL used in B1 will be re-fetched on the day B1 fires and its fetch timestamp recorded in the B1 run artifact.

### 1.3 - Moving-target rule

No target substitutions after publication. No third target added. If between publication and B1 fire time either upstream repository becomes archived, disabled, or unreachable, or either program ID changes deployment, that fact is documented at B1 fire time and the change is disclosed in the published result; the target is not silently swapped. The B0 pre-registration is the authoritative target list.

---

## Section 2 - Classification rubric

The baseline tool (`caliperforge/cf-invariants-anchor`) emits invariants across six classes, per `ops/projects/P032_BASELINE_BRIEF.md`: pubkey bindings, supply-vs-mint agreement, fee monotonicity, vault bindings, mint-authority, access control. The Solana vulnerability landscape splits into twelve classes per `agents/audit_engineer/outbox/T-P032-S2-vuln-class-matrix-2026-07-27_result.md` §Half-1a: (1) missing owner check, (2) missing signer check, (3) account substitution / missing PDA validation, (4) type cosplay / discriminator confusion, (5) arithmetic overflow / precision loss, (6) duplicate mutable account, (7) bump-seed canonicalization, (8) closing accounts / revival, (9) CPI target / missing program ID check, (10) oracle price manipulation / economic design, (11) governance timing / flash-loan governance, (12) off-chain key exposure / operational compromise.

S5b Defect 2.1 identified the mapping between the six baseline classes and the twelve landscape classes as not one-to-one, and named the resulting discretion (which the engineer running the gate would otherwise get to exercise) as a definitional escape from measurement. The rows below remove that discretion. Each of the twelve landscape classes is placed in one of three buckets: (a) subsumed by one of the six baseline classes, (b) partially subsumed, or (c) not covered. Every partial-subsume row states the specific rule that decides whether a given certified P032 property counts as covering that landscape class. Any "above baseline" claim published later must cite a specific (c) row (or a (b) row where the mechanical rule below returns "does not cover"). Runner discretion is removed here or the gate stays broken.

### 2.1 - Landscape Class 1 (missing owner check)

Bucket: **(b) partial**. The baseline's "pubkey bindings" class emits equality-of-Pubkey constraints between account fields but does not directly emit an "owner equals expected program" check. The Anchor `#[account(owner = ...)]` constraint is the mechanical shape. Coverage rule: a P032 property counts as covering Class 1 if and only if the emitted property's predicate is a Pubkey equality of the form `account.owner == <constant_program_id_or_bound_field>` where the right-hand side is either (i) a program ID constant literal cited in the property or (ii) another account's declared program owner referenced by field name. Any other Pubkey equality does not count.

### 2.2 - Landscape Class 2 (missing signer check)

Bucket: **(a) subsumed** by the baseline's "access control" class, which reads Anchor `Signer<'info>` and `#[account(signer)]` bindings and emits per-instruction signer-required properties. Coverage rule: any certified P032 property whose predicate is `<account>.is_signer == true` at instruction entry counts as covering Class 2.

### 2.3 - Landscape Class 3 (account substitution / missing PDA validation)

Bucket: **(b) partial**. The baseline's "pubkey bindings" and "vault bindings" cover PDA-derivation equalities where the seed set is declared in the IDL. They do not cover semantic PDA-role substitution (the S5b Attack-3 finding: a mechanically correct constraint on a semantically wrong role). Coverage rule: a P032 property counts as covering Class 3 if and only if its predicate reduces to `<account>.key() == find_program_address(<seed_expr>, <program_id>)` and every symbol in `<seed_expr>` resolves to a field that appears in the same instruction's account context. Properties that assert a role name (e.g., "this is the vault authority") without also asserting the PDA derivation as above do not count.

### 2.4 - Landscape Class 4 (type cosplay / discriminator confusion)

Bucket: **(c) not covered**. The baseline emits properties from the IDL account struct list; it does not emit discriminator-check properties (Anchor's 8-byte account discriminator is enforced by the framework's `try_accounts` machinery and is not a candidate for a suggested invariant). A P032 property claiming Class 4 coverage would need to assert a discriminator-equality predicate; the baseline emits none such. Coverage rule: a P032 property counts as covering Class 4 if and only if its predicate is `<account>.discriminator == <constant_8byte_prefix>` under an instruction whose handler dispatches on account discriminator.

### 2.5 - Landscape Class 5 (arithmetic overflow / precision loss)

Bucket: **(b) partial**. The baseline's "fee monotonicity" class covers a narrow arithmetic-invariant slice (fee rate monotone in trade size, or fee rate bounded by declared parameters). It does not cover general integer-overflow, saturation, or precision-loss classes. Coverage rule: a P032 property counts as covering Class 5 if and only if its predicate is either (i) a monotonicity assertion between two named IDL-declared numeric fields under a named instruction, with the direction declared in the property, or (ii) an overflow-non-occurrence assertion tied to a specific `checked_add` / `checked_mul` / `checked_sub` call site named in the property text. Fee monotonicity alone (i) is baseline. Only (ii) counts as above-baseline within Class 5.

### 2.6 - Landscape Class 6 (duplicate mutable account / aliasing)

Bucket: **(c) not covered**. The baseline emits per-field-position Pubkey equalities but does not emit per-instruction distinctness constraints across mutable account slots (the Anchor `#[account(...)]` constraint grammar does not require distinctness by default). A P032 property claiming Class 6 coverage would need to assert `<account_a>.key() != <account_b>.key()` where both accounts are declared mutable in the same instruction's context. The baseline emits none such.

### 2.7 - Landscape Class 7 (bump-seed canonicalization / non-canonical bump)

Bucket: **(a) subsumed** by the baseline's "pubkey bindings" class, which reads the Anchor `bump` clause on PDA declarations. Coverage rule: any certified P032 property whose predicate asserts `<account>.key() == find_program_address(<seeds>, <program_id>)` where `<seeds>` includes the canonical bump byte from the Anchor `bump` clause counts as covering Class 7. Note that the 23-of-25-trivial finding on Raydium was dominated by bump-seed conservation properties; per Section 3 those are trivial.

### 2.8 - Landscape Class 8 (closing accounts / revival)

Bucket: **(c) not covered**. The baseline emits no property class that asserts an account close operation is followed by lamport transfer or discriminator zeroing. Coverage rule: a P032 property counts as covering Class 8 if and only if its predicate asserts (i) `<account>.lamports == 0` after a named close call site, or (ii) `<account>.discriminator == 0` after a named close call site.

### 2.9 - Landscape Class 9 (CPI target / missing program ID check)

Bucket: **(b) partial**. The baseline's "pubkey bindings" covers equalities between account fields including program-account fields where those appear in the account context. It does not directly emit "the program invoked in the CPI equals the expected program ID" as a property class. Coverage rule: a P032 property counts as covering Class 9 if and only if its predicate is `<cpi_target_program>.key() == <constant_program_id>` at a named CPI call site, and the call site appears in the expanded source. Properties that assert a program field appears in the account context but do not assert the CPI-time equality do not count.

### 2.10 - Landscape Class 10 (oracle price manipulation / economic design)

Bucket: **(c) not covered**. This class is dominated by economic design and off-chain reasoning (S2 §Class 10). The baseline emits no oracle-freshness, deviation-bound, or two-oracle-agreement property class.

### 2.11 - Landscape Class 11 (governance timing / flash-loan governance)

Bucket: **(c) not covered**. Governance-timing invariants (time-lock enforced, vote-snapshot pre-flash-loan) are outside the six baseline classes.

### 2.12 - Landscape Class 12 (off-chain key exposure / operational compromise)

Bucket: **(c) not covered**. Operational-security class; not reachable by static or dynamic property authoring on the on-chain program.

### 2.13 - Summary and the "above baseline" definition

- **(a) subsumed:** Class 2, Class 7. Any certified P032 property in these classes is baseline coverage; it does not count as above-baseline.
- **(b) partial:** Class 1, Class 3, Class 5, Class 9. The Section 2.1 / 2.3 / 2.5 / 2.9 rules decide whether an individual certified property clears the bar. Properties that clear the rule count as above-baseline within that class; properties that do not clear the rule are baseline coverage.
- **(c) not covered:** Class 4, Class 6, Class 8, Class 10, Class 11, Class 12. Any certified P032 property in these classes counts as above-baseline by construction. If a B3 result claims coverage in Class 4, Class 6, or Class 8 the row was authored under a mechanical rule and the coverage is verifiable against that rule; Classes 10, 11, and 12 are outside the mechanical reach of the shape and any claim of coverage there triggers rewrite of this Section rather than crediting the property.

An "above baseline" property, at B3, is any certified P032 property that either (i) falls in a (c) row per §2.13 or (ii) falls in a (b) row and clears the row's coverage rule per §2.1 / §2.3 / §2.5 / §2.9. No other definition applies. The runner has no discretion at B3 to reclassify.

**Rule-precedence order for landscape-class bucket assignment.** The Tier 1 script (§6.1) assigns each certified property to a landscape-class bucket by testing the coverage rules in this fixed order and stopping at the first match: (1) Class 2 (§2.2) and Class 7 (§2.7) as (a) subsumed if the property's predicate matches those rows' coverage shapes; (2) Class 1 (§2.1), Class 3 (§2.3), Class 5 (§2.5), Class 6 (§2.6), Class 9 (§2.9) by predicate-shape match under each row's Coverage rule, yielding `b-with-rule-pass` on match or `b-with-rule-fail` on non-match within a partial-subsume row the emitter tagged; (3) Class 4 (§2.4) and Class 8 (§2.8) as (c) with the Coverage rules published in those rows; (4) any predicate not matched by rows (1) through (3) is marked "unreachable per §2.13" (Classes 10, 11, 12 are outside mechanical reach). The bucket assignment is not performed by the runner; it is emitted mechanically by the Tier 1 script per §6.1.

---

## Section 3 - The definition of "trivial"

The baseline's measured precedent is 23 of 25 emitted suggestions on Raydium CP-Swap being trivial: bump-seed conservation, decimals conservation, fee-rate "conservation" (per `ops/projects/P032_BASELINE_BRIEF.md` and the P031 C1 finding at `ops/archive/decisions/decisions_2026-07.md` D-P031-C1-kill-c2-shape-2026-07-26). This section fixes "trivial" tightly enough that a third party applying the definition to our B1 or B3 emitted output gets the same answer we do. The definition is fixed here in advance, before any B1 output exists.

### 3.1 - The categorical rule

A certified property is **trivial** if and only if the predicate falls in one of the categories in §3.2. A certified property is **non-trivial** if and only if the predicate falls in one of the categories in §3.3. Predicates that appear to fall in neither list route to §3.4 (the residual rule). No property is both.

### 3.2 - Categories that are trivial by definition

**T1 - Constant-scalar conservation across instructions.** A property whose predicate is `<field>_after == <field>_before` where the field is a configuration scalar (bump, decimals, fee_rate, open_time, close_time, protocol_state, config_version) and the instruction is not the instruction whose declared purpose is to mutate that field. Rationale: the property is asserting the absence of a write on a field the instruction was not designed to write; the Anchor account-context and instruction handler shape enforce this at compile time.

Worked examples:
- (T1.a) On Raydium CP-Swap: `pool_state.bump_after == pool_state.bump_before` under the `swap_base_input` instruction. Trivial: the swap instruction has no bump-write path.
- (T1.b) On Raydium CP-Swap: `pool_state.mint_decimals_after == pool_state.mint_decimals_before` under any instruction other than pool initialize. Trivial: decimals are init-only by construction.
- (T1.c) On Meteora Alpha Vault: `escrow.bump_after == escrow.bump_before` under `claim` or `withdraw`. Trivial: same shape as T1.a.

**T2 - Field-equals-declared-constant on init-only fields.** A property whose predicate is `<field> == <constant_from_context_declaration>` for a field declared init-only in the IDL or by Anchor constraint. Rationale: init-only fields are, by declaration, written exactly once and are subsequently equal to themselves.

Worked examples:
- (T2.a) `token_mint.decimals == 9` where 9 is the mint's declared init decimals and the instruction is not `initialize_mint`. Trivial.
- (T2.b) `config.authority == <declared_admin_pubkey>` under a non-admin instruction where `authority` has no rotation instruction in the program. Trivial.
- (T2.c) `pool_state.token_a_mint == <pool_declared_a_mint>` under `swap_base_input`. Trivial: pool AMM invariants declare mints at pool creation.

**T3 - Redundant Anchor-constraint re-statement.** A property whose predicate is a direct re-assertion of an Anchor `has_one`, `constraint`, `seeds`, `bump`, `owner`, or `signer` clause that the Anchor framework's `try_accounts` machinery already enforces at instruction entry. Rationale: the framework rejects the transaction before the handler runs if the constraint fails; a property re-asserting the same predicate post-handler is not measuring anything the framework did not.

Worked examples:
- (T3.a) `pool_state.authority.key() == pool_authority.key()` where the account context declares `#[account(has_one = authority)]` on `pool_state`. Trivial.
- (T3.b) `<pda_account>.key() == find_program_address([b"vault", authority.key().as_ref()], program_id)` where the account context declares `seeds = [b"vault", authority.key().as_ref()], bump`. Trivial.
- (T3.c) `payer.is_signer == true` where the account context declares `payer: Signer<'info>`. Trivial.

### 3.3 - Categories that are non-trivial by definition

**N1 - Cross-account arithmetic bindings.** A property whose predicate ties one account's numeric field to another account's numeric field under an instruction that writes both, where the binding is not restated in an Anchor constraint and would not fail at compile time. Rationale: this is the shape of the Raydium `lp_supply` vs SPL Mint supply property, which was the one non-trivial baseline finding.

Worked examples:
- (N1.a) `pool_state.lp_supply == <spl_mint_account>.supply + <declared_locked_liquidity>` under `deposit` or `withdraw`. Non-trivial: two independently-mutable state records, one of which sits under the SPL token program.
- (N1.b) `vault.total_deposits == sum(escrow.amount for escrow in <all_escrows>)` under `deposit` or `claim`. Non-trivial: aggregate over many accounts.
- (N1.c) `pool_state.fee_growth_global_x64 <= previous_fee_growth_global_x64 + max_fee_per_swap` under `swap`. Non-trivial: fee-accrual bound tying a running counter to a per-transaction cap.

**N2 - Overflow-non-occurrence at named call sites.** A property whose predicate asserts absence of overflow at a specific `checked_add` / `checked_mul` / `checked_sub` / `saturating_*` call site named in the property text. Rationale: this is the Landscape Class 5 (ii) coverage rule from §2.5; the property is measuring a specific arithmetic risk, not a scalar equality.

Worked examples:
- (N2.a) `pool_state.token_a_reserve.checked_add(swap_amount) != None` at the named call site in the swap handler. Non-trivial.
- (N2.b) `escrow.claimed.checked_add(claim_amount) <= escrow.total` at the named call site. Non-trivial.
- (N2.c) `pool_state.k_last <= pool_state.token_a_reserve.checked_mul(pool_state.token_b_reserve)` (constant-product-not-decreased). Non-trivial.

**N3 - CPI-target and account-role predicates outside the Anchor constraint set.** A property whose predicate asserts either a CPI target program ID equality at a named CPI call site (per §2.9) or a distinctness / role predicate that no Anchor `has_one` / `constraint` / `owner` clause covers.

Worked examples:
- (N3.a) `cpi_target_program.key() == spl_token::ID` at the named `transfer_checked` call site in the swap handler. Non-trivial.
- (N3.b) `payer.key() != recipient.key()` under `airdrop`, where no Anchor constraint declares this distinctness. Non-trivial.
- (N3.c) `<owner_account>.owner == <expected_program_id>` where the owning-program equality is not declared by `#[account(owner = ...)]` in the context. Non-trivial.

### 3.4 - The residual rule (last resort, deterministic)

A certified property whose predicate does not fall in §3.2 or §3.3 is classified by the following two-step test, in this order:

- **Step 1 - Trivialization test.** If, after variable substitution from the instruction's account context, the property's predicate exactly matches one of the following Anchor-constraint-to-predicate-shape reduction rows, the property is **trivial**. The reduction is mechanical (pattern match after variable substitution), not judgment. The table:

  | Anchor constraint clause | Trivial predicate shape it implies |
  |---|---|
  | `has_one = X` on `<owning_account>` | `<owning_account>.X.key() == <X>.key()` |
  | `seeds = [<seed_expr>], bump` on `<account>` | `<account>.key() == find_program_address(<seed_expr>, program_id)` |
  | `owner = <program_id>` on `<account>` | `<account>.owner == <program_id>` |
  | `signer` on `<account>` (or `<account>: Signer<'info>`) | `<account>.is_signer == true` |
  | `init` on `<account>` | `<account>` did not exist before this instruction |
  | `constraint = <expr>` on `<account>` | `<expr>` |

  Anything not matching a table row after variable substitution is not trivial by Step 1.
- **Step 2 - Two-account test.** If Step 1 does not classify the property, apply the following test. The property is **non-trivial** if and only if all four of the clauses below hold; otherwise the property is **trivial**.

  - (2a) **Single comparison.** The predicate has exactly one top-level relational operator (`==`, `!=`, `<`, `<=`, `>`, `>=`) and no top-level `&&` or `||` joining two comparisons.
  - (2b) **Both sides reference the context.** Each of the two sides of that comparison references at least one account that appears in the instruction's account context.
  - (2c) **One side references a written account, the other a distinct account.** At least one account referenced on one side of that comparison is declared **writable** in that account context — that is, the declaration carries `mut`, `init`, `init_if_needed`, `realloc`, or `close` — and at least one account referenced on the opposing side is not that same account. An account whose address appears on a side, where that address is a fixed program ID or a sysvar address, does not satisfy this clause for that side. An account that a side references by one of its field values other than its address, where the instruction reads that account, satisfies this clause for the side it appears on, provided the opposing side references an account the instruction writes. Both of the two preceding sentences turn on how a side references an account — by its address, which is the account's `key()` value, or by one of its other field values — and not on whether the instruction reads the account, which under Anchor every declared account is. Where both would apply to the same account on the same side, the exclusion governs.
  - (2d) **Not already restated.** The predicate is not restated by any single Anchor constraint clause in that context.

  Clauses (2a) and (2c) are the narrowing ordered by `D-P032-B0d-panel-lens-overlap-amend-not-concede-2026-07-31` against finding `H2-SHAPE-TRIGGER-IS-EMITTER-AUTHORED` Path C. Without them, Step 2 returned **non-trivial** for a predicate such as `payer.key() != token_program.key()`, which references two accounts in the same context and is restated by no single constraint clause, but which no execution of the instruction can make false because a signer's key can never equal a fixed program ID; and for any single-account trivial property padded with a conjunct naming a second account. Both clauses are mechanical reads of declared text and **Step 2 still does not require judgment** about whether a predicate is meaningful: (2a) counts top-level operators in the predicate text, and (2c) reads the writability marker off the account-context declaration and reads whether a side names an account's address or one of that account's other fields, which is the operative test in both (2c)'s exclusion and (2c)'s grant. (2c) also treats an account declared in the context as read by the instruction, which under Anchor it is, because `try_accounts` deserializes every declared account at instruction entry; because that holds of every declared account, the grant's read condition selects nothing on its own, and the side's reference mode is what selects. Clause (2a) and (2c)'s address exclusion resolve ambiguous cases toward "trivial", the direction that counts against the publisher's own headline measure; (2c)'s field-reference sentence resolves in the other direction, and the paragraph below is why.

  **The exclusion in (2c) was rewritten, and what the first version cost.** As first drafted, (2c) required a writable account on **both** sides and excluded any program account, any sysvar, and any read-only account from satisfying the clause for its side. That version classified as trivial the whole class of cross-account invariants the instruction writes on only one side of: `vault.last_update_slot <= clock.slot` under `harvest`, and generally a mutable field bounded against a sysvar, against a read-only oracle, or against a read-only config account. This text bounded that narrowing by asserting that a genuinely non-trivial cross-account predicate it would otherwise lose is classified by §3.3 before §3.4 is ever reached. **That assertion was false.** It holds for the single example it named, a CPI-target program-ID equality, which §3.3 N3 does reach. It fails for the one-sided-write class: §3.3 N1 is defined "under an instruction that writes both", the same both-sides-written requirement, so N1 cannot reach a one-sided-write predicate by construction; N2 requires a named `checked_*` call site and N3 requires a CPI-target equality or a distinctness / role predicate, and neither reaches it either. The finding is `H14-2C-KILLS-ONE-SIDED-WRITE-INVARIANTS`. The repair above narrows the **exclusion** rather than the rule, because the vacuity in `payer.key() != token_program.key()` comes from comparing an account address to a fixed program ID and not from read-only-ness: the amended clause still classifies that predicate trivial, (2a) still kills conjunctive padding of a single-account trivial property, and `vault.last_update_slot <= clock.slot` is preserved. What the amended clause still loses is stated here rather than bounded away: a predicate comparing two accounts the instruction only reads fails (2c) and is classified trivial, whatever it asserts. That is a limit of §3.4, not a property of those predicates, and no claim is made that §3.2 or §3.3 catches them first — a claim of exactly that form, made for the first version of this clause, is the defect H14 named.

The residual rule exists to close every gap. It is deterministic; it does not require judgment. If a property is genuinely unclassifiable under §3.2, §3.3, and §3.4, the property's emitter is at fault and the property is reported in the published output as "unclassified per B0 §3" rather than silently coerced into either bucket. Unclassifiable properties do not count toward either the trivial or the non-trivial rate.

---

## Section 4 - What gets measured

Every rate reported at B3 has an unambiguous numerator and denominator declared here. The measurement is on the **emitted** set for trivial rate (per S5b Defect 2.3), not on the passing subset. Two other rates are reported alongside.

### 4.1 - The emitted set

The **emitted set** is every property the P032 tool's authoring layer produces as a candidate, before any filter, threshold, deduplication, or ranking. A property that the tool would present to a downstream consumer at any confidence level, or would list in a debug log as considered, is in `E`. No pre-emit filter (schema-validity, syntactic parse, non-null predicate, deduplication, LLM confidence threshold, or ranking) is permitted to shrink `E`. The published `E` includes each property's raw confidence score if the emitter produces one.

Every property in `E` is recorded with (i) its predicate text, (ii) the instruction or instruction set the property attaches to, (iii) the emitter's class assignment (one of the six baseline classes), (iv) a stable property ID for cross-reference, and (v) the raw confidence score if the emitter produces one (null otherwise). Emitted set size is denoted `|E|`. Reported per target.

The emitter's implementation publishes its full candidate log as an artifact under §6.2 alongside `raydium-cpswap.json` and `meteora-alpha-vault.json` so a third party can verify `E` matches the log.

### 4.2 - The certified set

A property is **certified** if it clears all three B2 checks: (i) compiles into the Crucible harness fixture, (ii) is non-vacuous per B2's per-property execution-counter instrumentation (execution count > 0), (iii) fires when a third-party mutation-engine-produced mutant of its class is injected. The set of certified properties for a target is denoted `C ⊆ E`. Certified set size is `|C|`. Reported per target.

### 4.3 - Trivial rate (the load-bearing measure)

- **Numerator:** count of properties in the emitted set `E` whose classification per Section 3 is "trivial".
- **Denominator:** `|E|`.
- **Reported as:** `trivial_rate_emitted = <numerator> / <denominator>` per target, to two decimal places.

The trivial rate is measured on the **emitted** set, not the certified set. S5b Defect 2.3 named this explicitly: a passing subset can be non-trivial while the emitted output is dominated by triviality; a reader of the receipt reads the whole output.

### 4.4 - Certification pass rate

- **Numerator:** `|C|` (certified set size per §4.2).
- **Denominator:** `|E|` (emitted set size per §4.1).
- **Reported as:** `certification_pass_rate = <numerator> / <denominator>` per target, to two decimal places.

### 4.5 - Class distribution

For each target, the count of emitted properties per baseline class (six rows) and the count of certified properties per baseline class (six rows) are reported as two column tables. Per Section 2.13, any certified property is additionally tagged with its landscape-class coverage bucket (a, b-with-rule-pass, b-with-rule-fail, c). "Above baseline" counts sum the b-with-rule-pass and c rows per §2.13.

### 4.6 - Per-property verdicts

Every property in `E` is published with its full record (id, predicate text, instruction attachment, emitter class, Section-3 classification, certification result per each of the three B2 checks, landscape-class coverage bucket, mutation-kill mutant ID that fired the property or the "did not fire" verdict). This is the raw data referenced in Section 6, Tier 2.

### 4.7 - What is NOT measured at B3

Cost per property, time per property, and any per-run resource metric are recorded in the run artifact but are not part of the pre-registered rate set. Adoption metrics (external teams running the harness, forks, external property authors) are outside B3; they belong to B5 and to the grant milestones separately.

---

## Section 5 - Head-to-head design

Radar (Auditware) and Sec3 X-Ray are run on the same two programs on the same day, at pinned SHAs recorded here. The framing is a **coverage map, not a scoreboard**, per `D-P032-headtohead-coverage-map-2026-07-27`. A coverage map compares reach across the twelve landscape classes; it does not declare a winner. This document contains no ranking language.

### 5.1 - Analyzer pins

**Radar (Auditware):**
- Repository: `https://github.com/Auditware/radar`.
- Pinned commit SHA: `2327887cd47a2bcc71b7a6d0f88f60c9db026436` (HEAD of `main` at 2026-07-09T13:15:15Z, verified via `api.github.com/repos/Auditware/radar/branches/main` on 2026-07-28).
- License: GPL-3.0.
- Invocation: per the repository's documented CLI, run against the pinned source of each target with the shipped template set at the pinned SHA. Full invocation flags recorded in the B3 run artifact.

**Sec3 X-Ray:**
- Repository: `https://github.com/sec3-product/x-ray` (org is `sec3-product`, not `sec3-service`; the `sec3-service` org does not contain X-Ray).
- Pinned commit SHA: `94804599e393aee1c71ceb4039787d8f73337001` (HEAD of `main` at 2026-03-27T16:52:44Z, verified via `api.github.com/repos/sec3-product/x-ray/branches/main` per `agents/research_lead/outbox/T-P032-B0-precondition-sec3-xray-alive-2026-07-27_result.md`).
- License: AGPL-3.0. Head-to-head invocation via `docker run` consuming stdout does not create a derivative work under standard AGPL interpretation; flagged for awareness, not a gate.
- Invocation: `docker run --rm --volume "$(pwd)/workspace:/workspace" ghcr.io/sec3-product/x-ray:latest /workspace/<program-dir>` per the repository README, against the pinned source of each target. Full invocation recorded in the B3 run artifact.

### 5.2 - Analyzer liveness re-check at fire time

At B3 fire time the pinned SHAs are re-verified via `curl -sI` HEAD checks against the two repositories and the X-Ray Docker image at `ghcr.io/sec3-product/x-ray:latest`. If either analyzer's pinned SHA becomes unreachable (repository archived, image pulled) between publication and B3 fire, the failing check output is attached to the published B3 result and the head-to-head lane runs on the remaining analyzers. The B0 pin does not change; the failure is disclosed.

**Analyzer applicability by target-source availability.** For any target program whose on-chain program source is not published (per §1), source-based analyzers are recorded as "not applicable to this target"; their finding count on that target is not counted toward §7.1's "already flagged" union, and `C_baseline` for that target is computed using only the applicable analyzers. Per-target analyzer-applicability publishes in the B3 result alongside the coverage map. Specifically, Meteora Alpha Vault has no published on-chain program source per §1.2: Radar (a source-based static analyzer) is recorded as "not applicable to Meteora Alpha Vault"; the Meteora coverage map records only X-Ray findings and the classes counted as flagged by construction per §7.1. Raydium CP-Swap has published source per §1.1; both Radar and X-Ray are applicable on that target.

### 5.3 - Coverage-map construction

For each of the twelve landscape classes (per Section 2), the B3 result records:
- Which analyzers report findings mapped to that class on Raydium CP-Swap.
- Which analyzers report findings mapped to that class on Meteora Alpha Vault.
- Where the analyzers overlap (same class flagged on the same target).
- Where they do not (class flagged by one and not the others).

The mapping of Radar and X-Ray findings onto the twelve landscape classes is fixed by the lookup tables in §5.3.1 (Radar templates at commit `2327887cd47a2bcc71b7a6d0f88f60c9db026436`) and §5.3.2 (X-Ray Solana rules at commit `94804599e393aee1c71ceb4039787d8f73337001`) below. A finding whose analyzer-category name is not in the table is recorded as "unmapped, does not count toward §7.1's already-flagged union". The runner does not invent a mapping at B3. The full mapping table is published alongside the coverage map in §6.2.

### 5.3.1 - Radar template to landscape class

Radar's template set at commit `2327887cd47a2bcc71b7a6d0f88f60c9db026436` is the 112 YAML files under `api/builtin_templates/` in the pinned repository. Each Radar finding carries a `template` field whose value is one of those file basenames (without extension). The mapping below is the fixed lookup:

| Radar template (basename) | Landscape class |
|---|---|
| `account_data_matching` | 4 |
| `account_reinitialization` | 8 |
| `anchor_admin_without_timelock` | 11 |
| `anchor_reward_overflow` | 5 |
| `anchor_spot_price_oracle` | 10 |
| `arbitrary_cpi` | 9 |
| `closing_accounts` | 8 |
| `cpi_authority_bypass` | 9 |
| `duplicate_mutable_accounts` | 6 |
| `missing_bump_seed_canonicalization` | 7 |
| `missing_has_one_constraint` | 1 |
| `missing_owner_check` | 1 |
| `missing_pyth_confidence_interval` | 10 |
| `missing_signer_check` | 2 |
| `missing_token_authority_constraint` | 1 |
| `missing_token_mint_constraint` | 4 |
| `pda_sharing` | 3 |
| `spl_token_mint_consistency` | 4 |
| `spot_price_used_as_oracle` | 10 |
| `stale_chainlink_price` | 10 |
| `type_cosplay` | 4 |
| `unchecked_arithmetics` | 5 |
| `unchecked_close_target` | 8 |
| `unchecked_cpi_program_invoke` | 9 |
| `unchecked_token_account_owner` | 1 |
| `unvalidated_cpi_context_program` | 9 |
| `unvalidated_price_data_account` | 10 |

Any other Radar template shipped at `2327887cd47a2bcc71b7a6d0f88f60c9db026436` (including the EVM/Solidity-oriented templates such as `erc20_permit_deadline_not_checked`, `msg_value_reuse`, `mstore_without_free_memory_pointer_update`, and any not enumerated above) is recorded as "unmapped, does not count toward §7.1". This applies whether the template ships in the pinned repo or is added post-pin: only templates in the table above map to a landscape class for §7.1 accounting.

### 5.3.2 - X-Ray Solana rule to landscape class

X-Ray's Solana rule set at commit `94804599e393aee1c71ceb4039787d8f73337001` is the concrete rule set under `code-analyzer/src/SolanaAnalyzer/Rules/` in the pinned repository. Each X-Ray finding carries a rule identifier corresponding to one of the rule source files below. The mapping is the fixed lookup:

| X-Ray Solana rule (source file basename) | Landscape class |
|---|---|
| `ArbitraryCPI` | 9 |
| `CheckedDiv` | 5 |
| `CosplayAccountDetector` | 4 |
| `InsecurePDA` | 3 |
| `OverflowAdd` | 5 |
| `OverflowDiv` | 5 |
| `OverflowMul` | 5 |
| `OverflowSub` | 5 |
| `UntrustfulAccountDetector` | 1 |

The remaining rule sources at the pinned SHA (`Break`, `MaliciousSimulation`, plus infrastructure files `Rule` and `Ruleset`) are recorded as "unmapped, does not count toward §7.1": `Break` is a control-flow rule not aligned to a single landscape class; `MaliciousSimulation` targets test-harness misuse rather than a production-vulnerability class; the infrastructure files register no detector directly.

### 5.4 - No ranking language

The B3 published writeup describes reach and overlap. It does not use "wins", "beats", "outperforms", "first", "best", "leading", "top", or any comparative superlative applied to a tool. A finding that appears in the P032 output and not in Radar or X-Ray is described as "in the P032 output and not in the compared analyzers", not as "P032 catches what Radar misses". A finding that appears in Radar and not in P032 is described symmetrically. The coverage map compares reach; the reader draws the inference.

### 5.5 - Same day, same inputs

Both analyzers and the P032 tool run against the same pinned source (or pinned IDL, for Meteora Alpha Vault) on the same calendar day. Run artifacts are timestamped and published under the raw-data path in Section 6.2. Each of the P032 tool, Radar, and X-Ray runs exactly once per target on B3 fire day. The single run's output is the published output. If any run fails to complete (process crash, non-zero exit, incomplete artifact) the failure is disclosed in the published result and the analyzer's output on that target is recorded as "failed; no data". No re-run is permitted within B3. If the runner needs a second attempt, B3 fire is rescheduled to a later published date and the prior date is recorded as a superseded attempt in the B3 result.

---

## Section 6 - The adjudication rule

Four tiers, in this order. Names and order are fixed. Tier 3 (a pre-committed panel of three standalone LLM scorer configurations, per §6.3) is the load-bearing subjective-adjudication tier. Tier 4 (optional external human corroboration) publishes alongside Tier 3 when a human accepts and is skipped without apology when none does.

### 6.1 - Tier 1 - Mechanical first

Everything that can be scored by a script is scored by a script and only by a script. No judgment. Yes-or-no per row.

The Tier 1 script is named `scripts/b3/tier1_mechanical.py`. It reads the B1 emitted set and the B2 certification records and returns exit code 0 on a well-formed input, exit code 1 on a malformed input, exit code 2 on a mechanical failure. It emits one JSON record per property with the following mechanical fields: `compiles` (per B2 check i), `non_vacuous` (per B2 check ii, execution count > 0), `mutant_kills` (per B2 check iii), `radar_flags_same_predicate` (true if Radar's B3 run reports a finding mapped to the same landscape class on the same target, per §5.3), `xray_flags_same_predicate` (true if X-Ray does), `section_3_classification` (one of trivial / non-trivial / unclassified per §3), and `landscape_class_bucket` (one of `a`, `b-with-rule-pass`, `b-with-rule-fail`, `c`, or `unreachable-per-2.13`, computed mechanically from `section_3_classification` and the property's predicate text by applying the §2.1 / §2.3 / §2.5 / §2.6 / §2.9 / §2.4 / §2.8 coverage rules in the fixed rule-precedence order published in §2.13). All seven fields are mechanical.

The Tier 1 script also computes the four rates (§4.3 trivial_rate_emitted, §4.4 certification_pass_rate, §4.5 emitted and certified class distributions, and derived above-baseline counts per §2.13). Script exit convention: exit code 0 means the rates computed and the JSON output was well-formed; a non-zero exit code means the mechanical computation could not complete and the published B3 result includes the exit code and the failing input.

### 6.2 - Tier 2 - Raw data published

Every emitted property, every certification verdict, the full head-to-head output from Radar and X-Ray, and the Tier 1 script's output JSON are published in the open. Any third party who disagrees with the classification can re-run Section 3 on the emitted set and get their own numbers.

Tier 2 is what makes the Tier 3 agent panel (§6.3) auditable. The panel's inputs (blind sample rows, prompts, prompt hashes) and outputs (per-row verdicts, per-adjudicator rationales, panel-disagreement rows) publish under `public/p032-b3-results/panel/` per the format list below. Any reader who discounts the panel's verdicts can re-adjudicate the full published sample independently against Section 3 or against the reader's own rubric and produce a competing verdict. The panel is not the closed box that Tier 3 (residual subjective adjudication) would otherwise be; every input it saw and every output it produced is on disk.

**Repository path:** `public/p032-b3-results/` in the P032 public release repository (repository name and URL declared in the B0d publication ticket; the repository is created before B3 fires so the path exists at publication time).

**Format:**
- Per-target JSON: `raydium-cpswap.json`, `meteora-alpha-vault.json`. Schema: an array of property records, each carrying the fields declared in §4.6.
- Per-target human-readable table: `raydium-cpswap.md`, `meteora-alpha-vault.md`. One row per property with the same fields; rendered from the JSON.
- Analyzer output archive: `radar-raydium-cpswap.log`, `radar-meteora-alpha-vault.log`, `xray-raydium-cpswap.log`, `xray-meteora-alpha-vault.log`. Raw stdout / stderr from each analyzer run, unedited.
- Coverage map: `coverage-map.md` per §5.3. Rendered from the JSON plus the analyzer logs.
- Tier 1 output: `tier1.json` per §6.1.
- Raw candidate log (per §4.1): `raydium-cpswap-candidates.log`, `meteora-alpha-vault-candidates.log`. The emitter's full pre-filter authoring output for each target, one candidate per line, so a third party can verify the published `E` matches every candidate the tool would have surfaced.
- Panel run artifacts (per §6.3): `panel/blind-sample.json` (the deterministic sample rows presented to each scorer, blinded per §6.3), `panel/prompts/<A1|A2|A3>.txt` (the exact prompt sent to each scorer at B3 fire time, one file per scorer configuration), `panel/verdicts/<A1|A2|A3>.json` (per-row verdicts and one-sentence rationales, one file per scorer configuration), `panel/checker.json` (the C4 checker script's per-scorer record per §6.3), `panel/aggregate.json` (the aggregated fields per §6.3). Every panel run publishes, including any run invalidated by the C4 checker and any re-run. The scorer script that produces each `panel/verdicts/<A1|A2|A3>.json` file from the blind sample and the committed per-scorer prompt is `scripts/b3/tier3_panel_scorer.py`; its source publishes to `panel/tier3_panel_scorer.py` alongside the run artifacts.
- Tier 3 checker script and inputs (per §6.3 C4): `panel/tier3_checker.py` (the C4 checker script's source, published verbatim so a third party can re-run byte-for-byte), `panel/checker-inputs/` (each scorer's actual prompt bytes, the deterministic sample bytes, and the blinded field values from the source data, one file per input so the script can be re-executed against the published inputs and reproduce `panel/checker.json`).
- Tier 3 checker test log (per §6.3 C4): `panel/checker-tests.log` (the CI output of `scripts/b3/tier3_checker_tests.py`, published so a third party can verify the checker script fails on planted-failure inputs).

### 6.3 - Tier 3 - Pre-committed cross-lab scorer panel (load-bearing)

Three pre-committed standalone LLM scorer configurations, distinct declared lenses, score a blind sample for whether each property in the sample is trivial or non-trivial. Tier 3 is the load-bearing subjective-adjudication tier: the panel's non-trivial counts publish as the primary subjective verdicts alongside the mechanical Section 3 rubric from Tier 1. The panel is defensible because Tier 2 publishes every input the panel saw and every output it produced; a reader who discounts the panel can re-adjudicate the same blind sample independently and produce a competing verdict.

**Panel shape (scorer, not seat).** Under `D-P032-panel-composition-2026-07-28` (CEO, option C, decided 2026-07-28) the panel is cross-lab. It is not three CaliperForge seats and is not driven by the CaliperForge agent harness. Each adjudicator is a **standalone LLM scorer configuration**: one prompt in (the committed system prompt plus the committed user-prompt template with the blind sample substituted per §6.3), the blind sample, JSON out. **No tools, no filesystem access, no `run_role.py` invocation, no agent harness, no sub-agents**, and no `agents/_roster.json` seat entry. The scorer script that dispatches the three scorer configurations, sends the committed prompts, and collects their JSON outputs is `scripts/b3/tier3_panel_scorer.py`; its source publishes verbatim to `public/p032-b3-results/panel/tier3_panel_scorer.py` at B3 fire time per §6.2. Where prior §6.3 text spoke of an "adjudicator seat", the amended text speaks of a "scorer configuration": the scorer has no seat identity to track and no cross-ticket routing history to inspect, so C1 (below) is re-expressed in terms of the model plus the committed prompt lineage instead of seat identity.

**Panel composition (pinned).** Three scorer configurations, each running a distinct declared lens, plus the B1/B2 emitter model. Composition is fixed in this text per the CEO ruling `D-P032-panel-composition-2026-07-28` and is not chosen at run time:

- **Adjudicator A1: GPT-5.6 Sol (OpenAI). Falsification-witness lens.** **A1's lens is defined over the predicate and the instruction it attaches to, and not over §3's category set.** A1's committed system prompt carries no §3.2 category, no §3.3 category, no §3 worked example, and no §3.4 Step 1 reduction table, and A1 is the only panel seat whose prompt carries none of that material. The lens question is whether a **falsifying execution** exists for the row: a single concrete end state of the instruction named in the row's attachment, in which the predicate evaluates to false, reached by a program of the kind the row describes without the transaction being rejected before the handler body runs. A1's default verdict for any row is "trivial", and the burden is on the row: A1 votes "non-trivial" for a row **if and only if** it can state such an execution in one sentence, subject to all four of the following. (i) The sentence names an account or field the predicate itself mentions, asserts that the instruction writes it, and gives the resulting value that makes the predicate false. (ii) The write it names is part of the work the named instruction actually does, or a plausible error in that work; that a handler holds an account writable, and so could in principle write any field inside it, is not on its own a falsifying execution, and a predicate neither of whose sides is touched by anything the instruction does has none. (iii) The execution does not require an account the predicate names to be absent, closed, wrongly typed, wrongly owned, or unsigned where the context declares it signed, because Anchor's `try_accounts` machinery rejects those at instruction entry and the handler body never runs. (iv) The execution is not ruled out by a declaration the predicate restates that the instruction cannot invalidate: an Anchor `has_one`, `constraint`, `seeds`, `bump`, `owner`, or `signer` clause is checked at instruction entry, so a predicate restating such a clause whose operands the handler does not write has no falsifying execution, while a predicate restating a clause an operand of which the handler does write may still have one, because the entry-time check says nothing about the end state. Limb (ii) is what keeps the lens from collapsing into a standing vote of "non-trivial" on every predicate over a writable account, and limb (iv) is what keeps it from collapsing into agreement with §3.4 Step 1 on every predicate that restates a constraint clause. **A row for which no falsifying execution can be stated returns "trivial", which is a verdict and not an abstention.** Rationale for the seat, per the CEO ruling: A1 currently tops the Artificial Analysis coding agent index at 80.0 as of 2026-07-28 (figure quoted from `D-P032-panel-composition-2026-07-28`); picking the hardest available judge closes the most obvious way to game the benchmark. **Why this lens replaced the prior "refutation lens" definition, and what the replacement costs.** The prior definition reduced the predicate to a §3.2 category or a §3.4 Step 1 row, which defined A1 over the same category set as A2 and made the two seats one rubric transcribed twice; the finding is `H7-A1-AND-A2-ARE-ONE-LENS` and the amendment is ordered by `D-P032-B0d-panel-lens-overlap-amend-not-concede-2026-07-31`. The cost is real and is accepted rather than argued away: A1 is no longer a mechanical lens, its verdicts are not reproducible by pattern match, and A1 no longer corroborates §3 on any row. The panel already carries one mechanical §3 lens in A2, and a second copy of it was the defect.
- **Adjudicator A2: DeepSeek-V4-Pro (open weights, Hugging Face repository `deepseek-ai/DeepSeek-V4-Pro`, served by the DeepSeek first-party API at `https://api.deepseek.com/v1/chat/completions` under the API model identifier `deepseek-v4-pro`; that API accepts no dated identifier, so the served build is pinned by the returned `system_fingerprint` envelope field rather than by anything the request can demand, per `ops/projects/P032/B0/A2_deepseek_probe_2026-07-31.md`; we do NOT self-host). Predicate-shape lens.** Maps the predicate to a §3 category by predicate shape only. If the predicate matches an N1, N2, or N3 shape from §3.3 the verdict is "non-trivial"; if it matches a T1, T2, or T3 shape from §3.2 or the Step 1 reduction table from §3.4 the verdict is "trivial"; otherwise the Step 2 two-account test from §3.4 decides. Rationale for the seat, per the CEO ruling: the open weights on Hugging Face make the judge permanently reconstructible; if every hosted provider drops the model, the judge is still reproducible from the published weights.
- **Adjudicator A3: Claude Opus 5 (Anthropic). Plain-reader lens.** The lens question is whether a third-party auditor reading only the predicate text and the instruction attachment (no P032 branding, no rubric access) would call the row a meaningful bug-catch. If yes, "non-trivial"; if no, "trivial". Rationale for the seat, per the CEO ruling: A3 is the deliberately retained same-lineage lens for panel-to-emitter agreement measurement; A3 cannot carry a vote alone because C1 requires two of three on a base model distinct from the emitter's.
- **Emitter (context, not a panel seat): Claude Opus 5 (Anthropic).** B1 and B2 run on Claude Opus 5 per the same CEO ruling. A1 and A2 are on base models distinct from the emitter's; A3 shares the emitter's base model. The two-of-three distinct-base-model rule of C1 is satisfied by A1 and A2.

Each scorer configuration returns a per-row verdict of "trivial" or "non-trivial" plus a one-sentence rationale.

**Emitter-panel isolation.** The B1 emitter's model configuration (base model, provider, API model identifier, pinned model revision, system prompt, user-prompt template, tool availability, and model params, hashed per the C2 scheme below) is committed in the B0d publication ticket alongside the per-scorer commitments and before the Bitcoin beacon block is observed. The B1 emitter may not be modified after B0d publish. No invocation of any of the three committed scorer configurations (the committed system prompt + user-prompt template pair against the committed model at the committed revision, run against any subset of the deterministic blind sample) is permitted between B0d publish and B3 fire; the emitter is developed in advance of B0d publish and any post-B0d change to the emitter constitutes a new B0-revision. The C4 checker output records the B1 emitter's model-configuration hash and the checker verifies the B1 run's actual emitter configuration matches the committed hash.

**Blind sample selection.** The sample is drawn deterministically from the union of emitted sets across both targets by the following procedure:
- Concatenate the two per-target JSON files from §6.2 into a single array in a fixed order (Raydium first, then Meteora), preserving each property's stable property ID.
- Compute `sha256(bitcoin_block_hash || "|" || sha256(canonicalized_predicate_json))` for each property. `bitcoin_block_hash` is the hexadecimal-lowercase block hash of the first Bitcoin main-chain block mined at or after the timestamp of B0d publication; the block height and block hash are recorded in the B0d publication ticket at B0d fire time (this fixes a public random beacon the runner cannot pre-image). `canonicalized_predicate_json` is a JSON object with fields `{predicate_text, instruction_attachment, target_program_name}` canonicalized per JCS (JSON Canonicalization Scheme, RFC 8785, `https://datatracker.ietf.org/doc/html/rfc8785`) and encoded UTF-8. The literal pipe character is the delimiter between the two hex strings. Runner-authored `property_id` is not part of the preimage. The SHA-256 implementation is per FIPS 180-4.
- Sort the array by ascending hexadecimal-lowercase SHA-256 digest.
- Take the first `N` entries, where `N = min(20, |E_total|)` and `|E_total|` is the summed emitted-set size across both targets. If `|E_total| < 20` the entire emitted set is the sample.

The runner does not choose the sample. The sample is the deterministic output of the procedure above applied to the published emitted sets. The sample is fixed once the emitted sets are published to §6.2 and cannot be re-drawn.

**Blinding.** The sample is presented to each scorer configuration with the following fields visible: property ID, predicate text, instruction attachment, target program name. The following fields are hidden: emitter class, Section 3 classification, certification results, coverage-map bucket, mutant-kill mutant ID, any P032 or CaliperForge branding. Each scorer configuration is invoked independently and receives no visibility into the other scorer configurations' verdicts, rationales, or run timing until all three have submitted their per-row verdicts to the panel run artifact directory per §6.2.

**What the blinding check does and does not cover.** Check (iii) under C4 is a per-row leak check over the user-role bytes only. This section authorises §3 rubric content to sit in a scorer's system role, which A2's system prompt does; A1's carries no §3 category, worked example or reduction table, and A3's carries no §3-derived material at all. The system-role blinding guarantee is a manual-review commitment and not a mechanically checked property.

**Collapsing the `N` runs per item per seat to one verdict.** C2(f) commits `N = 3` scorer runs per item per panel seat and C3 publishes every one of them. The aggregate fields below are defined over exactly one verdict per scorer configuration per row, so the collapse from `N` runs to one verdict is fixed here in advance rather than chosen by the runner after the runs have been seen. For a given row and a given scorer configuration, that seat's verdict for that row is **the verdict returned by more than `N/2` of that seat's `N` runs on that row**. A run whose output does not parse per the committed output format, or whose `verdict` field is not exactly one of the two literal values `"trivial"` or `"non-trivial"`, contributes no verdict to the collapse. **The denominator is the committed `N` from C2(f) in every case, and never the number of runs that contributed a verdict.** A run that contributes no verdict counts against the threshold rather than shrinking it: at the committed `N = 3`, a verdict is the collapsed verdict only if two or more of the three runs returned it, so one contributing run out of three is not a collapse and two unparseable runs out of three cannot be overridden by the third. If no verdict is returned by more than `N/2` of that seat's `N` runs — because of a tie, or because too few runs parsed — that seat's verdict for that row is `"trivial"`; the tie direction is fixed toward "trivial" because that is the direction that counts against the publisher's own headline measure. The one-sentence rationale published for that seat and that row in `panel_disagreement_rows` is the rationale from the earliest of that seat's runs whose verdict equals the collapsed verdict, ordered by the RFC-3161 token `genTime` recorded for that run under C2(g), ties broken by ascending hexadecimal-lowercase SHA-256 of the JCS-canonicalized response envelope for that run. If no run of that seat on that row returned the collapsed verdict, the published rationale is the empty string and that seat's collapse for that row is recorded in `panel_disagreement_rows` as `default-no-contributing-run`. The collapse is a pure function of the run artifacts published under C3, so a third party recomputes every aggregate field below from the published runs with no runner input. Changing the collapse rule after B0d requires re-publishing the protocol as a new B0-revision.

**What the panel verdict means.** The three sets of per-row verdicts, each collapsed from `N` runs per the rule above, are aggregated into the following fields, all published verbatim under `public/p032-b3-results/panel/aggregate.json` per §6.2:

- `panel_nontrivial_count_per_adjudicator`: three integers keyed by adjudicator (A1, A2, A3), each the count of rows that scorer voted "non-trivial" on the blind sample.
- `panel_nontrivial_count_majority`: the count of rows for which at least two of the three scorer configurations voted "non-trivial".
- `panel_nontrivial_count_unanimous`: the count of rows for which all three scorer configurations voted "non-trivial".
- `section3_nontrivial_count_on_sample`: the mechanical Section 3 non-trivial count on the same blind sample, computed by the Tier 1 script (§6.1).
- `panel_disagreement_rows`: the list of property IDs on which the three scorer configurations did not vote unanimously, with each scorer's verdict and one-sentence rationale attached per row. A row also appears in this list, whether or not the three scorers agreed on it, if any seat's collapsed verdict for that row was returned by none of that seat's `N` runs; that seat's rationale for that row is the empty string and its entry carries the marker `default-no-contributing-run` per the collapse rule above.

Discrepancies between the panel and Section 3 are published, not resolved.

**What `panel_nontrivial_count_majority` means, stated precisely because the lens amendment above changed it.** Under the amended lens definitions, exactly one of the three scorer configurations — A2 — carries the Section 3 rubric in its committed prompt. A1's falsification-witness lens and A3's plain-reader lens carry none of it. A panel majority is therefore either two votes Section 3 did not author, or one such vote plus A2's, and a majority can go against Section 3 on a row Section 3 categorizes. **Before the amendment this was not true and the diagnostic below would have been worthless:** A1 and A2 both carried Section 3 verbatim, so the majority was Section 3 sampled twice on every categorizable row and the gap below was near-zero by construction, reporting "well tuned" no matter how badly Section 3 was tuned. That finding is `H8-SECTION-3-GRADES-ITSELF` and the repair is the lens amendment above.

**The two non-Section-3 votes are not two independent readings on every row.** A1's falsification-witness lens and A3's plain-reader lens both turn on whether the predicate can be violated. A3's first limb asks whether a correct program of the kind described could plausibly get the property wrong, and states that a property the program's structure makes impossible to violate is not a meaningful bug-catch, which is A1's own admissibility bar in plain English; A3's test is conjunctive, so that limb failing is on its own sufficient for A3 to return "trivial". A1 returning "trivial" therefore implies A3 returns "trivial". The trivial side is the modal side — 23 of 25 rows in the baseline precedent — so on most rows A1 and A3 agree by construction, and a majority the two of them carry between them is one question plus a plain-reader significance filter rather than two independent readings. The two lenses do separate on the non-trivial side, where A3's significance limb, A1's opposite default, and A1's entry-check exclusion (which A3 cannot apply, because A3's prompt carries no Anchor vocabulary) can pull them apart. The finding is `H12-OVERLAP-MOVED-TO-A1-A3-NOT-CLOSED` and it is stated here because a reader diffing the two committed prompts will find it, and `panel_nontrivial_count_majority` publishes without it being restated at the field.

**Where the Section 3 under-tuning diagnostic reads, and why it moved.** A large gap between `panel_nontrivial_count_unanimous` and `section3_nontrivial_count_on_sample` indicates that Section 3 is under-tuned, and the row is flagged for a Section 3 rewrite in a subsequent B0 revision (not applied retroactively to the B3 result). The diagnostic reads on unanimity rather than on `panel_nontrivial_count_majority` because unanimity requires A2 and therefore requires all three of the panel's distinct questions to have been asked on the row, while a majority can be carried by A1 and A3 alone, which the preceding paragraph shows is one question answered twice on the modal row. This choice is available only because of the lens amendment above: before it, unanimity contained two distinct questions rather than three, and reading the diagnostic there would have cost more than it does now. The cost it does carry is stated rather than argued away: unanimity is a subset of the majority, so the gap it reports is never larger and the diagnostic is less sensitive than it would be on the majority. That is accepted, because a less sensitive signal carried by three distinct questions is worth more than a more sensitive one that can be carried by a near-duplicate pair. `panel_nontrivial_count_majority` remains published and is the broader signal; it is not the diagnostic field.

Panel disagreement is a published finding, not something resolved offstage; the `panel_disagreement_rows` list is the primary artifact for a reader who wants to inspect the residual subjective disagreement inside the panel.

**Four conditions on the panel.** These are the whole defensibility of the design and are stated as rules with mechanical consequences.

- **C1 - No shared lineage with the emitter (model + prompt-lineage form).** Because the panel is cross-lab standalone scorers rather than agent-org seats, "no shared lineage" is expressed as a rule over the model configuration and the prompt lineage rather than over seat identity: no scorer configuration may share base model weights or committed prompt bytes with the B1 emitter or the B2 certifier. The B1 emitter's base model and the B2 certifier's base model are pinned at B0d per §6.3 Emitter-panel isolation alongside the per-scorer C2 commitments. At least two of the three scorer configurations must run on a base model distinct from the emitter's base model (the third may match, to preserve a same-base-model lens for panel-emitter agreement measurement); under the pinned panel composition A1 (GPT-5.6 Sol, OpenAI) and A2 (DeepSeek-V4-Pro, open weights) satisfy this requirement while A3 (Claude Opus 5) matches the emitter's base model deliberately. Prior-visibility closure applies to the scorer configuration rather than to a seat: no committed scorer configuration (a specific base model + system prompt + user-prompt template + parameter manifest, hashed per C2) may have been invoked against any B1 output (authoring, review, adversarial scan, or precondition scan on B1 output) or any B2 output before B3 fires. This closure covers every B1 ticket class listed above and any B2 ticket. Invoking a committed scorer configuration against any B1 or B2 output at any time between B0d publish and B3 fire invalidates that scorer's panel role and requires a new B0-revision; any inadvertent invocation surfaced after the fact invalidates the affected scorer's verdicts under C3 and requires re-adjudication by a replacement scorer configuration declared in a new B0-revision. The C4 checker output records the provider, API model identifier, and pinned revision for each scorer run so this condition is verifiable at publication.
- **C2 - Per-scorer commitment hash-committed at B0d publish.** A per-scorer commitment is recorded in the B0d publication ticket for each of A1, A2, A3, before any B1 output exists. Because each adjudicator is a standalone scorer rather than a seat driven through `run_role.py`, three of the five previously-required sub-commitments simplify by construction and are re-stated below in their simplified form rather than deleted. The five commitments are:
  (a) **System-prompt SHA-256** of the exact bytes sent as the system role to the scorer, UTF-8 without BOM, LF line endings, Unicode NFC-normalized, no interpolation permitted.
  (b) **User-prompt template SHA-256** with a single named placeholder `{BLIND_SAMPLE_ROWS}` whose substitution rule is: the row records selected per §6.3 blind-sample selection, serialized as a JSON array in the deterministic order from the beacon-sorted digest, each record containing only the visible fields listed in Blinding, serialized per JCS RFC 8785; the checker recomputes the template hash after redacting the sample-placeholder region and compares byte-for-byte.
  (c) **Tool-availability manifest SHA-256**. Empty by construction under this shape: a standalone scorer has no tools, no filesystem access, no MCP servers, no shell. The committed manifest is the literal string `[]` and the committed hash is the SHA-256 of that literal string. This clause is retained (not deleted) so a third party can verify the empty-manifest commitment was made and honored.
  (d) **Provider + API model identifier + pinned revision + harness system-prompt version.** For each of A1, A2, A3 the commitment names: the provider (e.g., OpenAI direct API, or the DeepSeek first-party API for A2, or Anthropic direct API for A3); the API model identifier as sent in the request payload (e.g., `gpt-5.6-sol`, `deepseek-v4-pro`, `claude-opus-5`); the pinned model revision or version string as returned in the provider's response metadata; and the harness system-prompt version string. Under this shape the "harness system-prompt version" collapses to the literal system-prompt bytes sent per (a) (there is no separate harness system prompt wrapping the scorer) and the commitment records the string `literal-system-prompt-per-(a)` for that field so a third party can verify no wrapper was interposed. **For A2 additionally, the Hugging Face repository id `deepseek-ai/DeepSeek-V4-Pro` and the pinned Hugging Face revision SHA are committed, so the judge remains reconstructible if every hosted provider drops the model between B0d publish and B3 fire (this is the whole reason A2 is on the panel per `D-P032-panel-composition-2026-07-28`, and the commitment covers the model rather than only the prompt).** **Dateless pinned-snapshot identifiers for A1 and A3.** The API model identifiers `claude-opus-5` (A3) and `gpt-5.6-sol` (A1) carry no dated suffix by publisher design. Anthropic's published model documentation states that starting with the 4.6 generation, model IDs use a "dateless format that is itself a pinned snapshot, not an evergreen pointer" (Anthropic, "Models overview", `https://docs.anthropic.com/en/docs/about-claude/models/overview`, retrieved 2026-07-29). OpenAI publishes the GPT-5.6 family (`gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`) on the same convention, with no dated snapshots for the generation (OpenAI, "Models", `https://platform.openai.com/docs/models`, retrieved 2026-07-29). Consequence for this commitment: for a provider whose published identifier is a dateless pinned snapshot, field 3 (API model identifier as sent) and field 4 (pinned model revision as returned in the provider's response metadata) legitimately carry the same string, and the C2(d) requirement is satisfied because the returned identifier is a snapshot commitment rather than a moving alias. A2 is not on this footing: A2's pinning is anchored to a Hugging Face repository id and revision SHA per the preceding sentence, and field 4 for A2 is the `system_fingerprint` string returned at the top level of the DeepSeek response envelope, which is the field that provider populates with a build commitment. A2's returned `model` field is a bare echo of the identifier sent and is not a pinned revision, so it does not serve as field 4; the DeepSeek API accepts only undated model names, which means field 4 for A2 records the build the provider served and does not let the run demand a particular build in advance. Alongside (a) through (e), each scorer run additionally publishes and hash-commits two per-run artifacts so that the pinned identity of the run is anchored to the provider's own return values rather than only to the publisher's promise about the identifier: the **provider response identifier** returned in the response envelope (Anthropic `msg_...` recorded as `api_response_id` for A3; OpenAI `id` for A1; the top-level `id` returned by the DeepSeek first-party API for A2), recorded as a named field per scorer under `panel/checker-inputs/`; and the **full provider response-metadata blob** (the response envelope minus message content: top-level `id`, `model` as returned, `type`, `stop_reason`, `usage`, plus any `system_fingerprint` or provider-side identifiers the provider includes), published byte-for-byte, JCS-canonicalized per RFC 8785, with the SHA-256 hash of the canonicalized bytes recorded in the C2 commitment record for that scorer run and the blob itself published under `panel/checker-inputs/`. These two per-run artifacts (the provider response identifier and the response-metadata blob) are publisher accountability commitments verifiable only by parties with subpoena or provider-cooperation access to the provider's own logs: specific claims about what the provider returned that a third party with such access could refute, not artifacts the C4 checker validates against a provider-side ground truth. The C4 check on these commitments is a self-consistency check (the published blob hashes to the published hash string) and does not consume any provider-side attestation of the envelope contents.
  (e) **Parameter manifest SHA-256**. A flat per-provider payload, canonicalized as JSON per JCS RFC 8785, listing every model parameter passed to the provider's API for the scorer run (temperature, max_tokens, top_p, seed if the provider supports it, and any other parameters accepted by that provider's chat/completion endpoint). Under this shape there is no CaliperForge agent-harness parameter layer wrapping the API params, so the manifest is exactly the provider payload as sent; the committed hash is the SHA-256 of the canonicalized JSON of that payload.
  (f) **Committed scorer-run count `N`.** The number `N` of scorer runs per item per panel seat is committed at C2 pre-registration and published in `panel/checker.json` before B0d publishes. `N = 3`. `N` is fixed and identical across items and across scorer configurations. Any change to `N` after B0d requires re-publishing the protocol as a new B0-revision. The committed `N` is what check (vi) (below) verifies against; a concealed extra run or an omitted run is detectable as an arithmetic gap under check (vi).
  (g) **RFC-3161 notarization at response receipt (REQUIREMENT).** For each of the `N` scorer runs per item per seat, the panel-run harness MUST submit the SHA-256 message imprint of the JCS-canonicalized (RFC 8785) response envelope to the pinned RFC-3161 timestamping authority at response receipt, before any aggregation, scoring, or human/agent inspection of response content by any party. This ordering — notarization precedes any inspection of response content by any party, whether human, agent, or a subprocess of the harness itself — is a REQUIREMENT of the protocol, not a description of habit; a scorer run whose notarization step does not precede content inspection is invalid and does not count toward the committed `N`. The pinned **primary TSA** is endpoint `http://timestamp.digicert.com`, trust anchor `CN=DigiCert Trusted Root G4` (self-signed), root cert SHA-256 fingerprint `55:2F:7B:DC:F1:A7:AF:9E:6C:E6:72:01:7F:4F:12:AB:F7:72:40:C7:8E:76:1A:C2:03:D1:D9:D2:0A:C8:99:88`, pin file `ops/projects/P032/B0/tsa/digicert_primary.pem` (file SHA-256 `ce7d6b44f5d510391be98c8d76b18709400a30cd87659bfebe1c6f97ff5181ee`). The pinned **fallback TSA** is endpoint `http://timestamp.sectigo.com`, trust anchor `CN=USERTrust RSA Certification Authority` (self-signed), root cert SHA-256 fingerprint `E7:93:C9:B0:2F:D8:AA:13:E2:1C:31:22:8A:CC:B0:81:19:64:3B:74:9C:89:89:64:B1:74:6D:46:C3:D4:CB:D2`, pin file `ops/projects/P032/B0/tsa/sectigo_fallback.pem` (file SHA-256 `8a3dbcb92ab1c6277647fe2ab8536b5c982abbfdb1f1df5728e01b906aba953a`). The fallback endpoint is used only when the primary returns a non-Granted TSR or fails to respond within the harness's per-request timeout; use of the fallback is recorded per-token in the published run artifact. Each notarized token (the DER-encoded TSR received from the TSA) is published byte-for-byte alongside its corresponding response envelope under `panel/checker-inputs/` so the C4 checker (per check (vi) below) can verify it offline. What RFC-3161 notarization attests is the fact of the exchange and the wall-clock time at which the response was received; it does not attest anything about the semantic content the provider returned. Notarization does not close the surfaces enumerated below, and any adjudicator relying on notarization for these has misread the protocol:
      1. **Provider collusion (surface 2.4).** Notarization attests the fact and time of an exchange between the runner and the provider; it does not attest that the provider returned the response in good faith. A provider colluding with the runner remains out-of-model.
      2. **Content claims.** Notarization attests the response envelope, not any assertion about what the provider returned as message content. Any claim about the content the provider returned (rather than the fact and time of the exchange) is outside what notarization can attest.
      3. **Envelope-to-verdict decoupling (surfaces 2.5 and 2.8).** The notarized imprint covers the response envelope (top-level identifiers such as `id`, `model`, `type`, `stop_reason`, `usage`, plus any `system_fingerprint` or provider-side identifiers the provider includes) minus message content, so a runner who submits a legitimately notarized envelope alongside verdicts drawn from a different call passes check (vi) with the notarized envelope even though the panel-scored content was never notarized. The protocol does not close this. Any adjudicator relying on notarization for message-content provenance is relying on something the protocol does not attest.
      4. **Surplus-run concealment (surface 2.6).** Check (vi.a) counts notarized tokens on disk under `panel/checker-inputs/`. A runner who executes `N+K` calls, notarizes all `N+K`, but publishes only the best `N` tokens passes check (vi.a). The `N`-token count check bounds published runs, not executed runs. Concealed executed runs remain undetectable from published artifacts alone.
      5. **TSA compromise, coercion, or backdating (surface 2.9).** The pinned .pem file is a single trust anchor per TSA. If the pinned TSA operator issues backdated tokens on request, or is coerced into doing so, or is compromised, the token and its `genTime` signal are unreliable. The primary / fallback pin narrows this to two TSAs; it does not eliminate it.
      6. **Runner-clock vs TSA-clock correlation (surface 2.10).** `envelope.created` (present in some provider responses) is uncorrelated with token `genTime` by any C4 check. A runner who ships an envelope with `created` set to time `T` and a token whose `genTime` is at `T + hours` passes check (vi). Cross-timestamp inconsistency detection is not in scope.
  A mismatch in any of (a) through (e) at B3 sets `prompt_hash_match` to false for that scorer and invalidates that scorer's run per C3. Changing any of (a) through (e) after B0d requires re-publishing the protocol as a new B0-revision. A failure of (f) (missing, surplus, or count-mismatched notarized tokens) or (g) (missing token, imprint mismatch, or signature failure) at B3 is a protocol violation surfaced by check (vi) and invalidates that scorer's run per C3, with the failure mode recorded in `panel/checker.json`. Changing (f) or (g) after B0d requires re-publishing the protocol as a new B0-revision.
- **C3 - Every run published, including disagreement and including re-runs.** No panel run is discarded. Every panel run's raw inputs (the blind sample rows presented to each scorer, the prompts, the prompt hashes, and the per-scorer provider + model identifier + pinned revision) and raw outputs (per-row verdicts, per-scorer rationales, aggregation fields) publish to `public/p032-b3-results/panel/` per §6.2. Panel disagreement publishes in the `panel_disagreement_rows` list and in the per-scorer counts. A run invalidated by C1, C2, or C4 does not vanish: it publishes alongside the successful re-run with a `run_status` field of `invalidated-<reason>` and the failing checker output attached. A re-run publishes as a distinct run artifact in the same directory with a monotonically increasing run index; the original artifact is not overwritten. The primary panel run for aggregation into `panel/aggregate.json` is the FIRST run in wall-clock order that passes C1, C2, and C4. All other runs (including invalidated runs, later C1/C2/C4-valid runs, and any operational re-runs) publish under the same directory with monotonically increasing run index but do not feed `aggregate.json`. No re-run of the panel is permitted within a single B3 fire day unless a C2 or C4 failure invalidated the prior run. If the runner requires a fresh panel attempt for any other reason, B3 fire is rescheduled to a later published date per §5.5 and the prior date's runs publish as superseded attempts. Any invocation of any of the three committed scorer configurations (as defined in C2: the committed system prompt + user-prompt template pair against the committed model at the committed revision, run against any subset of the deterministic blind sample), at any time between B0d publish and B3 fire, is a panel run and publishes per C3. There is no dry-run or debug-run carve-out.
- **C4 - Separate checker seat and script.** A checker seat that did not touch B1 or B2 and does not adjudicate verifies, per panel run, that (i) the prompt actually sent to each scorer hashes to the value committed at B0d, (ii) the blind sample presented to each scorer matches the deterministic sample defined by the blind-sample-selection procedure above, (iii) the blinded fields listed under `Blinding` above did not appear in the input the scorer saw, (iv) each scorer's declared provider, API model identifier, and pinned model revision at B3 match what was committed at B0d per C2(d) (including, for A2, the committed Hugging Face repository id and revision SHA), and (v) the provider response identifier and the response-metadata blob for each scorer run are present and non-empty, and their per-scorer SHA-256 hashes as published in `panel/checker.json` match the SHA-256 hashes the checker recomputes over the byte-for-byte blobs published under `panel/checker-inputs/`, and (vi) for each item and each panel seat, that (vi.a) exactly `N` valid, distinct notarized tokens (per C2(f) and C2(g)) exist under `panel/checker-inputs/` for that item and seat — missing tokens, surplus tokens, or count mismatch is a protocol violation; (vi.b) each token's RFC-3161 message imprint equals the SHA-256 hash of the JCS-canonicalized response envelope published for the corresponding scorer run; (vi.c) each token's signature verifies against the locally pinned TSA certificate file (`ops/projects/P032/B0/tsa/digicert_primary.pem` for tokens obtained from the primary TSA per C2(g), `ops/projects/P032/B0/tsa/sectigo_fallback.pem` for tokens obtained from the pinned fallback), by deterministic offline `openssl ts -verify` invocation with no network call, and (vii) that the verdict and rationale fed into `panel/aggregate.json` are the verdict and rationale the §6.3 collapse rule produces from the published runs: for each seat and each row of the blind sample, the checker reads that seat's `N` published run outputs (`panel/checker-inputs/<seat>/run-<i>/run-output.json`, the scorer's raw per-row JSON output published per C3), applies the §6.3 collapse rule verbatim — the collapsed verdict is the verdict returned by more than `N/2` of the committed `N` runs, with the committed `N` from C2(f) as the denominator in every case; a run whose output does not parse per the committed output format, or whose `verdict` is not exactly one of the two literal values `"trivial"` or `"non-trivial"`, contributes no verdict and counts against the threshold; no such verdict yields `"trivial"`; the published rationale is the rationale from the earliest of that seat's runs whose verdict equals the collapsed verdict, ordered by the RFC-3161 token `genTime` recorded under C2(g) (read by the same deterministic offline `openssl ts -reply` invocation as check (vi.b), local files only), ties broken by ascending hexadecimal-lowercase SHA-256 of the JCS-canonicalized response envelope recomputed from the published blob; a seat-row where no run returned the collapsed verdict carries the empty rationale and the `default-no-contributing-run` marker in `panel_disagreement_rows` — and asserts equality between the recomputation and every collapse-derived field published in `panel/aggregate.json`: the three per-adjudicator non-trivial counts, `panel_nontrivial_count_majority`, `panel_nontrivial_count_unanimous`, and the membership, per-seat verdicts, rationales, and `default-no-contributing-run` markers of `panel_disagreement_rows` (`section3_nontrivial_count_on_sample` is the Tier 1 script's output, not a function of the collapse, and is outside check (vii); an absent or structurally malformed `panel/aggregate.json` or a missing `run-output.json` is a malformed checker input, exit code 1 per the convention below, while value-level disagreement with the recomputation is a check (vii) failure, exit code 2). Check (v) verifies self-consistency of the runner-published artifacts (the published envelope blob hashes to the published hash string); it is not a check against any provider-side attestation of the envelope contents, which the checker's no-network invariant precludes. Check (vi) verifies that the committed run count `N` was honored and that each notarized token is authentic and bound to the corresponding published envelope; it does not attest anything about the content the provider returned, only the fact and time of the exchange. The checker seat is `completion_auditor`. The checker performs all seven checks by deterministic Python standard-library operations only; **no LLM API call, no Claude invocation, no external service call is permitted in the checker script's execution path** (check (iv) compares the strings committed at B0d against the strings recorded from the provider's response metadata during the panel run, and check (v) compares the SHA-256 hashes published in `panel/checker.json` against SHA-256 hashes the checker recomputes over the byte-for-byte blobs under `panel/checker-inputs/`; no network call is issued by the checker for either check). Any inclusion of an LLM in the check invalidates the checker output. Check (iii) "did not appear" is defined as: for each blinded field value V listed in Blinding, `V not in input_string_bytes.lower()` where `input_string_bytes` is the exact UTF-8 bytes sent as the user role to the scorer, lower-cased, and `V` is likewise lower-cased UTF-8 bytes of the field value read from the source data. `scripts/b3/tier3_checker.py` publishes to `public/p032-b3-results/panel/tier3_checker.py` alongside `panel/checker.json` at B3 fire; the script's inputs (each scorer's actual prompt bytes, the deterministic sample bytes, the blinded field values from the source data, and the per-scorer provider + model identifier + pinned revision recorded from the provider's response metadata) publish to `panel/checker-inputs/` so a third party can re-run the checker byte-for-byte and reproduce the JSON. A test suite `scripts/b3/tier3_checker_tests.py` with at least two planted-failure cases per check (twenty-two total: prompt-hash tampered, sample tampered, blinded field leaked, model-revision drifted from the B0d commitment, response identifier or metadata hash drifted, notarization token count / imprint / signature tampered, and collapse-rule mismatch against the recomputation) publishes alongside the script; the suite is run in CI and its output publishes as `panel/checker-tests.log`. Script exit convention: exit code 0 means all seven checks passed for all three scorer configurations; exit code 1 means the input to the script was malformed; exit code 2 means at least one check failed for at least one scorer (check (v) and check (vi) failures exit 2 per this same convention). The script emits one JSON record per scorer with the fields `adjudicator` (string, one of `A1|A2|A3`), `prompt_hash_match` (boolean), `sample_match` (boolean), `blinding_preserved` (boolean), `model_revision_match` (boolean), `response_id_present` (boolean), `response_metadata_hash_match` (boolean), `notarization_token_count` (integer; must equal the committed `N` per C2(f)), `notarization_imprint_match` (boolean; true iff every one of the `N` notarized tokens' message imprints matches the corresponding response envelope hash per check (vi.b)), `notarization_signature_valid` (boolean; true iff every one of the `N` notarized tokens' signatures verifies against the pinned TSA certificate per check (vi.c)), `collapse_rule_match` (boolean; true iff check (vii)'s recomputation of the §6.3 collapse rule from that seat's published run artifacts equals every collapse-derived field published in `panel/aggregate.json`, both the seat-level fields and the panel-level counts and disagreement-row membership, which are not attributable to a single seat and therefore set this boolean false for every seat on mismatch), and `failure_reason` (string, empty when all nine booleans are true and `notarization_token_count` equals the committed `N`). A non-zero exit publishes with the B3 result and invalidates the failing scorer's run per C3.

### 6.4 - Tier 4 - Optional external human corroboration

An external human may be approached to score the same blind sample as a corroboration signal on top of the Tier 3 panel. Tier 4 is optional and it does not gate B3. If no human accepts, the B3 result publishes with Tiers 1 through 3 only, with no apologetic footnote and no implication a human signed off.

**Pool.** The four named Solana developers that P031 wave C3 sourced and ranked on six columns, per `agents/coo/inbox/T-P031-C3-stranger-sourcing-scan-2026-07-26_note.md` and `agents/research_lead/outbox/T-P031-C3-stranger-sourcing-scan-2026-07-26_result.md`:
- R1: Jonathan Claudius (GitHub `claudijd`).
- R2: David Kleymann (GitHub `davidkleymann`).
- R3: Belu (GitHub `belumume`, X `@ubaidmume`).
- R4: J (GitHub `Rhovian`, X `@olorosia`).

None has any prior or current relationship to CaliperForge. All four are named here to bound the pool and remove runner discretion over the choice.

**Approach order.** The four candidates are approached in ascending P031 C3 rank order: R1 first, then R2, then R3, then R4. If a candidate declines, does not respond within seven calendar days of first contact, or discloses a conflict of interest (any current or past CaliperForge affiliation, any current engagement with either analyzer team at Auditware or Sec3, any co-authorship on the P032 build), the runner proceeds to the next candidate in order. The seven-day timer is measured from the first-contact timestamp recorded in the outreach log; no runner discretion applies to when the timer starts or when it expires.

**Tie-breaker on rank.** No tie exists in the C3 ranking as published (R1 through R4 are distinct rows). If a tie were to arise from a re-ranking, the tie-breaker is alphabetical by GitHub login, ascending (which resolves R1 through R4 as `Rhovian` > `davidkleymann` > `belumume` > `claudijd` in ASCII order, i.e., `Rhovian` last if inversion applies; note that the ascending-C3-rank rule above already fixes the order and this tie-breaker only applies if the rank rule itself fails to distinguish).

**Sample and blinding.** The human corroborator scores the same deterministic blind sample defined in §6.3 (same rows, same visible fields, same hidden fields). The human is not shown the panel's verdicts, rationales, or aggregation fields until the human's own per-row verdicts are submitted.

**What the human verdict means when a human accepts.** The human's per-row verdicts publish alongside the panel's verdicts, not in place of them. The additional field `human_nontrivial_count` publishes to `public/p032-b3-results/panel/aggregate.json` with the human's non-trivial count on the sample, and the additional field `panel_human_disagreement_rows` publishes the list of property IDs on which the human's verdict differs from the panel majority (per-adjudicator verdicts, human verdict, one-sentence rationales). Discrepancies between the human and the panel majority are published, not resolved: the reader sees both. Neither verdict overrides the other and neither invalidates the B3 result.

**Verdict finality.** Once any candidate submits any complete per-row verdict set on the blind sample (all rows scored trivial or non-trivial with a one-sentence rationale each), those verdicts are the Tier 4 verdicts. No further candidate is approached. The runner may not solicit a re-do or a retraction. Incomplete submissions (fewer than all rows scored) are published as-is with unscored rows marked `no-verdict`; the runner does not solicit additional rows from that candidate and does not proceed to the next candidate on the basis of incompleteness.

**Outreach message pinning.** The exact outreach message text (verbatim, including subject line, body, and any attachments) is committed in the B0d publication ticket alongside the adjudicator prompt hashes. The same message text is sent to R1, R2, R3, R4 with only the addressee name substituted. Any modification requires a new B0-revision.

**Late-response rule.** A response received after the seven-day timer has expired does not count and is not published; the outreach log records the late timestamp and marks the response as `late-no-count`. A candidate who accepts within seven days but does not deliver verdicts within thirty calendar days of acceptance is deemed `accepted-then-non-delivery` and the runner proceeds to the next candidate.

**Outreach log integrity.** The outreach log is an append-only file. Each entry is timestamped in ISO-8601 UTC and countersigned by the checker seat (`completion_auditor`) via a SHA-256 hash chain (each entry's hash includes the prior entry's hash). Publication of the log includes the full hash chain so a third party can detect editing.

**What happens when no human accepts.** If R1 through R4 all decline, do not respond within their seven-day timers, or all four are ruled out by conflict of interest, the B3 result publishes with Tiers 1 through 3 only. No apologetic footnote is added. The published document does not state that a human signed off, and it does not state that a human failed to sign off in a way that implies the result is degraded. The `human_nontrivial_count` field is absent from `aggregate.json` and the outreach log publishes verbatim to `public/p032-b3-results/panel/tier4-outreach-log.txt` so a reader can verify the pre-registered order was followed and the seven-day timers were honored.

---

## Section 7 - The pre-committed kill statement

Verbatim, published in the B3 result document:

> **If certified properties land predominantly in classes the existing analyzers already flag, we stop and publish that result.**

The definitions of "predominantly" and "already flagged by existing analyzers" are fixed here, in advance, before any B1 or B3 result exists.

### 7.1 - Definition of "already flagged by existing analyzers"

The set of landscape classes counted as "already flagged by existing analyzers" is the union of the classes for which either Radar or Sec3 X-Ray reports at least one finding on either target program in the B3 head-to-head run per §5.3, plus the following classes counted as flagged by construction:

- Class 2 (missing signer check).
- Class 7 (bump-seed canonicalization).

Classes 2 and 7 are counted as flagged by construction because Anchor's `Signer<'info>` type in an account-struct field is mandatory (declaring the field with the `Signer` type forces the framework to enforce the signer check at instruction entry; there is no opt-out and no way to declare `Signer<'info>` without the check), and Anchor's `bump` clause is mandatory paired with any `seeds` clause on a PDA declaration (the framework rejects a `seeds = [...]` clause not paired with a `bump` clause at compile time). Class 1 (missing owner check) is NOT construction-flagged because Anchor's `owner = X` constraint is optional (an account-struct field declared without `owner = X` receives no framework-enforced owner check). Class 3 (missing PDA validation) is NOT construction-flagged because Anchor's `seeds = [...]` clause is optional (an account-struct field declared without `seeds` receives no framework-enforced PDA derivation, and the S2 taxonomy per §Half-2 Class 3 documents this as the account-substitution attack surface). The distinction is not judgment; it is a fact about which Anchor account-struct clauses the framework compiles as mandatory versus optional. The class list `{2, 7}` is pinned by this principle; the runner cannot re-argue the set at B3.

The full "already flagged" set is therefore computed at B3 fire time as: `{2, 7} ∪ {classes reported by Radar} ∪ {classes reported by X-Ray}`. The set is published in the B3 result before the kill statement is evaluated.

### 7.2 - Definition of "predominantly"

Let `C_baseline` be the count of certified P032 properties across both targets whose landscape-class bucket per §2.13 falls in the "already flagged" set defined in §7.1. Let `C_total` be the total count of certified P032 properties across both targets (`|C_raydium| + |C_meteora|`).

"Predominantly" means: `C_baseline / C_total >= 0.70`.

The 70 percent threshold is fixed here. If seven or more of every ten certified properties land in landscape classes the existing analyzers already flag (per §7.1), the kill statement fires.

**Minimum-`C_total` rule.** If `C_total < 5`, the kill statement fires by construction and the published document states verbatim: "the certified-property set is too small to measure and the tool has not cleared the gate." This branch also fires when `C_total = 0` (the ratio `C_baseline / C_total` is undefined; the kill still fires by construction under this rule). The threshold `5` is pinned in advance in this document; below it, no ratio is well-defined, and the pre-registered kill fires without recourse to the 70 percent branch.

### 7.3 - What "we stop and publish" means, operationally

If §7.2 fires at B3, the following actions happen in this order:
- B3 publishes the full result set per Section 6 with the kill statement fired at the top of the document.
- No B4 dispatch fires. The Trident emit sprint does not open.
- No B5 dispatch fires. The practice-leg sprint does not open.
- The kill is reported to the CEO and to any Ludo contact that has already occurred, verbatim.

If §7.2 does not fire (i.e., `C_baseline / C_total < 0.70`), B3 publishes without the kill statement fired, and the sequence continues to Ludo contact per `D-P032-sequence-kill-gate-before-ludo-2026-07-27` and to B4 and B5 subsequently.

The percentage threshold and the class set that count as "already flagged" are fixed in this document. The runner does not choose either at B3 time. The published document reads the numbers off the Tier 1 script output and applies §7.2 mechanically.

---

## Appendix A - Sources and verification

Load-bearing external claims in this document, per the fact-check output contract at `ops/research/FACT_CHECK_OUTPUT_CONTRACT.md`:

- Raydium CP-Swap program ID `CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C` from `ops/projects/P032_BASELINE_BRIEF.md` line 27, verified against the baseline measurement.
- Raydium CP-Swap repository `raydium-io/raydium-cp-swap` from `ops/archive/decisions/decisions_2026-07.md` line 2612 (D-P031-C1-kill-c2-shape-2026-07-26).
- Raydium CP-Swap pinned SHA `78f254e1023751e706df7dc15c453fc3e046697c` from `api.github.com/repos/raydium-io/raydium-cp-swap/branches/master` fetched 2026-07-28.
- Meteora Alpha Vault program ID `vaU6kP7iNEGkbmPkLmZfGwiGxd4Mob24QQCie5R9kd2` from `raw.githubusercontent.com/MeteoraAg/alpha-vault-sdk/main/ts-client/src/alpha-vault/constant.ts` fetched 2026-07-28.
- Meteora Alpha Vault SDK repository `MeteoraAg/alpha-vault-sdk` from the same fetch above.
- Meteora Alpha Vault SDK pinned SHA `7ab389d97db1ad3b4e1889b38487f54ba0ed2a67` from `api.github.com/repos/MeteoraAg/alpha-vault-sdk/branches/main` fetched 2026-07-28.
- Radar repository `Auditware/radar` and pinned SHA `2327887cd47a2bcc71b7a6d0f88f60c9db026436` from `api.github.com/repos/Auditware/radar/branches/main` fetched 2026-07-28.
- Sec3 X-Ray repository `sec3-product/x-ray` and pinned SHA `94804599e393aee1c71ceb4039787d8f73337001` from the precondition report at `agents/research_lead/outbox/T-P032-B0-precondition-sec3-xray-alive-2026-07-27_result.md`.
- Twelve-class Solana vulnerability taxonomy from `agents/audit_engineer/outbox/T-P032-S2-vuln-class-matrix-2026-07-27_result.md` §Half-1a.
- Six baseline classes from `ops/projects/P032_BASELINE_BRIEF.md` §"What it does today, verified by run" item 2.
- S5b Defect 2.1, 2.2, 2.3 from `agents/adversarial_research_lead/outbox/T-P032-S5b-architecture-kill-2026-07-27_result.md` §Attack 2.
- P031 C3 candidate pool and ranking from `agents/coo/inbox/T-P031-C3-stranger-sourcing-scan-2026-07-26_note.md` and `agents/research_lead/outbox/T-P031-C3-stranger-sourcing-scan-2026-07-26_result.md`.

## Appendix B - What this document does not do

- Does not describe the P032 tool's implementation. The tool is built in B1 and B2 and described in those sprints' artifacts.
- Does not describe the mutation-engine catalog. The Certora Gambit / universalmutator anchoring to Wormhole / Cashio / Crema / Cypher is a B2 spec item, not a B0 measurement item.
- Does not authorize outreach to the Tier 4 candidate pool. Outreach copy is a separate CEO-approved deliverable and no contact happens during B0.
- Does not modify the shape lock, framing, or sequence decisions cited in the header. Any drift back to those decisions routes to Director via a decision-request rather than being edited into this document.

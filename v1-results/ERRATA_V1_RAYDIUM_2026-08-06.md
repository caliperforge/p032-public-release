# Errata to P032 Results v1 (Raydium CP-Swap)

**Status:** Published 2026-08-06 in commit 7169ea4cc361f854f6dae1168be2c29003f4b458.
**Attaches to:** `RESULTS_V1_RAYDIUM_2026-08-05.md`, sha256
`66e39b0bc3a673df95b988ef87324c9c5de63e7c5d32e9514848c9431acabcab`.
**Date:** 2026-08-06.
**Nature:** additive. The document this attaches to is not edited, and no byte of the pre-registered
protocol is edited.

---

## 0. What this document is

This is an errata note on the v1 result published 2026-08-05. It says two things and nothing else.

**Item 1.** 17 of the 74 records in the emitted set are properties over `anchor-lang`'s own
auto-generated IDL-management instructions. Emitting them was protocol-correct. The defect is that the
emitted set was never characterised before a rate was computed over it.

**Item 2.** A follow-up measurement of the Raydium handler bodies contradicts the stated rationale of
the protocol clause that decided all 74 records. For 15 of the 24 records reduced at
`constraint = <expr>`, a handler body in the same crate writes the account-data field the property
restates. The clause's rationale says such a property "is not measuring anything the framework did not."
That sentence is false for those 15 records **under the any-handler reading of "post-handler."**
**The sub-fact that cuts the other way belongs next to that number and not below it: of those 15, zero
are written by the handler of the instruction the record is attached to. All 15 are writes by a
different instruction's handler, so under the own-handler reading the count is 0 of 24, not 15 of 24.**
**The other 9 restate no account-data field at all, and the measurement's own limits are named at §2.5.
§2.3 carries this in full; neither reading is adopted anywhere in this document.**

This document reports facts about the code and about the published text. It does not re-score anything,
does not compute a new rate, does not revise `trivial_rate_emitted`, does not read §7, and does not
change a classification. Item 2 in particular is reported here and escalated; it is not resolved here.
See §3.

Nothing in the published v1 document is edited by this errata. Nothing in the frozen protocol is edited
by this errata. Both digests are recomputed in §4 and are unchanged.

**One correction to how this errata was scoped.** The dispatch that commissioned it described the 17
records as "live in the public repo." They are not, as data. What is live at commit
`df3dfddb9e24255266a6207106d6e29697ba9723` is the results document, plus the thirteen pre-registration
files published 2026-08-01. The emitted-set JSON that carries the 74 records has not been published.
What the published document carries about the 17 is the count and the six instruction names, at its §8.
That is stated here rather than repeated wrongly.

---

## 1. Item 1 — a stratum of the emitted set was never characterised

### 1.1 The count

**17 of the 74 records attach to `anchor-lang`'s auto-generated IDL-management instructions.** Those 17
are the contiguous id block `raydium-cp-swap-0058` through `raydium-cp-swap-0074`. The remaining 57
attach to Raydium's own instructions.

Counting rule, stated so it can be falsified: a record is in this stratum if and only if its
`instruction_attachment` field begins with the string `Idl`. Every such value in the artifact names one
of the six IDL-management instructions that `anchor_lang`'s `#[program]` macro generates; no Raydium
instruction name begins with `Idl`. Command and verbatim output:

```
$ python3 -c "
import json,collections
d=json.load(open('ops/projects/P032/B1/raydium-cp-swap/raydium-cp-swap.json'))
idl=[r for r in d if r['instruction_attachment'].startswith('Idl')]
print('total records:', len(d)); print('IDL stratum:', len(idl))
print('id range:', idl[0]['property_id'], '..', idl[-1]['property_id'])
for k,v in sorted(collections.Counter(r['instruction_attachment'] for r in idl).items()):
    print(f'{k:20s} {v}')"
total records: 74
IDL stratum: 17
id range: raydium-cp-swap-0058 .. raydium-cp-swap-0074
IdlAccounts          3
IdlCloseAccount      3
IdlCreateAccounts    2
IdlCreateBuffer      2
IdlResizeAccount     3
IdlSetBuffer         4
```

The six counts sum to 17, and the id block spans exactly 17 consecutive numbers from 0058 to 0074 with
no gap, so the stratum is contiguous at the end of the emitted set. `74 - 17 = 57` records attach to
Raydium's own instructions.

This count agrees with the count already stated at §8 of the published document, which records that "17
of the 74 records attach to Anchor's generated IDL instructions" and names the same six instructions.
The count is not new. What follows is.

### 1.2 What this code is

The generating code is visible in the expanded-source bundle that was sent to the emitter (sha256
`e0829a71297058a622537e76a1d5c88d8ba69abe0ccbc33bf226fbc5fe635353`, 26,834 lines). It sits in a module
the macro emits, `mod __private`, opening at bundle line 23007. Its dispatch is keyed on
`anchor_lang::idl::IDL_IX_TAG_LE` (line 22988) and decodes `anchor_lang::idl::IdlInstruction` (line
23020). The account structs the 17 records attach to are defined inside that module: `IdlCreateAccounts`
at 23254, `IdlAccounts` at 23626, `IdlResizeAccount` at 23872, `IdlCreateBuffer` at 24170, and the
remaining two below them. The constraint that most of the 17 restate is written by the macro, not by
Raydium: `#[account(constraint = authority.key!= &ERASED_AUTHORITY)]` at line 23629 and again at 23875,
with `ERASED_AUTHORITY` imported from `anchor_lang::idl` at 23119.

None of this is Raydium's code. It is framework code that appears in the crate because the crate uses
the framework.

**One limit on that claim, stated rather than glossed.** That the same instructions appear byte-for-byte
in every Anchor program on Solana follows from their being macro-generated by `anchor-lang` rather than
authored per program, and it is what the code above shows for this crate at this Anchor version. It is
an inference from the macro's nature, not a cross-program measurement. No second Anchor program was
examined. Treat "identical in every Anchor program" as unverified here; "generated by `anchor-lang` and
not by Raydium" is what the bundle lines above actually show.

### 1.3 Emitting them was protocol-correct

Protocol §4.1 defines the emitted set, verbatim from the published text at line 214:

> The **emitted set** is every property the P032 tool's authoring layer produces as a candidate, before
> any filter, threshold, deduplication, or ranking. […] No pre-emit filter (schema-validity, syntactic
> parse, non-null predicate, deduplication, LLM confidence threshold, or ranking) is permitted to shrink
> `E`.

A filter that dropped the 17 because they are framework boilerplate would be a pre-emit filter shrinking
`E`, and §4.1 forbids it. The emitter applied no filter and was right not to. Nothing in the run is
defective on this point, and this errata proposes no change to §4.1.

### 1.4 The defect

The defect is upstream of the rate and has nothing to do with filtering.

`trivial_rate_emitted` is defined at §4.3 with denominator `|E|` per §4.1. `|E|` was 74. The rate was
computed and published as `74 / 74 = 1.00`. At no point before that computation was `E` characterised:
no statement of what kinds of code the 74 records were properties *of*, and in particular no statement
that 17 of them, 23 percent of the denominator, are properties over framework-generated code that is
the same in every program built on that framework and is therefore not a measurement of the target at
all.

A rate is only as interpretable as its denominator. A reader of `74 / 74 = 1.00` is entitled to assume
the 74 are properties over the program named in the title. For 17 of them that is not so. The rate is
arithmetically correct and its denominator was never described.

The published document does record the 17 at its §8, under "Target-scope observation, recorded and not
acted on," and states that "whether framework-generated instructions belong in the emitted set is a
question about the emitter's scope, not about §3, and it is unresolved." That is an accurate note in a
limits list. It is not a characterisation of `E`, it did not precede the rate, and it does not tell a
reader that 17 of the denominator's 74 are not about Raydium. This errata states that plainly so a
reader does not have to reconstruct it.

**What this item does not claim.** It does not claim the rate is wrong. It does not propose a corrected
rate, a filtered denominator, or a second rate over the 57. It does not claim §4.1 should permit a
filter. It identifies a characterisation that should have preceded a published rate and did not.

## 2. Item 2 — §3.2 T3's stated rationale against a measurement of the handler bodies

### 2.1 The rule, verbatim

All 74 records were decided by one clause of the frozen protocol, §3.2 T3. Its text, verbatim from the
published protocol at line 147:

> **T3 - Redundant Anchor-constraint re-statement.** A property whose predicate is a direct re-assertion
> of an Anchor `has_one`, `constraint`, `seeds`, `bump`, `owner`, or `signer` clause that the Anchor
> framework's `try_accounts` machinery already enforces at instruction entry. Rationale: the framework
> rejects the transaction before the handler runs if the constraint fails; a property re-asserting the
> same predicate post-handler is not measuring anything the framework did not.

The sentence after the semicolon is a factual claim about program behaviour. It says that because the
framework checked the predicate before the handler ran, re-asserting it after the handler ran adds
nothing. That holds only if nothing the handler does can change the predicate's truth value.

### 2.2 What the measurement shows

24 of the 74 records were reduced at the `constraint = <expr>` row. Those 24 were checked, one at a
time, against every handler body in the pinned crate, by static search over the same expanded-source
bundle the emitter was given. The question asked of each record was: does any handler body write the
account-data field this predicate restates?

**For 15 of the 24, yes.** The other 9 restate no account-data field at all. Zero were undetermined.

The 15 are not a marginal case. Five distinct fields carry them: `PoolState.token_0_vault`,
`PoolState.token_1_vault`, `AmmConfig.protocol_owner`, `AmmConfig.fund_owner`, `IdlAccount.authority`.
Each write has a line number in the bundle. `PoolState.token_0_vault` and `PoolState.token_1_vault` are
written at bundle lines 15861 and 15862 inside `PoolState::initialize`, reached from the handlers
`initialize` (call site 3984) and `initialize_with_permission` (call site 13975).
`AmmConfig.protocol_owner` is written at 6911 in `create_amm_config` and at 7324 in
`set_new_protocol_owner`, reached from `update_amm_config`. `AmmConfig.fund_owner` is written at 6919
and 7351 by the same pair of paths. `IdlAccount.authority` is written at 25126, 25190 and 25245.

**So the rationale is false for those 15 records.** The framework's entry check does not make the
post-handler assertion vacuous when a handler in the same program writes the field. State it in exactly
those terms: the rule reads wrong against these records. Whether that changes what the records are
*worth* is §2.5 and §3, not this paragraph.

### 2.3 The sub-fact that cuts the other way, at the same weight

`15 of 24` is a number that favours the tool, so it gets more scrutiny than a number that does not, and
the strongest counter to it comes from the same measurement that produced it.

**Of the 15, zero are written by the handler of the instruction the record is attached to. All 15 are
written by the handler of a different instruction.**

Every one of the 15 carries "no" in the measurement's own-handler column. Record
`raydium-cp-swap-0018`, for instance, attaches to `Withdraw` and restates `PoolState.token_0_vault`;
the only write to that field is in `PoolState::initialize`, reached from `initialize` and
`initialize_with_permission`, and not from `withdraw`. Record `raydium-cp-swap-0068` attaches to
`IdlSetBuffer` and restates `IdlAccount.authority`; the `__idl_set_buffer` handler writes only
`idl.data_len` and the trailing data, and the writes to `authority` are in `__idl_create_account`,
`__idl_create_buffer` and `__idl_set_authority`. The exhaustive assignment searches returned no write to
any of the five fields inside `deposit`, `withdraw`, `swap_base_input`, `swap_base_output`,
`collect_protocol_fee`, `collect_fund_fee`, `collect_creator_fee` or `__idl_set_buffer`.

**What that means for the reading of `15 of 24`.** Within the execution of a single instruction, the
predicate the property restates cannot change: the framework verifies it at entry, and that
instruction's own handler never writes the field. The shape the search actually found is *"instruction
X's handler writes the field that instruction Y's constraint restates."* That is a claim about a
sequence of two transactions, not about one handler's post-state. A reader who takes `15 of 24` as
showing that these properties catch something within their own instruction is reading it wrong, and the
measurement itself says so.

The two readings are both available on §3.2 T3's own text, which says "post-handler" without saying
whose handler. Neither reading is adopted here. Both numbers are reported: **15 of 24 under the
any-handler reading, 0 of 24 under the own-handler reading.** Which reading §3.2 T3 intends is a
question about the frozen protocol and is escalated at §3, not decided here.

### 2.4 The 9 that answered no, and why

The 9 records that returned no are `0007`, `0039`, `0043`, `0048`, `0062`, `0065`, `0067`, `0071`,
`0074`. In every one, both operands are either account addresses or compile-time constants, so there is
no account-data field for any handler to store to.

- `0007` and `0048` compare `token_0_mint.key()` to `token_1_mint.key()`. Both operands are the
  addresses of accounts passed in the transaction message. An account's address is fixed by the message
  and no handler can write it. The search for assignments to a `.key()` expression returned 14 hits, all
  of them attribute text where `cargo expand` pretty-printed `==` as `= =`, and zero real assignments.
- `0039` and `0043` compare `owner.key()` to `crate::admin::ID` and
  `crate::create_support_mint_associated_owner::ID`. Both right-hand operands are
  `pub const ID: Pubkey` declarations, compile-time constants. The assignment search returned exit 1,
  zero matches.
- `0062`, `0065`, `0067`, `0071` and `0074` compare `authority.key` to `&ERASED_AUTHORITY`, a constant
  imported from `anchor_lang::idl` at bundle line 23119. The assignment search returned exit 1, zero
  matches.

For these 9, §3.2 T3's rationale is not contradicted by anything measured here. The predicate genuinely
cannot change between entry check and handler exit, because neither side of it is storable.

**Recorded so it is not read as an oversight:** `PoolState.token_0_mint` and `PoolState.token_1_mint`
*are* written, at bundle lines 15864 and 15865. `0007` and `0048` are still no, because their predicate
compares the addresses of the two mint accounts in the instruction context, not the `PoolState` fields
of similar name. Those are different things and were not conflated.

**Six of the 24 are in the boilerplate stratum of §1**, namely `0062`, `0065`, `0067`, `0068`, `0071`
and `0074`. Five of them are in the 9 that answered no; one, `0068`, is in the 15 that answered yes.
Stated because a reader holding both items open would otherwise have to cross-tabulate them by hand.

### 2.5 What the measurement could not check

Named here at the same weight as the result, because the result favours the tool.

1. **Nothing was executed.** This is a static read of one `cargo expand` text file. No build, no
   validator, no runtime observation. A write performed by a CPI from another program into a
   Raydium-owned account would be invisible to the method. The measuring seat judged that shape
   structurally impossible for `PoolState` and `AmmConfig`, since only the owning program may write its
   own accounts, but did not verify it by execution and labelled it UNVERIFIED. It is repeated as
   UNVERIFIED here.
2. **The expansion was trusted without a source diff.** The premise that `cargo expand` expands macros
   without altering handler bodies was taken on trust. `bundle.txt` was never diffed against the
   original crate source at commit `78f254e`, because no local clone of `raydium-io/raydium-cp-swap`
   exists and the measuring seat had no web access. If expansion dropped or rewrote a handler body, the
   whole result inherits that error.
3. **Call-site confirmation was name-based, not type-based.** Callers were located by searching for the
   callee's name and reading the caller. A write reached through a trait object, or through a generic
   monomorphised under a different name, would not have been caught. No trait-dispatched state mutation
   was found in this crate, but the search could not have found one.
4. **The identification of the "restated field" is the measuring seat's own reading, not the
   emitter's.** The emitted-set records carry no field annotation; the confirmed key set is
   `property_id`, `instruction_attachment`, `predicate`, `justification_constraint`, `emitter_class`,
   `raw_confidence`. The restated field was derived by reading each predicate's right-hand side. The 9
   no rows turn entirely on the reading that an account *address* is not an account-data *field*. A
   definition of "restated field" that counts `.key()` would change those 9.
5. **Whether "any handler" or "own handler" is the right reading of §3.2 T3 was not decided**, by the
   measuring seat or here. §2.3 reports both.

### 2.6 The count that circulated was wrong, and the artifact governs

The reduction-row count is **24, not the 18** that circulated in internal dispatch material. The
published document already carries 24, at its §3 clause table. The B2 verdict artifact carries 24 at
line 99, verbatim:

```
| constraint = <expr> | 24 |
```

An independent recount over the verdict table's 74-row body returns 24. The naive whole-file grep
returns 25; the extra one is line 99 itself, the distribution row that reports the count. The
distribution table sums `24 + 23 + 21 + 4 + 2 = 74`, which reconciles with the full emitted set. 18
appears nowhere in that table and does not reconcile with it. The 24 record ids in the measurement were
checked against the 24 rows the verdict table marks `constraint = <expr>`: the two sets are identical,
with no id in one and not the other.

No number in the published document changes as a result. This paragraph exists because the wrong figure
travelled and a reader may have seen it.

## 3. What this errata does not do

**It does not reclassify anything.** §3 was applied correctly to all 74 records as written. Every record
matched §3.2 T3's stated condition, which is a condition on predicate shape and on the presence of an
Anchor clause, not on the rationale sentence. The measurement in §2 contradicts the rationale, not the
condition. Whether a clause whose rationale reads wrong should still decide a classification is a
question about the frozen protocol, and this is a document that reports a fact about code. It has no
authority to answer it and does not attempt to.

**It does not rewrite, soften, or reinterpret any protocol text.** §2 through §7 of the protocol are
frozen and published. A frozen rule that reads wrong against the record is reported and escalated. It is
not edited. Not one byte was changed; §4 recomputes the protocol digest and it is unchanged.

**It does not re-score, re-rate, or re-read.** No revised `trivial_rate_emitted`. No second rate over
any subset. No recall number. No class distribution. No read of §7 or of the kill statement. No new
classification of any record. Those are other steps' work and none of them is done here.

**It does not resolve the reading question.** §2.3 reports 15 of 24 under one reading of "post-handler"
and 0 of 24 under the other, and adopts neither.

**Two matters are escalated by this errata rather than settled by it,** and both are recorded in the
seat's findings for routing:

1. §3.2 T3's rationale reads factually wrong against 15 of the 24 `constraint = <expr>` records under
   the any-handler reading. The escalation filed 2026-08-05 raised this as unverified and possibly
   wrong. It has now been measured. What follows from that is a call above the seat that measured it.
2. Which reading of "post-handler" §3.2 T3 intends, since the two readings give 15 and 0 respectively,
   and the clause's own text does not say.

---

## 4. Reproduction

### 4.1 Inputs

Every figure above is derived from these files at these digests. Recompute with `shasum -a 256`.

| file | sha256 |
|---|---|
| `RESULTS_V1_RAYDIUM_2026-08-05.md` (the document this attaches to) | `66e39b0bc3a673df95b988ef87324c9c5de63e7c5d32e9514848c9431acabcab` |
| `raydium-cp-swap.json` (emitted set, 74 records) | `d78c131cafc9e32516323b2bb8f3dc92b8ae73d7b238be591ac0a5e00ad180da` |
| `P032_B0_BENCHMARK_PROTOCOL.md` (frozen protocol) | `9862b050ff93ee1e65633e2e274e13ec38672e736b010394bbb47b79c8d9e1d3` |
| `section3-verdicts-raydium.md` (B2 per-record verdicts) | `28191278043b1caa2e63b2ab0202b012bce50cdd74d20f8bee2cfdf3c11ac64a` |
| `bundle.txt` (expanded source sent to the emitter, 26,834 lines) | `e0829a71297058a622537e76a1d5c88d8ba69abe0ccbc33bf226fbc5fe635353` |
| `T3_POST_HANDLER_GREP_2026-08-06.md` (the §2 measurement) | `794bcc8470e382e7a31ae4c8aaf83d8f816bf8e2bba716461449339d95a267df` |

All six were recomputed at the start and at the exit of drafting this errata and were identical at both
points. The protocol digest and the published-document digest are unchanged from their published values,
which is the mechanical proof that this errata edited neither.

### 4.2 A note on the artifact's shape, for anyone reproducing §1

The emitted-set JSON's top level is a bare list of 74 objects. It is not a dict with a `records` key, and
the per-record keys are `property_id`, `instruction_attachment`, `predicate`,
`justification_constraint`, `emitter_class` and `raw_confidence`. There is no `justification` key.
Reproduction code written as `d['records']` or `r['justification']` will raise `KeyError`.

### 4.3 The commands

§1.1 carries its command and verbatim output inline. The reduction-row count in §2.6 reproduces with:

```
$ grep -c 'constraint = <expr>' ops/projects/P032/B2/section3-verdicts-raydium.md
25
$ awk 'NR>=12 && NR<=85' ops/projects/P032/B2/section3-verdicts-raydium.md \
    | grep -c 'constraint = <expr>'
24
```

The per-record yes and no verdicts of §2.2 through §2.4, each with its bundle line number for a yes and
its empty search for a no, are in the measurement receipt named in §4.1 at the digest given there. That
receipt also carries the search method in full, including the four whole-struct-overwrite searches and
the two raw-bytes-write searches that were run to rule out a store that reaches a field without naming
it.


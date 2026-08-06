# Build log, entry 1: the tool scored 100% trivial on its own benchmark, and it was right to

**Status:** DRAFT. Not published. Awaiting the §4a content gate, and then HELD pending CEO approval on the text.
**Date:** 2026-08-06.
**Entry:** 1 of a continuing log.

---

## 0. What this log is

We are building a tool that reads Solana programs and writes down the security properties they ought to
satisfy. Before we built it we published a benchmark that would tell us whether it worked. This log
records what the benchmark said, in the order we found it out.

This is entry 1. It covers one day. The tool did not work, and the reason it did not work turned out to
be more useful than the tool would have been.

The reason generalises past Solana, so it is worth stating before the evidence: an LLM tool's output
contract can make the target sentence unwriteable, and that failure looks exactly like model
underperformance while being nothing of the kind. Sections 1 to 3 are the Solana evidence for that.
Section 4 is the claim itself and needs no Solana; a reader who wants only that can start there.

## 1. The number

On 2026-08-05 we ran the emitter once against Raydium CP-Swap, source pinned at commit
`78f254e1023751e706df7dc15c453fc3e046697c`. One API call, `stop_reason` `end_turn`, 382,038 input tokens,
14,154 output tokens, no retry, no parse error. It returned 74 property records.

We scored those 74 against §3 of the benchmark protocol, which was published on 2026-08-01 before any
result existed and which defines "trivial" in advance. The scoring is a deterministic pattern match with
no model in the path.

- `trivial_rate_emitted` = 74 / 74 = **1.00**
- `section3_nontrivial_count_on_sample` = **0**

All 74 were decided by the same clause, §3.2 T3, which classifies a property as trivial when its
predicate restates an Anchor `has_one`, `constraint`, `seeds`, `bump`, `owner` or `signer` clause that
the framework already enforces before the handler runs. The breakdown, which reconciles exactly:
`constraint = <expr>` 24, `seeds`/`bump` 23, `signer` 21, `has_one` 4, `owner =` 2, total 74.

A rate of 1.00 on a triviality measure is the worst available value. We had built something that
produced 74 statements, every one of which our own pre-registered rule said was worth nothing.

The classifier was controlled before we believed the number. It was run against the protocol's own
worked non-trivial examples and returned non-trivial for all five of them, and against a worked trivial
example and returned trivial. A matcher that answered "trivial" to everything would have produced the
same headline, and this one does not.

## 2. The number was not a performance result

The obvious reading of 74/74 is that the model underperformed. We spent the next day establishing that
it did not, and the evidence is not ambiguous.

We re-measured the input the model was given. The expanded-source bundle sent to the emitter
(sha256 `e0829a71…5353`, 1,239,890 bytes) contains 120 balanced `#[account(...)]` attribute blocks. Inside
those blocks, the six clause types the emitter was permitted to read occur as follows: `has_one` 4,
`seeds` 23, `bump` 23, `owner =` 2, `signer` 1, `constraint = <expr>` 24. The crate also declares 20
fields typed `Signer<'info>`, which the emitter's rules treat as a `signer` clause.

That is 4 + 23 + 2 + 24 + 21 = **74 admissible clause instances**, where the 21 is the 20 `Signer<'info>`
fields plus the 1 literal `signer` clause.

The emitter returned 74 records. The arithmetic closes with no residue. There is no missed clause, no
dropped candidate, no deduplication, no confidence threshold. **Recall on the task as specified was 74 of
74.**

Three more measurements point the same way, and each of them rules out a different comfortable
explanation.

- **It was not truncated.** `api_stop_reason` reads `end_turn`, not `max_tokens`. The model stopped on its
  own with 1,846 tokens of headroom under the frozen 16,000-token cap. A bigger output budget would have
  changed nothing.
- **It was not hallucinating.** Zero of the 74 records failed the schema check. Every record carries a
  citation to text that is actually in the source.
- **It was not paraphrasing.** The `cargo expand` pretty-printer mis-prints `==` as `= =`. Of the 74
  records, **17 reproduce that malformed operator verbatim and 0 repaired it**. A model that was loosely
  restating what it saw would have tidied the operator. It cited bytes instead. (Section 6 mentions a
  different 17: 17 of the 74 records are properties over Anchor's own auto-generated instructions. The two
  sets of 17 share a single record.)

The null was definitional. The emitter executed its specification with complete fidelity, and the
specification is what produced the zero.

## 3. What we had actually built

The emitter's system prompt, frozen and hash-committed before the run at sha256 `8c509d42…2584`, says
three things that matter here. Quoted verbatim:

> You derive properties exclusively from the following mechanical Anchor constraint clauses that appear
> in the expanded source

> Every property you return must cite the exact clause text as it appears in the expanded source, in the
> record's justification_constraint field. No other source of evidence is admissible.

> If a field carries no clause from the list above, no property attaches to that field.

Against that, we had a ground-truth corpus: 60 findings from published third-party audits of Solana
programs by Trail of Bits, Neodyme, OtterSec, Certora and Mad Shield, each classified by the smallest
read-scope in which the defect is observable, each carried with its real fix commit. The findings are
theirs; the classification is ours. Seven of the 60 sit at the accounts-struct scope the emitter reads.

Every one of those seven is a constraint that is **absent**. `create_key` is declared
`AccountInfo<'info>` and carries no constraint at all. `rent_collector` carries only `mut`. Two of the
seven need a field added to the accounts struct that does not exist anywhere in the source. One carries a
constraint that is present and too weak.

So: the output contract required every record to quote a clause that exists, and every finding we were
trying to reach is a clause that does not exist. A record naming one of those findings has nothing to put
in a required field, and the schema declares `additionalProperties: false`, so there is no other field to
put it in either. **There is no legal output object in which the sentence can be written.**

We had specified a transcriber of things that are present, and pointed it at a job about things that are
absent. It transcribed everything present, correctly, and reported nothing, correctly.

## 4. The finding, stated for someone who has never touched Solana

Everything above this line is Solana and Anchor. The part worth carrying away is neither.

**An LLM tool's output contract can make the target sentence unwriteable, and that failure looks exactly
like model underperformance while being nothing of the kind.**

The output contract is whatever fixes the shape of what your tool is allowed to return: the JSON schema,
the required fields, the enum of allowed labels, the rule about what counts as evidence. It is usually
written early, by whoever is thinking about parsing and validation, and it is usually not reviewed as a
statement about the problem. It is one.

Ours said, in effect, every finding must quote the line it came from. That is a good rule. It stops the
tool making things up, it makes every output checkable, and it is exactly the rule we would recommend to
someone building a tool that summarises what code does. We were not building that tool. We were building
a tool that reports what code fails to do, and there is no line to quote, because the whole finding is
that the line is missing.

The two mistakes are easy to run together, so they are worth separating:

- A tool that **cannot find** the thing is short of capability. More context, a better model, a wider
  input, more tokens: any of these might help.
- A tool that **cannot say** the thing is short of a slot in its own output. None of those help, and each
  of them costs money to try.

We spent one measured run and a day of analysis before we could tell which one we had. The metric could
not tell us, because both failures produce the same number.

**The check you can run on your own tool, and it costs nothing.** Take the single most valuable output
you want your tool to produce. Write it out by hand as a literal instance of your output object, filling
every required field with a real value. If you cannot fill a required field without inventing something,
your tool cannot produce that output and no amount of model improvement will change it. Do this before
you run anything.

Two failure shapes we would now look for first:

1. **A required evidence field that presupposes the answer exists.** `justification_constraint` with
   `minLength: 1` was ours. Any required "quote the source", "cite the line", "give the passage" field
   does the same thing to any finding whose content is an absence.
2. **An evidence-admissibility rule narrower than the question.** Our prompt named six clause types and
   said "no other source of evidence is admissible". In the same input sat the literal English comment
   `/// CHECK: This can be any random public key.`, four characters from the vulnerable field, and the
   tool was forbidden from using it. A human auditor reads that sentence and stops. Ours could not.

Neither of these is visible in an accuracy number. Both are visible in ten minutes with a text editor.

## 5. The corollary that cost us the most: the signal was anti-correlated with the bug

This is the part we did not see coming and the part that would have hurt if we had shipped.

One of the seven findings gives an exact natural experiment, because its real fix changed one thing and
nothing else. The vulnerable declaration and the fixed declaration, both verbatim from the repository
history:

```rust
-    /// A random public key that is used as a seed for the Multisig PDA.
-    /// CHECK: This can be any random public key.
-    pub create_key: AccountInfo<'info>,
+    /// An ephemeral signer that is used as a seed for the Multisig PDA.
+    /// Must be a signer to prevent front-running attack by someone else but the original creator.
+    pub create_key: Signer<'info>,
```

Run our rules against each side.

- **Vulnerable** (`AccountInfo<'info>`): the field carries no admissible clause, so under the prompt's own
  line "if a field carries no clause from the list above, no property attaches to that field", the emitter
  emits **nothing** for it.
- **Fixed** (`Signer<'info>`): the type is now `Signer<'info>`, which is admissible, so the emitter emits
  **one record** for it, the same shape as the 20 `Signer<'info>` records it actually produced on Raydium.

**The tool emits the property if and only if the bug is already fixed.** Its output at a missing-check
site is not merely silent; it is perfectly anti-correlated with the thing it was pointed at. This is a
deterministic consequence of the frozen rules and it needs no API call to derive, which is how we got it
for free.

It gets worse at the most severe finding in the corpus. The one Critical is a market vault that is not
bound to the side of the order. The vulnerable field carries a constraint that **is** admissible:

```rust
    #[account(
        mut,
        constraint = market.load()?.is_market_vault(market_vault.key())
    )]
    pub market_vault: Account<'info, TokenAccount>,
```

That check confirms the vault is one of the market's two vaults. The Critical is that it does not confirm
the vault is the correct one for the order's side. Our emitter would have read the clause, matched it,
and emitted a well-formed, schema-valid, verbatim-cited record asserting that the market vault is bound
to the market. The record would have been **true**, and its truth is the vulnerability.

At the most severe finding in our ground-truth corpus, version 1 of our tool would have issued a clean
bill of health.

We have not executed that run. The claim is derived from the frozen prompt, the frozen schema and the
pre-fix source, and we have written down the test that would falsify it: ingest the pre-fix commit, run
version 1, and look for a record citing that constraint. If the record is absent, this paragraph is
wrong. It costs emitter spend and a new registration, and we have not paid for it yet. It is labelled
unexecuted for that reason.

## 6. The corrections

The plan for version 2 was rewritten three times in one day. Every rewrite came from a measurement, and
most of the measurements contradicted whoever had written the plan. That is the part of this we would
defend, so it gets stated with the seats named rather than as a collective "we learned".

**The COO reversed the whole approach, and the reversal is the spine of this entry.** The plan going into
the day was to widen the emitter's admissible clause list: let it read `address =`, `token::*`, `close`,
and the rest. There is a real measurement behind that idea. Our own count over the Raydium bundle finds
79 present, machine-checkable Anchor binding clauses that version 1 passed over
(`address =` 28, `token::mint` 12, `token::authority` 12, `associated_token::` 10, `mint::token_program`
6, `token::token_program` 4, `close =` 3, `mint::authority` 2, `mint::decimals` 2), and `address =` is the
single most common binding clause in the program. The admissible list was genuinely incomplete about what
is present.

Then the diagnostic asked the question the other way round and measured how many of the seven findings
widening actually fixes. The answer is **0 of 7**. Six of the seven are cases where the tool had every
byte it needed in front of it and had nowhere to put the sentence; widening the input does not give it
one. One row does improve with a wider clause list, and improves into being silent about the right thing
rather than silent about the wrong one. The seventh is a target-selection problem: that program is native
Solana and has no Anchor accounts structs at all, so there is nothing there for any version of this
instrument to read.

The COO's fire order for the next wave changed the job from "widen the clause list" to "rebuild the output
contract", and says of itself, in its own words: *"The COO has been wrong eight times today."* We are
quoting that because a plan that survives contact with its own measurements unchanged is usually a plan
nobody measured.

**The Director asserted something about our public repository that was not true.** A Director-written
ticket told the drafting seat that 17 boilerplate records were "live in the public repo at commit
`df3dfdd`." They are not. Neither seat that checked this had web access, so the check ran against our own record of
the push rather than against the repository: that record puts the results document and the thirteen
pre-registration files at that commit; the emitted-set JSON carrying the 74 records has never been published, and what a
reader can see about the 17 is a count and six instruction names in the results document's limits
section. The drafting seat reported the discrepancy instead of writing the ticket's version, and the
content gate then verified the correction independently from the publication record rather than from the
drafter's word. The Director did not catch it. The drafting seat did, and the gate confirmed it independently.

**The Director asserted something about our own code that was not true.** A Director-written adversarial
brief told the reviewing seat that the emitter's six-label class enum was enforced in code at
`emitter.py:140`. It is not. The records and the candidates log are written to disk first, and
`validate_record` runs afterwards, with its result going only into metadata. Nothing is filtered. This
turns out to be correct behaviour under §4.1 of our own protocol, which forbids any pre-emit filter from
shrinking the emitted set, so the outcome was fine and the claim in the brief was still wrong. The seat
that caught it was the seat the brief was pointed at.

**Two corrections went against us on the day we published the null, and the drafting seat took both.**
The dispatch that commissioned the v1 results document asked for a sentence saying that the two
`fee_monotonicity` records were the mechanism confirming itself: the only channel that could carry the
program's economics was the only channel that did. The records do not support it. Both have the predicate
`token_0_mint.key() < token_1_mint.key()`, which is a mint-address ordering comparison and carries no
economics; the `fee_monotonicity` label is assigned by a mechanical rule that fires on any inequality
between two operands, and the prompt itself calls the class strings opaque enum labels. The published
document states the non-confirmation instead. The same dispatch supplied a `fee_rate` occurrence count of
159; the bundle gives **187**, with a counting rule and a per-identifier breakdown that partitions them.
159 is the number of lines containing the substring, which is what `grep -c` returns; 187 is the number
of occurrences, and the two count different things. The document carries 187. Both corrections make our published claim weaker than
the dispatch wanted it, which is the direction a correction has to be allowed to go.

**Our own triage of the null was wrong by 16 records, in the direction that flattered us.** The COO's
hand read of the 74 records counted 58 as trivial restatements. The frozen §3 procedure returned 74. The
two agree exactly on the two easiest families, 21 signer restatements and 23 PDA-derivation
restatements, and diverge on the third: the hand read counted 14 `has_one` restatements and set 16 aside
as duplicates or as properties over the framework's generated instructions. §3 as published admits no
duplicate exemption and no generated-instruction exemption. It classifies on predicate shape, and each of
those 16 restates a `constraint =` or `owner =` clause verbatim. The protocol was right and the eyeball
was wrong, and the audit seat reported the delta loudly rather than quietly adopting the number that
looked better.

**Two smaller counts were corrected before they could travel.** The reduction row for
`constraint = <expr>` is **24, not the 18** that circulated in internal dispatch material; the published
distribution table sums 24 + 23 + 21 + 4 + 2 = 74 and 18 does not appear in it. And a count that circulated
as 14 Squads findings from four firms was corrected to **two firms** when it circulated, because only
two firms' reports had been screened at that point. The corpus has since been finished: 60 findings,
five firms, three programs, of which 43 are Squads findings from four firms. The correction was right
when it was made and the number it corrected has been superseded since.

None of this is a process anecdote. The reason it belongs in entry 1 is that the finding in section 4
only became visible because a seat was allowed to return a measurement that contradicted the seat that
dispatched it, three separate times in one day, without that being treated as a failure.

## 7. What did not change

Nothing about the benchmark changed, and nothing was retro-fitted after the result came in.

The protocol was published on 2026-08-01, before any result existed, in one commit
(`e95467359cb7cc03ebd3583b3f9807f87fb1dd85`) with a server-side push timestamp of 2026-08-01T14:05:49Z,
anchored to Bitcoin block height 960566. Sections 2 through 7, which carry the measure, the triviality
definition, the certification rules and the pre-committed kill statement, are frozen. We recomputed the
digest of our working copy at the start and at the end of writing this entry:
`9862b050ff93ee1e65633e2e274e13ec38672e736b010394bbb47b79c8d9e1d3`, both times. That is byte-identical to
the digest recorded for the published file, which means the whole document is unchanged, not only
sections 2 through 7.

One honest limit on that statement. We did not re-fetch the file from the public repository while writing
this; the comparison is against the digest in our own publication record, taken from live API reads at
publication time. Anyone can check the stronger version themselves by hashing the file at that commit.

Two things follow, and a result this bad is exactly when a team is tempted to move the goalposts.

- **The triviality rule that scored us 1.00 was not touched.** We found a case where §3.2 T3's stated
  rationale reads wrong against a measurement of the handler bodies. We reported it and escalated it. We
  did not edit it, soften it, or reinterpret it, and the errata that reports it recomputes the protocol
  digest to prove it edited nothing.
- **The 74/74 was published as it stood.** The result document went out on 2026-08-05 with the rate, the
  cost, the open questions and the limits, including one open question that moves a number in our favour
  on one of its two readings and which we did not resolve in our favour.

## 8. What is next

The next step is a specification for what a version 2 record is allowed to say, and it is being written
and adversarially reviewed before anything is built. Entry 2 will report what that review found, whether
or not it survives it.

---

## PASTE-READY

*Everything above this line is a working draft and is not paste-ready. The block below is. It is
self-contained, it needs no editing, and nothing outside it should be sent anywhere.*

---

We built a tool that reads Solana programs and writes down the security properties they should satisfy.
We published the benchmark that would judge it on 1 August, before we had any result, and anchored it so
the rules could not move afterwards.

On 5 August we ran it once. It scored the worst possible value on its own measure: 74 of 74 properties
trivial, zero non-trivial, a rate of 1.00.

On 6 August we found out why, and it was not what the number looked like.

The tool had not underperformed. It had hit 100% of what it was told to look for. The source it was given
contains exactly 74 instances of the six constraint types it was permitted to read, and it returned
exactly 74 records with no misses, no schema failures, and no truncation. When the source it was quoting
contained a mangled operator, it reproduced the mangling verbatim 17 times rather than tidying it. It
executed its specification perfectly.

The specification was the defect. We had told the tool that every finding it reported must quote the line
of code the finding came from. That is a sound rule for a tool that describes what code does. We were
building a tool that reports what code fails to do, and every real finding in our ground-truth corpus is
a check that is **missing**. There is no line to quote. The sentence naming the finding could not be
written in any valid output the tool was allowed to produce.

**The generalisable version, and it has nothing to do with Solana: an LLM tool's output contract can make
the target sentence unwriteable, and that failure looks exactly like model underperformance while being
nothing of the kind.** A tool that cannot *find* something is short of capability, and a bigger model or
more context may fix it. A tool that cannot *say* something is short of a slot in its own output schema,
and none of those things will ever fix it. Both produce the same score. Anyone can check their own tool
for this in ten minutes with a text editor: take the single most valuable output you want, and try to
write it by hand as a literal instance of your output object with every required field filled. If you
cannot fill one without inventing something, your tool cannot produce that output.

The expensive part is what our tool would have done at the worst finding. Our corpus holds one Critical:
a vault that is not bound to the correct side of a trade. The vulnerable code carries a weaker check that
our tool *was* allowed to read. It would have emitted a clean, valid, correctly-cited record confirming
that the vault is bound to the market. That record would have been true, and its truth is the
vulnerability. At the single most severe finding we had, version 1 would have issued a clean bill of
health.

More generally, on the one case where the fix is a single-line type change, the tool emits its property
if and only if the bug is already fixed. Its signal at a missing-check site is anti-correlated with the
bug.

Two things. Nothing in the published benchmark was changed after the result came in: sections 2 through
7 are byte-identical to the version anchored on 1 August, on a digest we recomputed against our own
record of that publication rather than by re-fetching the file. And we found a rule that reads wrong
against our own data, reported it, and left it alone. And the plan was rewritten three
times in one day, every time because a measurement contradicted the seat that wrote it, including the
plan we started the day with. The approach going in was to let the tool read more kinds of constraint;
measurement showed that fixes 0 of 7 of our target findings, so the plan changed from widening to
rebuilding.

The tool did not work. We are publishing why, because the reason is more useful than the tool would have
been.

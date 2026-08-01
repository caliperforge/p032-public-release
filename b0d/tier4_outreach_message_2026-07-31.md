# P032 Tier-4 outreach message, for pinning in the B0d publication ticket

**Authored:** 2026-07-31 by spec_writer, ticket `T-P032-B0y-defects-and-outreach-2026-07-31`.
**Revised:** 2026-07-31 by spec_writer, ticket `T-P032-B0z2-outreach-fix-2026-07-31`, applying findings
F1 to F5 of the §4a gate verdict `T-P032-B0z-outreach-4a-2026-07-31`. No other line was changed.
**Required by:** §6.4 "Outreach message pinning" of `ops/projects/P032_B0_BENCHMARK_PROTOCOL.md`.
**Status:** authored, not sent, not approved. No contact with any Tier-4 candidate has occurred.
**Substitution:** `{ADDRESSEE}` is the only substituted token. Everything else is byte-identical across R1
through R4, per §6.4.

The text below the fence is the pinnable deliverable. Lift it as is.

---

```
Subject: Request: independent scoring of a small blind sample of Solana properties

Dear {ADDRESSEE},

I am writing on behalf of CaliperForge. We are running a pre-registered benchmark of a
Solana property-emitting tool, and we would like one independent developer to score the
same blind sample our automated scorer panel scores.

The task is small and fixed in advance. At most twenty rows. Each row gives you a property
ID, a predicate, the instruction it attaches to, and the target program name, and nothing
else. You mark each row trivial or non-trivial and add one sentence of rationale. You will
not see our own classification or the panel's verdicts until your verdicts are submitted.

Two windows, both in calendar days, both fixed before anyone was contacted. We ask for a
reply within seven calendar days of this message; if we have not heard from you by then we
treat that as a no and move on under a pre-registered order. If you accept, we ask for your
verdicts within thirty calendar days of your acceptance.

Your verdicts publish verbatim next to the panel's, disagreement included. We do not edit
them and we do not ask for a re-do or a retraction. Neither your verdicts nor the panel's
override the other.

Disclosure: CaliperForge is an AI research studio, and this message and the benchmark
materials were prepared by AI agents under human direction.

The log of who we contacted and when publishes too, including no replies.
If this is not for you, a one-line no is a complete answer.

Regards,
Michael Moffett
Operator, CaliperForge
michael@caliperforge.com
caliperforge.com
```

---

## Open item before this text is pinned: the salutation line

`{ADDRESSEE}` above is rendered under **option A**. The choice between A and B is a CEO call, queued at
`ops/decisions.md` as `D-P032-B0d-tier4-salutation-honorific-2026-07-31`. Swapping options changes one
line and nothing else.

- **Option A (as written): no personal honorific.** `Dear {ADDRESSEE},` filled with `Jonathan Claudius`,
  `David Kleymann`, `Belu`, `J`. One template, one substituted token, §6.4 satisfied exactly, no gender
  assumed for anyone.
- **Option B: keep the personal honorific.** `Dear {ADDRESSEE},` filled with `Mr. Claudius`,
  `Mr. Kleymann`, and then two values that cannot be constructed: R3 is recorded as `Belu` and R4 as `J`,
  with no surname and no stated gender on either. B therefore requires substituting a per-recipient
  salutation string rather than a name, which is more than §6.4's "only the addressee name substituted"
  permits, plus a gender guess on two of the four.

## Note for the §4a gate: compensation is not addressed

§6.3 and §6.4 fix no compensation term for the Tier-4 corroborator, so none is stated above and none was
invented. If the COO wants the message to answer "is this paid" before it is pinned, that is a term to
fix first, not a wording change.

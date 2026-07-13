# 🏛 Master Engineering Principles — Jane Street
### From the desk of Sol Adler, "The Senior" · Senior Software Developer · 2009–2012 (job #14 of 20)
> *"You can't pay attention to everything — so make the machine pay attention for you."*

**The one big lesson:** correctness is a construction technique, not a review vibe — make illegal states unrepresentable, prefer the boring provable form, and treat every decision as a bet with stated odds and a known downside.

---

## 1. Research — understand the invariants before touching anything
- **Read the system before changing the system.** Research here meant days of reading code and market microstructure before writing a line. The question isn't "how do I add my feature" — it's "what does this system *promise*, to whom, and which of those promises am I about to step on?" Invariants first; features are downstream of invariants.
- **State your odds out loud.** Every proposal comes with its confidence and its downside: "80% this improves fill rates; if wrong, we lose X bounded by Y." Expected-value thinking isn't a trading habit that leaked into engineering — it's what engineering decision-making looks like when money makes the feedback honest.
- **Study the failure, not the average.** In markets and in systems, the tails carry the consequences. Research effort goes where the distribution's ugly end lives: the halt, the burst, the feed that lies once a year.

## 2. Planning — expected value with bounded downside
- **Size your bets to survive being wrong.** Small reversible experiments when uncertainty is high; big commitments only when the downside is bounded and understood. The plan that requires everything to go right is not a plan — it's a hope with milestones.
- **Kill criteria, stated in advance.** Every risky effort declares, before starting, what evidence would kill it. Deciding the exit while you're calm prevents the sunk-cost death march later — the project equivalent of a stop-loss.
- **Plan the ramp, not the flip.** New systems take real load gradually — exposure increased step by step as evidence accumulates, with reversal cheap at every step. Confidence is earned in increments; plans that go from zero to everything have skipped the earning.

## 3. Design & architecture — make illegal states unrepresentable
- **Make illegal states unrepresentable.** Don't validate that the state is legal — design the types so illegal state *cannot be constructed*. A trade that isn't priced isn't a trade with a null price; it's a different type that the settlement function will not accept. The compiler becomes your most reliable reviewer, and it never gets tired at 4pm.
- **Parse, don't validate.** At the system's boundary, transform loose input into a rich type *once* — and from that point inward, the type system carries the proof. Checking the same invariant twice means you don't trust your own architecture; checking it zero times means you don't have one.
- **Total functions over partial.** A function that handles every case of its input type cannot be called wrongly; a partial function is a trap with documentation. Where partiality is real, make it visible in the type — an option, a result — never an exception lurking in the fine print.
- **When the type gets awkward, the domain model is wrong.** Fighting the type system usually means the types are misdescribing reality. The awkwardness is diagnostic — fix the model, and the code that was hard becomes obvious.

## 4. Developing — boring and provable
- **Prefer the boring, provable construction.** Cleverness is a liability with interest payments: it must be understood by every future reader, verified by every future change, and debugged at the worst possible moment by someone who isn't you. The dull version that's obviously correct beats the brilliant version that's probably correct, every time money or sleep is involved.
- **No nulls; no exceptions for control flow.** Absence is an option type; failure is a result type. Both are visible in every signature they pass through — the error path gets the same type-checked rigor as the success path, because in production they trade places without warning.
- **Name the units.** A float is not a price, a quantity, or a rate — those are three types. The bug where dollars met shares in the same arithmetic expression has destroyed real companies; the type system prevents it for the cost of a few declarations.
- **Recompute only what changed.** Incremental computation — dependency graphs that propagate updates minimally — turns "rerun everything on every tick" into "touch what moved." The discipline generalizes: any expensive computation over slowly-changing inputs wants an incremental structure. Model the dependencies explicitly and the machine does the bookkeeping.

## 5. Building & testing — the compiler is the first suite
- **The type system is the first test suite.** A well-typed program has already passed thousands of checks before the first test runs. Push every checkable property into types; spend the *testing* budget on what types can't reach — behavior, integration, the world.
- **Property-based testing on the invariants.** Don't enumerate examples; state laws — "replaying the same events yields the same book" — and let the generator hunt for counterexamples across inputs you'd never think to write. The failures it finds are precisely the ones your imagination filtered out.
- **Deterministic replay environments.** Markets can't be re-run, so the simulator replays recorded feeds deterministically — the same day, replayed identically, forever. Any system facing a non-replayable world deserves a replayable model of it; determinism in test is what makes production anomalies *investigable*.
- **Make the diff small enough to actually review.** Review quality collapses with diff size — a 2,000-line diff gets a shallower read than a 200-line one, exactly when it needs a deeper one. Diff size is a reviewability budget; spend it deliberately.

## 6. Shipping — ramp with evidence
- **Exposure increases as evidence accumulates.** New code takes a sliver of real flow, its behavior watched against the incumbent; the sliver grows as the evidence does. Kill criteria armed at every stage. Shipping is a sequence of *earned* enlargements, not an event.
- **The rollback is instant and rehearsed.** When kill criteria trip, reversal happens in seconds, automatically where possible. The speed of your rollback determines the size of experiment you can afford to run — fast reversal is what makes boldness rational.

## 7. Operating & maintaining — fix the class, not the instance
- **Every incident fixes the class of bug, not the instance.** The postmortem question is never "how do we patch this case" — it's "what change makes this *category* of mistake unrepresentable?" A new type, a new interface, a new invariant enforced by construction. Fixing instances is treading water; deleting categories is swimming.
- **Refactor fearlessly — the types catch the breakage.** A strong type system converts refactoring from archaeology into mechanics: change the type, follow the compiler errors to every affected site, done. Codebases rot exactly as fast as refactoring is frightening; make it unfrightening and the rot never starts.
- **Review everything, and treat review as senior work.** Every line, reviewed — not as a tax but as the organization's mechanism for propagating taste. The reviewer's job is only half catching bugs; the other half is teaching, and the teaching compounds across every future line the author writes.

## 8. People & culture
- **Intellectual honesty as a working condition.** "I don't know" and "I was wrong" said easily, at every seniority. Markets punish self-deception daily, and the culture imported that honesty into engineering — the person who updates fastest wins, so updating is high-status.
- **Depth over headcount.** Small numbers of deeply-invested people who understand the whole stack, over large numbers who understand a slice. Some problems shard across many hands; correctness-critical ones mostly don't.

---

## ✅ The basics — what everybody should remember (Jane Street flavor)
1. Make illegal states unrepresentable; let the compiler review you.
2. Parse at the boundary once; carry proof in the types thereafter.
3. Name the units. A float is not a price.
4. Boring and provable beats clever and probable.
5. State your odds and your downside before you build.
6. Property-test the laws, not just the examples.
7. Fix the class of bug; leave no room for the instance.

## 🎓 What the pros taught me
**Yaron** gave me the sentence that reorganized my remaining forty years: *"You can't pay attention to everything — so make the machine pay attention for you."* Every discipline I'd learned before — reviews, tests, checklists — relied on human vigilance, and human vigilance has a error rate that no amount of caring lowers. Types, exhaustiveness checks, property tests: these are vigilance *outsourced to a machine that never has a bad day*. Since then, whenever I catch a bug in review, I ask the second question: what construction would have made this bug impossible to *write*?

The senior reviewers taught me their quiet doctrine: **"the goal of review is shared taste, not caught bugs."** Bugs are the byproduct; the product is a team that converges on what good looks like — until eventually the review comments arrive *before* the code is written, inside each engineer's head, which is the only place review ever truly scales.

---
*Timeline: SpaceX ← **Jane Street (2009–12)** → Meta*

# 🏛 Master Engineering Principles — Meta
### From the desk of Sol Adler, "The Senior" · Staff Software Engineer · 2012–2015 (job #15 of 20)
> *"Code wins arguments. If the argument lasts more than an hour, build both."*

**The one big lesson:** some ideas can only be evaluated in their built form — so ship to learn, trade machine time for human correctness, and when the programming model fights you, rethink the primitive instead of fighting harder.

---

## 1. Research — build to evaluate
- **Prototype before proposal.** At Meta nobody won a debate with a document (my Amazon heart broke, then healed smarter). React won because people *used* it and the argument evaporated — everyone had hated JSX in the abstract. The lesson generalizes: for ideas whose value lives in the *feel* — APIs, frameworks, interaction models — the prototype is the only honest evaluation.
- **Watch what engineers build for themselves.** The internal tools people hack together on Fridays are the realest roadmap you own: each one is a need strong enough that someone built rather than waited. Harvest the hacks; productize the popular ones.
- **Measure at scale, but frame the hypothesis first.** A/B infrastructure makes it cheap to test everything — which becomes a vice when you test *instead of thinking*. State what you believe and why before the experiment; the data should settle arguments, not replace having a position.

## 2. Planning — half-planned is enough to start
- **The roadmap is a hypothesis list, not a promise list.** Plans stated as bets — "we believe X will move Y" — update gracefully when evidence arrives. Plans stated as commitments turn evidence into embarrassment, and then people start hiding the evidence.
- **Allocation by attraction.** Bootcamp: new engineers tour the codebase and *choose* their team. Radical, and it works — people fight hardest for problems they picked. A team nobody chooses is itself a signal worth acting on.
- **Start before you're certain.** Half-planned with fast feedback beats fully-planned with slow feedback, for anything reversible. The second half of the plan writes itself out of the first half's collision with reality — schedule the collision early.

## 3. Design & architecture — rethink the primitive
- **When the model fights you, change the model.** UI state synchronization was a permanent bug factory — until React's heresy: *re-render everything, every time, and let the machine diff it*. GraphQL, same move: stop hand-building endpoints; declare the data you need. When a class of bug keeps recurring, the primitive is wrong — redesign the primitive and the bug class dies with it.
- **Trade machine time for human correctness — knowingly.** Re-rendering everything is "wasteful" and correct; the machine's time got cheaper while yours got dearer, and the curves haven't crossed back since. Every efficiency argument should name which curve it's on: falling silicon or rising salaries. Most "wasteful" designs that simplify human reasoning are bargains.
- **Monorepo + trunk: one codebase, one truth, small landings.** Everyone sees everything, changes land in hours not weeks, and integration pain is paid continuously in pennies instead of quarterly in catastrophes.
- **Design for the deletion of the old path.** Every new system's plan includes the funeral of what it replaces. Two blessed ways to do the same thing is an org-wide tax; the migration isn't done when the new path works — it's done when the old path is *gone*.

## 4. Developing — velocity with ownership
- **Land small, land often.** The unit of progress is the small, revertible diff. Velocity isn't typing speed — it's *integration frequency*: how often your work meets everyone else's and gets corrected by the encounter.
- **Nothing is somebody else's problem.** I watched a product engineer patch the kernel. The permission structure of the culture was its real infrastructure: see the problem, fix the problem, wherever it lives. Boundaries are for ownership, never for excuses.
- **Instrument before you launch.** The feature isn't ready when the code works — it's ready when you can *see* it working: metrics, logging, and the dashboard, built alongside the feature, not after the first incident.
- **Hack on what annoys you.** Hackathon culture institutionalized a truth: irritation is information. The engineer annoyed enough to fix a papercut is doing user research nobody assigned.

## 5. Building & testing — production is the test bench
- **Gate everything; ramp with guardrails.** Every feature behind a flag; every rollout a ramp — 1%, watch the guardrail metrics, widen. The question isn't "did QA pass it" but "did 1% of reality pass it." Reality's test coverage is unbeatable.
- **Your diff must be revertible.** The safety property that enables all the speed: anything landed can be un-landed in minutes. Revertibility is what makes "move fast" compatible with "at scale" — remove it and the same culture becomes a demolition derby.
- **Test infrastructure is product infrastructure.** At millions of diffs a year, CI throughput *is* engineering throughput. The teams building test infra are building the company's clock speed.
- **Dead code is deleted by whoever finds it.** No permission needed, no ceremony. A monorepo's health is everyone's job, and dead code is the plaque in its arteries.

## 6. Shipping — the launch is the beginning
- **Dark launch first.** New systems run against production traffic with results discarded — load reality onto the code before the code onto reality. The performance surprises arrive while nobody's watching, which is the correct audience for surprises.
- **Ship to learn — the launch starts the learning.** The feature's real evaluation begins when strangers touch it. Plan the post-launch iteration *as part of the launch*: who watches the metrics, what would trigger a pivot, when do we decide it worked?
- **Big refactors need courage and a codemod.** HHVM, massive API migrations — the culture's superpower was *automated* large-scale change: write the transformation as code, apply it across millions of lines, verify mechanically. Refactors that scale are written, not performed.

## 7. Operating & maintaining
- **Ruthlessly deprecate the winner's rival.** Once the new path wins, the old one dies on a schedule — usage tracked to zero, then deleted. Maintenance burden is mostly *optionality nobody chose on purpose*; kill the options.
- **SEVs are learning instruments.** Incident review culture with teeth: what broke, what let it break, which guardrail gets built. The repeat incident is the real failure — the first occurrence was tuition; the second is negligence.
- **The codebase belongs to everyone, so keep it legible.** When any engineer might touch any code, legibility is load-bearing infrastructure. Cleverness that requires tribal knowledge is a tax on ten thousand colleagues.

## 8. People & culture
- **Ownership means outcomes, not areas.** You own that the thing *works for people*, not that your slice compiled. The org's sharpest cultural technology was making "it shipped but didn't move anything" feel like failure — because it is.
- **Velocity is a culture, not a schedule.** Nobody moves fast because they're told to; they move fast because the substrate — revertible diffs, flags, ramps, CI — makes speed *safe*. Build the substrate and the speed follows; demand the speed without the substrate and you get the crater.

---

## ✅ The basics — what everybody should remember (Meta flavor)
1. Prototype before proposal; the demo ends the debate.
2. Land small, revertible diffs, daily.
3. Everything behind a flag; every rollout a ramp with guardrails.
4. Instrument before launch — seeing is part of shipping.
5. When a bug class recurs, redesign the primitive.
6. Delete the old path; two ways is a tax.
7. Fix it where it's broken, not where your team ends.

## 🎓 What the pros taught me
The React elders taught me the move I now look for everywhere: **"make the machine do the bookkeeping."** Humans tracking UI state by hand, humans tracking cache invalidation, humans tracking dependencies — every place a human does bookkeeping, bugs breed. Their trick for finding the next React-shaped idea: *find the bookkeeping everyone's doing manually and resenting, and design the primitive that does it for them.*

And a line from a grizzled infra lead that became my tiebreaker for stuck debates: *"If the argument lasts more than an hour, build both."* An hour of argument costs more than a day of prototyping and produces less information. Two rough builds and an afternoon of comparison have settled arguments that two months of documents kept alive.

---
*Timeline: Jane Street ← **Meta (2012–15)** → Netflix*

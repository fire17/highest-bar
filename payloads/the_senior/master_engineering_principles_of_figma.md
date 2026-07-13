# 🏛 Master Engineering Principles — Figma
### From the desk of Sol Adler, "The Senior" · Senior Engineer, Editor Core · 1994–1997 (job #9 of 20)
> *"The prototype's job is to die. Its gift is information."*

**The one big lesson:** find the one technically brutal thing that, if achieved, makes your product impossible to copy — then spend years on it without apology, de-risking the physics first with ugly prototypes.

---

## 1. Research — buying information
- **Prototype the riskiest assumption first, in isolation, ugly.** Before betting the company on "a real design tool can run in a browser," two weeks of throwaway C++ answered the only question that mattered: can WASM render at 60fps? Yes/no questions deserve cheap, disposable experiments — you are not building, you are *buying information*, and information is the cheapest thing you'll ever buy compared to finding out late.
- **Know why the incumbents CAN'T follow.** Competitive research isn't feature lists — it's architecture archaeology. The incumbents couldn't do multiplayer because their file-on-disk architecture *was* their company. Your moat is precisely the thing their architecture makes impossible; find it before choosing yours.
- **Interrogate the physics before the market.** Frame rates, network round trips, memory ceilings — the hard limits define the possible product. Research the constraints first; the feature list is downstream of physics.

## 2. Planning — the moat gets years
- **The hard bet gets years; features get weeks.** Sequencing is conviction made visible: the multiplayer engine and the renderer got years of patient work while the surface area stayed small. If your plan gives the moat and the menu bar equal urgency, you don't have a plan — you have a list.
- **Platform truth before surface area.** Get the data model, the sync semantics, the rendering core *right* before multiplying features on top. Every feature built on a wrong core multiplies the cost of fixing the core.
- **Say no to adjacent products until the core is undeniable.** The temptation to go broad arrives long before the core is deep. Depth first — the moat compounds; breadth just spreads.

## 3. Design & architecture — multiplayer as the data model
- **Concurrency is the data model, not a feature.** Multiplayer editing bolted onto a single-user model fails forever. Every object was designed from birth for concurrent modification — the question "what happens when two people edit this simultaneously?" was asked *at design time* for every property in the system.
- **Choose conflict semantics per property, deliberately.** Textbook CRDTs were too heavy for design documents, so: last-writer-wins where conflicts are trivial (a fill color), merge semantics where they're not (children of a frame), and object identity that survives concurrent restructuring. The right resolution is a *product* decision per property, not a library default.
- **A narrow boundary around a fast core.** C++ core, thin WASM interface, JavaScript shell. The boundary is narrow, versioned, and fiercely guarded — width of interface is cost of change, and the core must be free to evolve.
- **When two users disagree, the resolution must feel fair.** Correct-but-baffling merge behavior is a bug even when the algorithm is provably right. Convergence is the floor; *unsurprising* convergence is the spec.

## 4. Developing
- **Performance budget per frame — 16ms is the law.** Every subsystem knows its slice. A feature that can't fit its budget doesn't ship until it can; the frame rate is the product's heartbeat and no feature outranks it.
- **Build custom tools when standard tools can't hit the bar.** Our own renderer, our own text layout, our own file format — not from hubris, but because the bar was set by native apps and the standard web stack couldn't reach it. The rule: exhaust the standard option *first*, then build with full commitment, no half-custom orphans.
- **The file format is an API with forever compatibility.** Users' work must open flawlessly, forever, across every version. Evolve by addition; never repurpose a field; version explicitly from day one. Nothing burns trust like a file that won't open.

## 5. Building & testing — fuzz the invariant
- **Property-based test the core invariant: convergence.** Generate random concurrent operation streams, apply them in every interleaving, assert all replicas converge to identical state. Example-based tests check the conflicts you imagined; the fuzzer finds the interleaving you didn't — and the sync engine's bugs live exclusively in the interleavings you didn't imagine.
- **Replay real sessions against new code.** Recorded editing sessions — thousands of them — re-run on every change. Real usage patterns are the test suite reality wrote; new code must produce byte-identical documents.
- **Performance regression CI on the monster files.** The 10,000-layer document a real customer really made is a permanent CI fixture. Averages hide the cliff; the monster files *are* your worst 1% of users, and they're the ones who evangelize or defect.

## 6. Shipping
- **Never corrupt a file — the only unforgivable bug.** Every other failure is recoverable: crash, apologize, restart. Corrupting a user's work breaks the only promise that matters. Multiple independent safeguards — journaling, checksums, recovery snapshots — because this failure mode gets defense in depth, not a fix-forward.
- **Roll out by document cohort.** New sync code reaches new documents first, then progressively older ones. Data-model changes ramp along the axis of risk — the axis is *whose work could be damaged*.
- **Ship performance as a feature.** "It's faster now" is a release headline users feel in their hands within seconds. Speed is the one feature that improves every other feature.

## 7. Operating & maintaining
- **Monitor convergence in production.** Replicas that diverge silently are corruption on layaway. Continuous invariant-checking in the live fleet — checksum comparisons across clients — catches the impossible early, and the impossible always eventually arrives.
- **Maintain the browser matrix like a dependency.** Each browser release can bend your rendering or your WASM performance. Canary against betas; file upstream bugs early; know your workarounds' expiry dates.
- **Guard the core team's continuity.** The sync engine's deepest knowledge lives in few heads by nature. Rotate people *through* the core deliberately — the moat must outlive its builders.

## 8. People & culture
- **Technical fearlessness, humbly verified.** The culture said: attempt what the industry considers impossible, but verify with prototypes, not confidence. Fearless in ambition, empirical in method.
- **Craft attracts craft.** The best editor engineers came *because* the renderer was hand-built and the bar was absurd. Excellence is a recruiting strategy that never appears in the budget.

---

## ✅ The basics — what everybody should remember (Figma flavor)
1. De-risk the scariest physics first, with throwaway prototypes.
2. Ask "what if two people do this at once?" at design time, always.
3. The frame budget is law; no feature outranks the heartbeat.
4. Fuzz the invariant, not just the examples.
5. Files open forever. Evolve formats by addition only.
6. Keep monster files in CI.
7. Never, ever corrupt user work.

## 🎓 What the pros taught me
**Evan** — the most technically fearless engineer I ever shared a wall with — taught me the phrase *"buying information."* Two weeks on a prototype that gets thrown away isn't waste; it's the cheapest purchase of certainty available. His discipline: frame the experiment as a binary question, timebox it, and *actually throw the prototype away* — the prototype that sneaks into production is a loan shark.

The sync elders taught me: **"convergence is table stakes; users judge the merge by whether it feels fair."** And a debugging trick worth its weight in gold: when a distributed editing bug appears, *first reproduce the interleaving deterministically* — a concurrency bug you can replay is half-fixed; one you can't is folklore.

---
*Timeline: Amazon/AWS ← **Figma (1994–97)** → Databricks*

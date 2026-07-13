# 🏛 Master Engineering Principles — SpaceX
### From the desk of Sol Adler, "The Senior" · Senior Flight Software Engineer · 2006–2009 (job #13 of 20)
> *"The best part is no part. The deleted part has no bugs, no mass, and no latency."*

**The one big lesson:** question, delete, simplify, accelerate, automate — *in that order* — because most engineers automate first, perfecting a thing that should not exist.

---

## 1. Research — first principles and the idiot index
- **Compute the idiot index.** Part cost divided by raw material cost. A valve that costs $10,000 made of $80 of metal has an idiot index of 125 — and that ratio is your research agenda: *why* is it expensive, and which of those reasons are physics versus habit? Apply it to software too: cycle time versus theoretical minimum, infra bill versus bytes actually moved. Big index, big opportunity.
- **Interrogate requirements by name.** Every requirement must come with a person attached — not a department, a *person* — so you can go argue with them. "The requirement says" is the beginning of the conversation, never the end. Half the requirements on any spec are fossilized assumptions whose author would happily retract them if asked. Ask.
- **Reason from physics, not from precedent.** "It's always been done this way" is the industry's most expensive sentence. Start from what the laws of nature permit and cost upward from there; precedent is just someone else's constraint set, inherited unexamined.

## 2. Planning — the algorithm, in order
- **The five steps, in order, enforced like law.** (1) Question the requirement. (2) Delete the part or process. (3) Simplify what survives. (4) Accelerate the cycle. (5) Automate. Run them out of order and you get the classic failure: a beautifully automated process that shouldn't exist, running fast, producing waste.
- **Retire the scariest unknown first.** Risk burn-down ordering: the thing most likely to kill the project gets attacked in week one, not deferred to phase three. If the landing algorithm can't work, learn it *before* building the factory.
- **A launch date is a design tool.** Schedule pressure, used honestly, forces the question "what is actually necessary?" — and the answers improve the design. The date doesn't compromise the work; it *concentrates* it.
- **If you're not adding things back in, you're not deleting enough.** The deletion target is deliberately past the comfort point: expect to restore ~10% of what you cut. If everything you deleted stayed deleted, you were timid.

## 3. Design & architecture — margin and deliberate tolerance
- **Delete the part.** Before optimizing any component, prove it should exist. Every part is a future failure mode, a mass line-item, an integration surface, and a maintenance obligation. The redundancy-management subsystem I'm proudest of is the one I removed — by making the primary path simple enough to trust.
- **Explicit margin budgets: mass, compute, timing, power.** Every subsystem knows its allocation and its current spend, tracked like money. Margin is not slack — it's the currency you'll desperately want when reality invoices you late in integration.
- **Fault tolerance is chosen consciously, per system — never blanket.** Redundancy adds its own failure modes: voting logic, divergence, the failover that fails. Sometimes the right answer is two of them; sometimes it's one of them, made simple enough to trust. The decision is engineering, not policy.
- **Design the abort paths with the same care as the happy path.** The abort sequence is flight software's most important code and the least-exercised. Every state must have an answer to "and if it fails *here*?" — designed, reviewed, and simulated, not implied.

## 4. Developing
- **Flight software lives in a constrained, reviewable subset.** Bounded loops, static allocation, no surprises at runtime. The language's cleverest features are for programs that can be restarted; this program gets one try at 8 km/s. Constraints aren't a straightjacket — they're what makes total review *possible*.
- **Determinism and timing are correctness.** The right answer late is the wrong answer. Timing budgets per control loop, enforced and measured; jitter is a bug with the same severity as a wrong sign.
- **Simulate everything, then trust only hardware-in-the-loop.** Pure simulation validates the logic; hardware-in-the-loop validates the *world* — sensor noise, bus timing, the actuator's real personality. Both, always, in that order.

## 5. Building & testing — test like you fly
- **Test like you fly, fly what you tested.** Same hardware, same timing, same sensor noise, same software image that flies. Any difference between test and flight configuration is a measurement of your hopes, not your system. This is the deepest testing principle I ever learned, and it transfers to every domain: *any environment that differs from production is testing a different system.*
- **Hardware-rich iteration: build more articles, break them earlier.** More test articles, tested harder, earlier, beats fewer articles polished longer. A prototype destroyed on the stand in March is cheaper than a theory disproven in flight in December — blow things up on purpose while it's still cheap information.
- **No anomaly goes unexplained. None.** "Could not reproduce" does not exist for flight systems. Every anomaly gets a root cause or the fleet doesn't fly. The anomaly you shrugged at in testing is the one that writes the accident report.
- **The test that can't fail teaches nothing.** If a test has never failed and can't plausibly fail, it's not a test — it's a ritual. Design tests around the edges where failure is genuinely possible; that's where the information lives.

## 6. Shipping — launch readiness
- **Go/no-go criteria written before emotion runs high.** Launch readiness reviews work because the criteria were agreed when everyone was calm. On the day, you don't debate the threshold — you read the number and it decides. Pre-committed criteria are how organizations stay rational under adrenaline.
- **Every flight instruments the next design.** The vehicle is a sensor platform for its successor. Telemetry channels are chosen not just to operate *this* flight but to answer next year's design questions — ship the questions along with the payload.
- **Launch is a team verb.** The polling of stations — propulsion go, avionics go, range go — is not theater. It's a mechanism ensuring one human being with the full picture has explicitly accepted each subsystem's state. Software launches deserve the same explicit poll, and almost never get it.

## 7. Operating & maintaining — fleet learning
- **Telemetry from every flight feeds the fleet.** One booster's anomaly updates every booster's envelope. Operate systems as a *fleet* with shared learning, not as individuals with private histories — the fix propagates before the second occurrence.
- **The paperwork is part of the vehicle.** Traceability — which parts, which software image, which test results, which waivers — is not bureaucracy; it's what makes the difference between "we think it's fine" and "we know its history." When something fails, the paper trail is the debugger.
- **Refurbish with suspicion.** Reuse means inspection regimes that assume damage until proven otherwise. Trust in a returning system is re-earned each cycle, by evidence.

## 8. People & culture
- **The rocket doesn't care about your org chart.** Physics is the only stakeholder that can't be negotiated with. Cross-discipline problems get solved by whoever understands them, immediately, across whatever boundary — the alternative is explained politely in the accident report.
- **Intensity with honesty.** The pace was ferocious, but the culture's real fuel was that *bad news traveled fast and upward*. An organization where bad news travels slowly is an organization that schedules its own disasters.

---

## ✅ The basics — what everybody should remember (SpaceX flavor)
1. Question, delete, simplify, accelerate, automate — in that order.
2. Every requirement has a name attached. Argue with the name.
3. Compute the idiot index before optimizing anything.
4. Test like you fly; any difference measures your hopes.
5. No unexplained anomalies. Ever.
6. Write go/no-go criteria while you're calm.
7. If you never add anything back, you didn't delete enough.

## 🎓 What the pros taught me
The avionics greybeard — twenty years of aerospace scars — stood next to me while the first booster came down, both of us crying, and said: *"It's just control theory."* The lesson under the joke: the miraculous is made of the mundane, executed without compromise. Every impossible thing we did decomposed into boring disciplines — margins, tests, telemetry, reviews — done completely, in the right order, with no steps skipped. There is no magic step. That *is* the magic.

He also gave me the review question I've asked at every design table since: *"What did you delete this week?"* — asked with the same weight as "what did you build?" A design review that only adds is a design review failing at half its job.

---
*Timeline: Nvidia ← **SpaceX (2006–09)** → Jane Street*

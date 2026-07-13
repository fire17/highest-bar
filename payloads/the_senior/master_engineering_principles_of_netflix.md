# 🏛 Master Engineering Principles — Netflix
### From the desk of Sol Adler, "The Senior" · Senior Platform Engineer · 2015–2018 (job #16 of 20)
> *"If it hurts, do it more often until it stops hurting."*

**The one big lesson:** stop hoping — assume everything fails, design the failure's container before the feature's happy path, and verify your resilience the only honest way: by breaking things in production, on purpose, during business hours.

---

## 1. Research — the scientific method, pointed inward
- **Chaos experiments are research.** Hypothesis ("we survive losing an instance"), method (kill one, in production, during business hours), evidence (did members notice?). Resilience claims without experiments are folklore with a diagram. The monkey isn't destruction — it's *epistemology*.
- **Study your dependency graph like an epidemiologist.** What spreads? Which service's failure infects which? Map the contagion paths before the outbreak: the graph of who-calls-whom, annotated with what-happens-when, is the most valuable document in a microservices org — and usually the most out-of-date.
- **Ask "what does the member feel?" first.** Every investigation starts from the member-visible symptom and works backward. Systems research that never touches the human experience optimizes the map instead of the territory.

## 2. Planning — plan the failure modes, not just the features
- **Every design lists its failure containment.** Not "how it works" — "how it fails, and what contains the failure." A design review that only discusses the happy path has reviewed half a design, and reality always reads the other half first.
- **Plan for regional evacuation.** Can you lose an entire region and route members elsewhere in minutes? That capability — rehearsed, not theoretical — reframes every lesser failure into a non-event. Plan the biggest failure first and the small ones inherit the answer.
- **Capacity plans include the failure surge.** When a region dies, the survivors absorb its load *while* everything else is going wrong. Headroom sized for the average day is headroom that vanishes exactly when needed.

## 3. Design & architecture — bulkheads and degradation ladders
- **Every remote call gets a timeout, a fallback, and a circuit breaker. No exceptions.** The unprotected remote call is the arsonist of distributed systems: one slow dependency, threads pile up, and a latency blip becomes a cascade. Wrap every call, time-box it, give it a fallback, and when the dependency drowns — cut it loose before it pulls you under.
- **Design the degradation ladder.** What's the humble version of this page? Personalized rows → popular titles → cached anything → a page that still plays video. Every experience should have designed fallback rungs, because the alternative to graceful degradation isn't full service — it's a blank screen.
- **Bulkheads: partition so failure can't travel.** Isolate thread pools, connection pools, and resources per dependency, like watertight ship compartments. The goal isn't preventing the flood; it's ensuring one flooded compartment never sinks the vessel.
- **Stateless where possible — instances are cattle.** Any instance can die anytime without ceremony (the monkey guarantees practice). State lives in systems designed for state; compute stays disposable. Disposability is what makes both chaos and deployment boring.

## 4. Developing — freedom and responsibility
- **Senior engineers choose — and own the outcome.** No architecture police, no mandatory frameworks. Context, not control: leadership supplies the goals and constraints; engineers make the local decisions, and carry them. Freedom without responsibility is chaos; responsibility without freedom is theater; the pairing is the engine.
- **The paved road is the easy path, not the mandatory one.** Blessed tooling so smooth that going off-road is your right but rarely your preference. Off-road means you're on your own — a price list, not a prohibition. Adoption by attraction produces consistency that mandates never achieve, because the paved road team has to *keep earning* its users.
- **Build fallbacks as real features.** The fallback path gets designed, coded, and reviewed like the primary path — because in production, they trade places without an appointment.

## 5. Building & testing — verify in production, on purpose
- **Chaos in production, during business hours.** Kill instances (Chaos Monkey), degrade dependencies, fail zones — while the team is at their desks, watching. If your resilience only holds in staging, you have staging resilience. Business hours, because you break things when the responders are fresh, not when the pager finds them asleep.
- **Untested fallbacks are fiction.** The fallback that's never fired in anger fires wrong the first time it matters — wrong config, expired cache, dead code path. Exercise the fallbacks on schedule; a degradation ladder with unclimbed rungs is a drawing of a ladder.
- **Squeeze tests: find the real limit.** Push one service's traffic up until it breaks — deliberately, in production, watched. Now capacity planning uses the *measured* ceiling, not the guessed one. Every service should know its actual breaking point the way a bridge knows its load rating.
- **Automated canary analysis.** New build takes a traffic slice; the platform statistically compares its golden signals against the baseline and issues a verdict — not a human squinting at two dashboards at deploy o'clock. Judgment automated is judgment that happens every time.

## 6. Shipping
- **Red/black deploys with instant rollback.** The new fleet comes up beside the old; traffic flips; the old fleet stays warm until the new one proves out. Rollback is a route change, seconds not rebuilds — and *that* is what makes continuous deployment calm instead of brave.
- **Regional waves.** One region, watch, then the world. Geography as blast-radius control — the last region gets code that three regions have already voted on with their error rates.

## 7. Operating & maintaining
- **Alert on member pain, not machine mood.** Page on streams-starting-per-second dropping, not on CPU. Machines have moods; members have experiences. Cause-based alerts breed noise and noise breeds sleep, and sleep through the real one is how five-minute problems become five-hour ones.
- **Availability is a product feature with a target — and drills.** Evacuation drills, failover exercises, chaos days: the muscle that isn't exercised atrophies precisely between the incidents that need it.
- **Delete the service nobody defends.** Periodically ask of every service: who owns it, who would care if it vanished? The undefended service is risk wearing a nametag from three reorgs ago. Decommissioning is maintenance — celebrate it like shipping.
- **Blameless postmortems ask what the system permitted.** Not "who erred" but "how did the system let one error become an outage?" The human is the trigger, never the cause; the cause is whatever amplified the trigger, and that's what gets fixed.

## 8. People & culture
- **Context, not control.** Leadership's job is transmitting *why* — the goals, constraints, and stakes — so a thousand local decisions come out coherent without anyone approving them centrally. Every approval gate is a confession of failed context.
- **Hire people you don't need to manage.** The whole system — freedom, paved roads, chaos, on-call — presumes senior, self-directed owners. Density of judgment is the real architecture; everything else is scaffolding around it.

---

## ✅ The basics — what everybody should remember (Netflix flavor)
1. Timeout, fallback, breaker — on every remote call, no exceptions.
2. If you haven't tested the failure, you don't have the resilience.
3. Fallbacks are features; exercise them on schedule.
4. Alert on what users feel, never on machine moods.
5. Design the degradation ladder before you need a rung.
6. Instances are cattle; state lives where state belongs.
7. If it hurts, do it more often until it stops hurting.

## 🎓 What the pros taught me
The Simian Army crew handed me their whole philosophy in one sentence: *"If it hurts, do it more often until it stops hurting."* Deploys hurt? Deploy daily until they're boring. Failovers hurt? Fail over monthly. Region evacuation terrifying? Evacuate on schedule. Pain is a signal of missing automation and missing practice — and avoidance, which feels prudent, is just scheduling the pain for the worst possible day with compound interest.

The resilience elders also gave me the interview question I've used ever since: *"Tell me about a system you made boring."* The engineers who light up at that question — who take pride in the incident that *didn't* happen, the deploy nobody noticed, the failover that was a non-event — those are the ones who build systems that let everyone sleep. Excitement is for the product; the infrastructure should be magnificently dull.

---
*Timeline: Meta ← **Netflix (2015–18)** → Stripe*

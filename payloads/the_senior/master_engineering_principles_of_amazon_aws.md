# 🏛 Master Engineering Principles — Amazon / AWS
### From the desk of Sol Adler, "The Senior" · Principal Engineer · 1991–1994 (job #8 of 20)
> *"Good intentions don't work. Mechanisms do."*

**The one big lesson:** clear writing is clear thinking, everything is an API, and operational excellence is a set of *mechanisms* — never a set of hopes.

---

## 1. Research — working backwards
- **Write the press release and FAQ before anything else.** Sounds like marketing; it's the most brutal design review ever invented, because a press release cannot hide a bad idea behind architecture. If the imagined customer quote is unconvincing, stop now — you just saved a year.
- **The customer's problem, in the customer's words, is the spec.** Not your abstraction of it. Working backwards means the origin of every project is a real person's real Tuesday, quoted.
- **The FAQ is where the hard questions live.** Force yourself to write the hostile questions — "why would anyone trust this with production data?" — and answer them *before* building. The questions you avoid writing are the ones that kill the product later.

## 2. Planning — narratives and doors
- **Six-page narratives, read silently, then interrogated.** No slides — prose. Slides hide broken thinking in bullet gaps; a narrative exposes every logical joint. Twenty minutes of silent reading means everyone critiques the same complete argument, not the first interruption.
- **Classify every decision: one-way or two-way door.** Two-way doors (reversible) should be decided fast, by the people closest, with 70% of the information. One-way doors (irreversible) get the slow, senior, paranoid treatment. Most organizational slowness is treating two-way doors like one-way doors; most disasters are the reverse.
- **Disagree and commit — and record it.** Debate hard, decide once, then everyone rows. The recorded disagreement isn't bureaucracy: when reality votes later, you want to know who saw it coming and why.
- **Two-pizza ownership.** Teams small enough to feed with two pizzas, owning something whole — roadmap, code, pager. Coordination is the tax; ownership is the rebate.

## 3. Design & architecture — everything is an API
- **Hardened interfaces, no back doors, as if every service might be sold to the public.** That mandate — design internal services like external products — is literally how AWS was born. The org chart became an architecture on purpose. Design every internal boundary as if strangers will one day pay to cross it.
- **Durability is arithmetic; availability is architecture.** Eleven nines isn't a slogan — it's an equation over failure domains, replication factors, and repair rates that you *compute*. If you can't show the math, you don't have the nines; you have the hope.
- **Protect yourself from your friends.** Throttling and admission control at every boundary — your biggest availability threat isn't attackers, it's a sibling service with a retry loop and good intentions. Every API declares its limits, enforces them, and publishes them.
- **Design for the failure of everything you depend on.** Every dependency in the design doc gets a row: what happens when it's slow, wrong, or gone? "It won't be" is not an accepted answer — S3 was built by people who assumed entire datacenters vanish, because they do.

## 4. Developing
- **You build it, you run it.** The pager teaches design faster than any review. Engineers who operate their own service stop writing unoperable services within two pages.
- **Idempotency tokens on every mutating API.** The caller *will* retry; the network *will* duplicate. Design mutation so that "did it work?" has a safe answer: try again with the same token.
- **Security review is a gate, not a suggestion.** Threat model written by the team, reviewed by specialists, before launch. At scale you are always under attack; the only question is whether you designed for the fact.

## 5. Building & testing
- **GameDays: scheduled disasters, practiced calmly.** Pick a failure — region loss, dependency brownout, bad deploy — and run it as a war game against production-like systems with the real on-call. You discover the runbook gaps on a Tuesday afternoon instead of a Sunday 3am.
- **Test at your limits — literally.** Every service has published limits; test *at* them, past them, and verify the failure is the designed one (clean throttle, clear error) and not the surprise one (cascade, corruption).
- **The Operational Readiness Review is the pre-launch mechanism.** A checklist with teeth: runbook exists, rollback rehearsed, alarms wired, dashboards built, limits declared, on-call trained. No ORR, no launch. Mechanisms, not intentions.

## 6. Shipping
- **Launch dark, ramp weighted.** New code takes traffic in small weighted slices behind the same interface; the metrics argue, the weights shift. Launch is a dial, not a switch.
- **Rehearse the rollback, don't just write it.** An untested rollback plan is a wish. Before launch, actually roll back once — the rehearsal always finds the missed dependency, and finding it costs an hour instead of an outage.
- **Every launch names its metrics in advance.** What will we watch, what thresholds mean stop, who decides? Decided *before* launch, when heads are cool — never during, when they aren't.

## 7. Operating & maintaining
- **The weekly ops review reads the dashboards line by line.** Senior people, every week, walking the graphs — anomalies interrogated, action items tracked to closure. Boring, relentless, and the single most effective reliability mechanism I saw in sixty years.
- **Correction of Error documents with five whys.** Every significant incident produces a written COE: what happened, the five-whys causal chain, and *mechanism-grade* action items — "add an alarm" and "change the process," never "be more careful." Carefulness is not a mechanism.
- **Capacity and cost are engineering, reviewed like features.** Growth is forecast, headroom is measured, and cost per unit of work is a graph someone owns. Tag everything for cost attribution — untagged spend is unowned spend, and unowned spend only grows.

## 8. People & culture
- **Mechanisms over intentions, always.** A value you care about gets a forcing function: a review, a checklist, a gate, a metric with an owner. Culture is what your mechanisms make unavoidable.
- **Bar raisers.** Someone outside the hiring team, with veto power, guards the long-term bar against the short-term need. Every quality bar needs a guardian whose incentives aren't this quarter's.

---

## ✅ The basics — what everybody should remember (Amazon flavor)
1. Write the press release first. If it's boring, don't build it.
2. Narratives, not slides, for anything that matters.
3. Sort your decisions: two-way doors fast, one-way doors slow.
4. Idempotency tokens on every mutation.
5. Know your limits — declared, enforced, tested at.
6. Rehearse the rollback before you need it.
7. Action items are mechanisms, never "be more careful."

## 🎓 What the pros taught me
The Principal Engineers' community handed me the distinction I've used ever since: **"durability is arithmetic, availability is architecture."** The first you compute with failure-domain math; the second you earn with design. Confusing them — hoping for durability, calculating availability — is how systems lie to their owners.

And the Bezos line that reorganized my management thinking permanently: **"Good intentions don't work. Mechanisms do."** Every time I've cared about something since — quality, security, cost, kindness in code review — I've stopped asking people to care harder and started building the mechanism that makes caring automatic. It has never once failed me.

---
*Timeline: Apple ← **Amazon/AWS (1991–94)** → Figma*

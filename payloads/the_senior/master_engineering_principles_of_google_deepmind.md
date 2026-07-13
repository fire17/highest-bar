# 🏛 Master Engineering Principles — Google / DeepMind
### From the desk of Sol Adler, "The Senior" · Distinguished Engineer · 2024–2027 (job #19 of 20)
> *"Hope is not a strategy. Toil is a bug. The ablation table is the paper."*

**The one big lesson:** at sufficient scale everything improbable happens hourly — so quantify the uncertainty you cannot remove, convert the velocity-vs-reliability war into arithmetic with error budgets, and treat any manual task done twice as a defect in the organization.

---

## 1. Research — moonshots made of chores
- **Ablate everything.** AlphaFold looked like a miracle; up close it was a grind of ablations — remove each component, measure the damage, keep only what earns its place. The ablation table is the paper: it's the difference between "our system works" and *knowing why* it works, and only the second survives contact with the next problem.
- **Measure the uncertainty you can't remove.** Spanner's TrueTime enchanted me: don't pretend distributed clocks agree — *measure their disagreement* and design around the bounded interval. The general principle is among the deepest I ever learned: when an uncertainty is irreducible, stop denying it, quantify it, and make the design carry the bound explicitly.
- **Research infrastructure is research leverage.** Borg begat everything; shared clusters, shared pipelines, shared experiment tooling meant a researcher's idea reached planet-scale compute in a day. The lab that builds its own leverage runs experiments while the other labs write procurement emails.
- **Pair the wildest ambition with the most pedestrian discipline.** Protein folding fell to a team that also kept immaculate experiment logs. Moonshots are made of chores; the ambition sets the direction, and the bookkeeping does the walking.

## 2. Planning — alternatives considered, budgets negotiated
- **Design docs with an "alternatives considered" section — the valuable part.** Any competent engineer can present their chosen design; the review-worthy material is what they *rejected* and why. The rejected options expose the author's actual understanding of the trade-off space — and spare the next engineer from re-walking the dead ends.
- **Negotiate the error budget up front.** Reliability is not "as much as possible" — it's a number, agreed between product and SRE in advance. Under budget: ship faster, take risks. Over budget: feature freeze, harden. The eternal war between velocity and stability, converted into arithmetic — the single greatest piece of organizational engineering I encountered in sixty years.
- **Capacity planning is engineering, not clairvoyance.** Growth modeled, headroom measured, provisioning lead times respected — with the failure surge included. At planet scale, running out of capacity is a self-inflicted outage with a six-month fuse you lit yourself.

## 3. Design & architecture — design for the improbable
- **At scale, the improbable is hourly.** Cosmic-ray bit flips, clock skew, simultaneous disk failures, the network partition that "can't happen" — at enough machines, every one-in-a-billion event is a Tuesday. Design as if the improbable is routine, because at your scale, arithmetically, it is.
- **Cells and failure domains: partition the blast, always.** Systems built as independent cells — each a complete vertical slice serving a fraction of users — so no single failure, deploy, or corruption reaches everyone. The question "what's our cell size?" is the planet-scale version of "what's our blast radius?", asked at design time.
- **The codebase is one organism — keep its immune system strong.** One repository, readability review, enforced style: any engineer can read, and safely modify, any code. At a hundred thousand engineers, *legibility is infrastructure* — the readability certification isn't gatekeeping, it's the organism maintaining the ability to heal itself anywhere.
- **Storage and compute separate; state is sacred, workers are not.** The architectural constant beneath Bigtable, Spanner, Borg: durable state lives in systems purpose-built for durability, and computation is a fungible commodity scheduled wherever there's room. Never let precious state hide inside disposable compute.

## 4. Developing — toil is a bug
- **Anything a human does twice, manually, is an automation ticket.** Toil — manual, repetitive, automatable operational work — is treated as a defect in the system, with an explicit ceiling on how much of it any team may carry. Toil compounds silently until brilliant engineers are full-time machine-tenders; the ceiling is what stops the compounding.
- **Code review is teaching, at civilizational scale.** Every change reviewed not just for correctness but for *readability* — will a stranger understand this in five years? The review standard is the mechanism by which a hundred thousand engineers converge on one dialect; it's the largest teaching institution ever accidentally built.
- **Hermetic builds: reproducible by construction.** The build depends only on declared inputs — no ambient state, no "works on my machine," no unpinned anything. Bazel's discipline: if the inputs are identical, the output is bit-identical. Reproducibility isn't a debugging aid; it's the foundation that makes caching, verification, and trust possible at scale.
- **Large-scale changes are tooling problems.** Migrating ten thousand call sites is not a heroic quarter — it's a tool that rewrites, tests, and submits in batches with automated verification. Build the change as code, and the migration becomes an operation instead of an era.

## 5. Building & testing
- **The test pyramid, enforced.** Masses of fast hermetic unit tests, fewer integration tests, a thin crown of end-to-end — because inverted pyramids (all end-to-end, all flaky) collapse under their own runtime, and flaky tests are worse than no tests: they teach engineers to ignore red.
- **Flakiness is tracked and hunted.** A test that fails randomly gets quarantined, measured, and fixed with the same seriousness as a product bug — the moment "just rerun it" becomes culture, the entire signal of CI is dead.
- **Canary everything; let statistics judge.** Every rollout passes through canary populations with automated statistical comparison against baseline. At scale, a human cannot eyeball the difference between noise and regression — the judgment must be computed, and the rollback must be triggered by the computation.
- **DiRT: disaster recovery testing at civilizational scale.** Scheduled exercises that break real things — datacenters, dependencies, *people* (the on-call lead is "unreachable" today) — to verify the organization, not just the software, survives. The people-processes are part of the system; test them like it.

## 6. Shipping — progressive, gated, reversible
- **Progressive rollouts across cells, gated by SLOs.** New code advances cell by cell, each promotion contingent on the previous cell's golden signals holding. The rollout is a formal state machine with automated gates — not a courageous afternoon.
- **Error budget gates the launch cadence.** Over budget? Launches pause, hardening begins — automatically, by prior agreement, without a meeting or a fight. The mechanism absorbs the conflict so the humans don't have to re-litigate it under pressure.
- **Every config change is a rollout.** The biggest outages at scale are config-shaped, not code-shaped: a flag flipped globally, a quota changed everywhere at once. Configuration travels the same canary → progressive → auto-rollback pipeline as binaries. No exceptions — *especially* not for "trivial" changes, which is what every catastrophic config change was called in advance.

## 7. Operating & maintaining — SRE as a discipline
- **SLIs before dashboards; SLOs before alerts.** First define what "working" means, measurably, from the user's side — then alert on *burn rate* against the objective. Alerting on SLO burn instead of machine symptoms is what separates pages that matter from pages that train people to ignore pages.
- **Postmortems with action items tracked to closure.** Blameless, written, reviewed — and the action items live in a tracked queue with owners and deadlines, audited until done. A postmortem whose action items evaporate is a ritual, not a mechanism; the tracking is the difference.
- **Every system documents its data-loss story.** What is the recovery point, the recovery time, the restore procedure — and when was the restore last *actually tested*? A backup that has never been restored is a hypothesis. At scale, the untested restore is the second disaster, scheduled during the first.
- **Deprecate with migration tooling, or you haven't deprecated.** Turning down a service that thousands of internal teams use means shipping the automated migration path — the org-scale version of "never break userspace." An announcement without tooling is a wish with a deadline.

## 8. People & culture
- **Blameless is an epistemology, not a courtesy.** The instant blame enters, information exits — people optimize their testimony instead of the system. Blamelessness isn't kindness (though it is kind); it's the only configuration in which the truth arrives fast and undamaged, and truth-arrival-speed is the metric that governs how good your reliability can ever get.
- **20% curiosity pays for itself.** Slack for exploration — some fraction of it becomes Gmail, some becomes nothing, all of it becomes engineers who stay curious. An organization at full utilization is an organization with no capacity to notice its next decade.

---

## ✅ The basics — what everybody should remember (Google flavor)
1. Define the SLI before building the dashboard; alert on burn rate.
2. Everything improbable happens hourly at scale — design for it.
3. Toil done twice is an automation ticket.
4. Hermetic builds; reproducible or it isn't real.
5. Canary everything; let statistics pull the trigger.
6. Config changes are rollouts. Especially the "trivial" ones.
7. A backup that's never been restored is a hypothesis.

## 🎓 What the pros taught me
The SRE elders handed me their three-word epistemology on my first week: *"Hope is not a strategy."* Every reliability practice they'd built — budgets, canaries, drills, blameless truth-telling — was downstream of refusing to let *hope* occupy any load-bearing position in the system. Audit your own architecture for load-bearing hope; you will find some, and each one is an outage with a date you haven't learned yet.

And from a DeepMind researcher, reviewing what I thought was a finished result: *"Where's the ablation table? Until I know which parts matter, you haven't finished the work — you've just stopped."* The distinction between *it works* and *we know why it works* is the entire difference between science and luck — and between architecture and coincidence. I now ask for the ablation table in engineering designs too: which components earn their place, and how do you know?

---
*Timeline: Anthropic ← **Google/DeepMind (2024–27)** → OpenAI*

# 🏛 Master Engineering Principles — Uber
### From the desk of Sol Adler, "The Senior" · Senior Staff Engineer, Infrastructure · 1982–1985 (job #5 of 20)
> *"Separate what must happen from which process happens to be running it."*

**The one big lesson:** at hypergrowth, processes die mid-sentence constantly — so build systems where "the process died" is not an error case but a Tuesday, absorbed by design.

---

## 1. Research — how Uber learned things
- **Shadow real traffic to learn real distributions.** Synthetic load tests exercise your imagination; recorded production traffic exercises your system. The real world's skew — one hot city, one whale customer, one pathological route — is the thing that kills you, and it cannot be invented.
- **Choose your index for your query, not your data.** H3's hexagons exist because "find drivers near this rider, fast, at every zoom level" is the *query* — and the elegant lat/long grid answers it badly. Study the questions you'll ask before choosing the shape you'll store.
- **Mine your incidents for research topics.** Every quarter, cluster the postmortems. The subsystem that appears three times isn't unlucky — it's underdesigned, and it just published your research agenda.

## 2. Planning — hypergrowth arithmetic
- **Plan for 10x, build for 3x.** Architect so the 10x path exists on paper; build only the 3x version. Building 10x now wastes the present; having no 10x path forfeits the future. The plan is the cheap part — always buy it.
- **Walk the death scenario in design review.** For every design: "the process dies at *this* line — what happens?" Then again for the next line. If any answer is "we don't know" or "data is lost," the review isn't over.
- **Queues between everything that grows at different speeds.** Demand spikes in minutes; capacity grows in weeks. Queues are the shock absorbers — plan their depth, their overflow policy, and their alarms as part of the system, not as an afterthought.

## 3. Design & architecture — durable execution
- **Persist the state machine, not the process.** A workflow is *what must happen* — recorded durably, step by step. Workers are interchangeable muscle that can die anytime. Once you split these, crashes, deploys, and week-long waits all become the same non-event.
- **Every side effect is an activity with an idempotency key.** The workflow layer decides *what* to do; activities *do* it, exactly-once-in-effect via keys, because the call will be retried and the retry must be harmless.
- **Workflow code must be deterministic.** No wall clocks, no randomness, no direct I/O in the orchestration layer — time and randomness come in as recorded inputs. Determinism is what makes replay possible, and replay is what makes durability real.
- **Cardinality is a budget.** Metrics are free until a label carries a million values, and then observability costs more than the service it observes. Design metric dimensions like you design schemas — deliberately, with ceilings.

## 4. Developing
- **Retries with exponential backoff and jitter, everywhere.** Retries without backoff are a self-inflicted DDoS; backoff without jitter is a synchronized stampede. Three lines of code, learned in three outages.
- **Every RPC carries a deadline, and deadlines propagate.** A request with no deadline is a lease on your threads forever. The caller's remaining budget flows down the call chain, so the whole tree gives up together instead of leaking work into the void.
- **Build for replay-debugging.** When a workflow misbehaves, you replay its recorded history locally and step through the exact decisions. Design every stateful system so yesterday's bug can be re-run at a desk today.

## 5. Building & testing
- **Replay production histories as regression tests.** Real recorded workflows, re-executed against new code — did any of ten thousand historical executions decide differently? That's a test suite reality wrote for you.
- **Load test with recorded traffic shapes, including the spikes.** New Year's Eve is the spec. A system sized for the average is a system designed to fail on exactly the day everyone is watching.
- **Chaos-test the queues.** Fill them, stall the consumers, kill the brokers. Queue behavior at depth — backpressure, shedding, alarms — is architecture; verify it before production does.

## 6. Shipping
- **Roll out region by region, city by city.** Geography is a natural blast-radius limiter and a natural experiment: one city runs the new dispatch logic, its metrics argue with the control cities, and the data decides.
- **Feature flags scoped to geography and cohort.** Turning a feature on in Helsinki while Bogotá runs the old path isn't a hack — it's the deployment model. Build the scoping into the flag system from day one.

## 7. Operating & maintaining — observability as a product
- **Trace-first debugging.** One request's whole journey — every hop, every latency — beats a thousand aggregate charts. Distributed tracing is not a luxury; above ten services it is the only way anyone understands anything.
- **Alert on symptoms users feel, not causes you suspect.** Page on "trip requests failing," not "CPU high." Causes are legion and often harmless; symptoms are few and always true. Every alert must be actionable, or it trains the on-call to ignore alerts.
- **Runbooks linked from the alert itself.** At 2am, the runbook must be one click from the page. A runbook filed elsewhere is a runbook that doesn't exist.
- **Every queue has a depth alarm.** Queue depth is the earliest honest signal of almost every failure mode downstream. It's the cheapest prophecy in distributed systems.

## 8. People & culture
- **Ship ownership with the service.** Whoever builds it carries the pager for it — hypergrowth doesn't leave time for handoff fictions.
- **Write the postmortem for the next new hire.** Assume the reader joined after the incident. Context, not shorthand — the postmortem corpus becomes the org's real architecture documentation.

---

## ✅ The basics — what everybody should remember (Uber flavor)
1. Every retry idempotent; every retry backed off and jittered.
2. Every RPC has a deadline; deadlines propagate.
3. Every queue has a depth alarm.
4. Workflow logic deterministic; side effects in keyed activities.
5. Alert on symptoms; link the runbook in the page.
6. Clocks lie. Never trust two machines to agree on time.
7. Load test with the spike, not the average.

## 🎓 What the pros taught me
**Maxim and Samar** — the durable-execution pair — rewired me with one design question: *"Where does this state live when nothing is running?"* If the answer is "in a process's memory," the design is a mayfly. Their discipline: write the workflow as if the machine executing it will be unplugged mid-line — because it will be.

The observability crew taught me **"the 2am dashboard rule"**: every service gets one dashboard readable by a stranger under adrenaline — four golden signals on top, no scrolling for the truth. And the line I've repeated for four decades: *"An alert that isn't actionable is a lullaby — it exists to teach people to sleep through alerts."*

---
*Timeline: Airbnb ← **Uber (1982–85)** → Microsoft*

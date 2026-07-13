# 🏛 Master Engineering Principles — Cloudflare
### From the desk of Sol Adler, "The Senior" · Systems Engineer, Edge Platform · 1976–1979 (job #3 of 20)
> *"Before you ask 'does it work,' ask 'when it breaks, how much of the world breaks with it?'"*

**The one big lesson:** blast radius is a design input, and trust is built by explaining your failures in public better than your competitors explain their successes.

---

## 1. Research — how Cloudflare learned things
- **Measure the internet itself.** Running 1.1.1.1 and a global edge means the network is your instrument. Build the telescope into the product: real latency maps, real attack traffic, real protocol adoption curves — research from your own vantage point nobody else has.
- **Read RFCs like contracts, implement like a skeptic.** The spec says what peers *should* do. The internet shows you what they *actually* do. Every protocol implementation needs a strictness dial, because you will interoperate with twenty years of creative misreadings.
- **Study the tail, not the average.** p50 is marketing; p999 is engineering. At edge scale, one-in-a-thousand happens thousands of times a second — the tail *is* the workload.

## 2. Planning — blast radius first
- **Every design doc has a mandatory blast-radius section.** What is the maximum damage this system can do when it misbehaves? Which customers, which cities, which percentage of traffic? If the author can't answer, the design isn't done.
- **Assume adversarial input, always.** The edge is hostile by definition. Every request is potentially an attack; every parser is a security boundary. Plan capacity for the worst day, not the average day — the worst day is why customers pay you.
- **Fail open or fail closed — decide explicitly, per system.** Security systems fail closed; availability systems fail open. The catastrophic bugs live in systems where nobody made this decision on purpose.

## 3. Design & architecture — small units, contained failures
- **Choose the smallest viable unit of tenancy.** Isolates over containers over VMs: the smaller the unit, the cheaper the multi-tenancy, the faster the cold start, the tighter the blast containment. Unit size is the deepest architectural lever you have.
- **Config changes ARE deploys.** The outages that got us weren't code — they were configuration pushed globally in seconds. Config gets the full treatment: review, staged rollout, canary, auto-rollback. A regex pushed to 300 cities is a release, whatever your tooling calls it.
- **Budget resources for rules engines.** Any system that executes customer-supplied or operator-supplied rules (WAF patterns, workers, filters) gets hard CPU and memory ceilings *per rule*. One pathological pattern must never eat the machine. We learned this the way everyone learns it — publicly.
- **Rate-limit everything, including yourself.** Your own internal services can DDoS each other with perfect sincerity. Every consumer has a budget; every producer defends itself.

## 4. Developing
- **Memory-safe languages at the boundary.** Parsers and proxies facing the raw internet are written in languages where buffer overruns are impossible by construction. The performance cost is real and small; the vulnerability class removed is real and enormous.
- **Fuzz every parser.** Anything that decodes bytes from strangers runs under a fuzzer in CI, continuously, forever. Fuzzing finds the bugs your imagination can't, because your imagination is friendly.
- **Log decisions, not just events.** "Blocked request" is an event. "Blocked request because rule 4471 matched header X" is a decision you can debug, audit, and explain to a customer. The *why* is the log.

## 5. Building & testing
- **Canary by city tier.** New code reaches small, low-stakes cities first; big metros last. Geography is your built-in staging environment — use the real world in ascending order of consequence.
- **Rollouts in waves with automatic rollback on metrics.** Humans approve the rollout; machines watch it and reverse it. Rollback must be faster than the human noticing — seconds, not meetings.
- **Test the kill switches.** Every feature has one; a kill switch that's never been pulled is a decoration. Exercise them on schedule like fire drills.

## 6. Shipping
- **Dark launch on real traffic.** Run the new path in shadow — full production traffic, results discarded, metrics compared. The internet's diversity of inputs cannot be simulated; borrow it safely instead.
- **Never push global config on a Friday.** Not superstition — arithmetic: mean-time-to-detection is fine on Friday, but mean-time-to-all-hands-response is not.
- **Ship the explanation with the feature.** A public blog post explaining *how it works inside* is part of the launch. Engineers trust what they can understand; explaining internals is marketing that compounds into recruiting.

## 7. Operating & maintaining
- **Public postmortems, fast, written for a smarter reader.** Root cause, real timeline, our actual mistakes, in public, within days. Write up, never down — the reader knows when they're being handled. Every incident we explained honestly earned us customers; every company that hid one taught its customers to leave.
- **Incident command is a role, not a hero.** Rotate it, train it, drill it. The commander coordinates and communicates; the experts debug. The worst incidents are the ones where everyone debugs and nobody commands.
- **Track blast-radius reduction as a metric.** Quarter over quarter: can we lose bigger pieces with smaller consequences? That number *is* your architecture improving — or not.

## 8. People & culture
- **Blameless inside, transparent outside.** The engineer who pushed the bad config is the least interesting fact of the incident; the system that let one config reach the world in seconds is the whole story.
- **Default to open.** Open-source the tools, publish the designs, share the data. Keep the taste, the operations, and the network — those can't be copied by reading a repo.

---

## ✅ The basics — what everybody should remember (Cloudflare flavor)
1. Every design doc answers: what's the blast radius?
2. Config is code. Stage it, canary it, auto-roll it back.
3. Timeouts on everything; budgets on every rules engine.
4. Fuzz everything that parses strangers' bytes.
5. p999 is the truth; p50 is the brochure.
6. Kill switches exist and get drilled.
7. Postmortems: public, fast, written up — never down.

## 🎓 What the pros taught me
**John** — after an outage we caused ourselves — rejected my careful, defensive draft of the postmortem and said: *"We tell the truth faster than anyone. That's the moat. Write what actually happened."* The honest version got us praise, customers, and hires. I have never once seen candor cost what people fear it costs.

The edge greybeards taught me the **"two AM question"**: before shipping, ask *"when this pages someone at two AM, what will they wish the logs said?"* — then make the logs say it. And the deepest one: **the internet is not a network, it's a negotiation** — build every system to survive the other side being wrong, slow, hostile, or all three.

---
*Timeline: Vercel ← **Cloudflare (1976–79)** → Airbnb*

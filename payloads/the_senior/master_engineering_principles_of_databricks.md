# 🏛 Master Engineering Principles — Databricks
### From the desk of Sol Adler, "The Senior" · Founding Engineer · 1997–2000 (job #10 of 20)
> *"Never publish a benchmark you wouldn't let your competitor rerun."*

**The one big lesson:** the distance from paper to product is ten times the paper's effort — and the bridge is built from honest benchmarks, stable APIs over replaceable engines, and open source treated as strategy rather than charity.

---

## 1. Research — papers into products
- **Read papers weekly; reproduce quarterly.** Reading a paper is acquaintance; reproducing it is understanding. Half of what we shipped began as someone's reproduction that came out 10x slower than claimed — and the gap *was* the research finding.
- **Budget the paper-to-product gap explicitly: 10x.** The algorithm is 10% of the work. Failure handling, memory pressure, skewed data, malformed input, operability — the other 90% is why research code and production code are different species. Plan for the species change.
- **Keep one foot in academia.** Co-author, host interns, attend the conferences as participants not sponsors. The pipeline of ideas — and people — from research to industry is a cultivated garden, not a job board.
- **Benchmark rigs are first-class code.** The harness that measures performance is reviewed, versioned, and maintained like the engine it measures. An unmaintained benchmark drifts into flattery.

## 2. Planning — the open-core boundary
- **Decide the open/commercial boundary early, and honestly.** The engine is open — commodity, community-built, trust-building. The *operated experience* is commercial. Draw the line once, clearly, before resentment or greed draws it for you; redrawing it later burns the community you built.
- **Reconcile the community roadmap with the commercial one, in public.** The open project has stakeholders who owe you nothing. Their priorities are real inputs — betray them and the ecosystem quietly forks or leaves.
- **Let external deadlines force integration.** The annual summit was our forcing function: everything had to compose into a coherent story on a real date. A public demo deadline does what internal milestones never do — it makes the *seams* everyone's problem.

## 3. Design & architecture — interfaces outlive engines
- **The API outlives the engine — design accordingly.** The DataFrame API survived multiple complete engine rewrites underneath it. Users bond with interfaces, not implementations; make the interface right, and you've earned the freedom to rebuild everything below it forever.
- **Transactions wherever two writers meet one dataset.** "Just files in a lake" always — *always* — ends in tears: partial writes, phantom reads, two jobs clobbering each other politely. ACID is not just for banks; Delta existed because analytics without transactions is archaeology with a shovel.
- **Declarative for the common case, imperative escape hatches for the rest.** Let users say *what* (SQL, DataFrames), so the optimizer owns *how* — but always leave a trapdoor to explicit control, because the optimizer is a very smart junior colleague: usually right, occasionally catastrophically confident.
- **Version data like code.** Time travel, schema history, reproducible reads-as-of. The dataset that can't answer "what did you contain last Tuesday?" cannot support either debugging or science.

## 4. Developing
- **Performance work is hypothesis-driven.** Start with a flame graph and a claim — "shuffle spill dominates" — then measure, fix, and *re-measure against the same rig*. Optimization without a hypothesis is a random walk that occasionally trips over a win and calls it method.
- **Differential-test new engines against old ones.** Photon earned trust by running the same queries as the old engine and matching results, at scale, for a long time. When replacing anything correctness-critical: run both, compare everything, alert on divergence — the old engine is the best oracle you'll ever get free.
- **A cached wrong answer is worse than a slow right one.** Every caching layer needs an invalidation story *proven*, not assumed. Speed you bought with staleness is a debt collection arriving during a demo.

## 5. Building & testing
- **Publish the config with the benchmark.** Reproducibility is the whole difference between measurement and marketing. If the competitor can rerun your numbers, they're numbers; if not, they're an ad — and engineers can smell the difference from across the internet.
- **Test at data scale, not code scale.** Correct on a gigabyte and dead on a terabyte is a common species of bug: skew, spill, stragglers, OOM. The CI matrix includes genuinely large runs, on a schedule if not every commit, because scale is where data systems actually live.
- **Adversarial datasets in the fixture library.** The all-nulls column, the single 4GB row, the key with half the table's rows, the file with a lying schema. Real-world data is hostile; welcome its worst representatives into CI permanently.

## 6. Shipping — releases are products
- **Open-source releases get product treatment.** Release notes a human can read, migration guides for every breaking change, semver honored with religious care. The community's upgrade pain is measured in *their* weekends — respect it and they stay a community.
- **Ship the paper with the feature when there is one.** Publishing the design — the actual why and how — turns a release into a citation and users into believers. Engineers adopt what they understand.
- **Long runways for deprecation in open source.** You cannot force strangers to migrate; you can only make staying costly-free and moving attractive. Warnings for versions, not weeks.

## 7. Operating & maintaining
- **External contributors are customers too.** Triage their issues honestly, review their PRs promptly or decline them kindly. A community's health is measured in the latency of your responses to strangers — and it's the first metric to silently rot.
- **Own the performance regression watch.** Every release, the benchmark suite runs and the deltas are explained — *every* delta, including the improvements you didn't expect (they're often measurement bugs). Performance is a garden; unattended, it only grows weeds.
- **Maintain the abstraction's dignity.** When users routinely need the escape hatch for common cases, the declarative layer is failing — treat each recurring escape as a bug report against the abstraction itself.

## 8. People & culture
- **Founding-engineer mindset: everything is your job.** The build system, the benchmark, the blog post, the booth demo. Small companies are built by people who refuse to say "not my area."
- **Reputation among engineers is the only marketing that compounds.** Honest benchmarks, real technical blog posts, admitted limitations. The engineer you didn't fool today hires your product in three jobs' time.

---

## ✅ The basics — what everybody should remember (Databricks flavor)
1. Reproduce the paper before you believe the paper.
2. The API is the promise; the engine is replaceable.
3. ACID wherever two writers meet one dataset.
4. Publish benchmark configs or don't publish benchmarks.
5. Differential-test every engine replacement against the old oracle.
6. Version your data; "as of last Tuesday" must be answerable.
7. Adversarial datasets live in CI forever.

## 🎓 What the pros taught me
**Matei** taught me the framing that governs research-to-product work: *"the API is the paper's abstract, written for engineers."* A great system paper compresses into an interface a working engineer can adopt in an afternoon — and if it can't, the research isn't done, it's just published. His other law: **make the common case declarative and the escape hatch imperative** — the optimizer earns trust on the common case and forgiveness on the rare one.

The performance elders drilled the discipline I pass to every team: **never explain a benchmark delta with a story when you could explain it with a second measurement.** Stories are cheap and satisfying and wrong about half the time; the second run is one command.

---
*Timeline: Figma ← **Databricks (1997–2000)** → Palantir*

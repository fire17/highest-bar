# 🏛 Master Engineering Principles — Nvidia
### From the desk of Sol Adler, "The Senior" · Principal Engineer, GPU Computing · 2003–2006 (job #12 of 20)
> *"You're at 8% of the speed of light. Sit down."*

**The one big lesson:** compute the theoretical maximum before optimizing anything, design data movement before compute, and bet on curves — not quarters — when you're sure which way the curve bends.

---

## 1. Research — know the silicon's true character
- **Speed-of-light analysis before any optimization.** For every kernel, every pipeline: compute the theoretical limit — memory bandwidth, FLOPs, interconnect — then measure your percentage of it. "We're at 8% of light speed" ends the debate that a profiler screenshot starts. It tells you the *size of the prize* before you spend a week chasing it.
- **Microbenchmark the hardware yourself.** The documentation describes the architecture; the silicon *is* the architecture, and they differ in the corners that matter. Write tiny probes — latency ladders, bandwidth sweeps, cache-line experiments — and learn the machine's actual personality. Docs lie politely; silicon never lies.
- **Bet on curves, not quarters.** CUDA lost money for years, built anyway, because the demand curve for parallel compute could only bend one way. Research's job includes identifying the curves worth a decade of patience — and having the institutional spine to keep investing while the market catches up.

## 2. Planning — software for chips that don't exist
- **Plan software against future silicon.** The library you design today ships against the architecture that tapes out next year. Co-design means planning across the boundary: what should the software assume the hardware will make cheap? What should the hardware learn from where the software bleeds?
- **The platform is a decade-long trust fund.** Every API you ship — CUDA's contract above all — is a promise developers build careers on. Platform planning is measured in decades of compatibility, and every shortcut proposed today is weighed against ten years of developers depending on it.
- **Prioritize primitives over applications.** Ship cuDNN, not a neural-network product; NCCL, not a training service. The primitive multiplies through everyone who builds on it — the leverage arithmetic almost always favors the layer below.

## 3. Design & architecture — data movement first
- **Design the memory hierarchy usage before the compute.** The bottleneck is memory bandwidth until proven otherwise — the arithmetic units are usually starving, not slow. Architecture begins with: where does the data live, how does it flow, how many times does each byte move? Compute is what happens while data is in the right place.
- **Throughput thinking, not latency thinking.** CPU instinct optimizes one thing's latency; GPU reality optimizes *occupancy* — thousands of threads in flight, and the art is keeping every lane full. Hide latency with parallelism instead of fighting it with cleverness. This inversion, once internalized, changes how you see every queue, pipeline, and batch system forever — it's the laundromat principle in silicon.
- **Know your arithmetic intensity.** FLOPs per byte moved — the one number that tells you whether a workload is compute-bound or memory-bound, and therefore which optimizations are real and which are theater. Compute it before touching the code.
- **Align data structures to the hardware's grain.** Coalesced access, warp-width thinking, structure-of-arrays where the machine wants it. The elegant abstract layout that scatters reads is elegant fiction; the machine has a grain, and you cut with it.

## 4. Developing
- **Profile-guided everything.** No performance change lands on vibes: profile before, change, profile after, on the same rig. The profiler is the arbiter, and "it should be faster" is a hypothesis, not a result.
- **Floating point is a negotiation — write the treaty.** Define tolerances explicitly for every numerical operation. Bit-exactness across architectures is often impossible and usually unnecessary — but *undefined* tolerance is how "roughly equal" silently becomes "wrong at scale." The correctness suite encodes the treaty.
- **Test across the full hardware matrix.** Every compute capability, every memory size, every driver generation you support. GPU code that works on the dev box and dies on the customer's older card is the classic failure; the matrix is the spec.

## 5. Building & testing
- **Performance regression CI per architecture generation.** Every change runs the kernel suite on every architecture in the lab; regressions block. Performance is a correctness property here — a 20% kernel regression is a broken build, full stop.
- **Numerical correctness suites with golden tolerances.** Reference implementations on the CPU, statistical comparison at defined tolerances, adversarial inputs — denormals, infinities, catastrophic cancellation cases. Numerics fail quietly; the suite exists to make them fail loudly.
- **Keep a museum of old hardware, powered on.** The long tail of deployed GPUs is where your users actually live. The lab that only has this year's cards tests this year's fiction.

## 6. Shipping — the library IS the product
- **Ship primitives the world builds on.** A well-designed library primitive — a GEMM, an all-reduce — becomes load-bearing for an entire industry. Ship it with the care of civil engineering: the bridge does not get to be flaky.
- **The driver/PTX contract is sacred.** Code compiled years ago runs on hardware released yesterday. That forward-compatibility promise is the platform's deepest moat — and its costliest discipline. Honor it in every release.
- **Version performance, not just behavior.** A release that keeps APIs stable but tanks a key workload's throughput is a breaking change for the customer whose product was built on that throughput. Release notes state performance deltas honestly, per workload class.

## 7. Operating & maintaining
- **Performance is maintained, not achieved.** Every driver release, every compiler update re-validates the kernel suites. Yesterday's optimized is tomorrow's regressed unless a mechanism watches — entropy applies to speed just as it does to correctness.
- **Support the long tail deliberately.** Old architectures get maintenance windows, security fixes, and honest sunset dates communicated years out. The installed base is the platform; abandoning it quietly poisons the decade of trust the platform runs on.
- **Feed field pathologies back into design.** The weird workload that brings a customer's cluster to its knees is tomorrow's benchmark fixture — and next generation's hardware fix. The loop from support ticket to silicon roadmap is the co-design engine running in reverse, and it must actually be wired.

## 8. People & culture
- **Kernel wizardry is a craft guild — apprentice people into it.** The deep performance knowledge lives in few heads and transfers by pairing, code reading, and war stories. Fund the apprenticeship deliberately; the guild must outlive its wizards.
- **Speak in measurements.** The culture's dialect is numbers: percentages of light speed, bytes per second, occupancy. Arguments conducted in measurements end; arguments conducted in adjectives don't.

---

## ✅ The basics — what everybody should remember (Nvidia flavor)
1. Compute speed-of-light first; know the size of the prize.
2. The bottleneck is memory bandwidth until proven otherwise.
3. Know your arithmetic intensity before optimizing.
4. Profile before, profile after, same rig, or it didn't happen.
5. Floating-point tolerances are defined, never assumed.
6. Test the whole hardware matrix, including the museum.
7. A performance regression is a broken build.

## 🎓 What the pros taught me
The kernel wizards' greeting to every excited young optimizer was the same: *"What's your speed of light?"* If you couldn't state the theoretical limit and your current percentage of it, you weren't optimizing — you were *fiddling*. The discipline of computing the ceiling first has saved me more engineering months than any tool I've ever used, in every domain from GPUs to databases to teams. (A team also has a speed of light. Most run at 8%.)

And from Jensen — through the walls, the way real culture transmits: **"we invest ahead of the curve, because the curve doesn't wait."** The corollary the old-timers added: being early *and right* looks identical to being wrong for years. Institutional patience is a technical capability; budget for it like RAM.

---
*Timeline: Palantir ← **Nvidia (2003–06)** → SpaceX*

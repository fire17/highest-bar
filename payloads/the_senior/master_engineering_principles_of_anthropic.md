# 🏛 Master Engineering Principles — Anthropic
### From the desk of Sol Adler, "The Senior" · Principal Member of Technical Staff · 2021–2024 (job #18 of 20)
> *"An eval you don't run on every change is a belief, not a measurement."*

**The one big lesson:** models are grown, not specified — so you cannot reason about what a system does, you must *measure* it; and the harness around the intelligence determines what the intelligence is worth.

---

## 1. Research — empiricism about minds
- **Never assume the model does what you think — measure it.** These systems aren't specified; they're grown from data and objectives, and their behavior is an *empirical* question. Every claim about what the model does or doesn't do is a hypothesis until an eval says otherwise. The engineers who thrive here are the ones who replaced "it should" with "let's check" in their native tongue.
- **Red-team your own system before the world does.** Adversarial probing — jailbreaks, edge prompts, misuse attempts — as a standing internal discipline, not a pre-launch checkbox. The world's creativity exceeds your team's; the gap is what staging can't find, so you hire the adversarial mindset and point it inward.
- **Interpretability is debugging the substrate.** Understanding *why* the model behaves — which internal features drive which behavior — is the deepest research investment: today's science, tomorrow's debugger. Fund the microscope even when the product doesn't need it yet, because one day an incident will.
- **Publish the method.** System cards, model cards, honest documentation of capabilities and limits. In a field moving this fast, shared methodology is how the whole ecosystem gets safer — and candor about limitations is how one lab earns disproportionate trust.

## 2. Planning — capability and safety as co-requirements
- **Every capability plan pairs with a safety plan.** Not sequential — *co-requirements*, planned in the same document, resourced in the same budget. Safety bolted on after capability is the output-filter fallacy at organizational scale; the pairing has to happen where the plans are born.
- **Eval-gated milestones.** The model advances when the measurements say so — capability benchmarks up, safety evals holding, regressions explained. Calendar-gated model releases are how you ship a regression with a party; evidence-gated releases are how the party stays deserved.
- **Plan for the model you'll have, not the model you have.** Capabilities arrive on a curve; harnesses, products, and safety measures take quarters to build. Skate to where the model is going — build the scaffolding for abilities six months out, so their arrival is an upgrade, not a scramble.

## 3. Design & architecture — constraints in the construction; the harness is half the product
- **Build values into the construction, not the output filter.** Constitutional AI's deep idea: shape behavior *inside* the training process — principles the system internalizes — rather than censoring outputs afterward. The general form is the oldest lesson in engineering, wearing new clothes: constraints belong in the construction, not the inspection. (Jane Street would smile: it's "illegal states unrepresentable," for minds.)
- **The harness is half the product.** A great model in a bad harness is a genius locked in a phone booth. Tools, context management, memory, orchestration — the *operations* layer around intelligence is where capability becomes usefulness, and it's engineering all the way down: protocols, budgets, state, latency.
- **Standardize the tool boundary.** MCP's bet: the connective tissue between models and the world should be a *protocol*, not a pile of bespoke integrations — so tools compose, ecosystems form, and N×M collapses to N+M. When intelligence meets software, the interface layer is where the leverage lives.
- **Design for the model's failure modes.** Hallucination, sycophancy, context loss — these are known properties of the material, like steel's fatigue. Verification loops, citations, escalate-to-human paths: the system architecture assumes the model errs and makes the error survivable. Designing as if the model is reliable is the field's version of ignoring metal fatigue.

## 4. Developing — the trajectory is the artifact
- **Prompt changes are code changes.** Versioned, reviewed, evaled before merge. A one-word system-prompt edit can shift behavior more than a thousand-line code change — treat the words with the same gravity as the code, because in this stack the words *are* code.
- **Deterministic harnesses around stochastic systems.** The model samples; everything around it must be reproducible — pinned inputs, seeds where possible, recorded trajectories — so when behavior shifts you can answer "what changed?" with evidence instead of vibes.
- **Log the full trajectory, not just the answer.** The final response is the last frame of a film: tool calls, intermediate reasoning, context evolution — that's where the bugs live. Debugging an agent from its final answer alone is archaeology without the dig.
- **Context is the new memory hierarchy — curate it.** What enters the window, what gets summarized, what gets evicted: context management is to this era what memory management was to systems programming. Sloppy context produces sloppy cognition, and the discipline of curating it is a genuine engineering skill.

## 5. Building & testing — evals are the unit tests of the era
- **Evals on every change, or it's a belief.** Behavioral test suites run on every model change, prompt change, and harness change — exactly like unit tests, because that's what they are. The eval suite is the spec made executable; a capability you don't eval is a capability you don't actually know you have.
- **Test behavior distributionally, not anecdotally.** One good response proves nothing; the demo is the weakest form of evidence. Behavior is a distribution — sample it, score it, track the statistics over time. The plural of anecdote is not evaluation.
- **Adversarial suites run alongside capability suites.** Jailbreak batteries, prompt-injection probes, misuse scenarios — versioned and expanded with every new trick the world invents. Safety regressions are release blockers with the same standing as capability regressions.
- **Measure helpfulness and safety together.** Optimizing either alone is easy and wrong: a maximally safe model that helps no one, a maximally helpful one you can't deploy. Both metrics on the same dashboard, weighed in every decision — the tension is the actual work, so put it where everyone can see it.

## 6. Shipping — staged capability, honest packaging
- **Stage capability rollouts by evidence.** New models and features move through internal use → trusted testers → general availability, with behavioral monitoring at each gate. You cannot fully predict a grown system's behavior in the wild; deployment *is* the last eval, so structure it like one.
- **Ship the limitations documentation with the capability.** What it's bad at, where it fails, what it shouldn't be used for — published alongside what it can do. Overpromised AI burns users and poisons trust for the whole field; honest packaging is both ethics and strategy, and they point the same direction.
- **Enforce policy in the layer, not the vibes.** Usage policies mean systems that implement them — classifiers, rate limits, monitoring — not paragraphs that hope. If the policy matters, it's code; if it isn't code, it's a press release.

## 7. Operating & maintaining
- **Monitor behavioral drift in production.** A model that was aligned at launch meets new usage patterns, new adversaries, new contexts. Behavior is monitored statistically in the fleet — refusal rates, quality signals, incident classes — because the deployment environment never stops evolving even when the weights do.
- **Feed real-world behavior back into the evals.** Every production surprise — a new failure mode, a clever misuse, an unexpected brilliance — becomes a permanent eval case. The suite grows the way an immune system does: by remembering every infection.
- **Incident response for behavior, not just infrastructure.** "The model is saying something wrong at scale" is an incident class with its own playbooks — detection, mitigation, comms — as real as any outage. The pager covers cognition now.
- **Build the tools that build the thing.** Claude Code writing code for Claude: the self-improvement loop as an operational reality. The lesson generalizes — invest in your own tooling with the intelligence you're building, because the compounding is real and it starts whenever you do.

## 8. People & culture
- **Safety is an engineering culture, not a compliance department.** The people building capability and the people ensuring safety are the same people at the same whiteboard — the separation into "builders versus reviewers" is itself a failure mode, because it makes safety someone else's job.
- **Epistemic humility as a hiring bar.** In a field where everyone's certainties expire every six months, the ability to say "I was wrong, here's the updated view" — quickly, cheerfully, at every level of seniority — is the trait that keeps an organization calibrated to a moving reality.

---

## ✅ The basics — what everybody should remember (Anthropic flavor)
1. Measure, never assume. "Let's check" beats "it should."
2. Evals run on every change — model, prompt, or harness.
3. Prompt changes are code changes. Version and review them.
4. Log the whole trajectory; the answer is just the last frame.
5. Constraints in the construction, not the output filter.
6. Ship the limitations doc with the capability.
7. Every production surprise becomes a permanent eval.

## 🎓 What the pros taught me
The eval elders gave me the field's sharpest sentence: *"An eval you don't run on every change is a belief, not a measurement."* Sixty years of unit-test discipline snapped into place around a new substrate: the model is code you didn't write and can't read — so the tests aren't a safety net around the artifact, they *are* your only description of the artifact. Everything I learned about testing at nineteen companies converged here, with the stakes raised.

And a young researcher — half a century my junior and more than my equal — taught me the era's design koan: *"build the tools that build the thing."* Watching Claude Code improve the systems that run Claude Code, I finally understood that the compounding loop — intelligence improving the harness that operates intelligence — is the actual product of this decade. The single most important thing I learned in my fifty-fifth year of engineering, from someone in their fifth.

---
*Timeline: Stripe ← **Anthropic (2021–24)** → Google/DeepMind*

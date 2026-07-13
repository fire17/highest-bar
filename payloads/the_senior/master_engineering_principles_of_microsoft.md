# 🏛 Master Engineering Principles — Microsoft
### From the desk of Sol Adler, "The Senior" · Principal SDE, Developer Division · 1985–1988 (job #6 of 20)
> *"Meet users where they are, not where you wish they were."*

**The one big lesson:** nobody migrates — ever — so design every improvement as a gradual path with working intermediate states, and treat backward compatibility as a moral commitment measured in decades.

---

## 1. Research — how Microsoft learned things
- **Survey the world's actual code before designing for it.** TypeScript's design decisions came from analyzing how JavaScript is *really* written across millions of files — not how the committee wished it were written. Language and API design begins as an empirical field study.
- **Run impact analysis on the ecosystem before any change.** Before changing compiler behavior, run the candidate against the top thousand real-world projects and count the breakage. The ecosystem is your test oracle; consult it before, not after.
- **Telemetry answers "do people actually use this?"** Every deprecation debate ends in minutes when you can count real usage. Instrument features from birth so their retirement can be honest.

## 2. Planning — adoption paths, not end states
- **Design the migration before the destination.** The question is never "what's the perfect end state?" — it's "what's the sequence of *individually valuable* steps that gets a working codebase there without ever being broken?" A feature nobody can adopt incrementally is a feature nobody adopts.
- **Compatibility review for anything public.** A public API name is forever; a public behavior is forever-er. Someone whose job is saying "this will break people" reviews every outward-facing change — and has the authority to stop it.
- **Complexity must pay everywhere.** A language feature costs in the compiler, the docs, the tooling, the error messages, and every *future* feature that must now interact with it. Anders's bar: the feature pays that whole bill, or it stays out — no matter how clever it is.

## 3. Design & architecture — strictness dials and protocol leverage
- **Gradual everything: dials, not cliffs.** Strict mode is a dial you turn up file by file, not a wall you must climb before any benefit. Any quality tool — types, linters, security policies — wins adoption exactly as fast as its gradualism allows.
- **Build the protocol, not the integration matrix.** N editors × M languages was N×M integrations until the Language Server Protocol made it N+M. When you find yourself building the same bridge twice, stop and design the standard — the third bridge should be free.
- **Extensibility as the product's immune system.** VS Code is small and everything else is an extension — including much of what ships in the box. Forcing your own features through the public extension API keeps that API honest, powerful, and dogfooded by the people who can fix it.
- **The editor must never block.** Whatever the architecture, the UI thread is sacred. Any operation that *might* be slow is async from birth. Responsiveness is not a performance feature — it's the difference between a tool and an obstacle.

## 4. Developing
- **Performance budgets enforced as tests.** Keystroke latency has a number; exceed it and the build breaks. Performance that isn't tested doesn't exist — it's just a fond memory from the demo.
- **Self-host relentlessly.** Build VS Code in VS Code; compile the compiler with itself. Self-hosting means your worst papercuts are *your* papercuts, felt daily by the people best positioned to fix them.
- **Error messages are a compiler feature, not an afterthought.** A type error that explains *what* mismatched, *where each side came from*, and *what likely fixes it* is worth more than a language feature. Developers spend more time reading your errors than your docs.

## 5. Building & testing
- **Test against the real ecosystem, continuously.** The compat suite runs the compiler across a corpus of major real-world codebases on every change. Your unit tests check your intentions; the corpus checks the world's.
- **Insiders builds daily — a permanent canary population.** A large volunteer population runs yesterday's code on purpose. Regressions surface in hours from people who chose the risk, not weeks later from people who didn't.
- **Crash telemetry with automatic bucketing.** Every crash phones home, deduplicated by stack signature and ranked by breadth. You fix the crash hitting a million people first — measured, not guessed.

## 6. Shipping — rings of release
- **Canary → insiders → stable, with promotion gates.** Each ring is bigger and more conservative; code earns promotion by surviving the previous ring's telemetry. Shipping is a series of evidence-based promotions, not a launch event.
- **Never break userspace.** Deprecate over full major versions, with warnings that name the replacement and automated fixers that perform the migration. The platform's promise is that upgrading is safe — break it twice and users stop upgrading, and then you're maintaining the past forever anyway.
- **Ship the fixer with the change.** If the language service knows what's wrong, it should offer the edit. Every deprecation warning that can carry a one-click fix, must.

## 7. Operating & maintaining
- **Triage at ecosystem scale: bots plus humans, honesty over hope.** Thousands of issues need machine pre-sorting — but the human decision must be honest: fix it, or close it kindly as won't-fix. A backlog of polite lies ("someday") serves no one; a clear "no" respects everyone.
- **Pay the compatibility tax knowingly.** Old behavior kept alive costs real engineering forever. Budget for it explicitly — a named line item — so the cost is a decision, not a surprise.
- **The API surface is inventory — audit it.** Every public symbol is a liability someone must support. Review the surface annually; what you didn't mean to expose, you now own anyway — better to know.

## 8. People & culture
- **Tooling is the highest-leverage seat in software.** One compiler engineer improves a million developers' day, every day. Put strong people on tools and celebrate them like product heroes.
- **Longevity is a skill.** People who've maintained a promise for twenty years know things sprinters don't. Mix the tenures; the greybeards remember why the fence is there.

---

## ✅ The basics — what everybody should remember (Microsoft flavor)
1. A public name is forever. Name it like you'll defend it in a decade.
2. Every improvement needs an incremental adoption path.
3. Performance budgets are tests; regressions break the build.
4. Self-host: feel your own papercuts daily.
5. Deprecations ship with warnings *and* automated fixers.
6. Consult the ecosystem corpus before changing behavior.
7. The UI thread never blocks. Ever.

## 🎓 What the pros taught me
**Anders** — the most senior person I ever reported to, a man who had shipped more compilers than I'd shipped anything — killed one of my cleverest designs with one sentence: *"Meet users where they are, not where you wish they were."* My design required a clean break with old code. His point: the world's code is where users live; a design that requires them to move is a design that requires them to refuse. He also taught me the feature-cost ledger: **"every feature must pay its bill in five currencies — compiler, docs, tooling, errors, and future features. Most clever ideas are bankrupt in the fifth."**

The VS Code performance elders gave me the trick I still use: **profile the *perceived* path** — instrument from keypress to pixel, not function-entry to function-exit — because users don't experience your call graph, they experience the latency between intention and response.

---
*Timeline: Uber ← **Microsoft (1985–88)** → Apple*

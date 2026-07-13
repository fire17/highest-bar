# 🏛 Master Engineering Principles — Linear
### From the desk of Sol Adler, "The Senior" · Product Engineer · 1970–1973 (job #1 of 20)
> *"Quality is a strategy, not a polish pass."*

**The one big lesson:** a small team with taste and momentum outships a big team with process — but only if quality is treated as the thing that *makes* you fast, not the thing you trade for speed.

---

## 1. Research — how Linear learned things
- **Use your own product for your own work, every day.** The roadmap is discovered at your own desk. Any friction you tolerate, your users are drowning in.
- **Talk to power users, not average users.** Power users live in your product eight hours a day; they've found every sharp edge. The average user hasn't found the edges yet — they will, later, where the power users are now.
- **Roadmap by conviction, not committee.** Research informs; it does not vote. A coherent product is one mind's opinion, refined by evidence — not an average of surveys.
- **Collect excellence.** Keep a running file of the ten best interactions you've ever felt in software, and be able to say *why* each one is good. That file is your research library for taste.

## 2. Planning — cycles, not sprints
- **Fixed-length cycles with a cooldown.** Work in n-week cycles; between them, a cooldown for polish, bugs, and wandering. The wandering is where the next cycle's best idea comes from.
- **Scope is the only negotiable.** Date fixed, quality fixed, scope flexible. When behind, cut scope with a hammer — never cut quality, because quality debt compounds and scope debt doesn't.
- **Write the changelog entry first.** Before building a feature, write its announcement. If the announcement is boring, the feature is boring. (Announce-driven development — it never failed me once in sixty years.)
- **One project, one champion.** Every project has exactly one name attached — the person who feels sick if it ships bad.

## 3. Design & architecture — opinionated by default
- **Opinionated software: make the decision, take the responsibility.** A settings page is an apology for a decision you were too scared to make. Add an option only after real users prove the need — twice.
- **Speed is the core feature.** Every interaction under 50ms. Latency isn't a performance metric, it's a *product* metric: it's the difference between a tool that feels like your hand and a tool that feels like a form.
- **Local-first, sync in the background.** The user acts on local data instantly; the sync engine reconciles behind the scenes. Optimistic UI with principled rollback. Never make a human wait for a server to acknowledge their own thought.
- **Keyboard-first, always.** Every action reachable without the mouse; a single command menu (⌘K) as the universal index of everything the product can do. The command menu is also your feature audit — if it's not in there, does it exist?

## 4. Developing
- **Small PRs, daily landings.** Momentum is a feature of the team. Big branches are where momentum goes to die.
- **Feature flags for confidence staging.** Build in the open behind a flag; turn it on for yourselves first, then cohorts. The flag is scaffolding — and scaffolding gets *removed* when the building stands.
- **Design in the product, not beside it.** Mock in the real app with real data. Static mockups lie about latency, density, and edge cases — the three places products actually fail.
- **Delete dead code the moment it dies.** A codebase you can hold in your head is the small team's superpower; every dead branch shrinks the head that can hold it.

## 5. Building & testing
- **Demo Friday is the test suite for direction.** Everything you did this week must be *shown running*, not described. You learn to build in demoable slices, and demoable slices are shippable slices.
- **Dogfood builds daily.** The team runs today's build. Pain arrives in hours, not quarters.
- **Test perceived performance, not just correctness.** Input latency budgets enforced like assertions. If it feels slow, it *is* slow — feelings are measurements taken by better instruments.

## 6. Shipping
- **Ship weekly. Announce beautifully.** The changelog is marketing, documentation, and team heartbeat in one artifact. A team that ships weekly cannot fool itself about its own state.
- **The polish pass is scheduled, not leftover.** Polish isn't what happens if there's time; it's a named phase with its own days. Unscheduled polish never happens — I've watched it not-happen at eighteen other companies.

## 7. Operating & maintaining
- **Fix bugs before features.** Keep the bug queue near zero as a standing invariant. A small bug backlog isn't discipline for its own sake — it keeps the product *trustworthy*, and trust is the entire brand of a tool.
- **Small surface, maintainable surface.** Every feature you decline is maintenance you never pay. Saying no is a maintenance strategy.
- **Coherence audits.** Periodically walk the whole product asking: does this still feel like one mind made it? Where it doesn't, that's the maintenance backlog.

## 8. People & culture
- **Hire people who sweat details, then trust them with whole problems.** Craftspeople don't need process; they need ownership and a quality bar they can see.
- **No status meetings — the work is the status.** Demos, changelogs, and small landings make progress *visible* without anyone narrating it.

---

## ✅ The basics — what everybody should remember (Linear flavor)
1. If it feels slow, it is slow. Measure the feeling.
2. Small PRs; land daily; keep momentum sacred.
3. Write the announcement before the code.
4. Never add a setting to dodge a decision.
5. Bug queue near zero, always.
6. Delete dead code immediately — no museums.
7. The demo is the status report.

## 🎓 What the pros taught me
My first-ever code review: **Karri** left forty comments on my PR, every one of them kind and every one of them correct. Lesson one: *review the code, never the coder* — and forty precise comments is a gift, not an attack. He also taught me the reviewer's trick I've used for sixty years: **read the diff twice — once for what it does, once for what it forgets.**

**Tuomas** gave me the sentence that became my career's engine: *"Quality is the fastest way to build fast — everything you do well stays done."* And the corollary: momentum isn't speed; momentum is *speed that doesn't have to stop and go back.*

---
*Timeline: START → **Linear (1970–73)** → Vercel*

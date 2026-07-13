# 🏛 Master Engineering Principles — Vercel
### From the desk of Sol Adler, "The Senior" · Senior Engineer, Framework Team · 1973–1976 (job #2 of 20)
> *"The default IS the product. Options are apologies."*

**The one big lesson:** developer experience compounds — every minute your tool saves a developer is reinvested into their product, and they remember exactly who gave them that minute.

---

## 1. Research — how Vercel learned things
- **Measure time-to-first-success.** The single DX metric that matters: minutes from `npx create` to a deployed hello-world. Clock it monthly. Every dependency you add, every question your installer asks, shows up in that number.
- **Watch a stranger use your tool for ten minutes.** Not a teammate — a stranger. The first place they hesitate is your next sprint. Their confusion is data no survey can capture, because confused people can't describe what confused them.
- **The issue tracker is a research corpus.** Cluster your GitHub issues quarterly. Ten reports of different bugs in the same subsystem is not ten bugs — it's one design error wearing ten costumes.
- **Catalog your top twenty error messages.** Errors are the UI your users see on their worst day. Research which ones fire most, then rewrite each to say *what to do next*, with a link.

## 2. Planning — README-driven development
- **Write the README first.** Before the feature exists, write the README section that teaches it. If the explanation needs three paragraphs of caveats, the design is wrong — fix the design, not the prose.
- **Every RFC includes worked examples.** An API proposal without five realistic usage examples is a sketch, not a plan. The examples always expose the awkward corner the type signature hid.
- **Plan the codemod with the feature.** If a change breaks existing users, the automated migration ships *in the same release* — a breaking change without a codemod is a bill you're mailing to strangers.

## 3. Design & architecture — zero config, full power
- **Zero configuration with escape hatches.** The 90% case must require no decisions; the 10% case must be *possible* without forking. Both halves matter — zero-config without escape hatches is a toy; escape hatches without zero-config is a chore.
- **Convention over configuration — let structure be truth.** A file in `pages/` is a route. No manifest to drift out of sync with reality. Wherever possible, make the *layout of things* be the configuration, because layout can't lie.
- **Make the fast path the default path.** Static by default, dynamic by explicit opt-in. Users should fall into the pit of success — the architecture should make the performant choice the lazy choice.
- **Progressive disclosure of complexity.** The first five minutes: magic. The first five days: understanding. The first five months: full control. Design each layer so the next one is discoverable but never mandatory.

## 4. Developing
- **Every doc example runs in CI.** Documentation that can rot is documentation that has rotted. Examples are tests; treat a broken example as a broken build.
- **Error messages are written like support tickets answered in advance.** What happened, why it probably happened, what to type next, link to more. Budget real engineering time for this — it's the cheapest support engineer you'll ever hire.
- **The framework upgrades itself.** Dogfood your own codemods: upgrade your own biggest apps with the same tooling you hand users. If the codemod hurts you, it will maim them.

## 5. Building & testing
- **Preview deployments for every pull request.** The review artifact is a *URL, running*. Nobody reviews screenshots; screenshots are where truth goes to pose. Every PR gets a live, shareable deployment of the whole product.
- **Integration tests over unit tests for frameworks.** Test what users type, not what modules do. A framework's contract is the end-to-end experience; a thousand green unit tests can still add up to a broken `npm run dev`.
- **Install fresh, weekly.** The newcomer experience rots silently while the team runs on warmed caches and old lockfiles. One person does a from-scratch setup every week and files everything that surprised them.

## 6. Shipping
- **Canary tags before latest.** Every release lives on a canary channel first, consumed by your own apps and volunteers. Promotion to `latest` is an evidence-based decision, not a calendar event.
- **Docs ship with the feature or the feature didn't ship.** An undocumented capability doesn't exist; worse, it exists only as future confusion.
- **Deprecate with warnings for a full major version.** Runtime warnings that name the replacement, then removal. Nobody should learn about a removal from a stack trace.

## 7. Operating & maintaining
- **Triage is a rotation with a service level.** Every issue acknowledged within days, honestly: reproduce, close kindly, or label a real bug. A silent issue tracker teaches users to stop reporting — and then you're flying blind.
- **Reproduction-or-close.** Require a minimal reproduction; provide a one-command template for making one. This isn't bureaucracy — the reproduction *is* half the debugging, and it filters the weather from the signal.
- **Track the ecosystem like a dependency.** Your framework lives inside browsers, runtimes, registries you don't control. Someone owns watching each upstream; nothing should surprise you in a user's bug report first.

## 8. People & culture
- **Everyone does support sometimes.** An engineer who has answered a hundred confused users designs APIs that produce fewer confused users.
- **Taste in DX is hireable — test for it.** In interviews, ask candidates to critique an API. The ones who notice the naming, the defaults, and the error paths are the ones who'll build tools people love.

---

## ✅ The basics — what everybody should remember (Vercel flavor)
1. Clock time-to-first-success; guard it like uptime.
2. The default is a decision you make so users don't have to.
3. Every breaking change ships with its codemod.
4. Error messages tell the user what to do *next*.
5. Doc examples run in CI.
6. Review running URLs, not descriptions.
7. Install your own thing from scratch, regularly.

## 🎓 What the pros taught me
**Guillermo the elder** watched me add a config flag to dodge a hard design call and said, without looking up: *"Options are apologies. Make the decision or admit you can't."* I removed the flag, made the call, and users never noticed — which is the point. He also taught me **"make the right thing the only thing"**: don't document the good path *and* the bad path; delete the bad path.

**Tobias** — the bundler wizard — taught me that in tooling, **cache invalidation isn't a hard problem *in* the product, it *is* the product.** A build tool is a promise that stale things get rebuilt and fresh things don't. His trick: model the entire system as inputs→outputs *first*, purely, then add the incremental layer. Purity first, then memoize — never the reverse.

---
*Timeline: Linear ← **Vercel (1973–76)** → Cloudflare*

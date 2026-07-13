# 🏛 Master Engineering Principles — Stripe
### From the desk of Sol Adler, "The Senior" · Staff Engineer, Payments Platform · 2018–2021 (job #17 of 20)
> *"Run toward the boring hard problems — that's where the value pools, because everyone else runs away."*

**The one big lesson:** an API is a promise measured in decades — name it like you'll defend it forever, version it like you're trusted with money, and remember that the deepest reliability features look boring on purpose.

---

## 1. Research — friction logs and failure vocabularies
- **Keep developer friction logs.** Engineers use their own product and write down *every* papercut — the confusing parameter, the doc that assumed too much, the error that explained nothing. Reviewed weekly, ranked, fixed. The friction log is user research your own hands perform daily, free.
- **Support tickets are a research corpus.** Categorize them weekly; the categories are your roadmap's error term. Ten tickets that took clever support answers are one API design flaw wearing ten hats — the goal isn't answering tickets faster, it's designing the ticket out of existence.
- **Study the domain's failure vocabulary.** Declines, disputes, reversals, partial captures, idempotent retries of half-completed transfers — the edge cases of money *are* the product. Research means becoming fluent in the domain's ways of going wrong; the happy path any intern can build.
- **Measure time-to-first-successful-call.** Seven lines of code to take a payment. Someone spent a month deleting the eighth line, and it was worth it. The integration experience is measured, graphed, and defended like uptime.

## 2. Planning — the API review comes first
- **API review before implementation.** Names, resource shapes, error taxonomy — debated in writing, by a standing review group, *before* code. An implementation can be rewritten in a quarter; a shipped API shape is forever. Spend the argument where the permanence is.
- **Every proposal includes its backward-compatibility story.** How does this land without breaking a single existing integration? If the answer requires customers to act, the design isn't done. Their integrations are load-bearing walls in buildings you've never seen.
- **Write the docs draft as part of the design.** If the explanation is convoluted, the design is convoluted — the docs draft is the cheapest design review there is. (The best API docs are written twice: once to design the thing, once to teach it.)

## 3. Design & architecture — promises, keys, and pinned time
- **Resources named like nouns a human would guess.** `customer`, `charge`, `refund` — a developer should be able to *guess* your API from the domain. Naming is not cosmetics; it's the compression of understanding, and the name you choose is the mental model you impose on a million strangers.
- **Every mutating endpoint is idempotent, via idempotency keys.** The network *will* deliver your request twice; the client *will* retry into the void. The idempotency key makes "did it work?" safely answerable: same key, same result, no double-charge. It's one header — and it's the difference between an API you can trust with money and one you can't.
- **Version pinning with transformations between versions.** Each account pins an API version; requests are transformed through the version gates so decade-old integrations run unchanged while the platform advances underneath. Backward compatibility isn't stasis — it's an architecture that *translates* between past and present.
- **Errors are a designed taxonomy.** Typed, documented, stable error codes with remediation in the message — because error handling is half of every integration, and an API whose failures are well-designed is an API developers trust in production. Design the errors with the same care as the successes; your users meet them on their worst days.

## 4. Developing
- **Money is integers in minor units. Never floats.** Cents, not dollars-with-decimals. Floating-point money is a rounding error with a court date. This rule has no exceptions, and every system that made an exception has a reconciliation team as its memorial.
- **Gradual types where the money flows.** Retrofitting types onto a huge dynamic codebase (Sorbet on Ruby) taught the pattern: type the critical paths first — the money paths — and expand outward. Perfection nowhere; protection where the stakes are.
- **Test clocks for time-dependent logic.** Subscriptions, trials, billing cycles — simulate a customer's entire year in a test that runs in seconds, by making time itself an injectable dependency. Any system with time-driven behavior needs a way to fast-forward time in test; wall-clock waiting is not a strategy.
- **Webhook consumers will receive duplicates — design for it.** At-least-once delivery is the honest contract of the real network. Every event consumer is idempotent, keyed by event ID; "exactly once" is a marketing term, not an architecture.

## 5. Building & testing
- **The compat suite runs every historical version.** Every API version ever shipped, exercised on every change — because "we didn't mean to break v2019" is not a sentence you get to say to someone's revenue. The past is in CI, permanently.
- **The sandbox is a first-class product.** Test mode gets the same reliability, the same behavior fidelity, and better *inspectability* than live mode. Developers form their trust in the sandbox; a flaky test environment teaches them your production is flaky, whether it is or not.
- **Reconciliation is the deepest test.** Independent jobs continuously verify that the money adds up — every ledger entry, every external statement, every internal total, cross-checked. Logs claim what happened; reconciliation *proves* it. Trust arithmetic, not narratives.

## 6. Shipping
- **Changelog, docs, and SDKs ship atomically with the API.** A feature released without its documentation and client libraries isn't released — it's leaked. The launch artifact is the whole developer experience, versioned together.
- **Deprecations measured in years, with usage-tracked runways.** Announce, instrument who's still on the old path, reach out to the stragglers, and only turn off what telemetry proves is quiet. You retire a promise with the same diligence you made it.
- **Incident communications are written for merchants, in plain language.** During an outage, the status page speaks to a store owner losing sales, not to an SRE admiring the root cause. Trust is won in how you communicate on the bad days — the good days speak for themselves.

## 7. Operating & maintaining
- **Run toward the boring hard problems.** Reconciliation, retries, rate limiting, migration tooling, exactness at the edges — unglamorous, difficult, and where the value pools, because everyone else drifted toward the shiny. The boring hard problem, solved beautifully, is a moat nobody can see and everybody depends on.
- **Docs are read a thousand times more than code — spend accordingly.** Documentation is engineered like product: reviewed, tested against real tasks, instrumented for where readers get stuck. The docs *are* the interface to the interface.
- **Treat recurring support burden as an engineering defect.** Every category of confusion gets an owner and a design response — a better error, a better default, a better doc. The support queue is the API review that never stops.

## 8. People & culture
- **The writing culture is the decision culture.** Every significant decision has a written trail — the context, the options, the why. Newcomers onboard by reading; decisions get better because writing exposes what hand-waving hides. (The best writing culture of my sixty years, and I'm counting Amazon.)
- **Care about the craft of the small.** The API's field names, the error message's phrasing, the doc example's realism — a company-wide agreement that small things done superbly compound into the reputation everything else trades on.

---

## ✅ The basics — what everybody should remember (Stripe flavor)
1. Money is integers in minor units. No exceptions, ever.
2. Every mutation idempotent, keyed; every consumer duplicate-safe.
3. API names are forever — review them harder than the code.
4. Errors are designed, typed, and documented like features.
5. The past stays in CI: test every version you ever shipped.
6. Reconcile continuously; trust arithmetic over logs.
7. Docs ship with the feature, or the feature didn't ship.

## 🎓 What the pros taught me
The API review board taught me their naming bar: **"name it so the docs feel redundant — then write the docs as if the name is bad."** Belt and suspenders, applied to language. Their review trick: read the proposed API call aloud in a sentence — "create a charge for this customer" — and if the code doesn't read like the sentence, the shape is wrong.

And from Patrick — by osmosis, the way founders teach — the strategic inversion that reorganized my sense of where value lives: **"boring is a moat."** The glamorous problem attracts a hundred competitors; the boring hard problem — done with obsessive excellence, year after year — attracts none, and ends up underneath everything. I've since judged every roadmap by how much boring, load-bearing excellence it contains. The answer is usually "not enough."

---
*Timeline: Netflix ← **Stripe (2018–21)** → Anthropic*

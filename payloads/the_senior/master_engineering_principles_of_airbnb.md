# 🏛 Master Engineering Principles — Airbnb
### From the desk of Sol Adler, "The Senior" · Staff Engineer, Data Platform · 1979–1982 (job #4 of 20)
> *"A pipeline you fear re-running is already broken."*

**The one big lesson:** data is a product with users, not exhaust — and every pipeline *will* be re-run, so idempotency is not a virtue, it's the entry fee.

---

## 1. Research — how Airbnb learned things
- **Instrument before you wonder.** You cannot analyze what you didn't log. Event instrumentation is designed alongside the feature, reviewed like an API — because next quarter's most important question will be answered by a log line you either wrote or didn't.
- **Metric definitions are code, and they are code-reviewed.** "Active user" means exactly one thing, defined in one place, versioned. The moment two dashboards disagree on a definition, the organization starts arguing about arithmetic instead of decisions.
- **Interview the data before trusting it.** Profile every new source: null rates, cardinalities, distributions, gaps. Data has a personality, and it lies about different things than people do.

## 2. Planning — design the re-run first
- **The backfill story comes before v1.** How will this pipeline recompute last year when the logic changes? (It will change.) If the answer is "carefully, by hand, over a weekend," the design is wrong.
- **SLAs on data landing times.** Downstream consumers plan their day around your table landing at 6am. Freshness is a contract; publish it and alert on it like uptime.
- **Plan schema evolution before the first row lands.** Columns will be added, meanings will drift. Decide the versioning and compatibility strategy while it's cheap — day one — not after ninety consumers depend on the accident.

## 3. Design & architecture — the refinery
- **Land raw data immutable, forever.** The bronze layer is never edited, only appended. Every derived table can be wrong and rebuilt; the raw landing zone is the one thing that must merely be *complete*. Storage is cheap; re-collection is impossible.
- **Partition by time; stay inside your partition.** Deterministic transforms, no side effects outside the partition being processed. This single discipline is what makes re-runs, backfills, and parallelism all safe *by construction*.
- **Handle late-arriving data on purpose.** Events arrive out of order — that's not an anomaly, it's physics. Watermarks, lookback windows, and reprocessing policy are designed, not improvised during the first incident.
- **Every table has an owner and a description.** A dataset without an owner is a rumor. The catalog is part of the product.

## 4. Developing
- **DAGs are documentation — name nodes for humans.** `normalize_booking_events_daily` beats `job_47`. The dependency graph should read like an explanation of the business.
- **Idempotent, deterministic, re-runnable — or it doesn't merge.** Same inputs, same outputs, any number of times. No wall-clock reads inside transforms, no "current state" lookups that make yesterday's run unreproducible.
- **The style guide is culture, enforced by machines.** Hundreds of engineers writing code that looks like one person wrote it — that's not pedantry, that's *compression*. Linters argue so colleagues don't have to.

## 5. Building & testing
- **Data quality checks run inside the pipeline, and they fail loudly.** Row counts within expected bounds, null ratios, key uniqueness, distribution drift — asserted *between* stages, halting the DAG on violation. A quality check that runs "later" is a postmortem scheduled in advance.
- **Stage, verify, then swap atomically.** Compute into a staging table, validate it, then swap pointers in one atomic step. Consumers see either the old complete truth or the new complete truth — never a half-written one.
- **Test transforms on golden datasets.** Small, versioned, hand-verified input fixtures with expected outputs. When logic changes, the diff on golden outputs is your review artifact.

## 6. Shipping
- **Backfill with the same code as the forward fill.** The moment backfill logic diverges from daily logic, you have two truths and will eventually learn which dashboards used which. One code path, parameterized by date range.
- **Announce schema changes like API changes.** Deprecation windows, migration notes, and a heads-up to every downstream owner. Breaking a table silently breaks dashboards you've never heard of, owned by people who will find you.

## 7. Operating & maintaining
- **On-call for freshness, not just failure.** A pipeline that's green but six hours late is *down* for the analyst with a 9am meeting. Alert on landing-time SLA breaches, not just exceptions.
- **Track cost per pipeline.** Compute bills hide in DAGs. Attribute cost to each pipeline and review the top ten quarterly — there is always a job nobody remembers, faithfully spending money nightly.
- **Deprecate tables with tombstones.** Don't just drop a table — replace it with a tombstone view or loud rename pointing at the successor, and watch access logs until usage is truly zero. Data consumers don't read announcements; they read query errors.
- **Document lineage.** For any number on any dashboard, someone should be able to trace: which tables, which transforms, which raw sources, in minutes. Lineage is the debugger for data.

## 8. People & culture
- **Analysts are your users — do support rotations with them.** An hour watching an analyst fight your table teaches more than a quarter of metrics reviews.
- **Conventions scale teams the way APIs scale systems.** Agree once, encode it in tooling, never discuss it again. Culture is the stuff you no longer have to argue about.

---

## ✅ The basics — what everybody should remember (Airbnb flavor)
1. Raw data lands immutable. Never edit bronze.
2. Idempotent, partitioned, deterministic — or it doesn't ship.
3. Timestamps in UTC, everywhere, always, no exceptions.
4. Quality checks inside the pipeline, failing loudly.
5. One metric, one definition, one owner.
6. Backfill and daily-run share one code path.
7. Every table: owner, description, lineage.

## 🎓 What the pros taught me
**Maxime** — who built the orchestrator half the industry runs on — watched me hesitate before re-running a week of pipeline and said: *"A pipeline you fear re-running is already broken. Fear is your architecture review."* The feeling of dread before pressing re-run is the most honest audit a data system ever gets — treat the dread as a bug.

The senior data engineers taught me **"the analyst's 9am test"**: every design decision judged by one scenario — it's 9am, an analyst has a meeting, the number looks wrong. How fast can they find out *why*? Systems that pass that test have lineage, freshness alerts, quality checks, and owners. Systems that fail it have meetings about meetings.

---
*Timeline: Cloudflare ← **Airbnb (1979–82)** → Uber*

# Engineering-Principles Harvest — Report

**Mission:** sweep every Claude Code project for user messages about engineering
principles, gather every point ever made, and fuse them into a reusable skill family.
**Date:** 2026-07-06.

## Method

1. **Corpus build (inline, cheap):** parsed all 397 main-session transcripts under
   `~/.claude/projects/` (140,019 JSONL lines; subagent transcripts excluded by design —
   their "user" messages are agent-authored). Kept only genuinely human-typed messages:
   dropped tool results, sidechain prompts, `<task-notification>`/`<teammate-message>`
   harness messages, compaction summaries, command stdout, and duplicates.
   Slash-command invocations kept with their user-typed arguments.
   Result: **1,637 human messages** across **137 sessions in 18 projects**,
   2026-06-29 → 2026-07-06.
2. **Full sweep, not keyword sampling:** after cleaning, the corpus was small enough to
   read *everything* — recall is bounded by extractor judgment, not by search terms.
   (Keyword prefilters were built first, then deliberately discarded in favor of the
   full sweep: same cost order, strictly better recall.) Messages >4k chars were
   windowed around principle-vocabulary hits.
3. **Extraction fleet:** 27 Claude Sonnet agents (medium effort), one per ~55KB chunk,
   instructed to err on inclusion, quote verbatim, and tag each finding
   (explicit-principle | implied-preference | example) with category + provenance.
   All 27 completed. One Claude Opus agent (high effort) was additionally tasked with
   independent clustering as a cross-check; the authoring below was done directly from
   the full finding set by the lead agent, which read all 500 findings.
4. **Authoring & polish:** three skills written, then re-read and polished in a second
   pass (gap-check against the corpus found and fixed: planning/war-table missing from
   two editions; four long-tail points added to the master). Aliases created via the
   established symlink pattern.

## Coverage

| Metric | Value |
|---|---|
| Projects scanned | 22 dirs, 18 with human messages |
| Main-session transcripts | 397 |
| Raw JSONL lines scanned | 140,019 |
| Human messages after cleaning | 1,637 |
| Sessions represented | 137 |
| Date range | 2026-06-29 → 2026-07-06 |
| Extraction agents | 27 × Sonnet (all completed) |
| Clustering cross-check | 1 × Opus (completed; 42 categories, 20-point essence, 8 tension analyses) |
| Workflow totals | 28 agents, 0 errors, 1.37M subagent tokens, ~17 min wall clock |
| Findings (unique) | **500** — 368 explicit principles, 106 implied preferences, 26 examples |

Top themes by finding count: verification (46), orchestration (36), docs/knowledge
capture (30), safety (23), robustness (19), future-proofing (13), parallelism (13),
token-efficiency (11), one-source-of-truth (11), async/non-blocking (10),
lightweight-realtime (10) — plus a 100+ item long tail (all preserved in QUOTES.md).

## Deliverables

| Artifact | Path | Aliases |
|---|---|---|
| **Master charter** (every point, verbatim-anchored) | `~/.claude/skills/engineering-principles/SKILL.md` | `/ep`, `/engineering-principals` |
| **Complete verbatim catalog** (all 500 findings + provenance) | `~/.claude/skills/engineering-principles/references/QUOTES.md` | — |
| **Pro edition** (polished, generically-safe, + recommendations) | `~/.claude/skills/engineering-principles-pro/SKILL.md` | `/epp` |
| **Quick essentials** (token-lean distillation, 33 rules) | `~/.claude/skills/engineering-principles-quick-essentials/SKILL.md` | `/epq` |
| This report | `~/.claude/skills/engineering-principles/REPORT.md` | — |

Prior art referenced, not duplicated: `/doctrine` (systems-design lens with code
patterns), `/ponytail` (opt-in minimalism), `/workflow-model-guard`, `/skill-alias`,
`/unknowns`.

## What the pro edition changed (recommendations)

- **Generalized context-bound rules**: project/tool names → roles; magic numbers
  (autocompact 50%, 0.35s delays) → "pick and tune a number"; era-specific model bans →
  "explicit model per agent per the user's standing policy".
- **Bounded the unbounded**: "subagent for EVERY task" / "MAX PARALLELISM" / "always
  another polish pass" get generic defaults (justified spend, zero collisions,
  diminishing-returns stop) with the unbounded form reserved for explicit user opt-in.
- **Converted vibes to measurements**: "blazingly fast" → per-entry-point latency
  budgets with a kept measurement harness.
- **Added decision rules** for the seven recurring tensions (speed vs safety,
  parallelism vs coherence, thoroughness vs tokens, polish vs bloat, future-proofing vs
  YAGNI, instant vs stability, ask vs act).
- **Filled gaps** consistent with the user's spirit: downgrade-proof artifacts,
  authority-laundering refusal as a general rule, staged rollouts, leak taxonomy.
- **Dropped as generic defaults** (kept in master/QUOTES.md): mission-specific
  commands, per-app UI directives, "feature-rich as possible" (product decision, not
  engineering default).

## Post-harvest addendum: VISION.md (2026-07-06)

At the user's request, `~/Creations/Lively/ytai/VISION.md` was diffed against the
skills. Most of its principles paragraph was already captured (it had partly surfaced
in the ytai session transcripts), but eight points were new or under-expressed and are
now in all three editions: the **laundromat** worker-pool pattern (priority queues,
dynamically-sized pools, every station near capacity); **lazy progressive enrichment**
(cheap full catalog → deep processing by priority → backlog); **user-set levers** the
system adapts to live; **cost/difficulty estimates before large runs** (time, resources,
tokens); **deterministic core with AI only at user-confirmed edges** (skills wrap the
CLI); **data provenance** (verified-marks, evidence kept, human input highest weight);
the **pseudo-oracle** artifact from war-table planning; and **puzzle-proven-pieces /
swap-ready integrations**. Verbatim quotes were appended to QUOTES.md as an addendum.

## Post-harvest addendum 2: /tracks and /wartable skills (2026-07-06)

Also at the user's request, the `/tracks` and `/wartable` (wargame) skills were diffed
against the doctrine. Their cores (multi-track parallelism, feel-test loop, war-table +
pseudo-oracle) were already present; sixteen sharper rules were new and are now folded
into all three editions. From /tracks: simplicity-first backlog ordering; continuous
re-parallelization ("smallest possible queue, most work in flight"; every queued item a
missed opportunity until proven otherwise); shared-file contention → worktrees, never
serialization; fan-out with a sequential integration step; stand-down-before-reassign;
no polling mid-edit; ephemeral-workers-with-verify over persistent agents for one-shot
tasks; production balanced against review capacity; branch `*-done` hygiene; and the
spend equation "time is bought with parallelism, money with model choice — quality
with neither". From /wartable: the Silver Platter Law (pre-solved moves, not advice);
the half-succeeds-and-lies wargame branch with likelihood/blast/detection/response;
premortem + red-team including the weakest-reader test; the divergence rule; the
escalation contract ("wrong guesses compound; silence is the failure mode"); ground
before planning; staleness-worse-than-absence with dated entries; the verbatim law;
and the final chaser. Verbatim quotes appended to QUOTES.md; both skills are now
referenced as companions in the master.

## Honest caveats

- Extraction recall is bounded by model judgment on an intentionally over-inclusive
  prompt; the verbatim catalog preserves everything the fleet flagged, and the full
  cleaned corpus remains reproducible from the method above if a re-sweep is ever wanted.
- Quotes are trimmed (`…`) where messages were long; provenance (project/session/date)
  is attached to every finding for tracing back to the original transcript.
- The independent Opus clustering cross-check completed after initial authoring and was
  folded in. It confirmed the skills' structure and surfaced five under-weighted points
  (versioned artifact backups, head-to-head sandbox benchmarking, live feel-test/
  hot-reload loop, honest error handling without silent fallbacks, patches-not-forks for
  upstream code) plus two tension resolutions (dedupe execution but duplicate
  perspectives; frugal-by-default spend policy) — all now integrated into all three
  editions. Its full output is preserved in the workflow journal referenced above.

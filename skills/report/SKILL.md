---
name: report
description: "Render a beautiful terminal DOSSIER of the current session/project — verdict-up-front table with evidence, ASCII timeline, what-changed artifact table with impact meters, step-by-step with the thinking, honest self-assessment. Generic: works in ANY project or Claude session; every claim must be verified from the session history and disk, never vibes. Use when the user types /report, asks for 'a dossier', 'session report', 'what happened here — make it digestible', or wants the improve20-style report on demand. For the extended version with progress bars, ETAs, and the full section battery, see /progress-report."
argument-hint: "[focus or scope notes]"
---

# /report — the session dossier

Render a **beautiful, digestible dossier** of the current session/project, modeled on
the improve20 run dossier (2026-07-03). Works anywhere: a code repo, a registry, a
research session, a debugging thread.

## Evidence rules (non-negotiable)

- Every claim comes from THIS session's actual history or a fresh disk check — never
  from vibes. If the project has a cheap health command (validator, test suite,
  linter), RUN it and report the real output.
- Honest verification: unverified items are labeled ("NOT re-run here", "assumed").
  Failures and skipped steps are reported plainly, not hidden.
- Numbers over adjectives: bytes, counts, findings closed, baselines proven, timestamps.
- If the environment exposes live session data (e.g. cship snapshots — cost, context
  %, model/effort), fold it in; omit silently when absent.

## Dossier shape (render in this order)

1. **Header** — `# 📋 <Project/Session> — Dossier · <date>`
2. **⚡ Verdict up front** — a table answering the questions the reader would ask
   first (Did it work? What's the state? Anything broken?), each with an evidence
   cell. Badges: ✅ ⚠️ ❌.
3. **🕐 Timeline** — the session arc as a fenced ASCII line
   (`t0 ▶ phase ███ … ▶ CLOSED/NOW`), with budget-vs-used when timeboxed.
4. **🔨 What changed** — one row per touched artifact:
   `Artifact | Before → After | Impact ▰▰▰▱▱ | Why it matters`.
5. **🧠 Step-by-step, with the thinking** — table: what was done AND the reasoning
   behind each choice (why this, what was rejected, what constraints forced).
6. **🔍 Self-assessment / notes** — what worked, frictions found, honest caveats.
7. **Bottom line** — one paragraph: the state of the world now, verified.

## Style rules

- Tables + light visuals only where they aid digestion: ✅/⚠️/❌ badges, ▰▰▰▱▱ impact
  meters, fenced ASCII timelines. No decoration for its own sake.
- Lead with the verdict; supporting detail after. Dense beats verbose — every line
  earns its place (the densification law).
- Adapt section names to the work at hand; keep the SHAPE (verdict → timeline →
  changes → thinking → assessment → bottom line).

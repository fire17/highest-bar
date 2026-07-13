---
name: do-and-learn
description: One-shot "do it, then distill it" meta-skill — execute the user's request completely, verify it GENUINELY works (real runs, honest verification status), and only after confirmed success retroactively distill the whole verified flow into a generic reusable skill — the original ask generalized, the live learnings and gotchas captured from the actual attempt, and every working script/file/resource bundled — installed with a quoted argument-hint + one alias, synced into the Creations vault, logged in the Creations registry, polished, and made publish-READY (never auto-published). Use when the user types /do-and-learn or /dnl, says "do X and make a skill out of it", "do this and learn from it", "make this repeatable", "so we never have to do this manually again", "turn this into a skill after it works", or asks for any task where they also want the flow captured for reuse. Also covers the retroactive case — invoked with no arguments after work is already done in-session, it verifies and distills THAT work into a skill. When the ask references an EXISTING skill, the learnings fold INTO that skill (update, not duplicate — new skills only when genuinely warranted), every reference gets updated, and anything shipped before gets its republish staged via the ripple law (/ripple).
argument-hint: "what do you want done? it gets done, verified, then distilled into a skill"
---

# do-and-learn (alias: dnl) — do the thing, then keep the knowledge

The manual pattern this replaces: the user asks for something, you do it, it works, and
*then* they have to remember to ask "now make a great skill out of that." Same result,
two asks, and the second one often never happens — so the hard-won knowledge evaporates
with the session. This skill is the one-shot version: the request to *do* carries a
standing request to *learn*, armed from the start.

The single most important mechanic: **journal while doing, distill after verifying.**
Learnings captured in the moment (the exact error, the exact fix, the command that
finally worked) are what make the distilled skill valuable. Learnings reconstructed
afterwards are smoothed-over guesses. And a skill created *before* verified success
encodes hope, not knowledge — so skill creation is gated hard behind verification.

## Modes

- **Normal**: `/do-and-learn <ask>` — run all phases below on the ask.
- **Update an existing skill**: when the ask references a skill that already exists
  (by name, alias, or clearly by subject — "improve /shipit's X", "do this the way
  /sas does but fix Y"), the learnings flow INTO that skill: run the phases as usual,
  but Phase 3 UPDATES the referenced skill(s) instead of creating a new one. Create a
  new skill only when it's genuinely relevant — nothing existing covers the ask, or
  the user asked for both an update and a new skill. Follow the user's intent
  intelligently; when the ask is ambiguous between update and create, updating the
  existing skill is the default (skill sprawl is its own failure). Either way, every
  reference to what changed gets updated and everything relevant gets pushed — see
  Phase 4's ripple step.
- **Retroactive**: invoked with no arguments after substantive work already happened
  in-session — treat the session's work as Phase 1 already done: recover the user's
  original words verbatim from the conversation, journal what actually happened
  (including the dead ends you remember precisely because you lived them), then enter
  Phase 2 and continue.
- **Sandbox/test**: when explicitly testing this skill, write the journal AND the
  distilled skill under the caller-specified directory instead of the defaults, and skip
  vault sync and registry logging. Everything else runs identically. Sandbox artifacts
  are throwaway — the distilled skill's absolute script paths point into the sandbox, so
  don't treat it as durable or relocatable.

## Phase 0 — Capture verbatim, open the journal

Before touching the task, write the user's ask **verbatim** to a journal file —
`<scratchpad>/do-and-learn/<task-slug>/journal.md` (or the project's working dir if more
natural). The distillation phase needs the original words, not your paraphrase; and the
user's words are sacred — a generalized skill that lost the original intent can't be
checked against it.

The journal is append-only and grows through every phase. Log as you go:
- dead ends and *why* they were dead (the error text, not "it didn't work")
- the fix that worked, as the exact command/edit
- environment quirks discovered (versions, paths, permissions, timing)
- every file, script, function, or resource created or relied on — the future skill's
  dependency closure is exactly this list

## Phase 1 — Do

Execute the request fully, the way you would without this skill: use whatever existing
skills, doctrine, and tools fit. Don't let the meta-goal distort the work — the primary
deliverable is the thing the user asked for; the skill is the residue of doing it well.
Keep artifacts organized (you'll be bundling them later), and every time something
fails-then-succeeds, journal it immediately — that pair is the highest-value learning.

## Phase 2 — Verify (the gate)

Verify by **running the real thing**, end to end, the way the user would use it — not by
reading your own code approvingly. Feel-test it. Record an honest verification status
("verified live: X, Y" / "NOT yet live-verified: Z") in the journal.

**This is the gate.** Only confirmed success — all testing done, nothing unaccounted —
opens Phase 3. If the work can't reach verified success, report the honest state and
stop here: no skill. Distilling an unverified flow would launder guesses into doctrine.

## Phase 3 — Distill

Now — and only now — turn the verified flow into a skill:

1. **Generalize the ask.** Take the verbatim original and strip the incident-specifics
   (this path, this name, this one-off value) into arguments and parameters, keeping the
   intent intact. If the ask was already generic, keep it. The skill should work for the
   *class* of task, not replay the instance.
2. **Structure it per skill-creator conventions** (load the `skill-creator` skill if you
   need the details): a pushy `description` covering what it does AND when to trigger, a
   **quoted** `argument-hint`, one short **alias** (real directory + `SKILL.md` symlink —
   never a hardlink, never a dir symlink), scripts referenced by absolute path so the
   alias resolves them.
3. **Bundle the working solutions.** Every script/function/resource from the journal's
   closure list goes into the skill (`scripts/`, `references/`, `assets/`) — the versions
   that actually worked, not cleaned-up rewrites you haven't run — with executable bits
   and shebangs preserved exactly as they ran.
4. **Write the learnings in.** A gotchas/anti-patterns section where every item is
   something that actually burned during the live run, stated with its fix. This section
   is the skill's soul — it's what a fresh session cannot know.
5. **Stamp provenance.** One line in the skill noting the run that birthed it (date +
   what was done), so future readers know it was distilled from a verified live flow.

## Phase 4 — Preserve and register

- **Vault**: sync the skill AND its alias dir into the Creations vault —
  `python3 ~/Creations/Skills/sync_skill.py ~/.claude/skills/<name> [--extra-dep …]`
  — pass `--extra-dep` for closure the path-scan can't see, and quote the printed
  `✔ synced` line in your report. If `~/Creations/Skills/` doesn't exist on this
  machine, say so and skip — never silently drop the step.
- **Registry**: log the creation in `~/Creations` across all three surfaces atomically
  (`<slug>.md` entry from `_TEMPLATE.md` + README row + `index.json` object), then run
  `python3 ~/Creations/.deify/reconcile.py` to prove health. Check shared-surface
  quiescence first if parallel sessions are live. Skip (and say so) outside this
  ecosystem.
- **Ripple — mandatory when anything touched was shipped before.** Load the `ripple`
  skill (alias /rpl) and run
  `python3 ~/.claude/skills/ripple/scripts/ripple_graph.py check <changed paths>`.
  If any touched node carries a `.project` marker or is referenced by a published
  project, update every affected reference in this same pass and stage the republish
  wave for one batched confirmation. This is default-on — the user never has to ask.

## Phase 5 — Polish (last chance)

Re-read both the deliverable and the new skill with fresh eyes. This is the deliberate
final pass before anything is presented as done: fewer, more meaningful words; remove
what isn't pulling its weight; fix the rough edge you noticed but deferred. Polish beats
accretion — an overlong skill is its own regression.

## Phase 6 — Publish-ready, never auto-published

Prepare the skill so publishing is one confirmation away: set the registry entry to
`publish: ready` **with a written plan** (usually: `/shipit` on confirmation), and stage
anything publishing would need. Then STOP. Nothing leaves the machine — no push, no
post, no publish — without the user's explicit confirmation. End your report by telling
the user exactly what one word from them would trigger.

## Final report — always include

- Deliverable: what was done, where it lives.
- Verification status (honest): what was run live, what wasn't.
- Skill: path, alias, argument-hint; the vault `✔ synced` line; registry health line.
- Publish-readiness: the plan, and the explicit "say the word" ask.

---
*Provenance: distilled from its own creation run, 2026-07-06 — built under a live
`/goal`, then sandbox-tested end-to-end by an opus lane whose friction findings shaped
this file (sandbox journal placement, throwaway-artifact warning, executable-bit rule).*

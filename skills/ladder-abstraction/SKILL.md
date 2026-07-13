---
name: ladder-abstraction
description: Derive a project-specific ladder of abstraction — zoom levels over any information surface — so users fluidly move between granular data and big-picture views and ACT from every altitude. Distilled to first principles from Amelia Wattenberger's AI Engineer Summit talk (transcript + every demo ingested); AI generates the levels, glues them, preserves control. Works in any medium (GUI, TUI, CLI, API, pipeline, report, voice, agent). Use whenever designing or building ANY user-facing interface, view, dashboard, report, or navigation model; on "ladder of abstraction", "zoom levels", "overview + drill-down", "big picture", "too much information", "see everything at once"; when /highest-bar Phase 3 needs its enforcement engine; or via /ladder-abstraction or /ladder — even if none of these words appear but an interface is being shaped.
argument-hint: "<the project/surface to derive a ladder for — its data, users, and core questions>"
---

# /ladder-abstraction — climbing the ladder, from first principles

The revolution (from the founding vision, verbatim — never rewrite):

> The revolution proposed by Amelia Wattenberger lies in shifting AI from a passive
> chatbot into a dynamic interface for navigating the 'Ladder of Abstraction.'
> Instead of merely automating isolated tasks, this design philosophy enables users
> to fluidly zoom between granular data and high-level summaries, treating complex
> information like an interactive map or spreadsheet. By automating the 'stacked'
> rote processes behind the scenes, the AI acts as a lens that alleviates cognitive
> load, allowing users to remain in control and perform precise, meaningful actions
> directly from the big picture, ultimately transforming how we interact with and
> reason about information.

Source understanding: `references/talk-essence.md` — read it before deriving any
ladder. ⚠️ **Its examples are poison**: books, listings, walk-minutes, the
card→table→scatter progression exist to teach the concepts, never to be copied.
The video (youtube.com/watch?v=PAy_GHUAICw) stays the authority; `/watch` on doubt.
Founding provenance: this skill's `VISION.md` + the SelfMonitor genesis message
(2026-07-13) whose sibling demands — blazing fast, zero overhead, seamless,
live-synced — live on in Method §6 budgets and Law 9 liveness.

## The Twelve Laws

1. **Re-representation, not shrinking.** A rung shows the world in a different
   vocabulary of objects. If a higher rung's objects are a subset of the rung
   below's — same things, smaller or fewer — it is not a rung, it is cosmetic zoom.
   Abstraction granularity is also per-field: any field may carry its own local
   zoom (short/long, sparkline/series); the rung is not the smallest unit.
2. **Every rung answers one named question.** Design each altitude by asking: *what
   decision lives here, and who decides?* Then drop everything irrelevant to it.
   Two budgets force the dropping: the head (working memory) and the surface
   (pixels/lines/tokens). When the decision is multi-criteria, the next rung up is
   a trade-off space — axes, physical or semantic (risk, mood, health).
3. **Augmentation = stacked automations.** Automate exactly the rote sub-steps that
   stand between the user and their motivating question (aggregate, extract,
   summarize, curate) — behind the scenes. The trust boundary decides the split:
   tedious-and-verifiable → automate; creative, nuanced, judgment-laden → augment,
   never auto-decide. The payoff is redirected attention, not saved keystrokes.
4. **Structure over blob.** A chatbot is a calculator: general, powerful,
   unstructured. Serve typed structure at the requested altitude — in any medium —
   never an unstructured text blob as the primary surface for information work.
5. **Action at every altitude — and the ladder is a loop.** Every rung preserves
   real actions (mutating state or dispatching effects; navigation doesn't count),
   with an invariant verb vocabulary in a predictable slot across rungs. The crown
   move: a selection expression at the top rung + one batch operation over it.
   Actions may also gather information (batch-ask, probe) whose replies feed the
   decision — a loop, not a funnel. AI may pre-draft the action; the human approves.
6. **The user's deciding factors are first-class.** Elevated views strip branding
   and filler, then surface the person's OWN criteria as extracted, evidence-backed
   fields. The rung composes around the current question, not a fixed template.
   **Derived ≠ observed**: AI-derived fields are visually distinguishable from
   ground truth at a glance; provenance is a path (one consistent drill
   affordance), not a badge on every value. Elevation may overlay surfaces you
   don't own — and any lens must be dismissible in one gesture.
7. **One schema, not one box.** The same field schema over heterogeneous sources
   makes unlike things comparable side by side. A shared schema is a comparison
   contract, NOT a card template — /impeccable's bans on identical card grids and
   hero-metric tiles win over any ladder convenience.
8. **Altitude legible in the medium's own idiom.** The zoom control is first-class:
   discrete, stepped, revealing how many rungs exist and which you're on
   (`references/medium-adapters.md` for each medium's form). Transitions carry
   **focus-carry**: the user's focus object survives the zoom — highlighted inside
   its new parent going up, landed-on going down; re-representation without
   focus-carry is teleportation. Plus a compression cue (how much less there is)
   and lateral movement: next/previous peer at the same altitude. Accessibility
   floor: keyboard-operable zoom (never gesture-only), altitude announced to
   assistive tech on change, a reduced-motion alternative for every transition,
   and rung + focus encoded in the URL/state so Back zooms out and a rung is
   shareable.
9. **Bidirectional and live.** Edits at altitude propagate down to ground truth
   behind a previewed diff; ground changes ripple up live (the spreadsheet's core
   mechanic). Write at altitude, verify at ground.
10. **Working memory is the requirements document.** Whatever users juggle in their
    heads across items, tabs, or time IS the next rung — and each rung must cite
    the ground evidence (observation, log, quote, schema) that proves the need.
11. **Reversible from the sky.** Every altitude action resolves its selection to a
    visible count + expandable member list, previews the resolved diff BEFORE
    firing, and offers single-step undo AFTER. An irreversible batch action from
    the big picture is a footgun, not a crown move.
12. **No rung is privileged.** Higher is not better — the win is fluid movement
    between levels, with ground truth always reachable. Summarization is a means;
    the destination is the user's decision.

## The Method — derive THIS project's ladder

Each step writes a section of `LADDER.md` (skeleton: `assets/LADDER-template.md`)
before any surface is built. Rung specs use the typed schema in
`references/rung-spec.md`. Files: `references/talk-essence.md` (read before
deriving — its examples are poison) · `references/medium-adapters.md` (step 0 +
per-medium bars) · `VISION.md`/`SWARM.md`/`test-prompts.json` (build provenance,
not runtime reading).

0. **Declare the medium + tone source.** Pick the adapter row
   (`references/medium-adapters.md`); cite the project's design-token/brand file
   (or run /impeccable init to create one). Tone conditions the IA from the start.
1. **Ground inventory.** Real entities, sources, volumes — each with an observation
   source cited (interview line, log sample, schema, ticket). No imagined terrain;
   unobserved claims carry the flag "ASSUMED — no user data".
2. **Task-per-altitude map.** One question (ending "?") + decider + evidence per
   altitude. Rung count == number of distinct evidenced tasks — 2 is legal, 7 is
   legal; a count chosen before the task map is a template.
3. **Rung specs.** One typed YAML block per rung (schema: `references/rung-spec.md`):
   vocabulary, new_objects, dropped, representation (chosen to fit task + medium +
   tone; cards are the lazy answer), fields with locators, actions, selection,
   reversibility, edit block, automations with engine + cost.
4. **The glue.** Zoom control per the adapter; lateral peer navigation; continuity
   + compression cues; default rung per entry point; where edits-at-altitude are
   allowed and how propagation previews.
5. **Personal-relevance engine.** How deciding factors are captured — asked,
   learned from behavior, or fixed per consumer (APIs/pipelines/reports have
   consumers, not sessions) — and rendered as evidence-backed fields.
6. **Budgets.** Medium-appropriate numbers (adapter table): p95 transition latency
   measured on a stated device/volume, generation cost, freshness SLA, tokens/$
   per rung. Degradation path named. Cache invalidates on ground change — Law 9
   outranks the latency budget; a stale rung says so.
7. **Style/Convention fusion.** Per-rung concrete choices drawn from the step-0
   source — visual media: chart form, palette ref, type scale from design tokens
   (adjectives without a token path = FAIL; /dataviz loaded before any chart);
   non-visual media: flag grammar, error formats, envelope keys from the project's
   convention source (adapter table maps both).

🔴 **CHECKPOINT — LADDER.md acceptance, before building any surface.** Run tests
a–g from `references/rung-spec.md` as field predicates; paste the PASS/FAIL matrix
into the reply; keep the rung graveyard. Any FAIL → 🛑 redesign or drop the rung —
fewer real rungs beat fake ones. (First-try all-PASS + empty graveyard = red flag.)

🔴 **CHECKPOINT — act-from-the-big-picture.** Before any batch action fires: print
the exact resolved member list + count + the action; explicit user confirm;
irreversible actions require a preview/dry-run diff first. 🛑 Never auto-fire.

## Do NOT — the blacklist

- Do NOT ship cosmetic zoom — a rung whose objects ⊆ the rung below's (Law 1).
- Do NOT make chat/an unstructured blob the primary surface (Law 4).
- Do NOT build a look-only rung — no mutate-action means not done (Law 5).
- Do NOT copy the talk's examples or another project's ladder — derive from THIS
  project's evidence (Method §1–2; tests f/g).
- Do NOT keep all information visible at high rungs "to be safe" (Law 2).
- Do NOT drop information invisibly — each rung surfaces one consistent
  "what's not shown at this altitude" affordance (Law 2).
- Do NOT auto-act above the user's head — selection + preview + confirm + undo
  (Laws 5, 11).
- Do NOT strand a derived field without `from` + `locator` provenance (Law 6).
- Do NOT bury the altitude — one glance/line must name the rung (Law 8).
- Do NOT render a rung as an identical card grid or hero-metric tile row —
  /impeccable's absolute bans win (Law 7).
- Do NOT build an un-dismissible elevation over someone else's surface (Law 6).
- Do NOT treat the top rung as the destination (Law 12).

## When it breaks — failure branches

| Trigger | First fix | Still failing → |
|---|---|---|
| Rung fails an acceptance test | redesign against its named question | 🛑 drop the rung; record in graveyard |
| Rung generation slow/costly | pre-generate + cache adjacent rungs; cheap engine for rote extraction | degrade honestly: cached + "refreshing", never fake freshness |
| Data too thin for a high rung | collapse to fewer rungs | never pad with synthetic data |
| Users lost between rungs | add continuity + compression cues | fresh-user re-test; glue redesign |
| Derived field wrong/unverifiable | evidence inline + confidence mark | pull the field; one wrong first-class fact poisons trust |
| Edit-at-altitude propagates wrongly | previewed diff before apply | restrict editing to rungs covered by a round-trip test (edit → ground → re-derive → matches) |
| Batch action hit unintended members | undo; audit the selection resolver | require expandable member list review before fire |

## Boundaries — precedence, not territory

- **/impeccable + /frontend-design** own surface craft AND within-surface hierarchy;
  this skill owns **cross-altitude IA** — which rungs exist, what lives at each, how
  they connect. Run /impeccable setup FIRST (its PRODUCT/DESIGN context is the §0
  tone source); derive LADDER.md; build each rung under impeccable. **On conflict,
  impeccable's absolute bans win.** A rung expressible only as banned chrome is a
  rung designed wrong.
- **/dataviz** owns every chart, palette, and stat-tile inside a rung — load before
  drawing any rung chart. Deliverables stay local-first per /frontend-design.
- **/highest-bar** is the kickoff protocol; its Phase 3 points here — `LADDER.md`
  is the IA.md it demands. `/highest-bar-abstract` activates both as one.
- Budgets integrate with `BUDGETS.md` (highest-bar Phase 2) when present.

## Definition of done

`LADDER.md` carries its **verification table** (`references/rung-spec.md`): every
shipped surface maps to an accepted rung · every rung's a–g tests pass on the LIVE
surface · budgets met with measured numbers on a stated device/volume · at least
one act-from-the-big-picture flow works end-to-end (selection → preview → confirm
→ undo) · altitude legibility passes the adapter's fresh-user test. Untested rows
carry the literal "NOT yet live-verified" — empty evidence path = NOT DONE.

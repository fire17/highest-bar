---
name: changes-visualizer
description: "Print a colorful ASCII CARD-GRID of a project's changes/features — done vs in-progress, every card with a progress bar — DIRECTLY IN THE REPLY. A bundled Python script does all the drawing/coloring from a JSON spec; the agent gathers honest data, runs the script, and PASTES its output into the message inside a fenced code block. The whole point (and the thing that kept failing before): the boxes must appear IN THE MESSAGE THE USER READS — not buried in a tool/bash-output block, not summarized, not narrated. Use on /changes-visualizer, /cviz, 'changes visualizer', 'visualize the changes', 'boxes of changes', 'what's new as boxes/cards', 'task boxes', 'feature cards', 'card grid', 'done vs in-progress', or any ask to SEE changes/features as colored cards with progress bars."
argument-hint: "[what to card up — e.g. 'this session's changes', 'done vs todo', a project path]"
---

# /changes-visualizer — colored change/feature cards, PRINTED IN THE REPLY

A bundled script draws pixel-perfect ASCII cards (two sections — DONE and IN PROGRESS —
each card a rounded box with a colored progress bar) from a JSON spec. You never hand-draw
boxes. Your job: gather honest data, run the script, and **print its output in your reply**.

## ⛔ THE ONE RULE THAT KEPT FAILING — PRINT THE BOXES IN YOUR MESSAGE

After the script runs, **reproduce its EXACT `--no-color` stdout inside a fenced ```code
block``` in your assistant reply.** This is the entire deliverable and the thing that keeps
going wrong. Concretely:

- **In the message, not the tool result.** The boxes must appear in the reply the user
  reads — NOT left sitting only in the Bash/tool-output block, NOT described, NOT summarized.
- **`--no-color`, always, for the printed copy.** Colored ANSI paints only in a live
  terminal; pasted as text it shows raw `[96m` codes and looks broken. Print the `--no-color`
  output. (You may ALSO run the colored version for the terminal, but the copy you put in
  the message is the plain one.)
- **Verbatim, character-for-character.** The script's output is already aligned. Never
  hand-draw, retype from memory, or "tidy" the box art — only ever reproduce the script's
  real stdout.
- **The grid IS the whole reply.** No summary paragraph before or around it. At MOST ONE
  short line AFTER the grid (a legend, or an "awaiting your input on X" pointer). Don't
  narrate the cards — the cards speak.

If you find yourself writing prose about the features instead of pasting the boxes, stop:
paste the boxes.

## Do exactly this

1. **Gather the changes/features**, newest-first, split into two buckets, from whatever
   ground truth exists — `git log` / `PATCHES.md` / a `CHANGELOG` / a registry / `TODOS.md`
   / the live task list / this session's work:
   - **DONE** — shipped/landed. `progress: 100`.
   - **IN PROGRESS** — in-flight/planned, each with an **honest** `progress` 0-100 by
     evidence (substrate landed but unwired ≈ 30; designed only ≈ 5-10; built & awaiting
     user validation ≈ 90). Never invent a number — if you can't justify it, say why in the
     `desc` and use a low bar.
2. **Write a JSON spec** (schema below) to a scratch file.
3. **Run the renderer** (absolute path so aliases resolve):
   ```bash
   python3 ~/.claude/skills/changes-visualizer/scripts/changes_grid.py --no-color <spec.json>
   # colored variant for a live terminal (do NOT paste this one into the message):
   python3 ~/.claude/skills/changes-visualizer/scripts/changes_grid.py <spec.json>
   ```
4. **Print the `--no-color` output in your reply, inside a ``` fence** (see THE ONE RULE).

## JSON spec

```json
{
  "title": "HERDR++  —  CHANGES",
  "subtitle": "fire17's patched fork of herdr  ·  59 patches",
  "sections": [
    {"name": "DONE", "accent": "green", "cards": [
      {"id": "0058", "title": "Startup session picker",
       "desc": "Pick a session from both roots on launch; d sets default.",
       "tag": "live", "progress": 100}
    ]},
    {"name": "IN PROGRESS", "accent": "yellow", "cards": [
      {"id": "Ph3b", "title": "Self-extend harness",
       "desc": "Wire the build agent + hotload; gated on the user's call.",
       "tag": "gated", "progress": 30}
    ]}
  ],
  "stats": ["59 patches  ·  2646 tests green  ·  HEALTHY",
            "HEAD bc8c288  ·  series == branch"]
}
```

- **Card fields:** `id` (patch #, phase, ticket — short), `title` (a few words), `desc`
  (one sentence; wraps to 3 lines, longer is truncated), `tag` (one status word — palette
  below), `progress` (0-100).
- **`tag` palette:** `live`=green, `gated`=yellow, `exp`=magenta, `inert`/`safe`=blue,
  `dev`/`docs`=cyan, `next`=bright-yellow, `planned`/`wip` handled too; unknown → cyan.
- **`accent`** colors a section's headers (`green`, `yellow`, `cyan`, `magenta`, `red`,
  `blue`…). Convention: DONE=green, IN PROGRESS=yellow.
- **Progress-bar color is automatic:** 100=bright-green, ≥67=green, ≥34=yellow, >0=red,
  0=dim.
- **`stats`** — optional centered footer lines.

## Rules

- **Honesty over vanity.** Bars must reflect real state; a 100% bar on unfinished work is a
  lie the user will act on. Reserve 100 for actually-landed.
- **Newest-first** within each section.
- **Two sections is the point** — always render DONE and IN PROGRESS (omit one only if it's
  genuinely empty, and say so).
- The script is the single source of layout/color truth. If a card looks wrong, fix the
  DATA, not the drawing. Reads at most one spec; no network, no state.
- Grid is 2 columns × 40-col cards (82 wide); fits a standard terminal.

## Gotchas (burned live during this skill's own creation, 2026-07-06)

- **Boxes in the tool result ≠ boxes in the reply.** Running the script via Bash leaves the
  output in a tool-output block the user may never see prominently. It must be re-emitted
  IN the assistant message. This was the #1 repeated failure of the old `/features-grid`.
- **Colored output pasted as text = garbage.** `[96m…[0m` codes render as color only in a
  live terminal. For the message copy, always `--no-color`.
- **Commentary drowns the grid.** The skill's job is the boxes; a summary paragraph around
  them defeats the purpose. Boxes first and essentially only.

---
*Provenance: distilled via /dnl on 2026-07-06 from a live run where the renderer was perfect
but the invocation contract (print-in-reply) kept failing three times before it clicked.
`/features-grid` is an alias of this skill; the pre-rewrite version is stashed under
`(pre-merge archive on origin machine)`.*

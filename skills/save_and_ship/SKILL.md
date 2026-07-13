---
name: save_and_ship
description: Saves To Creations + Ships it — if already exists, and there are changes — then it updates and republishes changes. For more details — checkpoint the CURRENT session so its work outlives the context window, then publish it — snapshot the entire conversation transcript + every file and skill produced (or needed to continue in a fresh space) into ~/Creations/<ProjectName>, register it in the Creations registry, and chain into /shipit. Idempotent, and it never ships for nothing — a delta gate checks the manifest and skips /shipit when nothing changed. Use when the user types /save_and_ship or /sas, says "save this session/conversation", "snapshot our work", "preserve what we built", "back this up into Creations", "checkpoint and ship/publish", or when a build session is wrapping up and its artifacts deserve to survive — even if they only say "save" or only say "ship", this skill covers both halves.
argument-hint: "[ProjectName] [--no-ship] — name inferred from the session when omitted"
---

# save_and_ship (alias: /sas) — checkpoint the session, then ship it

One move, two halves. **Save**: make this session's work survive context death — the
verbatim conversation, every artifact, and a briefing a fresh session can continue from.
**Ship**: hand the result to /shipit. Idempotent by design: the first run creates the
snapshot; every later run syncs deltas and asks whether the world should see them.

## Phase 0 — Mode & name

- **Project name**: an explicit argument wins. Otherwise check whether a snapshot already
  claims this work (`grep -l <session-id> ~/Creations/*/.save_and_ship/manifest.json`),
  else infer from the session's subject / cwd / dominant artifact. If genuinely ambiguous,
  ask in one line — a wrong name here haunts the registry forever.
- **Mode**: `~/Creations/<ProjectName>/.save_and_ship/manifest.json` exists → **UPDATE**;
  absent → **FRESH**. `--no-ship` limits either mode to the save half (a pure checkpoint).

## Phase 1 — Locate YOUR transcript (session-exact, never newest-file)

Parallel sessions share the same project bucket, so picking the newest `.jsonl` cross-maps
sessions (an observed bug class on this machine). Prove identity with a nonce instead:

```bash
NONCE="sns-$(python3 -c 'import uuid; print(uuid.uuid4().hex[:12])')" && echo "$NONCE"
# bucket = cwd with '/' → '-', e.g. /Users/magic/Proj → -Users-magic-Proj
sleep 2 && grep -l "$NONCE" ~/.claude/projects/<bucket>/*.jsonl
```

Exactly one hit is your transcript (the filename stem is your session id). Zero hits →
flush lag; wait 2s and re-grep. Multiple hits → stop and investigate, never guess.
If `~/.cship/live/<session-id>.json` exists, capture it too — model/cost/effort provenance
for the manifest.

## Phase 2 — Harvest what the session produced

- **Deterministic pass**:
  `python3 ~/.claude/skills/save_and_ship/scripts/harvest.py <transcript.jsonl>`
  → JSON of every file Written/Edited, every skill invoked, and which of those paths
  still exist. (Read-only, stdlib-only; pass subagent transcripts as extra args.)
- **Judgment pass** — harvest sees only tool calls, so add what it structurally cannot:
  files created via Bash (redirects, `cp`, generators, installers), skills created this
  session under `~/.claude/skills/`, and *related* files a fresh session would need to
  continue — configs, referenced scripts, the docs that shaped decisions.
- **Exclusions**: scratchpad/temp dirs, caches, build artifacts, and **secrets** (`.env`,
  keys, tokens) — never copy secrets into ~/Creations; list their original paths in
  CONTINUE.md instead so a fresh session knows they exist.
- Everything is **copy, never move**. The live world stays exactly as it is.

## Phase 3 — Write the snapshot

```
~/Creations/<ProjectName>/
├── CONTINUE.md                    # the fresh-space briefing — the point of it all
├── conversation/<sid>.jsonl       # verbatim transcript copy (+ subagents, cship snapshot)
├── files/…                        # produced/related files, source structure preserved
├── skills/<name>/…                # skills born or reshaped this session
└── .save_and_ship/manifest.json   # source→dest map, sha256s, session ids, timestamps
```

- **CONTINUE.md** is written for a fresh Claude with zero context: what this project is
  and why, current state (honest — what works, what's untested), the exact original
  location of every copied file, how to resume (`claude --resume <sid>` from the original
  cwd, or read `conversation/`), and concrete next steps. A snapshot without it is a pile
  of files; with it, the directory IS the project.
- Transcript copies are **SACRED verbatim** — never edit, trim, or reformat; verify each
  copy with `cmp` *immediately* after copying. The live transcript keeps growing while
  you work (this very run appends to it), so in the manifest mark conversation/cship
  copies `point_in_time: true` and record the sha256 of the **copy**, not the source —
  asserting source==dest there fails by design moments later (observed on the first
  dogfood run).
- **UPDATE mode**: compute the delta set first — sources whose sha256 changed plus newly
  harvested files — and re-copy only those; add this session's transcript alongside the
  earlier ones. Record the delta set in the manifest: Phase 5's ship gate reads it. If a
  *destination* file was hand-edited (dest hash ≠ manifest hash), never clobber it —
  write the fresh copy as `<file>.new-<YYYY-MM-DD>` beside it and flag the conflict in
  the report.
- **Skills also go to the vault — both, always.** If the work being saved includes a
  *skill* (developed, saved, or published this session — harvest's skills list plus the
  judgment pass over `~/.claude/skills/`), ALSO sync each one AND each of its aliases
  into the Creations Skills vault with its full dependency closure:
  `python3 ~/Creations/Skills/sync_skill.py <skill-dir> [--extra-dep …] --category <fit>
  --note "<provenance>"`. The two copies serve different masters and neither replaces
  the other: `~/Creations/<ProjectName>/skills/` is the frozen point-in-time snapshot
  (history), while `~/Creations/Skills/<category>/<name>/` is the living
  current-version library (INDEX.md + `.provenance.json` are its record). Skipping the
  vault half leaves the library stale the moment the skill evolves — this is the
  registry-wide vault law (see ~/Creations/CLAUDE.md), enforced here so no /sas run can
  forget it.

## Phase 4 — Register in the Creations registry

The snapshot lives inside the registry, so it must be an entry — three surfaces changed
atomically, per `~/Creations/CLAUDE.md`: `<slug>.md` from `_TEMPLATE.md` + a README index
row + an `index.json` `creations[]` object; bump the entry's `updated:` and index.json's
top-level `updated:`; UPDATE runs leave a `> YYYY-MM-DD: …` changelog note.

Collision safety first (other sessions write these surfaces daily): confirm README.md and
index.json are quiescent (untouched ≥3 min), re-read both fresh, and bracket the write
with `python3 ~/Creations/.deify/reconcile.py` — it must exit 0 after, or stop and fix
before anything else.

## Phase 5 — Ship (only when there is something to ship)

- **Delta gate first — never ship for nothing.** In ANY mode, before touching shipit,
  check what actually changed since `last_shipped` (or since nothing, on a first save):
  the manifest's recorded delta set of changed/new files and skills. Artifact deltas
  justify a ship; conversation growth alone does not — a longer transcript is a reason
  to re-save, never to re-publish. Empty delta set → report "snapshot refreshed —
  nothing to ship" and end here; that outcome is a success, not a shortfall.
- **FRESH** (or saved-but-never-shipped): invoke the **shipit** skill on
  `~/Creations/<ProjectName>` — it owns the release gates (edge-case design, runtime-matrix
  tests, install-from-published-channel verification) and it *asks* before anything leaves
  the machine, so chaining into it is always safe.
- **UPDATE + already published**: the gate passed, so propose the update ship (version
  bump, release notes, formula/installer refresh) via shipit's publish/retrospect phases.
- **The README gate (/awesome-readme) — mandatory before true completion.** Whenever the
  run touches a public repo surface (fresh ship or update), load the **awesome-readme**
  skill and hold the repo's README to its bar — the 13-element checklist + the live
  verification battery (banner content-type, badge URLs, anchors vs GitHub's rendered
  ids, links, observed numbers, CI green). Add it to the run's todo list at start; skip
  ONLY when no public repo surface was touched, and record that reason in the report.
- **The .project marker (ripple gate)** — a first ship CREATES `<project>/.project/`
  (DIR form with a `status` file inside — default for anything pushed to GitHub, so
  richer state stores naturally as sibling files; a plain `.project` file is fine for
  local-only work), and every later ship refreshes `last_shipped`/`version`. Its
  presence means "published before → changes here always ripple". Spec:
  `~/.claude/skills/ripple/references/project-file.md`; tool:
  `python3 ~/.claude/skills/ripple/scripts/ripple_graph.py ensure-project <slug>`.
- **The ripple law (/ripple, alias /rpl) — default-on, runs BEFORE the report.** Run
  `python3 ~/.claude/skills/ripple/scripts/ripple_graph.py check <changed paths>`.
  When anything this run changed was shipped before (or is referenced by a published
  project), update every affected reference (vault copies, aliases, snapshots,
  doc-mentions, registry entries) in the same pass and STAGE the republish wave of all
  affected published projects — ONE batched confirmation covers the whole wave. The
  user must never have to remind us to update references and republish related projects.
- Record the outcome in the manifest (`last_shipped`, version) and the registry entry.

## Phase 6 — Verify & report honestly

Close with a verification table, each row observed rather than assumed: transcript copies
`cmp`-identical · files copied == manifest count · reconcile HEALTHY · CONTINUE.md present
and self-sufficient · ship gate outcome. Anything not live-verified is reported as
exactly that: "NOT yet live-verified".

**End with the repo links — HARD LAW, zero exceptions, every run.** Every /sas report —
fresh, update, or delta-gate-skipped — ENDS with a repo-link block: EVERY repo CREATED
and EVERY repo UPDATED by the run, each labeled (`🆕 created:` / `🔄 updated:`), release
links beside them where they exist; a table when more than one. When the project has
never been published, the block's line is the explicit `not published — no repo yet` so
the absence is loud, never silent. NOTHING may follow the link block — it is the
report's mandatory last content, and a report without it is an UNFINISHED run (hardened
2026-07-06 because a run ended without the link and the user had to ask). This is
shipit's close-with-the-links law, inherited verbatim; chained runs surface the links
themselves, never assuming shipit's print was seen.

## Anti-patterns (each defends a real failure mode)

- Picking the transcript by newest-mtime — parallel sessions cross-map; the nonce exists
  to kill this.
- `mv` instead of `cp` — the checkpoint must never disturb the live world it preserves.
- A snapshot without CONTINUE.md — unusable in a fresh space, which was the whole point.
- Writing README/index.json without the quiescence check + reconcile bracket.
- Claiming "shipped" without shipit's install-from-published-channel gate.
- Shipping when nothing changed — the delta gate exists so /shipit never runs for
  nothing; re-publishing an unchanged project wastes the channel and the reader's trust.
- Overwriting snapshot-side hand edits on a re-run.
- Copying secrets into ~/Creations.
- Ending the report without the repo-link block (or with anything after it) — the links
  are the mandatory last content of every run's report.
- Touching a public repo surface without the /awesome-readme gate — or skipping it
  silently instead of recording why it didn't apply.
- Finishing a run that changed something shipped-before WITHOUT the ripple check —
  stale references and outdated published dependents are exactly what the ripple law
  (/ripple + .project markers) exists to prevent; a missing check is an unfinished run.

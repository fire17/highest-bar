# THE MAP — /highest-bar full nested-skill closure (v2)

Derived 2026-07-13 by 6 parallel Opus mappers; hardened by adversarial miss-hunt
cycle 1 (2 hunters: 16 findings, all resolved below); cycle 2 verified clean.
Legend: 📄 markdown-only · ⚙ has code · 🔗 symlink · 🧩 plugin/builtin ·
📚 external payload · ⛔ hard blocker · ⚠ degraded/annoyance

**Alias law (shapes every copy operation):** an alias is a REAL DIR whose
`SKILL.md` is a RELATIVE file-symlink to the canonical skill's SKILL.md. Copy
with symlinks preserved (`cp -R`, never `-RL`) and always ship alias + canonical
together. Alias pairs in this closure: sas→save_and_ship · dnl→do-and-learn ·
wargame→wartable (canonical dir wartable ships too, so both names register)
· pyr→pyramid · epp→engineering-principles-pro · ep + engineering-principals→
engineering-principles · sol→master_engineering · mkalias→skill-alias ·
cviz→changes-visualizer · fable→fable_mind (Tier-3, not shipped) · awr→awesome-readme ·
grand-start→highest-bar · hba→highest-bar-abstract · ladder→ladder-abstraction.

## Tier 0 — the core (this repo's own skills)

| Skill | Contents | Live refs out | Blockers |
|---|---|---|---|
| 📄 highest-bar | SKILL.md (~210L) + assets/kickoff-message.md + test-prompts.json | stack (Tier 1) + /workflow-model-guard /ladder-abstraction /highest-bar-abstract /watch /darwin-skill /mindblown /zenith* | one `~/.claude/...` path (kickoff asset pointer) |
| 📄 highest-bar-abstract (+hba) | SKILL.md (composition) | /highest-bar /ladder-abstraction /impeccable | none |
| 📄 ladder-abstraction (+ladder) | SKILL.md + references/{talk-essence,rung-spec,medium-adapters}.md + assets/LADDER-template.md + test-prompts.json + VISION.md(+sha256) + SWARM.md + .activation-ledger.md — all internal links verified resolving | /highest-bar(-abstract) /impeccable **/dataviz** (builtin) **bare /frontend-design** (must resolve → vendor mandatory) /watch /ladder | do-not-ship: `.skill-r0.bak` |
| 🔗 grand-start | alias dir | — | — |

## Tier 1 — the activation stack (ledger skills; missing ✅ = build HALT)

| Skill | Payload | Runtime | Blockers |
|---|---|---|---|
| ⚙ impeccable | 97 files 2.2MB: 62 .mjs + 5 .js + command-metadata.json + 28 reference/*.md | node ≥18; optional puppeteer+Chrome, @babel/parser, npx impeccable | ⚠ `allowed-tools` glob is project-relative → per-script permission prompts when installed at ~/.claude (annoyance, not block); browser flows dead without npm deps (static flows fine); writes `.impeccable/` into user project |
| 🧩 frontend-design:frontend-design | plugin (claude-plugins-official): SKILL.md + LICENSE, zero scripts | none | ⛔ fresh machine: `/plugin install frontend-design@claude-plugins-official` OR vendored plain `frontend-design/` dir — vendoring is MANDATORY because ladder-abstraction references the bare name |
| 📄 wargame→wartable | wartable/SKILL.md + .project (published fire17/wartable); wargame = alias dir | /goal only | ship both dirs |
| 📄 unknowns | ⛔ dir is ABSOLUTE symlink → ~/Creations/unknowns/skills/unknowns; real payload = **1 file (SKILL.md)** | none | de-symlink = copy 1 file; no outbound skill refs |
| 📄 mindblown-fast + mindblown | 2 SKILL.md (fast delegates by path) | none | ship both; Gantry degrade line now written into mindblown (2026-07-13) |
| 📄 engineering-principles-pro (+epp) | SKILL.md 23K | none | deep-dive index → ep bundle (ship together); refs /wartable (404-by-name, /wargame works) + /doctrine |
| 📄 engineering-principles (+ep, engineering-principals) | 336K: SKILL.md + REPORT.md + references/QUOTES.md (181K) + references/skills/ bundle of 7 (doctrine·ponytail·tracks·wartable·unknowns·workflow-model-guard·skill-alias w/ ⚙skill_alias.py) + MANIFEST.md | python3 stdlib | self-contained ✅ |
| 📄 master_engineering (+sol) | SKILL.md 22K — pointer skill | none | ⛔ needs 📚 the_senior/ payload (25 files 352KB: book 95K + 20 volumes + README + video/) + **TWO** path rewrites (frontmatter description ~-path AND body /Users/magic absolute); optional provenance dep senior_cv (skip) |
| 📄 ponytail | SKILL.md 3.9K self-contained | none | DEFERRED law: builder subagents only, tmux, post-design |

## Tier 2 — machinery invoked by the core

| Skill | Payload | Runtime | Blockers |
|---|---|---|---|
| 📄 workflow-model-guard | SKILL.md | none | refs /doctrine /pyramid |
| 📄 doctrine | SKILL.md (14K) + DOCTRINE.md (14K) — referenced by wmg, ep, epp | none | mentions ~/Creations/nexus + ~/Tokenomics paths as EXEMPLARS only (never read) — non-fatal off-machine; vendored copy also inside ep bundle |
| 📄 awesome-readme (+awr) | SKILL.md 12K + .project/status; MANDATORY README gate of save_and_ship (Phase) + ShipIt (Phase 6½) | none | exemplar dep ~/Creations/Fable-Masterclass/README.md (live: github.com/fire17/fable-masterclass) — off-machine: fetch from GitHub or proceed with the skill's own criteria, note the degrade |
| ⚙ watch | live: 68 files sans .git; shipped after strip: 31 — scripts/ 7 .py + build-skill.sh, hooks/{hooks.json, scripts/check-setup.sh}, commands/watch.md, .claude-plugin/{plugin.json,marketplace.json}, tests/ (10 .py), LICENSE/README/CHANGELOG/test-prompts.json/.github/ | ⛔ yt-dlp, ffmpeg, ffprobe; pip whisper engine (+~1.5GB model, first captionless run); config ~/.config/watch/.env | 3rd-party upstream (mathiaschu/watch) with local darwin-branch mods; hooks use ${CLAUDE_PLUGIN_ROOT} (plugin ctx) but SKILL.md self-locates via $SKILL_DIR ✅; own installer + honest degrade table ✅; strip .git/.pytest_cache/__pycache__ |
| ⚙ darwin-skill | SKILL.md + references/ (3 md) + results.tsv + test-prompts.json | git (ratchet; .bak fallback documented), node+playwright (cards) | known dead refs: scripts/screenshot.mjs + templates/*.html DON'T EXIST — result-card rendering dead code, activation unaffected |
| 📄 pyramid (+pyr) | SKILL.md + .project (published fire17/pyramid) | tmux, herdr*, ~/.cship* | refs /workflow-model-guard /engineering-principles /master_engineering; tmux→Agent-tool degrade documented ✅ |
| 📄 tracks | SKILL.md | none | /tokenomics /effort-set refs have degrade text ✅ |
| ⚙ features-grid + changes-visualizer (+cviz) | SKILL.md ×2 + changes_grid.py (byte-identical dupe ×2, stdlib, md5-confirmed) | python3 | ⛔ BOTH SKILL.md twins hardcode /Users/magic/... (patch sites :49,:51 / :48,:50 → $HOME on install) AND both cite `~/.claude/skills/.archive/...` provenance (:113 each) — dead pointer off-machine, patched to "(archive on origin machine)" in repo copies |
| 📄 progress-report + report | 2 SKILL.md | jq, date; ~/.cship* | ⚠ cship-absent fallback names /checkwindow+/identify which are Tokenomics-symlinked (would 404) — install note: "no live session data → report N/A honestly" |
| ⚙ ripple (+rpl) | SKILL.md + scripts/ripple_graph.py (494L stdlib) + references/project-file.md | python3 | HARD dep of do-and-learn+save_and_ship+shipit; strip scripts/__pycache__ |
| 📄 do-and-learn (+dnl) | canonical dir: SKILL.md; dnl = alias | python3 | Creations-registry-coupled (degrades off-machine) |
| ⚙ save_and_ship (+sas) | canonical dir: SKILL.md + scripts/harvest.py + .project (published fire17/save-and-ship); sas = alias | python3 | ⛔ assumes ~/Creations registry (reconcile.py, index.json, CLAUDE.md) — off-machine: registry steps skip |
| ⚙ shipit (+sota) | skill dir = ⛔ TWO ABSOLUTE symlinks (SKILL.md + references/) → ~/Creations/ShipIt (git repo, published fire17/shipit, has install.sh with copy mode); plus stale SKILL.md.bak (don't ship) | gh (authed), git, brew/npm* | install via ShipIt/install.sh copy mode |
| ⚙ skill-creator | SKILL.md + 13 non-md: scripts/ 9 .py (run_eval, run_loop, package_skill, quick_validate, improve_description, aggregate_benchmark, generate_report, utils, __init__), eval-viewer/{generate_review.py, viewer.html}, assets/eval_review.html, LICENSE.txt + agents/ + references/ md | python3; `claude -p` (description opt) | refs /identify + identify.py (evidence layer — degrade); vault law → sync_skill.py (bundle: 179L stdlib) |
| ⚙ skill-alias (+mkalias) | SKILL.md + skill_alias.py (stdlib) | python3 | writes ~/.claude/skills (also knows ~/.codex, ~/.cursor roots) |

## Tier 3 — optional / environment (documented degrades, not bundled)

| Thing | Why optional | Story off-machine |
|---|---|---|
| 🧩 dataviz, artifact-design | built into claude-code binary (no files on disk — verified) | present wherever current claude-code runs |
| zenith | MCP + ~/welcome checkout + uv | highest-bar failure table covers absence ✅ |
| gantry family | ABSOLUTE dir-symlinks → ~/Creations/Lively/gantry (unpublished) | mindblown degrade line written 2026-07-13 ✅; highest-bar table row added ✅ |
| fable→fable_mind | every ref points into ~/Creations/Lively/Fable-a-Fable.md (personal book) | mindblown lists parenthetically; absence tolerated |
| tokenomics, identify, checkwindow, cship-data, effort-set | fire17 infra (cship/nexus/Tokenomics; checkwindow = absolute symlink → Tokenomics) | callers degrade; progress-report note above |
| herdr, nexus, ~/.cship, ~/.gantry, ~/.nexus | machine infra; ~/.nexus referenced NOWHERE in Tier 0-2 (verified) | out of scope |
| senior_cv, engineering-principles-quick-essentials (+epq), ytai | provenance-only / 3rd edition / false-lead (prose path, not a ref) | skip |

## Graph (who loads whom)

```
highest-bar ─┬─ impeccable (node toolchain, self-contained refs)
             ├─ frontend-design:frontend-design 🧩 (+ vendored bare /frontend-design)
             ├─ wargame(→wartable)
             ├─ unknowns ── report
             ├─ mindblown-fast ── mindblown ─┬─ pyramid(→ep, →master_engineering, →wmg)
             │                               ├─ tracks (→tokenomics*, →effort-set*)
             │                               ├─ gantry* (degrade written)
             │                               ├─ do-and-learn(dnl) ── ripple ── skill-creator (→identify*)
             │                               ├─ save_and_ship(sas) ── ripple · sync_skill.py · registry*
             │                               ├─ shipit ── ripple · gh · awesome-readme(awr)
             │                               ├─ save_and_ship ── awesome-readme (README gate)
             │                               ├─ progress-report ── report (· cship*)
             │                               ├─ features-grid ⇄ changes-visualizer (script dupe)
             │                               └─ fable* · master_engineering · epp
             ├─ engineering-principles-pro ── engineering-principles (+ 7-skill bundle incl doctrine)
             ├─ master_engineering ── 📚 the_senior/ (book + 20 volumes, 352KB)
             ├─ ponytail (DEFERRED: builder subagents, tmux, post-design)
             ├─ workflow-model-guard ── doctrine · pyramid
             ├─ watch (⚙ yt-dlp/ffmpeg/whisper*) ── skill-creator
             ├─ darwin-skill (git; judge subagents; dead card-render refs)
             ├─ ladder-abstraction ── impeccable · dataviz🧩 · /frontend-design (bare) · watch
             │        └─ highest-bar-abstract (hybrid)
             └─ zenith* (pointer; failure-table fallback)
                                     (* = optional/degradable, documented)
```

## Do-not-ship list (stale/junk found by hunters)

`ladder-abstraction/.skill-r0.bak` · `shipit/SKILL.md.bak.20260706-060448` ·
`ripple/scripts/__pycache__/` · `watch/{.git,.pytest_cache,__pycache__}` ·
`~/.claude/skills/.archive/` anything.

## Fresh-machine verdict

Markdown core + 8 stdlib-python scripts + one node toolchain (impeccable) + one
352KB book payload + 1-file unknowns payload + vendored frontend-design md.
Hard binaries: python3, node ≥18. Optional: ffmpeg/yt-dlp/whisper (watch),
puppeteer+Chrome (impeccable live/URL), gh (shipit), tmux (pyramid), git
(darwin ratchet). Repo-build patches (applied by build_repo.sh, verified): features-grid +
changes-visualizer $HOME paths + archive-pointer neutralized (both twins),
master_engineering body path → ~ form, shipit copy-mode, unknowns de-symlinked,
`.project` markers stripped (they carry fire17's publish identity). install.sh
prints skipped-as-stale names and refreshes payloads on --force. Everything
else degrades along written failure branches.

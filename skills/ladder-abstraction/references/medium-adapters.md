# Medium adapters — the ladder in every surface's own idiom

The ladder is not a GUI pattern. Method step 0 declares the medium; this table
translates the four load-bearing concepts into that medium's native idiom. Rows are
starting points — a project may define its own adapter, but it must fill all four
columns.

| Medium | A RUNG is | The ZOOM CONTROL is | ACT-AT-ALTITUDE is | PROVENANCE is |
|---|---|---|---|---|
| GUI (web/app) | a view with its own object vocabulary | persistent discrete stepped control (slider/keys), rung count visible, minimap showing compression | selection (lasso/filter) → resolved count + member list → previewed batch action + undo | drill-down path; evidence quotes on derived fields |
| TUI | an output pane/mode | keybound levels + breadcrumb line naming the altitude | filtered selection + one batch command, `--dry-run` first | `:explain <id>` opens source rows |
| CLI | an output mode / verbosity tier | `--level N` / `-v..-vvv`; header line names the altitude | batch command over a filter expression, `--dry-run` default for mutations | `--explain <id>` prints source lines |
| API | a response projection | `?depth=` / `Prefer: level=`, echoed in the response envelope | batch mutation over a selection query, dry-run flag + idempotency key | `_source` links per derived field |
| Data pipeline | a materialized view/table per altitude | choosing which view to read; lineage names its level | a job over a selected set, staged-then-applied | column-level lineage to source rows |
| Scheduled report | a section per altitude (headline → appendix) | section order + "expand" links to deeper rungs | recommended-actions block with exact commands, never auto-fired | footnotes/links to underlying records |
| Voice | an answer length/altitude tier | "more detail / zoom out" verbal commands; altitude stated in the answer | confirm-gated batch intent ("message all three?") | "how do you know?" reads the evidence |
| Agent-facing | a typed summary schema per altitude | a `level` parameter in the tool/contract | batch tool-call over an explicit id list, echoed before commit | source ids carried in every derived field |

## Per-medium legibility test · budget bars · tone source

These make the rung-spec verification table enforceable outside GUI (starting bars —
tighten per project, never loosen silently):

| Medium | Legibility test (fresh-user, n≥3, 3/3 pass) | Budget bars | Tone source (§7) |
|---|---|---|---|
| GUI/TUI | name current rung unaided within 5s on screen | p95 transition ≤100ms on stated device+volume | design tokens / brand file |
| CLI | name the level from one screen of output (header line) | first output ≤500ms; `--explain` ≤1s | the tool's flag grammar + help style |
| API | name the level from the response envelope alone (fresh integrator) | p95 ≤200ms, payload ≤50KB/rung, ≤$0.01/rung | API style guide / error-format contract |
| Pipeline | name a view's altitude from its schema+lineage docs | recompute cost stated; freshness SLA met | warehouse naming conventions |
| Report | name the section's altitude from its heading | generation ≤stated cost; staleness stamped | report house style |
| Voice | answer states its own altitude; user repeats it back | answer starts ≤1.5s | the assistant's persona guide |
| Agent-facing | consumer echoes `level` from the payload | schema-validated; tokens/rung stated | the tool contract |

For non-visual media, Method §7 "Style fusion" reads as **Convention fusion**: flag
grammar, error formats, envelope keys, naming — cited from the project's own
convention source. The token-path FAIL rule bites only visual media.

Universal invariants: the current altitude is always legible in one glance/line/
field (Law 8); tokens/$ per rung generation stated in LADDER.md §6.

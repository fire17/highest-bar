# LADDER.md rung-spec schema + acceptance machinery

Every rung in `LADDER.md` is a typed YAML block. The acceptance tests are field
predicates a reviewer can check by grepping the artifact — compliance is verifiable,
not claimed.

## The schema (fixed keys, per rung)

The example below is deliberately from a NON-GUI medium and an unglamorous domain
(a CLI fleet-log tool) so it cannot be copied as a design. Field meanings, not
values, are the schema.

```yaml
- rung: 2
  medium: cli                                     # from the medium adapters table
  task: "Which hosts need a restart this shift?"  # QUESTION form ending in "?"; one decision
  decider: "the on-duty operator"                 # who answers it
  evidence: {claim: "ops juggle ~30 host tabs", locator: "issue #412, shadow notes 6/12"}  # locator REQUIRED — an evidence string without a checkable source is fabrication
  objects: [host-health, restart-candidate]       # vocabulary at this altitude
  new_objects: [restart-candidate]                # non-empty; absent from the rung below
  dropped: [raw-log-lines, per-process-memory]    # non-empty; real field names from §1 inventory
  representation: "aligned table, one host/line, --level 2 header names the altitude"
  fields:
    - {field: flap_count_24h, from: "journald restart events", locator: "--explain <host>", confidence: extracted}
  actions:                                        # ≥1 kind:mutate; navigation/read does NOT count
    - {name: drain, kind: mutate, scope: item}
    - {name: restart-selected, kind: mutate, scope: batch}   # top rung: ≥1 scope:batch
  selection: "filter expression resolves to printed host list + count"
  reversibility: {preview: "--dry-run diff before fire", undo: "undrain / restart-abort"}
  edit: {fields: [], propagation: none, reason: "read-only rung"}   # explicit, never omitted
  automations: [{step: classify-flapping, engine: cheap-model, cost: "$0.001/host"}]
```

## Acceptance tests — field predicates (the 🔴 checkpoint)

| # | Test | Predicate (greppable) |
|---|---|---|
| a | Named task | `task` is a question ending `?` + `decider` named + `evidence` has BOTH claim and locator (a checkable source path/link — a bare quote string is fabrication and FAILS) |
| b | Changed vocabulary | `new_objects` non-empty AND disjoint from rung-below `objects`. objects(N) ⊆ objects(N−1) → FAIL (that IS cosmetic zoom) |
| c | Dropped information | `dropped` non-empty, names real fields from the §1 ground inventory — AND the rung surfaces a "what's not shown at this altitude" affordance (one consistent control) |
| d | Preserved actions | ≥1 `kind: mutate` (mutates state / dispatches side-effect); top rung additionally has `scope: batch` with `selection` + `reversibility` filled |
| e | Provenance | every `fields` row has `from` + `locator`; row count == derived fields rendered |
| f | Anti-template swap | strip the project's nouns: if the ladder still reads valid for another project, it IS a template → FAIL |
| g | Uniqueness | ≥1 rung no project in a different domain could reuse |

## Required artifacts inside LADDER.md

- **Acceptance matrix** — rows = rungs, cols = a–g, PASS/FAIL per cell, pasted into
  the reply when the checkpoint runs. A first-try all-PASS with an empty graveyard is
  a red flag, not a win.
- **Rung graveyard** — rungs designed then dropped, each with the test that killed it.
- **Verification table** (the Definition of Done) — one row per claim:
  `claim | how tested | date | result | evidence path`. Numeric bars and the
  legibility test come from the medium's row in `medium-adapters.md` (e.g. GUI:
  p95 transition ≤100ms measured on a stated device + volume, fresh-user n≥3
  3/3 within 5s; API: p95 ≤200ms, payload ≤50KB/rung, integrator names the level
  from the envelope). Tighten per project, never loosen silently. The only legal
  placeholder is the literal string "NOT yet live-verified". Empty evidence
  path = NOT DONE.

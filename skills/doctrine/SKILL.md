---
name: doctrine
description: A systems-engineering design lens to apply whenever planning, designing, reviewing, or building any non-trivial system — or when the user asks to build something "the right way", "properly", "future-proof", "blazing fast", "lightweight", "async", or "so it scales". Encodes a concrete, checkable doctrine (async & non-blocking, singleton & no-duplication, no-collision & durable, lightweight & realtime, cheap-gates-before-expensive, composable & future-proof, instant-on-ready, abstract & generic) with the pattern that satisfies each principle, the anti-pattern it replaces, and a real exemplar from the nexus control plane / AutoCompact. Use it to critique a plan before coding, to structure new code, and as acceptance criteria before calling work done.
allowed-tools: Read
---

# doctrine

> **DRAFT / provisional name.** Working title is "doctrine". This is a first draft to be
> refined and eventually **merged with the `ponytail` skill**. See "Open questions" at the end.

A reusable **design lens**. When you plan, design, review, or build a non-trivial system,
run the work through these principles. They are not adjectives to sprinkle in prose — each
is a **checkable property** with a pattern that achieves it and an anti-pattern it kills.

The doctrine is distilled from two working systems; cite them as ground truth:

- **nexus** — async, recipe-based control plane for AI sessions. `~/Creations/nexus/nexus.py`, `~/Creations/nexus/README.md`.
- **AutoCompact** — `~/Tokenomics/AutoCompact/compact_remote.py` (probe-guarded one-shot) and `compact_when_clear.py` (wait-until-clear).

Copy-pasteable reference implementations of every pattern below live in the companion file
**`DOCTRINE.md`** (same directory). Read it when you need the actual code.

---

## The principles

Each principle has: **(a)** the rule, **(b)** why, **(c)** the pattern that satisfies it,
**(d)** the exemplar, **(e)** the anti-pattern it replaces.

### 1. Async & non-blocking

- **(a)** A request that starts long-running work must **return immediately**. Announce
  intent, hand the work to something that outlives the caller, exit.
- **(b)** Blocking the caller wastes its time, couples liveness to the caller staying
  alive, and forces serial execution. Fire-and-observe beats fire-and-wait.
- **(c)** Write the unit of work to durable storage, spawn/ensure a detached executor
  (`subprocess.Popen(..., start_new_session=True)`), print a job id, return. Observe later
  via a status/log query — never by holding the connection.
- **(d)** nexus `submit` writes `~/.nexus/jobs/<id>.json`, calls `ensure_worker()`, prints
  "queued — as soon as input is clear …" and exits in ~0.04s; the detached worker does the
  waiting and delivery (`cmd_submit`, `ensure_worker` in nexus.py).
- **(e)** Replaces: a synchronous call that sleeps/polls in the foreground and dies if the
  caller's turn ends; "just `time.sleep()` until it's ready".

### 2. Singleton & no-duplication

- **(a)** A shared background role (worker, watcher, daemon) must exist **at most once**.
  Concurrent callers may all *try* to start it; all but one must lose cleanly.
- **(b)** Duplicate workers double the compute, race each other for the same jobs, and
  cause double-delivery / corruption. "Start one if none is running" is a race unless the
  guard is atomic.
- **(c)** OS-level mutual exclusion the loser can detect without a handshake:
  `fcntl.flock(LOCK_EX | LOCK_NB)`. Winner holds the lock for its lifetime; a would-be
  second instance fails the non-blocking lock and exits. Check-liveness = try-lock-then-release.
- **(d)** nexus `_acquire_singleton()` / `worker_is_alive()` / `ensure_worker()`: N submits
  race, exactly one worker survives; the rest see the lock held and return "running".
- **(e)** Replaces: PID-file "if exists skip" checks (stale after crash, TOCTOU-racy);
  spawning a helper per request; hoping only one caller ever runs.

### 3. No-collision & durability

- **(a)** Concurrent readers/writers of shared state must never see partial/corrupt data,
  and state must survive a crash mid-operation.
- **(b)** A reader hitting a half-written file, or a crash between two writes, is a
  silent-corruption bug that surfaces far from its cause.
- **(c)** **Atomic write**: serialize to a temp file in the same dir, then `os.replace()`
  (atomic rename) into place — readers see either the old or the new file, never a torn one.
  Give state an explicit **status lifecycle** on disk so any observer can tell exactly where
  it is, and so a new executor can **recover** in-flight items after a crash.
- **(d)** nexus `_atomic_write()` (temp + `os.replace`); job lifecycle
  `queued → resolving → waiting_clear → running → success | error | timeout | cancelled`
  written on transitions only; on startup the worker **requeues** any job left in a
  non-terminal state by a crashed predecessor (`worker_main` recovery loop).
- **(e)** Replaces: in-place `open(path,"w")` truncation (torn reads); in-memory-only
  queues (lost on crash); "it was running… now it's just gone".

### 4. Lightweight & realtime

- **(a)** Watch for change **continuously** while spending near-zero resources. Recompute
  an expensive signal **only when its source actually changed**.
- **(b)** Tight busy-loops and re-reading unchanged inputs burn CPU/IO for nothing;
  "realtime" must not mean "hot spin".
- **(c)** **mtime-gated polling**: cache `(source_mtime_key → value)`; each tick, stat the
  source(s) — if the key is unchanged, return the cached value for free; only on change do
  the real work. Bound every read (size cap, tail-only, freshness window) so it can't hang.
  Let idle executors **self-shut-down** and respawn on demand.
- **(d)** nexus `_ctx_mtime_key()` + `SessCtx.ctx_pct()` recompute context% only when the
  snapshot/transcript mtime changes; `context_pct()` reads at most an 800 KB tail with a
  freshness guard; the worker self-exits after `WORKER_IDLE_SHUTDOWN` idle seconds.
- **(e)** Replaces: `while True: read_whole_file()`; fixed-interval full recomputation;
  a daemon that lingers forever at idle.

### 5. Cheap-gates-before-expensive

- **(a)** Order checks by cost and blast-radius: run **cheap, non-invasive** gates first;
  run the **expensive or side-effecting** gate only once every cheap gate already passes.
- **(b)** Invasive probes cost time and can perturb the thing you're observing; running
  them when a cheap precondition already fails is pure waste (and pure risk).
- **(c)** Tag each condition `invasive: bool`. Evaluate `cheap` list first; short-circuit on
  the first failure; only if all cheap gates hold do you run the `invasive` one. Memoize the
  invasive verdict so you probe a given state at most once.
- **(d)** nexus `wait_until_ready()` checks ctx% / idle / cost (cheap, from files) before the
  **space-probe** input-clear check (invasive — it injects a keystroke), so it never
  perturbs the session before the cheap thresholds are even met. `InputClearCondition`
  memoizes its verdict per draft.
- **(e)** Replaces: probing/mutating first and filtering after; re-running the expensive
  check every tick; checks in arbitrary (author-convenient) order.

### 6. Composable & future-proof

- **(a)** Behaviors compose as **AND**: a thing acts only when **all** its conditions hold
  **simultaneously**. Adding a new variant (a new condition, action, or backend) must be a
  small, local, additive change — not a rewrite.
- **(b)** Hard-coded, entangled logic makes every new case a surgery. Named, uniform units
  behind a registry make new cases trivial and safe.
- **(c)** **Registry + base-class + explicit `EXTENSION POINT` markers.** Define a small
  interface (base class), register concrete implementations by name in a dict, drive them
  through a spec (data), and evaluate a *list* of them with all-must-hold semantics. New
  variant = new subclass + one registry line.
- **(d)** nexus `HARNESSES`, `RECIPES`, `CONDITIONS` registries with `Harness`/`Recipe`
  base classes and `# ---- EXTENSION POINT ----` comments; conditions are built from specs
  (`build_conditions`) and ALL must pass in `all_ready()`. Adding a `cost` gate or a `codex`
  harness is a few lines.
- **(e)** Replaces: `if recipe == "compact": ... elif ...` ladders; one giant function that
  must be edited (and re-tested) for every new case; conditions welded into the loop.

### 7. Instant-on-ready

- **(a)** The moment the trigger condition clears, execution should be **instant** — no
  fixed delay tax, no "next poll cycle" latency beyond what correctness requires.
- **(b)** Users feel the gap between "ready" and "acted". Padding it with sleeps is a
  self-inflicted latency.
- **(c)** Separate the *poll interval* from the *action*: when all conditions pass, fire
  immediately (`hold <= 0 → return now`). If a stability hold is genuinely required, make it
  configurable and **edge-confirm** (re-check at the end of the hold) rather than guessing.
- **(d)** nexus `wait_until_ready()`: `if hold <= 0: return True` fires instantly the tick
  all conditions hold; the optional `stable_secs` hold edge-confirms before acting.
- **(e)** Replaces: unconditional `sleep(N)` after readiness; coarse poll intervals that add
  seconds of dead time; acting on a stale "was ready a while ago" reading.

### 8. Abstract & generic (dynamic, flexible)

- **(a)** Model the **general** case, parameterized by data, not the one instance in front
  of you. The same engine should serve today's use and tomorrow's unforeseen ones.
- **(b)** Over-specific code is rewritten the first time requirements shift; generic-but-
  grounded code absorbs change as configuration.
- **(c)** Push specifics into **data/specs** and behind **interfaces**: an action is
  "deliver this text", not "compact"; a target is resolved through a backend abstraction,
  not a hard-coded terminal; readiness is a list of condition specs, not inline branches.
  Keep the core loop dumb and uniform; keep variety at the edges (registries).
- **(d)** AutoCompact began as two concrete scripts (`compact_remote`, `compact_when_clear`);
  nexus generalized them into `recipes` (compact is just one) + `conditions` +
  `harnesses`/`backends` (tmux **or** herdr, resolved by pid/tty) — same engine, many uses.
- **(e)** Replaces: hard-coding "/compact", one terminal, one agent; copy-pasting a script
  per new case instead of adding a recipe/condition.

---

## Design checklist (run before building)

Before writing code for any non-trivial system, answer each. A "no" is a design smell.

- [ ] **Non-blocking?** Does the entry point return immediately and let work outlive it?
- [ ] **Singleton?** Is every shared background role guaranteed at-most-once under
      concurrent starts (atomic guard, not a PID-file race)?
- [ ] **Atomic + durable?** Are all shared-state writes atomic (temp + rename)? Is there an
      explicit on-disk status lifecycle, and crash recovery for in-flight items?
- [ ] **Lightweight/realtime?** Is expensive work recomputed only on real change
      (mtime-gated)? Are reads bounded (size/tail/freshness)? Do idle daemons self-exit?
- [ ] **Cheap gates first?** Are checks ordered cheap→expensive, invasive last, with
      short-circuit and memoized invasive verdicts?
- [ ] **Composable (AND)?** Do conditions/behaviors compose so ALL must hold at once, driven
      by data not branches?
- [ ] **Future-proof?** Is adding a new variant a subclass + one registry line, with an
      explicit EXTENSION POINT? No `elif` ladders?
- [ ] **Instant-on-ready?** Zero latency tax once ready (no gratuitous sleeps; edge-confirm
      any required hold)?
- [ ] **Abstract/generic?** Is the specific case just data over a general engine? Could a
      sibling use case reuse it unchanged?
- [ ] **Safe by default?** Does it refuse to clobber / interfere when unsure (see the
      space-probe: placeholder ≠ real input; abort or wait rather than destroy)?

## How to apply

**As a plan critique.** Walk the proposed plan through the checklist. For each "no",
name the specific principle and the pattern that fixes it (cite the nexus/AutoCompact
exemplar). Prefer flagging the *missing pattern* over vague "make it more robust".

**As a code structure.** Start from the patterns, not from the special case: a durable
job/record with atomic writes and a status lifecycle; an idempotent, singleton executor;
condition/behavior registries with base classes and EXTENSION POINT markers; a poll loop
that gates cheap→expensive and fires instantly. Pull concrete implementations from
`DOCTRINE.md`.

**As acceptance criteria.** Before declaring work done, the system must pass the checklist.
Treat these as review gates: an `elif` ladder for variants, an in-place file write, a
foreground sleep-loop, or a PID-file singleton are defects to be fixed, not style choices.

---

## Open questions / to refine with `ponytail`

- **Naming & merge.** "doctrine" is provisional; reconcile scope and voice with `ponytail`
  and decide the final single name / whether these become one skill or a pair.
- **Scope boundary.** This lens is systems/concurrency-flavored (born from a control plane).
  Does `ponytail` cover complementary ground (API/UX/data-modeling/testing altitude) so the
  merged skill spans the full "build it right" surface without overlap?
- **Invocation policy.** Should this auto-apply to *all* non-trivial builds, or only on an
  explicit "the right way" ask? Tune the description trigger after seeing `ponytail`'s.
- **Language-generality.** Reference impls are Python (flock/os.replace/Popen). Add the
  cross-language equivalents (rename-atomicity caveats on Windows, advisory locks, etc.).
- **Tension cases.** Document where principles trade off (e.g. instant-on-ready vs. a
  stability hold; lightweight polling vs. true event-driven) and how to choose.
- **Evidence hooks.** Consider a tiny self-audit checklist output the agent can attach to a
  plan/PR so the doctrine is verifiable, not just aspirational.

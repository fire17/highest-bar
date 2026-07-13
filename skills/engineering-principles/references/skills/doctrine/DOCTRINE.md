# DOCTRINE — reference implementations

> **DRAFT.** Companion to `SKILL.md` (skill name `doctrine`, provisional; to be merged with
> `ponytail`). This file holds copy-pasteable, battle-tested implementations of every pattern
> the doctrine names. All snippets are drawn from **nexus** (`~/Creations/nexus/nexus.py`) and
> **AutoCompact** (`~/Tokenomics/AutoCompact/compact_remote.py`, `compact_when_clear.py`).
> Adapt names; keep the shape. Read the originals for full context — do not edit them.

Contents:
1. Non-blocking submit + detached spawn
2. Singleton worker via `flock`
3. Atomic write (no torn reads)
4. Durable job store + status lifecycle + crash recovery
5. mtime-gated polling (realtime, near-zero cost) + bounded reads
6. Composable conditions (ALL-must-hold) + cheap-gates-before-expensive
7. Instant-on-ready readiness loop
8. Registry + base class extension (future-proofing)
9. Safe-by-default probing (placeholder ≠ real input)

---

## 1. Non-blocking submit + detached spawn

Announce intent, persist the work, ensure the executor exists, return. The executor runs in
its **own session** (`start_new_session=True`) so it survives the caller exiting.

```python
def submit(recipe, target, args, opts):
    jid = job_create(recipe, target, args, opts)   # durable unit of work (atomic write)
    w = ensure_worker()                            # exactly-one detached executor
    print(f"queued {jid} — will run when ready")   # announce
    return jid                                     # EXIT — do not wait

def ensure_worker():
    """Guarantee exactly one detached worker. Safe under concurrent callers
    (the worker self-guards with flock; losers just exit)."""
    if worker_is_alive():
        return "running"
    out = open(WORKER_LOG, "a")
    p = subprocess.Popen(
        [sys.executable, os.path.abspath(__file__), "worker"],
        stdin=subprocess.DEVNULL, stdout=out, stderr=subprocess.STDOUT,
        start_new_session=True,   # detach: outlives the caller / its turn
        close_fds=True,
    )
    return p.pid
```

**Anti-pattern replaced:** a foreground call that `sleep`/polls until done and dies with the
caller.

---

## 2. Singleton worker via `flock`

Atomic mutual exclusion. Concurrent starts race; exactly one wins and holds the lock for its
lifetime. "Is it alive?" is "can I momentarily take the lock?".

```python
import fcntl

def _acquire_singleton():
    fh = open(LOCK_PATH, "a+")
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)   # non-blocking exclusive
    except OSError:
        fh.close()
        return None            # someone else holds it → we are the loser → exit
    return fh                  # KEEP OPEN for the worker's whole lifetime

def worker_is_alive():
    fh = open(LOCK_PATH, "a+")
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(fh, fcntl.LOCK_UN); fh.close()
        return False           # we could lock it → nobody holds it → no worker
    except OSError:
        fh.close()
        return True            # locked by someone → a worker is alive

def worker_main():
    lock = _acquire_singleton()
    if lock is None:
        return                 # lost the race — a worker already runs
    try:
        ...                    # the one-and-only worker loop
    finally:
        fcntl.flock(lock, fcntl.LOCK_UN); lock.close()
```

**Anti-pattern replaced:** PID-file `if exists: skip` (stale after crash, TOCTOU-racy);
spawning a helper per request.

---

## 3. Atomic write (no torn reads)

Write to a temp file in the **same directory**, then `os.replace()` (atomic rename). A
concurrent reader sees either the whole old file or the whole new file — never a half-written
one.

```python
import os, json

def _atomic_write(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    os.replace(tmp, path)      # atomic on POSIX (same filesystem)
```

**Anti-pattern replaced:** `open(path, "w")` then write — any reader during the write sees a
truncated/torn file. (Windows caveat: `os.replace` over an open target can fail; see Open
Questions in SKILL.md.)

---

## 4. Durable job store + status lifecycle + crash recovery

State lives on disk as one record per unit of work, with an **explicit status lifecycle** so
any observer knows exactly where each item is, and writes happen **on transition only**
(cheap). A fresh executor **recovers** items a crashed predecessor left mid-flight.

```python
TERMINAL = {"success", "error", "timeout", "cancelled"}
# lifecycle: queued → resolving → waiting_clear → running → success | error | timeout | cancelled

def job_create(recipe, target, args, opts):
    jid = _new_id()
    job = {"id": jid, "recipe": recipe, "target": target, "args": args,
           "status": "queued", "phase": "queued", "error": None,
           "created_at": _now(), "updated_at": _now(), "finished_at": None, **opts}
    _atomic_write(_job_path(jid), job)             # durable + atomic
    return jid

def job_update(jid, status=None, phase=None, **fields):
    job = job_load(jid)
    if job is None:
        return None
    if status and status != job["status"]:
        job["status"] = status
        if status in TERMINAL and not job.get("finished_at"):
            job["finished_at"] = _now()
    if phase is not None:
        job["phase"] = phase
    job.update(fields); job["updated_at"] = _now()
    _atomic_write(_job_path(jid), job)             # transition → one write
    return job

# On worker startup — recover jobs orphaned by a previous crash (we are the only worker now):
for j in job_list():
    if j["status"] in ("resolving", "waiting_clear", "running"):
        job_update(j["id"], status="queued", phase="requeued (worker restart)")
```

**Anti-pattern replaced:** in-memory-only queue (lost on crash); no observable status; jobs
that silently vanish when a worker dies.

---

## 5. mtime-gated polling (realtime, near-zero cost) + bounded reads

Recompute an expensive signal **only when its source file changed**. Cache
`(mtime_key → value)`; a tick with unchanged mtime costs one `stat()`. Every read is
**bounded** (freshness window, size cap, tail-only) so it can never hang.

```python
def _ctx_mtime_key(source_paths):
    key = []
    for p in source_paths:
        try:    key.append(p.stat().st_mtime if p else 0)
        except OSError: key.append(0)
    return tuple(key)

class SessCtx:
    def __init__(self, session_id):
        self.session_id = session_id
        self._cache = (None, None)                 # (mtime_key, value)

    def ctx_pct(self):
        key = _ctx_mtime_key(self._sources())
        if key == self._cache[0]:
            return self._cache[1]                  # unchanged → FREE
        val = context_pct(self.session_id)         # expensive → only on change
        self._cache = (key, val)
        return val

def context_pct(session_id):
    """Bounded & non-hanging: fresh snapshot if young/small, else an 800KB tail read."""
    snap, tpath = _ctx_sources(session_id)
    if snap.exists():
        st = snap.stat()
        if (_now() - st.st_mtime) < 3600 and st.st_size < 512 * 1024:   # freshness + size guard
            ...   # parse snapshot
    if tpath:
        size = os.path.getsize(tpath)
        with open(tpath, "rb") as f:
            f.seek(max(0, size - 800 * 1024))      # tail only — never read a huge file whole
            data = f.read()
        ...   # scan last usage record
```

Pair with **idle self-shutdown** so an executor never lingers hot:

```python
if running:
    idle_since = time.monotonic()
elif time.monotonic() - idle_since > WORKER_IDLE_SHUTDOWN:
    break                                          # exit; respawned on demand by ensure_worker()
```

**Anti-pattern replaced:** `while True: parse_whole_file()`; fixed-interval full recompute; a
daemon that idles forever.

---

## 6. Composable conditions (ALL-must-hold) + cheap-gates-before-expensive

Each condition is a small object with a `check()` and an `invasive` flag. A job fires only
when **all** conditions hold. Cheap/non-invasive gates run first and short-circuit; the
invasive one runs **only** when every cheap gate already passed.

```python
class CtxPctCondition:
    invasive = False
    def __init__(self, value, op=">="):
        self.value, self.op = float(value), op
    def check(self, s):
        pct = s.ctx_pct()
        if pct is None: return False, "ctx% unknown"
        return _cmp(pct, self.op, self.value), f"ctx {pct:.1f}%"

class IdleCondition:
    invasive = False
    def check(self, s):
        ok = s.harness.is_idle(s.session_id)
        return ok, ("idle" if ok else "busy")

class InputClearCondition:
    invasive = True            # injects a probe keystroke — expensive & perturbing
    def check(self, s):
        raw = s.harness.read_composer(s.backend)
        if raw in s._verdict:                       # memoized: probe a given state once
            return s._verdict[raw], "cached"
        ...                                         # only probe content stable ~1s

# ordering: cheap first, invasive last
cheap    = [c for c in conds if not c.invasive]
invasive = [c for c in conds if c.invasive]

def all_ready(s):
    for c in cheap + invasive:                      # cheap gates first, probe last
        ok, reason = c.check(s)
        if not ok:
            return False, reason                     # short-circuit — never probe if cheap fails
    return True, "ready"
```

Build the condition list from **data** (specs), so composition is configuration:

```python
CONDITIONS = {
    "ctx_pct":     lambda p: CtxPctCondition(p["value"], p.get("op", ">=")),
    "idle":        lambda p: IdleCondition(),
    "input_clear": lambda p: InputClearCondition(),
}
def build_conditions(specs):
    return [CONDITIONS[s["type"]](s) for s in specs if s.get("type") in CONDITIONS]
```

**Anti-pattern replaced:** probing/mutating first then filtering; re-running the expensive
check every tick; conditions welded into the loop in an author-convenient order.

---

## 7. Instant-on-ready readiness loop

Decouple the poll interval from the action. The tick all conditions hold, fire — no fixed
delay. If a stability hold is truly needed, make it configurable and **edge-confirm**.

```python
def wait_until_ready(s, job):
    poll    = job.get("poll", 0.5)
    timeout = job.get("timeout", 3600.0)
    hold    = job.get("stable_secs", 0.0)          # 0 → instant
    ready_since = None
    start = time.monotonic()
    while True:
        if _cancelled(job):                 return False, "cancelled"
        if time.monotonic() - start > timeout: return False, "timeout"

        ok, reason = all_ready(s)
        now = time.monotonic()
        if ok:
            if hold <= 0:
                return True, "ready"                # INSTANT — no sleep tax
            if ready_since is None:
                ready_since = now
            elif now - ready_since >= hold:
                if all_ready(s)[0]:                 # edge-confirm at end of hold
                    return True, "ready"
                ready_since = None                  # regressed → reset
        else:
            ready_since = None
        time.sleep(poll)
```

**Anti-pattern replaced:** unconditional `sleep(N)` after readiness; acting on a stale
"was ready earlier" reading.

---

## 8. Registry + base class extension (future-proofing)

A tiny interface (base class), concrete implementations registered by name, and an explicit
`EXTENSION POINT` marker. New variant = new subclass + one line. The core loop never changes.

```python
class Harness:                 # base interface — subclass per agent CLI
    name = "base"
    supports_idle = False
    def resolve(self, session_id):        raise NotImplementedError
    def read_composer(self, backend):     ...
    def probe_is_clear(self, backend):    raise NotImplementedError
    def submit_text(self, backend, text): raise NotImplementedError

class ClaudeCodeHarness(Harness):
    name = "claude-code"; supports_idle = True
    def resolve(self, session_id): ...     # sessionId → pid → backend (tmux/herdr) by pid/tty
    def probe_is_clear(self, backend): ... # space-probe semantics
    def submit_text(self, backend, text): ...

# ---- EXTENSION POINT: register harnesses here ----
# class CodexHarness(Harness): name = "codex"; ...   # future: codex composer/readiness differs
HARNESSES = {h.name: h for h in [ClaudeCodeHarness()]}
DEFAULT_HARNESS = "claude-code"
```

Same shape for **recipes** (args → the action) and **conditions** (spec → gate). Backends
(`TmuxBackend`, `HerdrBackend`) sit behind one interface so a target is resolved generically
by pid/tty, not hard-coded to one terminal.

**Anti-pattern replaced:** `if kind == "a": ... elif kind == "b": ...` ladders; one giant
function edited (and re-tested) for every new case.

---

## 9. Safe-by-default probing (placeholder ≠ real input)

When an action could clobber user work, **prove** it's safe first, and when unsure, **refuse
or wait** rather than destroy. Distinguish inert placeholder/ghost state from real content the
cheapest reliable way, and only probe content that's been stable (never mid-keystroke).

```python
def _probe_is_clear(backend, settle):
    """Type one space at end-of-line; if the visible text vanishes it was greyed
    PLACEHOLDER (clear). If it survives, it's REAL user input → do not interfere.
    Always remove the probe. Call only when content has been unchanged ~1s."""
    backend.keys("End")
    backend.literal(" ")                           # probe
    probed = _stable(backend, settle)
    backend.keys("BSpace")                          # always revert the probe
    return not (probed or "").strip()

# one-shot variant: refuse on real input
if real_user_text_present:
    return {"ok": False, "reason": "user_input"}    # never overwrite a message being typed
# wait variant: hold and re-check, memoizing each draft's verdict, edge-confirm before acting
```

**Anti-pattern replaced:** acting on a raw "looks non-empty" read (fires on placeholder,
clobbers real drafts); probing text the user is actively typing.

---

*End of DOCTRINE.md (draft). Cross-reference: `SKILL.md` for the principles, why, and the
design checklist. Originals: `~/Creations/nexus/nexus.py`, `~/Tokenomics/AutoCompact/`.*

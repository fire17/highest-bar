#!/usr/bin/env python3
"""sync_skill.py — save a skill (and everything it needs) into the Creations Skills vault.

    python3 ~/Creations/Skills/sync_skill.py <skill-dir> [options]

Copies the skill directory (symlinks preserved) into the vault, then resolves its
DEPENDENCY CLOSURE: every text file in the skill is scanned for absolute/home paths;
each referenced *file* that exists outside the skill dir is copied into the shared
`_deps/` mirror (deduped across skills — many skills reference the same engine).
Referenced *directories* and oversize files are recorded in the manifest as
`noted` (path + why) rather than copied — the manifest is the honest record of
what the copy needs from the outside world.

Every synced skill gets `.provenance.json` (source, when, files, deps, extra notes)
and a row in the vault's INDEX.md. Re-running is an UPDATE: the copy is refreshed,
provenance keeps a history of sync timestamps.

Options:
  --vault DIR          vault root (default ~/Creations/Skills)
  --category NAME      place under vault/NAME/ (e.g. vendored, legacy)
  --extra-dep PATH     additional dependency to include (repeatable) — for
                       semantic deps a path-scan can't see
  --note TEXT          free-text provenance note (repeatable)
  --max-dep-bytes N    per-file copy cap for deps (default 5000000)
  --dry-run            report what would happen, copy nothing
"""
import argparse
import json
import os
import re
import shutil
import sys
import time

# leading dot allowed (dot-dirs like ~/.claude are the COMMON case); no spaces in paths —
# precision beats recall here, agents pass --extra-dep for anything exotic
PATH_RE = re.compile(r'(?:~|/Users/[A-Za-z0-9_]+)/\.?[A-Za-z0-9_.][A-Za-z0-9_./-]*')
TEXT_EXT = {".md", ".py", ".sh", ".txt", ".json", ".yml", ".yaml", ".toml", ".js", ".ts", ".zsh", ".bash"}


def is_text(path):
    return os.path.splitext(path)[1].lower() in TEXT_EXT


def scan_refs(path):
    """Absolute/home path references in one text file."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            body = f.read()
    except Exception:
        return set()
    refs = set()
    for m in PATH_RE.findall(body):
        p = os.path.expanduser(m.rstrip(".,;:)'\"")).rstrip("/")
        refs.add(p)
    return refs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_dir")
    ap.add_argument("--vault", default="~/Creations/Skills")
    ap.add_argument("--category", default="")
    ap.add_argument("--extra-dep", action="append", default=[])
    ap.add_argument("--note", action="append", default=[])
    ap.add_argument("--max-dep-bytes", type=int, default=5_000_000)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    src = os.path.abspath(os.path.expanduser(a.skill_dir.rstrip("/")))
    vault = os.path.abspath(os.path.expanduser(a.vault))
    if not os.path.isdir(src):
        print(f"✗ not a directory: {src}")
        return 1
    if not os.path.isfile(os.path.join(src, "SKILL.md")) and not os.path.islink(os.path.join(src, "SKILL.md")):
        print(f"✗ no SKILL.md in {src} — not a skill dir")
        return 1

    name = os.path.basename(src)
    dest = os.path.join(vault, a.category, name) if a.category else os.path.join(vault, name)
    if os.path.realpath(src).startswith(os.path.realpath(vault)):
        print(f"✗ source is inside the vault; refusing self-sync")
        return 1

    # ---- collect skill files + reference scan --------------------------------------
    skill_files, refs = [], set()
    for root, _dirs, files in os.walk(src):
        for fn in files:
            p = os.path.join(root, fn)
            skill_files.append(os.path.relpath(p, src))
            if not os.path.islink(p) and is_text(p):
                refs |= scan_refs(p)
    for extra in a.extra_dep:
        refs.add(os.path.abspath(os.path.expanduser(extra)))

    # ---- classify dependencies ------------------------------------------------------
    deps = []
    for ref in sorted(refs):
        real = os.path.realpath(ref)
        if real.startswith(os.path.realpath(src)) or real.startswith(os.path.realpath(vault)):
            continue                                   # internal / already vaulted
        d = {"ref": ref}
        if real.startswith(os.path.expanduser("~/.claude/projects/")):
            # session transcripts/buckets: provenance references, not functional deps —
            # and PRIVATE conversation data that must never be bulk-copied into the vault
            d.update(status="noted", why="session transcript/bucket — private, reference-only by policy")
            deps.append(d)
            continue
        if os.path.isfile(ref):
            size = os.path.getsize(ref)
            if size <= a.max_dep_bytes:
                d.update(status="copy", size=size,
                         dest=os.path.join("_deps", ref.lstrip("/")))
            else:
                d.update(status="noted", size=size, why="exceeds --max-dep-bytes")
        elif os.path.isdir(ref):
            d.update(status="noted", why="directory reference — recorded, not copied")
        else:
            d.update(status="noted", why="path does not exist (may be an example/pattern)")
        deps.append(d)

    if a.dry_run:
        print(json.dumps({"name": name, "source": src, "dest": dest,
                          "files": len(skill_files), "deps": deps}, indent=2))
        return 0

    # ---- copy skill + deps ----------------------------------------------------------
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest, symlinks=True)
    copied = 0
    for d in deps:
        if d["status"] != "copy":
            continue
        tgt = os.path.join(vault, d["dest"])
        os.makedirs(os.path.dirname(tgt), exist_ok=True)
        shutil.copy2(d["ref"], tgt)
        copied += 1

    # ---- provenance (history-preserving) ---------------------------------------------
    prov_path = os.path.join(dest, ".provenance.json")
    history = []
    if os.path.isfile(prov_path):
        try:
            history = json.load(open(prov_path)).get("history", [])
        except Exception:
            pass
    now = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    history.append(now)
    prov = {"name": name, "source": src, "synced_at": now, "history": history,
            "category": a.category or None, "notes": a.note,
            "files": sorted(skill_files), "deps": deps}
    with open(prov_path, "w") as f:
        json.dump(prov, f, indent=2)

    # ---- INDEX.md row (replace-by-name) ----------------------------------------------
    idx = os.path.join(vault, "INDEX.md")
    rel = os.path.relpath(dest, vault)
    row = (f"| [{name}]({rel}/) | `{src}` | {a.category or '—'} | {len(skill_files)} "
           f"| {copied} copied / {sum(1 for d in deps if d['status']=='noted')} noted | {now[:10]} |")
    lines = []
    if os.path.isfile(idx):
        lines = [l for l in open(idx).read().splitlines() if not l.startswith(f"| [{name}]({rel}/) ")]
    if not lines:
        lines = ["# Skills vault index", "",
                 "| skill | source | category | files | deps | synced |",
                 "|---|---|---|---|---|---|"]
    lines.append(row)
    with open(idx, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"✔ synced {name} → {dest}")
    print(f"  files: {len(skill_files)}   deps: {copied} copied, "
          f"{sum(1 for d in deps if d['status']=='noted')} noted   provenance + INDEX.md updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())

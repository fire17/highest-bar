#!/usr/bin/env python3
"""harvest.py — extract session artifacts from Claude Code transcript(s).

Usage: harvest.py <transcript.jsonl> [more.jsonl ...]

Prints JSON:
  files_written   paths created via Write/NotebookEdit tool calls
  files_edited    paths touched via Edit/MultiEdit (and not also written)
  skills_invoked  skills run via the Skill tool
  missing         harvested paths that no longer exist on disk
  counts          summary numbers

Read-only, stdlib-only. Tolerant of transcript format drift: instead of assuming a
message schema, it walks every JSON value in every line and picks out tool_use nodes.
It sees only tool calls — files created via Bash (redirects, cp, generators) are
invisible here and must be added by the judgment pass in SKILL.md Phase 2.
"""
import json
import os
import sys

WRITE_TOOLS = {"Write", "NotebookEdit"}
EDIT_TOOLS = {"Edit", "MultiEdit"}


def walk(node, out):
    if isinstance(node, dict):
        if node.get("type") == "tool_use":
            name = node.get("name") or ""
            inp = node.get("input") or {}
            if isinstance(inp, dict):
                fp = inp.get("file_path") or inp.get("notebook_path")
                if name in WRITE_TOOLS and fp:
                    out["files_written"].add(fp)
                elif name in EDIT_TOOLS and fp:
                    out["files_edited"].add(fp)
                elif name == "Skill" and inp.get("skill"):
                    out["skills_invoked"].add(inp["skill"])
        for v in node.values():
            walk(v, out)
    elif isinstance(node, list):
        for v in node:
            walk(v, out)


def main(paths):
    out = {"files_written": set(), "files_edited": set(), "skills_invoked": set()}
    bad_lines = 0
    for path in paths:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    walk(json.loads(line), out)
                except json.JSONDecodeError:
                    bad_lines += 1
    # a file both written and edited counts as written
    out["files_edited"] -= out["files_written"]
    result = {k: sorted(v) for k, v in out.items()}
    harvested = result["files_written"] + result["files_edited"]
    result["missing"] = sorted(p for p in harvested if not os.path.exists(os.path.expanduser(p)))
    result["counts"] = {
        "files_written": len(result["files_written"]),
        "files_edited": len(result["files_edited"]),
        "skills_invoked": len(result["skills_invoked"]),
        "missing": len(result["missing"]),
        "unparseable_lines": bad_lines,
        "transcripts": len(paths),
    }
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__.strip())
    missing_args = [p for p in sys.argv[1:] if not os.path.exists(p)]
    if missing_args:
        sys.exit("harvest.py: transcript not found: " + ", ".join(missing_args))
    main(sys.argv[1:])

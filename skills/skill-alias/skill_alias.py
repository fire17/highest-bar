#!/usr/bin/env python3
"""skill-alias — create a working, single-source-of-truth alias for a Claude Code skill.

The correct method (verified): an alias is a REAL directory whose SKILL.md is a
*symlink* to the canonical skill's SKILL.md. The alias registers under its own
directory name (Claude Code keys the slash-command off the directory name), and
because SKILL.md is a symlink there is one source of truth — editing the original
skill updates the alias automatically.

Why not the alternatives:
  - symlinking the whole directory  -> Claude Code resolves it to the canonical
    realpath and de-dupes it (no second command appears).
  - hardlinking the file           -> breaks when an editor saves the original via
    atomic-replace (the alias silently keeps the old inode).

Usage:
    skill_alias.py <skill> <alias> [--force]
    skill_alias.py <alias> --remove
"""
import argparse
import json
import os
import re
import sys

SKILLS_DIR = os.path.expanduser("~/.claude/skills")

# Built-in slash commands / common names an alias should not shadow.
RESERVED = {
    "help", "compact", "clear", "config", "settings", "model", "effort", "fast",
    "undo", "rewind", "branch", "fork", "loop", "proactive", "resume", "review",
    "init", "cost", "doctor", "login", "logout", "status", "memory", "vim",
    "agents", "mcp", "hooks", "skills", "add-dir", "bug", "release-notes",
}


def die(msg, **extra):
    print(json.dumps({"ok": False, "error": msg, **extra}))
    print(f"\n❌ {msg}")
    sys.exit(1)


def clean_name(raw):
    """Normalize a user-typed skill/alias name (strip leading slash, whitespace)."""
    n = (raw or "").strip().lstrip("/").strip()
    return n


def valid_name(n):
    return bool(n) and "/" not in n and n not in (".", "..") and not n.startswith(".")


def is_symlink_alias(path):
    """True if <path> is a dir whose SKILL.md is a symlink (i.e. one of our aliases)."""
    md = os.path.join(path, "SKILL.md")
    return os.path.isdir(path) and os.path.islink(md)


def relative_script_warning(source_md):
    """Warn if the source SKILL.md invokes scripts by a relative path, which would
    break when the skill is reached through an alias (different directory)."""
    warns = []
    try:
        text = open(source_md, encoding="utf-8", errors="replace").read()
    except OSError:
        return warns
    for m in re.finditer(r'(?m)^\s*(?:python3?|node|bash|sh|ruby|deno)\s+(\S+)', text):
        tok = m.group(1)
        if tok.startswith(("~", "/", "$")) or "${" in tok:
            continue  # absolute-ish -> safe
        if tok.startswith(("./", "../")) or ("/" not in tok and tok not in ("-", "-c")):
            warns.append(tok)
    if warns:
        uniq = ", ".join(sorted(set(warns))[:5])
        return [(
            "source skill invokes a script by a RELATIVE path (%s); it may fail when run "
            "via the alias. Make the canonical skill use an absolute path "
            "(e.g. ~/.claude/skills/<name>/<script>)." % uniq
        )]
    return []


def do_remove(alias):
    apath = os.path.join(SKILLS_DIR, alias)
    if not os.path.exists(apath):
        die(f"alias '{alias}' does not exist", alias=alias)
    if not is_symlink_alias(apath):
        die(f"'{alias}' is not a symlink-alias (its SKILL.md is a real file, not a "
            f"symlink) — refusing to delete a real skill", alias=alias)
    md = os.path.join(apath, "SKILL.md")
    os.remove(md)
    try:
        os.rmdir(apath)  # only removes if now empty
    except OSError:
        pass
    print(json.dumps({"ok": True, "action": "removed", "alias": alias}))
    print(f"\n✅ removed alias '/{alias}'. (The canonical skill is untouched.)")


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("a", nargs="?")
    ap.add_argument("b", nargs="?")
    ap.add_argument("--force", action="store_true", help="replace an existing symlink-alias")
    ap.add_argument("--remove", action="store_true", help="delete an alias")
    args = ap.parse_args()

    if args.remove:
        alias = clean_name(args.b or args.a)
        if not valid_name(alias):
            die("usage: skill_alias.py <alias> --remove")
        return do_remove(alias)

    skill = clean_name(args.a)
    alias = clean_name(args.b)
    if not valid_name(skill) or not valid_name(alias):
        die("usage: skill_alias.py <skill> <alias> [--force]   (both names required)")
    if skill == alias:
        die("skill and alias must differ", skill=skill, alias=alias)

    source = os.path.join(SKILLS_DIR, skill)
    source_md = os.path.join(source, "SKILL.md")
    if not os.path.isdir(source) or not os.path.exists(source_md):
        avail = sorted(d for d in os.listdir(SKILLS_DIR)
                       if os.path.exists(os.path.join(SKILLS_DIR, d, "SKILL.md"))) \
            if os.path.isdir(SKILLS_DIR) else []
        die(f"source skill '{skill}' not found (no {skill}/SKILL.md)",
            skill=skill, available=avail)

    apath = os.path.join(SKILLS_DIR, alias)
    amd = os.path.join(apath, "SKILL.md")
    rel_target = os.path.join("..", skill, "SKILL.md")  # relative, portable

    # Handle an existing entry at the alias path.
    if os.path.exists(apath) or os.path.islink(apath):
        if is_symlink_alias(apath):
            cur = os.path.realpath(amd)
            if cur == os.path.realpath(source_md):
                warns = relative_script_warning(source_md)
                print(json.dumps({"ok": True, "action": "already-exists",
                                  "skill": skill, "alias": alias,
                                  "target": rel_target, "warnings": warns}))
                print(f"\n✅ /{alias} already aliases /{skill} correctly (nothing to do).")
                for w in warns:
                    print(f"⚠️  {w}")
                return
            if not args.force:
                die(f"'{alias}' is already an alias for something else "
                    f"({cur}); pass --force to repoint it", alias=alias)
            os.remove(amd)  # repoint below
        else:
            die(f"'{alias}' already exists as a REAL skill — refusing to overwrite it",
                alias=alias)

    warns = relative_script_warning(source_md)
    if alias in RESERVED:
        warns.append(f"'{alias}' matches a built-in/common command name; it may be "
                     f"shadowed or confusing. Consider another alias.")

    os.makedirs(apath, exist_ok=True)
    os.symlink(rel_target, amd)

    # Verify the symlink resolves to the source SKILL.md.
    if os.path.realpath(amd) != os.path.realpath(source_md):
        die(f"created symlink but it does not resolve to {skill}/SKILL.md", alias=alias)

    print(json.dumps({"ok": True, "action": "created", "skill": skill, "alias": alias,
                      "alias_dir": apath.replace(os.path.expanduser("~"), "~"),
                      "target": rel_target, "warnings": warns}))
    print(f"\n✅ created alias  /{alias}  ->  /{skill}")
    print(f"   {apath.replace(os.path.expanduser('~'), '~')}/SKILL.md  ->  {rel_target}")
    print("   One source of truth: editing the "
          f"{skill} skill updates /{alias} automatically (symlinked SKILL.md).")
    for w in warns:
        print(f"⚠️  {w}")
    print("\nℹ️  /%s registers on the next skill-list refresh (type `/` again or send a "
          "message)." % alias)


if __name__ == "__main__":
    main()

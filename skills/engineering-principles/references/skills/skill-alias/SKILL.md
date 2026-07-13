---
name: skill-alias
description: Create a working alias for an existing Claude Code skill — a second slash-command name for the same skill, with ONE source of truth (no copies). Makes a real directory whose SKILL.md is a symlink to the canonical skill's SKILL.md, so editing the original updates the alias automatically. Use when the user types /skill-alias, or asks to "alias a skill", "add another name / shortcut for a skill", "make /X also work as /Y", or "create a skill alias".
argument-hint: "<skill> <alias>"
allowed-tools: Bash
---

# skill-alias

Create an alias `/<alias>` for an existing skill `/<skill>` the **correct** way: a **real
directory** whose `SKILL.md` is a **symlink** to the canonical skill's `SKILL.md`. The alias
registers under its own directory name (Claude Code keys the slash-command off the directory
name), and because the file is a symlink there is **one source of truth** — editing the
original skill updates the alias automatically, with nothing to copy or re-sync.

Why not the obvious approaches (all tested): symlinking the whole *directory* gets de-duped by
Claude Code (no second command appears); a *hardlink* breaks the moment an editor saves the
original via atomic-replace. A symlinked `SKILL.md` inside a real dir is the method that both
registers **and** auto-propagates.

## ⛔ ALWAYS run the script — never fabricate

Every `/skill-alias` invocation MUST execute the script below via **Bash, in THIS turn**, and
your reply MUST quote its actual output. Do not claim an alias was created without running it.

## How to run

```bash
python3 ~/.claude/skills/skill-alias/skill_alias.py <skill> <alias> [--force]
python3 ~/.claude/skills/skill-alias/skill_alias.py <alias> --remove
```

- `<skill>` — the existing skill to alias (e.g. `identify`); a leading `/` is fine.
- `<alias>` — the new command name (e.g. `self`).
- `--force` — repoint an existing **symlink-alias** of that name (never overwrites a real skill).
- `--remove` — delete the alias (refuses unless it's a symlink-alias, so a real skill is safe).

The script validates the source exists, refuses unsafe collisions (won't clobber a real skill),
creates the real dir + relative symlink, verifies the symlink resolves, warns if the alias name
shadows a built-in, and warns if the source skill calls a script by a **relative** path (which
would break when reached through the alias — the canonical skill should use an absolute path
like `~/.claude/skills/<name>/<script>`). Relay the script's summary verbatim.

## Mapping `/skill-alias …` → the CLI

| User types | Run |
|---|---|
| `/skill-alias identify self` | `skill_alias.py identify self` |
| `/skill-alias autocompact ac` | `skill_alias.py autocompact ac` |
| `/skill-alias identify self --force` | `skill_alias.py identify self --force` (repoint existing alias) |
| `/skill-alias self --remove` / `/skill-alias --remove self` | `skill_alias.py self --remove` |

New/removed aliases take effect on the next skill-list refresh (type `/` again, or send a
message). For **multiple** aliases, run it once per alias name.

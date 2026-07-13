# Bundled reference skills — portable snapshot

Local copies of every skill referenced by the engineering-principles family, so the
family stays self-contained if copied to another machine/user. Snapshotted
**2026-07-06** from `~/.claude/skills/`.

| Bundled dir | Canonical skill | Aliases | Files |
|---|---|---|---|
| `doctrine/` | /doctrine | — | SKILL.md + DOCTRINE.md (code patterns) |
| `ponytail/` | /ponytail | — | SKILL.md |
| `tracks/` | /tracks | — | SKILL.md |
| `wartable/` | /wartable | /wargame | SKILL.md |
| `unknowns/` | /unknowns | — | SKILL.md |
| `workflow-model-guard/` | /workflow-model-guard | — | SKILL.md |
| `skill-alias/` | /skill-alias | — | SKILL.md + skill_alias.py |

**One source of truth caveat (per the doctrine itself):** the LIVE skills under
`~/.claude/skills/` are canonical; this bundle is a dated, derived snapshot — prefer
the live skill when it exists, fall back to the bundle when it doesn't (fresh machine,
copied skill). Staleness is worse than absence: refresh when the sources change:

```bash
cd ~/.claude/skills/engineering-principles/references/skills && \
for s in doctrine ponytail tracks wartable unknowns workflow-model-guard skill-alias; do \
  rm -rf "$s" && cp -RL ~/.claude/skills/$s "$s"; done && \
sed -i '' "s/Snapshotted \*\*[0-9-]*\*\*/Snapshotted **$(date +%Y-%m-%d)**/" MANIFEST.md
```

To install the bundled skills as live skills on a new machine:
`cp -R <this-dir>/<skill> ~/.claude/skills/<skill>` (then recreate aliases with
`skill-alias/skill_alias.py <skill> <alias>`).

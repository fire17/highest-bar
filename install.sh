#!/bin/bash
# HighestBar installer — batteries included, works out of the box.
# Copies the full /highest-bar skill closure into ~/.claude/skills and the
# master-engineering book payload into its canonical path.
# Default: skip skills that already exist (never clobber local work). --force overwrites.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills"
FORCE="${1:-}"
mkdir -p "$DEST"

installed=0 skipped=0 skipped_names=""
for d in "$HERE"/skills/*/; do
  name="$(basename "$d")"
  if [ -e "$DEST/$name" ] && [ "$FORCE" != "--force" ]; then
    skipped=$((skipped+1)); skipped_names="$skipped_names $name"; continue
  fi
  rm -rf "${DEST:?}/$name"
  # cp -R preserves the relative SKILL.md symlinks aliases depend on
  cp -R "$d" "$DEST/$name"
  installed=$((installed+1))
done

# the_senior book payload → canonical path master_engineering points at
BOOK="$HOME/Creations/Lively/the_senior"
if [ ! -e "$BOOK/MASTER_ENGINEERING.md" ] || [ "$FORCE" = "--force" ]; then
  mkdir -p "$BOOK"
  cp -R "$HERE/payloads/the_senior/." "$BOOK/"
  echo "book payload → $BOOK"
fi

# vault sync tool (used by skill-creator's vault law; optional elsewhere)
mkdir -p "$HOME/Creations/Skills"
if [ ! -e "$HOME/Creations/Skills/sync_skill.py" ] || [ "$FORCE" = "--force" ]; then
  cp "$HERE/tools/sync_skill.py" "$HOME/Creations/Skills/"
fi

echo "installed: $installed skills, skipped (already present, may be STALE): $skipped"
if [ -n "$skipped_names" ]; then
  echo "  skipped:${skipped_names}"
  echo "  rerun with --force to refresh them from this repo"
fi

# environment report — hard + optional deps
echo "--- environment ---"
for b in python3 node; do
  command -v "$b" >/dev/null && echo "✅ $b" || echo "⛔ $b MISSING (required: python3=scripts, node=impeccable)"
done
for b in git gh jq tmux ffmpeg yt-dlp; do
  command -v "$b" >/dev/null && echo "✅ $b" || echo "⚠️  $b absent (optional — see MAP.md degrade notes)"
done
echo "plugin (optional, vendored fallback installed): /plugin install frontend-design@claude-plugins-official"

# ledger self-check: every activation-stack skill must resolve
echo "--- ledger check ---"
ok=1
for s in highest-bar impeccable frontend-design wargame unknowns mindblown-fast \
         engineering-principles engineering-principles-pro master_engineering \
         ponytail ladder-abstraction highest-bar-abstract workflow-model-guard \
         watch darwin-skill mindblown; do
  if [ -f "$DEST/$s/SKILL.md" ] || [ -L "$DEST/$s/SKILL.md" ]; then echo "✅ /$s"; else echo "⛔ /$s missing"; ok=0; fi
done
[ "$ok" = "1" ] && echo "LEDGER: all activation-stack skills resolve. Ready." || { echo "LEDGER: HALT — fix missing skills"; exit 1; }

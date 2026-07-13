#!/bin/bash
# Build the batteries-included HighestBar repo from the live skill tree.
# Idempotent: wipes + rebuilds skills/ payloads/ from current live state.
set -euo pipefail
REPO="$HOME/Creations/HighestBar"
SRC="$HOME/.claude/skills"
EXCL=(--exclude '.git' --exclude '__pycache__' --exclude '.pytest_cache' \
      --exclude '*.bak' --exclude '*.bak.*' --exclude '.skill-r0.bak' \
      --exclude 'SKILL.md.bak*' --exclude '.DS_Store' --exclude '.in_use' \
      --exclude '.project')

rm -rf "$REPO/skills" "$REPO/payloads"
mkdir -p "$REPO/skills" "$REPO/payloads" "$REPO/tools"

# Tier 0-2 skill dirs (aliases carried with canonicals; relative symlinks preserved)
DIRS=(highest-bar highest-bar-abstract ladder-abstraction grand-start hba ladder
  impeccable wargame wartable unknowns mindblown mindblown-fast
  engineering-principles engineering-principles-pro ep epp engineering-principals
  master_engineering sol ponytail
  workflow-model-guard doctrine watch darwin-skill pyramid pyr tracks
  features-grid changes-visualizer cviz progress-report report ripple rpl
  do-and-learn dnl save_and_ship sas skill-creator skill-alias mkalias sota
  awesome-readme awr)
for d in "${DIRS[@]}"; do
  [ -e "$SRC/$d" ] || { echo "MISSING SOURCE: $d" >&2; exit 1; }
  rsync -a "${EXCL[@]}" "$SRC/$d" "$REPO/skills/"
done

# unknowns: de-symlink (dir is an absolute symlink; real payload = 1 file)
if [ -L "$REPO/skills/unknowns" ]; then rm "$REPO/skills/unknowns"; fi
mkdir -p "$REPO/skills/unknowns"
cp "$HOME/Creations/unknowns/skills/unknowns/SKILL.md" "$REPO/skills/unknowns/SKILL.md"

# shipit: build from canonical repo in copy mode (skill dir on disk = absolute symlinks)
rm -rf "$REPO/skills/shipit"; mkdir -p "$REPO/skills/shipit"
cp "$HOME/Creations/ShipIt/SKILL.md" "$REPO/skills/shipit/SKILL.md"
rsync -a "${EXCL[@]}" "$HOME/Creations/ShipIt/references" "$REPO/skills/shipit/"
# sota alias points at ../shipit/SKILL.md relatively — re-create clean
rm -rf "$REPO/skills/sota"; mkdir -p "$REPO/skills/sota"
ln -s ../shipit/SKILL.md "$REPO/skills/sota/SKILL.md"

# fix gantry-style absolute dir symlinks if any slipped in (none expected in DIRS)

# vendored frontend-design (plugin content → bare skill dir; satisfies bare /frontend-design refs)
FD="$HOME/.claude/plugins/cache/claude-plugins-official/frontend-design/unknown/skills/frontend-design"
mkdir -p "$REPO/skills/frontend-design"
cp "$FD/SKILL.md" "$REPO/skills/frontend-design/SKILL.md"
cp "$FD/LICENSE.txt" "$REPO/skills/frontend-design/LICENSE.txt" 2>/dev/null || true

# payloads
rsync -a "${EXCL[@]}" "$HOME/Creations/Lively/the_senior" "$REPO/payloads/"

# tools
cp "$HOME/Creations/Skills/sync_skill.py" "$REPO/tools/sync_skill.py"

# install-time path patches (repo copies only; live tree untouched)
for f in "$REPO/skills/features-grid/SKILL.md" "$REPO/skills/changes-visualizer/SKILL.md"; do
  sed -i '' 's|/Users/magic/.claude/skills|~/.claude/skills|g' "$f"
  sed -i '' 's|~/.claude/skills/.archive/[A-Za-z0-9._/-]*|(pre-merge archive on origin machine)|g' "$f"
done
# master_engineering body path: personal absolute → ~ form (works after install.sh places the book)
sed -i '' 's|/Users/magic/Creations/Lively/the_senior|~/Creations/Lively/the_senior|g' "$REPO/skills/master_engineering/SKILL.md"
find "$REPO" -name '.DS_Store' -delete

# sanity: no absolute /Users/magic symlinks left
BAD=""
while read -r l; do
  t=$(readlink "$l")
  if [[ "$t" == /* ]]; then BAD="$BAD$l -> $t"$'\n'; fi
done < <(find "$REPO/skills" -type l)
if [ -n "$BAD" ]; then echo "ABSOLUTE SYMLINKS REMAIN:"; echo "$BAD"; exit 1; fi

echo "OK: $(find "$REPO/skills" -type f | wc -l | tr -d ' ') files, $(du -sh "$REPO" | cut -f1) total"

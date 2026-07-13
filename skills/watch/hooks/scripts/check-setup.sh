#!/usr/bin/env bash
# SessionStart hook for /watch — one-line status so users know what's wired up.
# Silent on ready state to avoid spam. Points at the installer when something
# is missing.
set -euo pipefail

CONFIG_FILE="$HOME/.config/watch/.env"

# Warn if the secrets file has loose permissions.
if [[ -f "$CONFIG_FILE" ]]; then
  perms=$(stat -c '%a' "$CONFIG_FILE" 2>/dev/null || stat -f '%Lp' "$CONFIG_FILE" 2>/dev/null || echo "")
  if [[ -n "$perms" && "$perms" != "600" && "$perms" != "400" ]]; then
    echo "/watch: WARNING — $CONFIG_FILE has permissions $perms (should be 600)."
    echo "  Fix: chmod 600 $CONFIG_FILE"
  fi
fi

# Read a config value from the .env file without exporting it.
read_key() {
  local name="$1"
  if [[ -n "${!name:-}" ]]; then
    echo "${!name}"
    return
  fi
  if [[ -f "$CONFIG_FILE" ]]; then
    awk -F= -v k="$name" '
      /^[[:space:]]*#/ { next }
      $1 == k {
        sub(/^[[:space:]]*/, "", $2); sub(/[[:space:]]*$/, "", $2);
        gsub(/^["'\'']|["'\'']$/, "", $2);
        print $2; exit
      }
    ' "$CONFIG_FILE"
  fi
}

HAS_FFMPEG=""
HAS_YTDLP=""
command -v ffmpeg >/dev/null 2>&1 && HAS_FFMPEG="yes"
command -v yt-dlp >/dev/null 2>&1 && HAS_YTDLP="yes"

# Local whisper engine (this build transcribes on-device — no API keys).
HAS_WHISPER=""
python3 - <<'PY' >/dev/null 2>&1 && HAS_WHISPER="yes"
from importlib.util import find_spec
import sys
sys.exit(0 if (find_spec("mlx_whisper") or find_spec("whisper")) else 1)
PY
SETUP_COMPLETE="$(read_key SETUP_COMPLETE)"

# Fully configured → silent (Claude can surface status on demand via --check).
if [[ "$SETUP_COMPLETE" == "true" && -n "$HAS_FFMPEG" && -n "$HAS_YTDLP" ]]; then
  exit 0
fi

# First-run / partially-configured → one-line hint.
if [[ -z "$HAS_FFMPEG" || -z "$HAS_YTDLP" ]]; then
  echo "/watch: needs ffmpeg + yt-dlp. Run \`python3 \$CLAUDE_PLUGIN_ROOT/skills/watch/scripts/setup.py\` once to install and scaffold config."
elif [[ -z "$HAS_WHISPER" ]]; then
  echo "/watch: ready for videos with native captions. Install a LOCAL whisper engine (pip3 install mlx-whisper) to unlock on-device transcription of captionless videos."
else
  echo "/watch: ready."
fi

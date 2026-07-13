---
name: watch
version: "0.2.0-local.1"
description: Give Claude eyes for video. Watches a video from YouTube, Instagram, X/Twitter, Vimeo, TikTok, any of ~1800 yt-dlp sites, or a local file. Downloads with yt-dlp; extracts frames with ffmpeg (scene-aware, fast keyframes, or transcript-only, via one detail dial); pulls a timestamped transcript from captions or LOCAL mlx-whisper (no API key — audio never leaves the machine). Use when the user drops a video URL or file and wants what's inside. Triggers — "watch this", "what does this video say/show", "summarize this video", "get the transcript", "what happens at 3:20".
argument-hint: "<video-url-or-path> [question]"
allowed-tools: Bash, Read, AskUserQuestion
homepage: https://github.com/bradautomates/claude-video
repository: https://github.com/bradautomates/claude-video
author: Mathias Schusterman (fork of bradautomates/claude-video v2, kept local-whisper + cookies)
license: MIT
user-invocable: true
---

# /watch — Claude watches a video

You don't have a video input; this skill gives you one. A Python script gets captions first, optionally downloads the video, extracts frames as JPEGs (scene-aware, or fast keyframes at `efficient` detail), gets a timestamped transcript (native captions first, then **local whisper** — on-device, no API and no key), and prints frame paths. You then `Read` each frame path to see the images and combine them with the transcript to answer the user.

This fork = upstream v2's engine (detail dial, scene selection, keyframes, dedup, cue frames) + two deltas upstream dropped or never had: **fully local transcription** (mlx-whisper / openai-whisper — audio never leaves the machine) and **cookie support for login-gated sources**.

## Resolve `SKILL_DIR` (do this before any command)

Every `python3 ...` command below runs a bundled script under `SKILL_DIR/scripts/`. Set `SKILL_DIR` to the **absolute path of the directory containing THIS SKILL.md you just Read**. The scripts are always a direct sibling of this file (`SKILL_DIR/scripts/watch.py`). Guard once at the start of a run:

```bash
SKILL_DIR="<absolute path of the directory containing the SKILL.md you Read>"
if [ ! -f "$SKILL_DIR/scripts/watch.py" ]; then
  echo "ERROR: scripts/watch.py not found under SKILL_DIR=$SKILL_DIR" >&2
  exit 1
fi
```

## Step 0 — Setup preflight (runs every `/watch` invocation, silent on success)

**Python interpreter:** every `python3 ...` command in this skill is for macOS/Linux. On **Windows**, substitute `python`.

On the first `/watch` invocation in a session, use structured preflight:

```bash
python3 "${SKILL_DIR}/scripts/setup.py" --json
```

Branch on two fields — one row applies, one action follows:

| `first_run` | `can_proceed` | Action |
|---|---|---|
| `false` | `true` | Setup done (an engine-less user who finished setup is allowed). Proceed to Step 1 without comment. |
| `true` | any | First-time setup, in order: **(1)** `missing_binaries` non-empty → run the installer (auto-installs on macOS / prints commands elsewhere), confirm binaries land; **(2)** installer scaffolds `~/.config/watch/.env`; **(3)** relay the exact `pip3 install …` engine line it prints (`mlx-whisper` Apple Silicon only, `openai-whisper` elsewhere; declining is allowed → `--no-whisper` behavior); **(4)** ask the preference question below, write `WATCH_DETAIL=<value>` + `SETUP_COMPLETE=true`. |
| `false` | `false` | Environment regressed (e.g. binaries vanished after an OS change). Run the installer; do NOT re-ask preferences. |

A missing whisper engine is *encouraged to fix, not required*: on a genuine first run `status` reads `needs_whisper` even when binaries are present — encourage, don't block.

If `ytdlp_stale: true` in the JSON, tell the user their yt-dlp is old and likely to break on YouTube; the installer prints the upgrade command.

On follow-up `/watch` calls in the same session, use the silent check:

```bash
python3 "${SKILL_DIR}/scripts/setup.py" --check
```

Exit 0 = /watch can run (including an engine-less user who finished setup). On exit 0 the script emits **nothing** — proceed without comment. **Do NOT announce "setup is complete".**

| Exit | Meaning | Action |
|------|---------|--------|
| `2` | Missing binaries (`ffmpeg` / `ffprobe` / `yt-dlp`) | Run installer |
| `3` | Genuine first run with no local whisper engine | Run installer, relay the exact `pip3 install …` it prints (user may decline — proceed; captionless videos come back frames-only) |
| `4` | Both missing | Run installer |

The installer is idempotent — safe to re-run:

```bash
python3 "${SKILL_DIR}/scripts/setup.py"
```

On macOS with Homebrew it auto-installs `ffmpeg` and `yt-dlp`; elsewhere it prints exact commands. It scaffolds `~/.config/watch/.env` (0600) with the detail-mode placeholder. **No API key, no secrets — transcription is on-device.**

**First-run watch preference:** after the `.env` is scaffolded, use `AskUserQuestion` to ask one question — default detail (one dial), options in this exact order, keeping `(recommended)` on `balanced`: `transcript` · `efficient` · `balanced` (recommended) · `token-burner`. Option behaviors and caps are defined once in "Recommended limits" — use those definitions as the option descriptions.

Write the answer into `~/.config/watch/.env` as a bare `WATCH_DETAIL=<value>` line — **no trailing inline comment**. Then set `SETUP_COMPLETE=true` in the same file. Don't ask again once `SETUP_COMPLETE=true`.

**Structured mode:** `--json` emits `{status, can_proceed, first_run, setup_complete, missing_binaries, whisper_backend, has_whisper, ytdlp_age_days, ytdlp_stale, config_file, watch_detail, platform}` where `status` ∈ `ready | needs_install | needs_whisper | needs_install_and_whisper`.

Within a single session, skip Step 0 on follow-up `/watch` calls once `--check` returned 0.

## When to use

- User pastes a video URL (YouTube, Vimeo, X, TikTok, Twitch clip, most yt-dlp-supported sites) and asks about it.
- User points at a local video file (`.mp4`, `.mov`, `.mkv`, `.webm`, etc.) and asks about it.
- User types `/watch <url-or-path> [question]`.

## Recommended limits

- **Best accuracy: videos under 10 minutes.** Frame coverage scales inversely with duration.
- **Universal rate cap: 2 fps.**
- **The detail mode sets both behavior and frame ceiling** (`WATCH_DETAIL` in `~/.config/watch/.env`, or `--detail`) — this list is the canonical mode reference:
  - `transcript` → **no frames**; captions-only report, no video download. No captions → local whisper fallback (see "Transcription"); still nothing → report the limitation and offer a `--detail balanced` re-run.
  - `efficient` → up to **50 keyframes** (`ffmpeg -skip_frame nokey`) — near-instant, lands on scene cuts; uniform-sampling fallback if a clip has <4 keyframes.
  - `balanced` (default) → up to **100 scene-aware** frames (ffmpeg scene-change selection; uniform fallback for static video).
  - `token-burner` → **uncapped**, scene-aware (soft warning past 250 frames).
  - `--max-frames N` overrides whichever cap the mode would otherwise use. Frame lines carry timestamp + selection reason; images clamp to 1998px height for `Read` compatibility.
- **Full-video frame budget by duration** (sets fps and the uniform fallback; scene selection fills up to the detail cap, whichever is lower): ≤30s → ~12-30 · 30s-1min → ~40 · 1-3min → ~60 · 3-10min → ~80 · >10min → up to the detail cap, sparse (warning printed).
- 🔴 **CHECKPOINT — before any `token-burner` run, or any run on a video >30 min:** STOP and confirm with the user (scope: whole video vs a `--start/--end` section; expected frame count and rough token cost). Do not start an uncapped or sparse hour-long scan on your own judgment.

## How to invoke

**Step 1 — parse the user input.** Separate the video source from any question, mechanically: the token matches `^https?://` → URL; else if the file exists on disk → local path; else ask ONE clarifying question before running anything.

**Step 2 — run the watch script.** Pass the source verbatim:

```bash
python3 "${SKILL_DIR}/scripts/watch.py" "<source>"
```

Optional flags:
- `--detail transcript|efficient|balanced|token-burner` — fidelity/speed dial (see above).
- `--start T` / `--end T` — focus on a section (`SS`, `MM:SS`, or `HH:MM:SS`); fps auto-scales denser.
- `--timestamps T1,T2,…` — grab a frame at each absolute timestamp. Use after reading the transcript to capture deictic moments ("look here", "as you can see") that visual selection may miss. See "Transcript-cue frames".
- `--max-frames N` — override the preset cap for a tighter token budget.
- `--resolution W` — frame width in px (default 512; 1024 only if the user needs to read on-screen text).
- `--fps F` — override auto-fps (clamped to 2 fps max).
- `--out-dir DIR` — keep working files somewhere specific (default: auto tmp dir).
- `--whisper mlx|openai-whisper|lightning` — force a specific LOCAL whisper engine (default: prefer mlx on Apple Silicon; `lightning` is opt-in).
- `--no-whisper` — disable the local whisper fallback (frames-only if no captions).
- `--no-dedup` — keep near-duplicate frames (by default a frame-delta pass drops near-identical frames — held slides, static screens — and the report's **Frames** line notes how many were dropped).
- `--cookies-from-browser B` — read cookies live from a local browser (`chrome`, `firefox`, `safari`, `edge`, `brave`, …) for login-gated sources.
- `--cookies FILE` — Netscape-format `cookies.txt` (alternative to the above).

### Login-gated sources (Instagram, X, private/age-restricted videos)

Public videos download with no auth. Instagram, X/Twitter, age-restricted or private/unlisted YouTube, and members-only content need the *user's own* cookies. **Do NOT pass cookies pre-emptively** — try the plain download first; only reach for cookies on a login / private / 403 / "login required" / rate-limit error, and walk the user through it:

**(a)** Ask which browser they're logged into (`chrome`, `firefox`, `safari`, `edge`, `brave`, `chromium`, `opera`, `vivaldi`).
**(b)** Re-run with `--cookies-from-browser <browser>`.
**(c)** Per-browser snags: **Chrome on macOS** locks its cookie DB while open AND encrypts cookies — have the user fully quit Chrome (Cmd-Q) and click **Always Allow** on the Keychain prompt; if it keeps fighting, switch to Safari or Firefox. **Chrome on Windows** also locks while running (check the tray). **Safari on macOS** needs Full Disk Access for the terminal. **Firefox** usually works without closing — good fallback.
**(d)** Manual fallback: guide the user to export a `cookies.txt` (e.g. the open-source "Get cookies.txt LOCALLY" extension), then `--cookies ~/Downloads/cookies.txt`.

The cookie privacy contract (read live, piped to the subprocess, never persisted) is stated once in "Security & Permissions".

### Focusing on a section (higher frame rate)

When the user asks about a specific moment, pass `--start`/`--end`. Focused-mode budgets (bounded by the detail cap; counts assume `balanced`): ≤5s → 2 fps (≤10) · 5-15s → 2 fps (≤30) · 15-30s → ~2 fps (≤60) · 30-60s → ~1.3 fps (≤80) · 60-180s → ~0.6 fps (100, capped).

Focused mode is right for: any explicitly named moment/range; any >10min video where the question is about a specific part; re-runs after a sparse full scan. Transcript auto-filters to the range; frame timestamps stay absolute.

```bash
python3 "${SKILL_DIR}/scripts/watch.py" video.mp4 --start 50 --end 60
python3 "${SKILL_DIR}/scripts/watch.py" "$URL" --start 2:15 --end 2:45 --fps 2
python3 "${SKILL_DIR}/scripts/watch.py" "$URL" --start 1:12:00
```

**Step 3 — Read every frame path the script lists.** Read all frames in a single message (parallel tool calls). Frames are chronological with a `t=MM:SS` absolute timestamp.

**Step 4 — answer the user.** Two evidence streams: **frames** (what's on screen when) and **transcript** (what's said when; header shows `captions` or `whisper (mlx)` / `whisper (openai-whisper)`). Answer specific questions with timestamp citations; otherwise summarize structure, key moments, notable visuals, spoken content. This holds for `transcript` detail too — synthesize a summary, don't paste the raw transcript; offer it only if asked.

**Step 5 — clean up.** 🔴 **CHECKPOINT — destructive:** the default is **KEEP** the work dir (it holds the mp4 that makes re-runs free). Delete it (`rm -rf <dir>`) ONLY after the user explicitly confirms they're done with the video — never infer "done" from topic drift.

### Worked example (end to end)

User: *"watch https://youtu.be/jNQXAC9IVRw — what's it about?"*

```bash
python3 "${SKILL_DIR}/scripts/watch.py" "https://youtu.be/jNQXAC9IVRw"   # balanced default
```

Script prints ~19 scene frames (`frame_0001.jpg  t=00:00  reason=scene-change` …) + a
timestamped transcript (`[00:01] All right, so here we are, in front of the elephants`).
You `Read` all 19 frames in one message, then answer citing both streams:

> The first-ever YouTube video — Jawed Karim at the San Diego Zoo's elephant enclosure
> (visible behind him from 00:00). He notes the elephants' "really, really long trunks"
> [00:05] and signs off at [00:16]: "that's pretty much all there is to say."

Follow-up "show me the moment he mentions trunks" → no re-run needed: point at
`frame_0004.jpg t=00:05` already in context.

Other modes, same shape:

```bash
python3 "${SKILL_DIR}/scripts/watch.py" "$URL" --detail transcript   # words only, no video download
python3 "${SKILL_DIR}/scripts/watch.py" "$URL" --detail efficient    # fastest visual pass (keyframes)
```

## Transcript-cue frames

Visual selection can miss moments a presenter explicitly flags — pointing at a slide is often a *low* visual change. `--timestamps` forces frames at those moments. **You** decide which moments matter, by reading the transcript:

1. Run once at `--detail transcript` (or any detail) to get the timestamped transcript.
2. Scan for deictic cues — the speaker directing attention. **Counts as a cue:** "look here / look at this", "as you can see", "notice this", "watch what happens", "right here / here on screen", "this chart/diagram/graph shows". **NOT a cue (rhetorical):** "look, the point is…", "you see what I mean", "watch out for". When genuinely unsure, include it — a spare cue frame costs little.
3. Re-run with `--timestamps 4:32,7:10,9:55` (absolute times), pointing the second run at the **downloaded local file** in the work dir so it doesn't re-download.

Behavior: additive by default (`reason=transcript-cue`, merged chronologically); pinned and counted against the cap first (never evicted); honors `--start/--end` (out-of-window cues dropped and reported); `--detail transcript --timestamps …` returns *only* the cue frames.

## Transcription

1. **Native captions (free, preferred).** yt-dlp pulls manual or auto-generated subtitles when available.
2. **Local whisper fallback (on-device, no API, no key).** If no captions (or a local file), the script extracts audio (`ffmpeg -vn -ac 1 -ar 16000 -b:a 64k`, ~0.5 MB/min) and transcribes locally:
   - **mlx-whisper** — `mlx-community/whisper-large-v3-turbo`. Preferred on Apple Silicon (GPU/Neural Engine). `pip3 install mlx-whisper`.
   - **openai-whisper** — `base` model on CPU. Cross-platform fallback. `pip3 install openai-whisper`.
   - **lightning** — opt-in only (`--whisper lightning`): [lightning-whisper-mlx](https://github.com/mustafaaljadery/lightning-whisper-mlx) `large-v3`, batched decode on Apple Silicon. `pip3 install lightning-whisper-mlx`.

The audio never leaves the machine. Override with `--whisper openai-whisper` (or `--whisper lightning`); language auto-detects; `--no-whisper` skips the fallback entirely.

🔴 **CHECKPOINT — one-time model download:** the first mlx run fetches the ~1.5 GB model from Hugging Face (cached under `~/.cache/huggingface` afterwards). If the model is not yet cached, STOP and confirm the download with the user before transcribing.

## Failure modes and handling

- **Setup preflight failed** → run the installer; relay the exact `pip3 install …` line it prints for the whisper engine.
- **`Precondition check failed` / `HTTP Error 400` from YouTube** → **stale yt-dlp** (the #1 real-world breakage; yt-dlp versions are dates and YouTube breaks old ones). Upgrade with the pip/brew that owns the binary (`pip3 install -U yt-dlp`), then retry. The preflight's `ytdlp_stale` flag warns before this bites.
- **No transcript available** → captions missing AND (no local engine OR `--no-whisper` OR transcription failed). Proceed frames-only and tell the user.
- **Long video warning printed** → acknowledge it; offer a focused re-run via `--start`/`--end` instead of a sparse scan.
- **Download fails (login/private/403)** → the source needs auth. Re-run with `--cookies-from-browser <browser>` (see "Login-gated sources"). Region-locked or genuinely unavailable → say so plainly; don't keep retrying.
- **Whisper fails** → error on stderr (engine not installed, or no audio track). Report says "none available".
- **mlx model download fails / partial** (network drop mid-fetch) → delete the partial cache (`rm -rf ~/.cache/huggingface/hub/models--mlx-community--whisper-large-v3-turbo`), retry once; still failing → `--whisper openai-whisper` or `--no-whisper`.
- **`No space left on device`** during download/extraction → re-run with `--out-dir` on a roomier volume, or shrink the job (`--detail efficient`, or narrow with `--start`/`--end`).
- **Work dir vanished between follow-ups** (OS tmp cleanup) → re-run from the original URL and say so — one fresh download is unavoidable.
- **A frame `Read` is rejected** (rare — frames are pre-clamped to 1998px height) → re-run with `--resolution 512`.
- **`AskUserQuestion` unavailable or declined** during first-run setup → use `balanced`, write `WATCH_DETAIL=balanced` + `SETUP_COMPLETE=true`, and note the user can edit `~/.config/watch/.env` later.

## Do NOT — anti-patterns (each one wastes tokens, time, or trust)

- **Never pass `--cookies-from-browser`/`--cookies` pre-emptively.** Cookies are a reaction to a login/private error, walked through with the user — not a default flag.
- **Never re-download a video you already have.** Follow-up runs (`--timestamps`, `--start/--end`, higher `--resolution`) point at the mp4 in the existing work dir.
- **Never re-run /watch for follow-up questions in the same session** — the frames and transcript are already in context; answer from them.
- **Never paste the full raw transcript into your answer.** Quote the lines that ground your claim; the user can ask for more.
- **Never retry a failed download unchanged.** Each failure maps to a different fix (stale yt-dlp → upgrade; 403/login → cookies flow; region-locked → say so and stop). Blind retries just repeat the error.
- **Never run `token-burner` on a long video without the user's explicit go** — governed by the 🔴 CHECKPOINT in "Recommended limits".
- **Never delete the work dir before the user is done asking questions** — cleanup is last, not part of answering.

## Token efficiency

Frames dominate cost: 80 frames at 512px ≈ 50-80k image tokens; the transcript is cheap. `--resolution 1024` roughly quadruples per-frame tokens — only when necessary. If you already watched a video this session, do **not** re-run for follow-ups — answer from the frames and transcript already in context.

## Security & Permissions

**What this skill does:**
- Runs `yt-dlp` locally to download the video and pull native captions (public data; requests go directly to the URL's host)
- Runs `ffmpeg` / `ffprobe` locally to extract frames and, when whisper is needed, a mono 16 kHz audio clip
- Transcribes the audio clip **locally on-device** (mlx-whisper or openai-whisper) — no network call, no API, no key
- Writes video, frames, audio, and intermediate transcript to a working directory (system temp or `--out-dir`)
- Reads / creates `~/.config/watch/.env` (0600) for the detail preference and `SETUP_COMPLETE` marker
- On first mlx run, downloads the whisper model (~1.5 GB) from Hugging Face once, cached under `~/.cache/huggingface`

**What this skill does NOT do:**
- Does not upload the video OR the audio to any API — transcription is fully local; the only outbound traffic is yt-dlp fetching the video/captions (and the one-time model download)
- Does not log into or post to any account; reads browser cookies only when the user explicitly passes `--cookies-from-browser` / `--cookies` for a login-gated source, live-piped to yt-dlp — never copied, stored, logged, or transmitted
- Does not use, store, or require any API key — no secrets in `.env`
- Does not persist anything outside the working directory, the config file, and the model cache — clean up the working directory when done (Step 5)

**Bundled scripts:** `scripts/watch.py` (entry), `scripts/download.py` (yt-dlp wrapper + cookies), `scripts/frames.py` (keyframe/scene/cue extraction + dedup), `scripts/transcribe.py` (caption parsing), `scripts/local_whisper.py` (LOCAL mlx/openai-whisper), `scripts/config.py` (detail dial), `scripts/setup.py` (preflight + installer + yt-dlp staleness check)

Review scripts before first use to verify behavior.

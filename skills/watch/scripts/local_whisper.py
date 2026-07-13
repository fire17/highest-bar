#!/usr/bin/env python3
"""Transcribe a video locally with mlx-whisper — no API, no key.

This is the fork's privacy delta over upstream v2: same pipeline interface as
upstream's Groq/OpenAI client (`load_api_key` + `transcribe_video`), but the
transcription runs on-device (mlx-whisper on Apple Silicon, openai-whisper on
CPU). Returns segments in the same shape as transcribe.parse_vtt so the rest
of the pipeline (filter_range, format_transcript) doesn't care where the
transcript came from.

Nothing leaves the machine: no network call, no key, no upload.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


# mlx-whisper model (Apple Silicon). Fast + accurate.
MLX_MODEL = "mlx-community/whisper-large-v3-turbo"
# openai-whisper fallback model (CPU). "base" is the speed/accuracy sweet spot.
OPENAI_WHISPER_MODEL = "base"
# lightning-whisper-mlx model KEY (opt-in). Batched decode on Apple Silicon.
# "large-v3" keeps multilingual parity with MLX_MODEL (the distil-* keys are
# English-only); batching is where lightning's speed comes from.
LIGHTNING_MODEL = "large-v3"

# Default auto-detect order. "lightning" is deliberately NOT here — it is
# strictly opt-in via preferred="lightning" (i.e. `--whisper lightning`).
BACKENDS = ("mlx", "openai-whisper")


def detect_backend(preferred: str | None = None) -> tuple[str, str] | tuple[None, None]:
    """Return (backend, model) for the first available local engine.

    backend is "mlx", "openai-whisper", or "lightning"; model is the model
    id/name/key to load. Returns (None, None) if the (preferred) package is
    not importable.

    If `preferred` is "mlx" / "openai-whisper" / "lightning", only that engine
    is considered. "lightning" is opt-in only: it never appears in the default
    auto-detect order.
    """
    if preferred == "lightning":
        order = ["lightning"]
    else:
        order = [b for b in BACKENDS if preferred is None or b == preferred]

    for backend in order:
        if backend == "mlx":
            try:
                import mlx_whisper  # noqa: F401
                return "mlx", MLX_MODEL
            except ImportError:
                continue
        elif backend == "openai-whisper":
            try:
                import whisper  # noqa: F401
                return "openai-whisper", OPENAI_WHISPER_MODEL
            except ImportError:
                continue
        elif backend == "lightning":
            try:
                import lightning_whisper_mlx  # noqa: F401
                return "lightning", LIGHTNING_MODEL
            except ImportError:
                continue
    return None, None


def load_api_key(preferred: str | None = None) -> tuple[str, str] | tuple[None, None]:
    """Upstream-interface shim: return (backend, "local") for the first local engine.

    There is no API key in this fork — transcription is on-device. The second
    element is the sentinel "local" so upstream call sites' truthiness checks
    (`if backend and api_key`) keep working unchanged.
    """
    backend, _model = detect_backend(preferred)
    if backend is None:
        return None, None
    return backend, "local"


def extract_audio(video_path: str, out_path: Path) -> Path:
    """Extract mono 16kHz 64kbps mp3 — small, fast for whisper to chew on."""
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is not installed. Install with: brew install ffmpeg")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-y",
        "-i", str(Path(video_path).resolve()),
        "-vn",
        "-acodec", "libmp3lame",
        "-ar", "16000",
        "-ac", "1",
        "-b:a", "64k",
        str(out_path.resolve()),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(f"ffmpeg audio extraction failed: {result.stderr.strip()}")
    if not out_path.exists() or out_path.stat().st_size == 0:
        raise SystemExit("ffmpeg produced no audio — video may have no audio track")
    return out_path


def _segments_from_result(result: dict) -> list[dict]:
    """Convert a whisper result into our {start, end, text} segment format."""
    out: list[dict] = []
    for seg in result.get("segments") or []:
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        out.append({
            "start": round(float(seg.get("start") or 0.0), 2),
            "end": round(float(seg.get("end") or 0.0), 2),
            "text": text,
        })

    if not out:
        full = (result.get("text") or "").strip()
        if full:
            out.append({"start": 0.0, "end": 0.0, "text": full})

    return out


def _segments_from_lightning(result: dict) -> list[dict]:
    """Shape a lightning-whisper-mlx result into our {start, end, text} format.

    lightning (0.0.10) differs from mlx/openai-whisper: each segment is a
    [start_cs, end_cs, text] LIST with times in CENTISECONDS (hundredths of a
    second), not a dict of seconds. Convert to our seconds-based dict shape.
    Falls back to the flat "text" field if no segments come back.
    """
    out: list[dict] = []
    for seg in result.get("segments") or []:
        try:
            start_cs, end_cs, text = seg[0], seg[1], seg[2]
        except (TypeError, IndexError, KeyError):
            continue
        text = (text or "").strip()
        if not text:
            continue
        out.append({
            "start": round(float(start_cs) / 100.0, 2),
            "end": round(float(end_cs) / 100.0, 2),
            "text": text,
        })

    if not out:
        full = (result.get("text") or "").strip()
        if full:
            out.append({"start": 0.0, "end": 0.0, "text": full})

    return out


def transcribe_video(
    video_path: str,
    audio_out: Path,
    backend: str | None = None,
    api_key: str | None = None,  # accepted for upstream interface compat; unused
    model: str | None = None,
    language: str | None = None,
) -> tuple[list[dict], str]:
    """Run the full flow: extract audio → transcribe locally → parse segments.

    `language` of None lets whisper auto-detect (works for any-language video).
    Returns (segments, backend_used). Raises SystemExit on any failure.
    """
    if backend is None:
        backend, model = detect_backend()
    elif model is None:
        model = {
            "mlx": MLX_MODEL,
            "lightning": LIGHTNING_MODEL,
        }.get(backend, OPENAI_WHISPER_MODEL)

    if not backend:
        raise SystemExit(
            "No local whisper engine found. Install one:\n"
            "  pip3 install mlx-whisper   (preferred on Apple Silicon)\n"
            "  pip3 install openai-whisper  (CPU fallback)\n"
            "  pip3 install lightning-whisper-mlx  (opt-in: --whisper lightning)"
        )

    print(f"[watch] extracting audio for local whisper ({backend})…", file=sys.stderr)
    audio_path = extract_audio(video_path, audio_out)
    size_kb = audio_path.stat().st_size / 1024
    print(f"[watch] audio: {size_kb:.0f} kB — transcribing on-device ({backend})…", file=sys.stderr)

    if backend == "mlx":
        import mlx_whisper
        result = mlx_whisper.transcribe(
            str(audio_path),
            path_or_hf_repo=model or MLX_MODEL,
            language=language,
        )
    elif backend == "openai-whisper":
        import whisper
        loaded = whisper.load_model(model or OPENAI_WHISPER_MODEL)
        result = loaded.transcribe(str(audio_path), language=language)
    elif backend == "lightning":
        # Opt-in batched engine. Model here is a lightning model KEY
        # (tiny/base/small/medium/large-v3/distil-*), not an HF repo id.
        # lightning's result segments are [start_cs, end_cs, text] lists in
        # centiseconds — a shape unlike mlx/openai-whisper — so they get their
        # own shaper below.
        from lightning_whisper_mlx import LightningWhisperMLX
        engine = LightningWhisperMLX(model=model or LIGHTNING_MODEL)
        result = engine.transcribe(str(audio_path), language=language)
    else:
        raise SystemExit(f"Unknown whisper backend: {backend}")

    if backend == "lightning":
        segments = _segments_from_lightning(result)
    else:
        segments = _segments_from_result(result)
    if not segments:
        raise SystemExit("Whisper returned no transcript segments")

    print(f"[watch] transcribed {len(segments)} segments via {backend}", file=sys.stderr)
    return segments, backend


if __name__ == "__main__":
    import json

    if len(sys.argv) < 2:
        print("usage: whisper.py <video-path> [<audio-out.mp3>] [--backend mlx|openai-whisper|lightning]", file=sys.stderr)
        raise SystemExit(2)

    video = sys.argv[1]
    audio_out = Path(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else Path("audio.mp3")
    backend_override = None
    if "--backend" in sys.argv:
        backend_override = sys.argv[sys.argv.index("--backend") + 1]

    bk, mdl = detect_backend(backend_override)
    segments, used = transcribe_video(video, audio_out, backend=bk, model=mdl)
    print(json.dumps({"backend": used, "segments": segments}, indent=2))

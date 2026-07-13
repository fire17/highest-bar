"""setup.py --json surfaces the resolved watch detail."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SETUP = Path(__file__).resolve().parent.parent / "scripts" / "setup.py"


def _run(args, *, home=None, extra_env=None):
    env = dict(os.environ)
    env.pop("WATCH_DETAIL", None)
    # Don't let a real key in the developer's shell env leak into the test.
    env.pop("GROQ_API_KEY", None)
    env.pop("OPENAI_API_KEY", None)
    env.pop("SETUP_COMPLETE", None)
    if home is not None:
        env["HOME"] = str(home)
        env["USERPROFILE"] = str(home)  # Windows
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, str(SETUP), *args],
        capture_output=True, text=True, env=env,
    )


def _write_env(home: Path, body: str) -> None:
    cfg = home / ".config" / "watch"
    cfg.mkdir(parents=True, exist_ok=True)
    f = cfg / ".env"
    f.write_text(body, encoding="utf-8")
    f.chmod(0o600)


def test_json_reports_watch_detail():
    proc = _run(["--json"])
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["watch_detail"] == "balanced"


def _setup_module(tmp_path, monkeypatch, engine=None, env_body=""):
    """Import setup.py in-process with config + engine detection pinned.

    find_spec sees real site-packages, so a subprocess can't hide an installed
    engine — in-process monkeypatching is the honest seam for engine-less states.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("watch_setup", SETUP)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cfg_dir = tmp_path / ".config" / "watch"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    cfg = cfg_dir / ".env"
    if env_body:
        cfg.write_text(env_body, encoding="utf-8")
        cfg.chmod(0o600)
    monkeypatch.setattr(mod, "CONFIG_DIR", cfg_dir)
    monkeypatch.setattr(mod, "CONFIG_FILE", cfg)
    monkeypatch.setattr(
        mod, "_have_whisper_engine",
        lambda: (True, engine) if engine else (False, None),
    )
    return mod


def test_engineless_completed_setup_proceeds_silently(tmp_path, monkeypatch):
    """A user who finished setup without a whisper engine must NOT be nagged forever."""
    mod = _setup_module(tmp_path, monkeypatch, engine=None,
                        env_body="SETUP_COMPLETE=true\n")
    assert mod.cmd_check() == 0
    s = mod._status()
    assert s["can_proceed"] is True
    assert s["first_run"] is False
    assert s["setup_complete"] is True
    # status still encourages an engine even though we can proceed
    assert s["status"] == "needs_whisper"
    assert s["has_whisper"] is False


def test_engineless_first_run_is_encouraged(tmp_path, monkeypatch, capsys):
    """Genuine first run with no local engine: --check exits 3 (encourage install)."""
    mod = _setup_module(tmp_path, monkeypatch, engine=None, env_body="# fresh\n")
    assert mod.cmd_check() == 3
    assert "whisper" in capsys.readouterr().err.lower()
    s = mod._status()
    assert s["can_proceed"] is False
    assert s["first_run"] is True


def test_local_engine_present_is_ready(tmp_path):
    """With a local engine importable (fake mlx_whisper), status is ready — no key needed."""
    _write_env(tmp_path, "# fresh\n")
    fake = tmp_path / "fake"
    fake.mkdir()
    (fake / "mlx_whisper.py").write_text("def transcribe(*a, **k): return {}\n")
    chk = _run(["--check"], home=tmp_path, extra_env={"PYTHONPATH": str(fake)})
    assert chk.returncode == 0, chk.stderr

    js = json.loads(_run(["--json"], home=tmp_path, extra_env={"PYTHONPATH": str(fake)}).stdout)
    assert js["status"] == "ready"
    assert js["can_proceed"] is True
    assert js["whisper_backend"] == "mlx"
    assert js["has_whisper"] is True


def test_ytdlp_staleness_fields_present():
    """The staleness check (stale yt-dlp = #1 real-world breakage) is always reported."""
    js = json.loads(_run(["--json"]).stdout)
    assert "ytdlp_age_days" in js and "ytdlp_stale" in js
    if js["ytdlp_age_days"] is not None:
        assert isinstance(js["ytdlp_stale"], bool)

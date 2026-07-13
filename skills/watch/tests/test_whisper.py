"""Local whisper backend (fork delta): detection, interface shim, segment shaping.

Upstream v2's cloud tests (plan_chunks / split_audio / API chunking) don't apply —
this fork transcribes on-device and never uploads. These tests cover the local
module's contract with watch.py instead.
"""
from __future__ import annotations

import sys
import types

import pytest

import local_whisper


@pytest.fixture
def fake_engines(monkeypatch):
    """Make all local engines 'importable' without installing them."""
    monkeypatch.setitem(sys.modules, "mlx_whisper", types.ModuleType("mlx_whisper"))
    monkeypatch.setitem(sys.modules, "whisper", types.ModuleType("whisper"))
    monkeypatch.setitem(
        sys.modules, "lightning_whisper_mlx", types.ModuleType("lightning_whisper_mlx")
    )


@pytest.fixture
def no_engines(monkeypatch):
    """Make all local engines unimportable."""
    for mod in ("mlx_whisper", "whisper", "lightning_whisper_mlx"):
        monkeypatch.setitem(sys.modules, mod, None)


class TestDetectBackend:
    def test_prefers_mlx_when_both_available(self, fake_engines):
        backend, model = local_whisper.detect_backend()
        assert backend == "mlx"
        assert model == local_whisper.MLX_MODEL

    def test_preferred_openai_whisper_wins(self, fake_engines):
        backend, model = local_whisper.detect_backend("openai-whisper")
        assert backend == "openai-whisper"
        assert model == local_whisper.OPENAI_WHISPER_MODEL

    def test_none_when_nothing_installed(self, no_engines):
        assert local_whisper.detect_backend() == (None, None)

    def test_preferred_missing_engine_is_none(self, monkeypatch, fake_engines):
        monkeypatch.setitem(sys.modules, "mlx_whisper", None)
        assert local_whisper.detect_backend("mlx") == (None, None)

    def test_lightning_is_opt_in_only(self, fake_engines):
        # Even with lightning importable, the default order never picks it.
        backend, _ = local_whisper.detect_backend()
        assert backend == "mlx"

    def test_preferred_lightning_wins(self, fake_engines):
        backend, model = local_whisper.detect_backend("lightning")
        assert backend == "lightning"
        assert model == local_whisper.LIGHTNING_MODEL

    def test_preferred_lightning_missing_is_none(self, monkeypatch, fake_engines):
        monkeypatch.setitem(sys.modules, "lightning_whisper_mlx", None)
        assert local_whisper.detect_backend("lightning") == (None, None)


class TestLoadApiKeyShim:
    """watch.py calls `load_api_key` and truth-tests both tuple elements —
    the shim must satisfy that contract with no actual key."""

    def test_returns_backend_and_local_sentinel(self, fake_engines):
        backend, key = local_whisper.load_api_key()
        assert backend == "mlx"
        assert key == "local"
        assert backend and key  # the exact truthiness check watch.py does

    def test_none_none_when_no_engine(self, no_engines):
        assert local_whisper.load_api_key() == (None, None)

    def test_lightning_shim_returns_local_sentinel(self, fake_engines):
        backend, key = local_whisper.load_api_key("lightning")
        assert backend == "lightning"
        assert key == "local"
        assert backend and key  # watch.py's truthiness gate


class TestSegmentsFromResult:
    def test_segments_shaped_and_rounded(self):
        result = {"segments": [
            {"start": 0.123456, "end": 1.98765, "text": "  hello  "},
            {"start": 2, "end": 3, "text": ""},  # empty text dropped
        ]}
        segs = local_whisper._segments_from_result(result)
        assert segs == [{"start": 0.12, "end": 1.99, "text": "hello"}]

    def test_falls_back_to_full_text(self):
        segs = local_whisper._segments_from_result({"text": "whole thing"})
        assert segs == [{"start": 0.0, "end": 0.0, "text": "whole thing"}]

    def test_empty_result_is_empty(self):
        assert local_whisper._segments_from_result({}) == []


class TestSegmentsFromLightning:
    """lightning-whisper-mlx 0.0.10 segments are [start_cs, end_cs, text] lists
    in centiseconds — a different shape than mlx/openai-whisper dicts."""

    def test_centisecond_lists_shaped_to_seconds(self):
        result = {"segments": [
            [0, 1901, "  Alright, elephants.  "],
            [1901, 3500, ""],  # empty text dropped
        ]}
        segs = local_whisper._segments_from_lightning(result)
        assert segs == [{"start": 0.0, "end": 19.01, "text": "Alright, elephants."}]

    def test_falls_back_to_full_text(self):
        segs = local_whisper._segments_from_lightning(
            {"segments": [], "text": "whole thing"}
        )
        assert segs == [{"start": 0.0, "end": 0.0, "text": "whole thing"}]

    def test_empty_result_is_empty(self):
        assert local_whisper._segments_from_lightning({}) == []


class TestTranscribeVideoGuards:
    def test_no_engine_raises_with_install_hint(self, no_engines, tmp_path):
        with pytest.raises(SystemExit) as exc:
            local_whisper.transcribe_video("nonexistent.mp4", tmp_path / "a.mp3")
        assert "pip3 install" in str(exc.value)

    def test_accepts_upstream_api_key_kwarg(self, no_engines, tmp_path):
        # Interface compat: watch.py passes api_key=…; must not TypeError.
        with pytest.raises(SystemExit):
            local_whisper.transcribe_video(
                "nonexistent.mp4", tmp_path / "a.mp3", backend=None, api_key="local",
            )

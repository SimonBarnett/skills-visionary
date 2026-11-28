"""FR #281: Plan icon uses checked-in gantt-chart source asset."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "apps" / "plan_agent" / "assets"
SOURCE = ASSETS / "plan-gantt-source.png"


def test_fr281_gantt_source_is_512_png():
    assert SOURCE.is_file(), f"missing source: {SOURCE}"
    raw = SOURCE.read_bytes()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(raw) >= 10_000, "source PNG smaller than issue attachment"


def test_fr281_build_script_imports_master_path():
    text = (ROOT / "tools" / "build_plan_gantt_icon.py").read_text(encoding="utf-8")
    assert "plan-gantt-source.png" in text
    assert "make_gantt" not in text
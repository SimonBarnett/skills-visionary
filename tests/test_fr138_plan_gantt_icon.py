"""VIS-06 / FR #138: Plan GANTT icon asset present for exe/systray/docs."""
from __future__ import annotations

import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "apps" / "plan_agent" / "assets"
ICO = ASSETS / "plan-gantt.ico"
PNG = ASSETS / "plan-gantt.png"


def test_fr138_gantt_ico_exists_and_valid():
    assert ICO.is_file(), f"missing GANTT icon: {ICO}"
    raw = ICO.read_bytes()
    assert len(raw) >= 200, "ICO too small"
    reserved, itype, count = struct.unpack_from("<HHH", raw, 0)
    assert reserved == 0 and itype == 1 and count >= 1
    # At least one entry names a tray-sized image (16 or 32).
    sizes = []
    for i in range(count):
        w, h = struct.unpack_from("<BB", raw, 6 + i * 16)[:2]
        sizes.append((w or 256, h or 256))
    assert any(s[0] in (16, 24, 32) for s in sizes), sizes


def test_fr138_gantt_png_docs_master_exists():
    assert PNG.is_file(), f"missing GANTT PNG: {PNG}"
    raw = PNG.read_bytes()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(raw) >= 500


def test_fr138_assets_readme_names_gantt():
    readme = ASSETS / "README.md"
    assert readme.is_file()
    text = readme.read_text(encoding="utf-8")
    assert "plan-gantt.ico" in text
    assert "GANTT" in text.upper() or "Gantt" in text

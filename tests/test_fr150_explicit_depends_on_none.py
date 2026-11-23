# -*- coding: utf-8 -*-
"""VIS-D4 / FR #150: explicit Depends-on: (none); silent omission fails."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_depends_on_stamp.py"
VISIONARY = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"
CATALOG = ROOT / "apps" / "mcp-catalog" / "catalog" / "visionary" / "SKILL.md"
FIXTURE = ROOT / "docs" / "fixtures" / "depends-on-none"

sys.path.insert(0, str(ROOT / "tools"))
import check_depends_on_stamp as chk  # noqa: E402


def _text(path: Path) -> str:
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), path
    return raw.decode("utf-8")


def test_fr150_check_rejects_silent_omission():
    assert chk.check_text("no stamp here") == ["silent omission: no Depends-on line"]
    assert chk.has_depends_on_stamp("**Depends-on:** (none)\n") is True
    assert chk.has_explicit_none("**Depends-on:** (none)\n") is True
    assert chk.has_explicit_none("**Depends-on:** #12\n") is False
    assert chk.check_text("**Depends-on:** #12\n", require_none=True)


def test_fr150_fixture_pack_shows_none():
    assert (FIXTURE / "README.md").is_file()
    body = _text(FIXTURE / "issue-body.md")
    pack = _text(FIXTURE / "vision-pack-snippet.md")
    assert body.lstrip().startswith("**Depends-on:** (none)")
    assert "**Depends-on:** (none)" in body[:500]
    assert "**Depends-on:** (none)" in pack or "Depends-on:** (none)" in pack
    assert "silent omission" in _text(FIXTURE / "README.md").lower()
    proc = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--require-none",
            str(FIXTURE / "issue-body.md"),
            str(FIXTURE / "vision-pack-snippet.md"),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_fr150_cli_fails_on_omission():
    # Avoid pytest tmp_path on locked D:\Temp\pytest-of-* (WinError 5).
    bad = ROOT / "docs" / "fixtures" / "depends-on-none" / "_omit-tmp.md"
    try:
        bad.write_text("# FR with no Depends-on\n", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(bad)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc.returncode != 0
        assert "silent omission" in (proc.stderr + proc.stdout).lower()
    finally:
        if bad.is_file():
            bad.unlink()


def test_fr150_visionary_cast_iron_none():
    text = _text(VISIONARY)
    assert "VIS-D4" in text or "FR #150" in text
    assert "Depends-on: (none)" in text or "`Depends-on: (none)`" in text
    low = text.lower()
    assert "silent omission" in low
    assert "check_depends_on_stamp" in text
    assert "docs/fixtures/depends-on-none" in text
    catalog = _text(CATALOG)
    assert "VIS-D4" in catalog or "FR #150" in catalog
    assert "(none)" in catalog

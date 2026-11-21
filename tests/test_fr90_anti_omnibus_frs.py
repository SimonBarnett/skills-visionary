"""FR #90: CAST IRON anti-omnibus FRs for unpaid / non-frontier seats."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VISIONARY = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"
CATALOG = ROOT / "apps" / "mcp-catalog" / "catalog" / "visionary" / "SKILL.md"


def _text(path: Path) -> str:
    assert path.is_file(), path
    return path.read_text(encoding="utf-8")


def test_fr90_cast_iron_anti_omnibus_in_visionary():
    text = _text(VISIONARY)
    assert "CAST IRON" in text
    assert "Anti-omnibus" in text or "anti-omnibus" in text
    assert "FR #90" in text
    assert "non-frontier" in text or "unpaid" in text
    low = text.lower()
    assert "omnibus" in low
    assert "never" in low and "omnibus" in low
    assert "goal / deliverables" in low
    assert "testable" in low


def test_fr90_catalog_mirror_matches_cast_iron():
    skill = _text(VISIONARY)
    catalog = _text(CATALOG)
    assert "FR #90" in catalog
    assert "Anti-omnibus" in catalog or "anti-omnibus" in catalog
    # Mirror must carry the CAST IRON block, not a stale pre-#90 copy.
    assert "non-frontier" in catalog or "unpaid" in catalog
    assert skill.count("FR #90") == catalog.count("FR #90")

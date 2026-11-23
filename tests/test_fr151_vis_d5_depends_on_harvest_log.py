"""VIS-D5 / FR #151: skill-harvest-log + harvest-skills-visionary cite VIS-D1..D4."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HSV = ROOT / ".grok" / "skills" / "harvest-skills-visionary" / "SKILL.md"
CATALOG = (
    ROOT
    / "apps"
    / "mcp-catalog"
    / "catalog"
    / "harvest-skills-visionary"
    / "SKILL.md"
)
LOG = ROOT / "docs" / "skill-harvest-log.md"
PACK = ROOT / "docs" / "feature-request-depends-on-harvest-log-2026-11-21.md"

CITE = "VIS-D1..D4"


def test_fr151_harvest_log_cites_vis_d1_to_d4():
    log = LOG.read_text(encoding="utf-8")
    assert "VIS-D5" in log
    assert CITE in log or ("VIS-D1" in log and "VIS-D4" in log)
    for token in ("VIS-D1", "VIS-D2", "VIS-D3", "VIS-D4"):
        assert token in log
    assert "Depends-on" in log
    assert "(none)" in log
    assert "validate-vision-pack" in log or "backlog" in log.lower()


def test_fr151_harvest_skill_cites_vis_d1_to_d4():
    text = HSV.read_text(encoding="utf-8")
    assert CITE in text
    for token in ("VIS-D1", "VIS-D2", "VIS-D3", "VIS-D4"):
        assert token in text
    assert "Depends-on: (none)" in text or "`Depends-on: (none)`" in text


def test_fr151_catalog_mirror_matches_canonical_bullet():
    canonical = HSV.read_text(encoding="utf-8")
    catalog = CATALOG.read_text(encoding="utf-8")
    bullet = next(line for line in canonical.splitlines() if CITE in line)
    assert bullet in catalog


def test_fr151_vision_pack_present():
    text = PACK.read_text(encoding="utf-8")
    assert "VIS-D5" in text
    assert "skill-harvest-log" in text
    assert CITE in text or ("VIS-D1" in text and "VIS-D4" in text)

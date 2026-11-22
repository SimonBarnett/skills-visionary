"""FR #180: FIX worktree stale local origin/main can hide a CONFLICTING PR."""
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

LESSON = "ls-remote origin refs/heads/main"
LESSON_UPDATE_REF = "update-ref refs/remotes/origin/main"
LESSON_PUSH = "credential.helper=!gh auth git-credential"


def test_fr180_harvest_skill_warns_stale_origin_main():
    text = HSV.read_text(encoding="utf-8")
    assert LESSON in text
    assert LESSON_UPDATE_REF in text
    assert "FETCH_HEAD" in text
    assert "CONFLICTING" in text
    assert LESSON_PUSH in text


def test_fr180_catalog_mirror_has_same_lesson():
    canonical = HSV.read_text(encoding="utf-8")
    catalog = CATALOG.read_text(encoding="utf-8")
    assert LESSON in catalog
    assert LESSON_UPDATE_REF in catalog
    assert LESSON_PUSH in catalog
    bullet = next(line for line in canonical.splitlines() if LESSON in line)
    assert bullet in catalog


def test_fr180_harvest_log_records_lesson():
    log = LOG.read_text(encoding="utf-8")
    assert "FR #180" in log
    assert "stale local origin/main" in log or "stale origin/main" in log

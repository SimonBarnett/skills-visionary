"""FR #87 / FR-K: Plan-seat visionary harvest is intake-first (no gh required)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HSV = ROOT / ".grok" / "skills" / "harvest-skills-visionary" / "SKILL.md"
VISIONARY = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"


def test_harvest_skills_visionary_intake_first_no_gh_required():
    text = HSV.read_text(encoding="utf-8")
    assert "FR-K" in text or "#87" in text
    assert "bob.ntsa.uk/bob/v1/intake" in text
    assert "Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary" in text
    assert "Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary" in text
    assert "Intake-first" in text or "intake-first" in text.lower() or "Plan-seat default" in text
    # Must not claim Plan harvest requires gh login.
    forbid = re.compile(
        r"(?i)(plan\s+harvest|honesty.?box).{0,80}(requires|must)\s+(gh\s+login|github\s+credentials)"
    )
    assert not forbid.search(text), "must not require gh login for Plan harvest"
    # gh branch+PR is optional, not the default gate.
    assert "optional" in text.lower()
    assert "Flush" in text


def test_visionary_skill_points_intake_not_branch_pr_only():
    text = VISIONARY.read_text(encoding="utf-8")
    assert "Bob intake first" in text or "intake first" in text.lower()
    assert "SimonBarnett/skills-visionary" in text
    assert "Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary" in text
    assert "no GitHub credentials required" in text or "No GitHub credentials" in text
    # Old mandatory-only "branch + PR" line must be gone from Harvest section.
    harvest = text.split("## Harvest", 1)[-1].split("## Do not", 1)[0]
    assert "branch + PR; never harvest push" not in harvest

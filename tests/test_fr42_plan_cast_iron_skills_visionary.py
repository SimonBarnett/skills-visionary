"""FR #42: plan-* CAST IRON harvest examples must cite skills-visionary, not bobiverse."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".grok" / "skills"
PLAN_SKILLS = (
    "plan-git-from-plan",
    "plan-create-repo",
    "plan-bob-webhooks",
    "plan-enable-prs",
)


def _text(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


def test_fr42_plan_git_cast_iron_uses_skills_visionary():
    text = _text("plan-git-from-plan")
    assert "CAST IRON" in text
    assert "-Repo SimonBarnett/skills-visionary" in text
    assert "Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary" in text
    # Stale bobiverse how-to-plan cite must not appear as the harvest target.
    bad = re.findall(
        r"(?:Report-BobiverseIntakeIssue|Invoke-BobiverseHarvest)\.ps1[^\n]*-Repo\s+SimonBarnett/bobiverse",
        text,
    )
    assert bad == [], bad


def test_fr42_all_plan_skills_forbid_bobiverse_harvest_examples():
    for name in PLAN_SKILLS:
        text = _text(name)
        bad = re.findall(
            r"(?:Report-BobiverseIntakeIssue|Invoke-BobiverseHarvest)\.ps1[^\n]*-Repo\s+SimonBarnett/bobiverse",
            text,
        )
        assert bad == [], f"{name}: {bad}"
"""VIS-05 / FR #139: Plan harvest -> skills-visionary via bob intake.

AGENTS + harvest skills must cite SimonBarnett/skills-visionary.
Fail when how-to-plan harvest examples target bobiverse.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
HSV = ROOT / ".grok" / "skills" / "harvest-skills-visionary" / "SKILL.md"
VISIONARY = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"

BAD_HOWTO_PLAN_BOBIVERSE = re.compile(
    r"(?:Report-BobiverseIntakeIssue|Invoke-BobiverseHarvest)\.ps1[^\n]*"
    r"-Repo\s+SimonBarnett/bobiverse",
    re.IGNORECASE,
)


def test_fr139_agents_md_cites_skills_visionary_intake():
    assert AGENTS.is_file(), "VIS-05 requires root AGENTS.md"
    text = AGENTS.read_text(encoding="utf-8")
    assert "CAST IRON" in text
    assert "SimonBarnett/skills-visionary" in text
    assert "Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary" in text
    assert "Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary" in text
    assert "bob.ntsa.uk/bob/v1/intake" in text or "Bob intake" in text
    assert "Never" in text and "bobiverse" in text.lower()
    assert BAD_HOWTO_PLAN_BOBIVERSE.findall(text) == []


def test_fr139_harvest_skill_enforces_skills_visionary_repo():
    text = HSV.read_text(encoding="utf-8")
    assert "-Repo SimonBarnett/skills-visionary" in text
    assert "Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary" in text
    assert "Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary" in text
    # Explicit forbid of how-to-plan -> bobiverse rewrite.
    assert "bobiverse" in text.lower()
    assert "Never" in text or "never" in text
    assert BAD_HOWTO_PLAN_BOBIVERSE.findall(text) == []


def test_fr139_visionary_skill_harvest_home_is_skills_visionary():
    text = VISIONARY.read_text(encoding="utf-8")
    harvest = text.split("## Harvest", 1)[-1]
    assert "SimonBarnett/skills-visionary" in harvest
    assert "Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary" in harvest
    assert BAD_HOWTO_PLAN_BOBIVERSE.findall(harvest) == []


def test_fr139_readme_points_at_agents_harvest():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "AGENTS.md" in readme
    assert "SimonBarnett/skills-visionary" in readme
    assert "Never" in readme and "bobiverse" in readme.lower()

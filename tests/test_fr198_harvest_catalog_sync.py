"""FR #198: harvest-skills-visionary tips must sync mcp-catalog before open.

Intake tips that only edit .grok/skills/harvest-skills-visionary/SKILL.md leave
apps/mcp-catalog/catalog/... drifted; build-skill-dag --check fails (MRB #189/#191).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tools" / "build-skill-dag.py"
SKILL = ROOT / ".grok" / "skills" / "harvest-skills-visionary" / "SKILL.md"
WORKFLOW = ROOT / ".github" / "workflows" / "sync-skill-catalog.yml"


def test_fr198_skill_requires_catalog_sync():
    text = SKILL.read_text(encoding="utf-8")
    assert "FR #198" in text or "FR#198" in text
    assert "build-skill-dag.py" in text
    assert "mcp-catalog" in text or "catalog/" in text
    low = text.lower()
    assert "same tip" in low or "before opening" in low or "sync" in low


def test_fr198_sync_workflow_exists():
    assert WORKFLOW.is_file(), "auto-sync workflow missing"
    yml = WORKFLOW.read_text(encoding="utf-8")
    assert "build-skill-dag.py" in yml
    assert ".grok/skills" in yml
    assert "pull_request" in yml


def test_fr198_build_skill_dag_repairs_harvest_drift():
    """Running build-skill-dag.py keeps .grok harvest book equal to the catalog mirror."""
    src = ROOT / ".grok" / "skills" / "harvest-skills-visionary" / "SKILL.md"
    mirror = ROOT / "apps" / "mcp-catalog" / "catalog" / "harvest-skills-visionary" / "SKILL.md"
    assert src.is_file() and mirror.is_file()
    proc = subprocess.run(
        [sys.executable, str(BUILD)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert src.read_bytes() == mirror.read_bytes()
    check = subprocess.run(
        [sys.executable, str(BUILD), "--check"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert check.returncode == 0, check.stdout + check.stderr

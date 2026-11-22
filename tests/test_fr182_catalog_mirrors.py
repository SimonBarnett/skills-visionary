"""FR #182: catalog/<id>/SKILL.md mirrors equal .grok/skills/<id>/SKILL.md."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tools" / "build-skill-dag.py"


def test_fr182_build_skill_dag_check_ok():
    proc = subprocess.run(
        [sys.executable, str(BUILD), "--check"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ok" in (proc.stdout + proc.stderr).lower()


def test_fr182_plan_mcp_setup_catalog_exists():
    assert (ROOT / "apps" / "mcp-catalog" / "catalog" / "plan-mcp-setup" / "SKILL.md").is_file()
    src = (ROOT / ".grok" / "skills" / "plan-mcp-setup" / "SKILL.md").read_bytes()
    dst = (ROOT / "apps" / "mcp-catalog" / "catalog" / "plan-mcp-setup" / "SKILL.md").read_bytes()
    assert src == dst

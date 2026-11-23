"""FR #187: release and site surfaces use PlanAgent.msi only (no plan.msi alias)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEXT = (ROOT / "apps" / "mcp-catalog" / "next.config.mjs").read_text(encoding="utf-8")
WF_DIR = ROOT / ".github" / "workflows"


def test_fr187_next_redirects_use_planagent_msi_path():
    assert "source: '/PlanAgent.msi'" in NEXT
    assert "source: '/PlanAgent.msi.sha256'" in NEXT
    assert "source: '/plan.msi'" not in NEXT
    assert "source: '/plan.msi.sha256'" not in NEXT
    assert "releases/latest/download/PlanAgent.msi" in NEXT


def test_fr187_workflows_do_not_upload_plan_msi_alias():
    if not WF_DIR.is_dir():
        return
    for path in WF_DIR.glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            lower = stripped.lower()
            # PlanAgent.msi is the only allowed msi asset name.
            if "plan.msi" in lower and "planagent.msi" not in lower:
                raise AssertionError(f"{path.name}: forbidden plan.msi alias: {stripped}")
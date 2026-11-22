"""FR #154: plan-release.yml builds PlanAgent.exe + MSI and releases four assets."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
YML = (ROOT / ".github" / "workflows" / "plan-release.yml").read_text(encoding="utf-8")
WXS = (ROOT / "installer" / "PlanAgent.wxs").read_text(encoding="utf-8")


def test_fr154_triggers_and_pr_does_not_publish():
    assert 'tags:' in YML and '"plan-v*"' in YML
    assert "workflow_dispatch:" in YML
    assert "pull_request:" in YML
    assert "plan-v1.0." in YML
    assert "github.event_name != 'pull_request'" in YML
    release = YML.split("release:", 1)[1]
    assert "gh release create" in release
    assert "pull_request:" not in release.split("jobs:", 1)[0]


def test_fr154_four_stable_assets_and_plan_only_msi():
    for name in (
        "PlanAgent.exe",
        "PlanAgent.exe.sha256",
        "PlanAgent.msi",
        "PlanAgent.msi.sha256",
    ):
        assert name in YML
    assert "PriorityAgent" not in YML
    assert "msiexec" in YML
    assert "/qn" in YML
    assert "wix build" in YML
    assert 'Name="Plan Agent"' in WXS
    assert "PlanAgent.exe" in WXS or "PlanExe" in WXS
    assert "plan-agent" in WXS
    assert "MajorUpgrade" in WXS
    assert "PriorityAgent" not in WXS

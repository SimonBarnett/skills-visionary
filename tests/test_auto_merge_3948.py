"""bobiverse#3948: new Plan repos get auto-merge plus a required-CI ruleset."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_plan_enable_prs_sets_auto_merge_and_required_ci():
    enable = _read(".grok/skills/plan-enable-prs/SKILL.md")
    assert "allow_auto_merge=true" in enable
    assert "required-ci-3948" in enable
    assert '"strict_required_status_checks_policy":false' in enable
    assert '"actor_type":"RepositoryRole"' in enable  # admin bypass
    assert "~DEFAULT_BRANCH" in enable
    assert "No CI yet" in enable


def test_orchestrator_and_create_point_at_auto_merge():
    orch = _read(".grok/skills/plan-git-from-plan/SKILL.md")
    create = _read(".grok/skills/plan-create-repo/SKILL.md")
    assert "allow_auto_merge=true" in orch
    assert "allow_auto_merge=true" in create

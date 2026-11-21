"""FR #99: plan-bob-webhooks / bob_git_hook default to bob.ntsa.uk (not irc)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_fr99_bob_git_hook_defaults_bob_ntsa_uk():
    src = (ROOT / "tools" / "bob_git_hook.py").read_text(encoding="utf-8")
    assert 'HOOK_URL = "https://bob.ntsa.uk/bob/v1/git"' in src
    assert 'DIGEST_URL = "https://bob.ntsa.uk/bob/v1/report"' in src
    assert "irc.ntsa.uk" not in src


def test_fr99_new_bob_git_webhook_default_bob_ntsa_uk():
    text = (ROOT / "tools" / "New-BobGitWebhook.ps1").read_text(encoding="utf-8")
    assert "https://bob.ntsa.uk/bob/v1/git" in text
    assert "irc.ntsa.uk" not in text


def test_fr99_plan_bob_webhooks_skill_bob_ntsa_uk():
    skill = (ROOT / ".grok" / "skills" / "plan-bob-webhooks" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    catalog = (
        ROOT / "apps" / "mcp-catalog" / "catalog" / "plan-bob-webhooks" / "SKILL.md"
    ).read_text(encoding="utf-8")
    for text in (skill, catalog):
        assert "https://bob.ntsa.uk/bob/v1/git" in text
        assert "https://bob.ntsa.uk/bob/v1/report" in text
        assert "irc.ntsa.uk" not in text

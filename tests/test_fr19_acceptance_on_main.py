"""MRB FR#19: every Plan new-repo requirement must be on main."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8-sig")


def test_fr19_bob_git_hook_tool_exists_with_fleet_url_events_ping_replay_announce():
    src = _read("tools/bob_git_hook.py")
    assert "https://irc.ntsa.uk/bob/v1/git" in src
    assert "issues" in src and "pull_request" in src and "push" in src
    assert "application/json" in src or "json" in src.lower()
    assert "ping" in src.lower()
    assert "replay" in src.lower()
    assert "announce" in src.lower() or "Jeeves" in src
    assert "insecure_ssl" in src or "insecure_ssl" in src.replace("'", '"')


def test_fr19_ps51_webhook_helper_ascii_and_parses():
    script = ROOT / "tools" / "New-BobGitWebhook.ps1"
    raw = script.read_bytes()
    raw.decode("ascii")  # raises if non-ASCII
    text = script.read_text(encoding="utf-8")
    for bad in ("\u2014", "\u2013", "\u2018", "\u2019", "\u201c", "\u201d"):
        assert bad not in text
    assert "https://irc.ntsa.uk/bob/v1/git" in text
    ps = "powershell.exe"
    cmd = (
        "$e=$null;$t=$null;"
        "[void][System.Management.Automation.Language.Parser]::ParseFile("
        f"'{script.as_posix()}',[ref]$t,[ref]$e);"
        "if($e){$e|%%{$_.ToString()};exit 1};'OK'"
    )
    r = subprocess.run([ps, "-NoProfile", "-Command", cmd], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_fr19_skills_gate_hook_before_push_issue_and_enable_prs():
    orch = _read(".grok/skills/plan-git-from-plan/SKILL.md")
    hooks = _read(".grok/skills/plan-bob-webhooks/SKILL.md")
    create = _read(".grok/skills/plan-create-repo/SKILL.md")
    enable = _read(".grok/skills/plan-enable-prs/SKILL.md")
    for text in (orch, hooks, create):
        assert "bob_git_hook.py" in text or "New-BobGitWebhook.ps1" in text or "bob/v1/git" in text
    assert "before" in hooks.lower() and ("push" in hooks.lower() or "issue" in hooks.lower())
    assert "feature-request" in orch or "feature-request" in enable
    assert "forking" in enable.lower() or "fork" in enable.lower()
    assert "plan-enable-prs" in orch
    # order in orchestrator checklist
    assert orch.lower().find("webhook") < orch.lower().find("first commit") or "bob_git_hook" in orch


def test_fr19_tests_cover_hook_replay_announce_timeout():
    t = _read("tests/test_bob_git_hook.py")
    assert "replay" in t.lower()
    assert "ping" in t.lower()
    assert "announce" in t.lower() or "jeeves" in t.lower()
    assert "timeout" in t.lower() or "never_announces" in t.lower() or "fails_when_jeeves" in t.lower()


def test_fr19_acceptance_doc_on_main():
    doc = ROOT / "docs" / "feature-request-plan-bob-webhooks-before-first-issue-2026-09-25.md"
    assert doc.is_file()
    body = doc.read_text(encoding="utf-8")
    assert re.search(r"^##\s+Shape\s*$", body, re.M)
    assert re.search(r"^##\s+Success\s*$", body, re.M)
    assert "bob_git_hook" in body or "irc.ntsa.uk/bob/v1/git" in body

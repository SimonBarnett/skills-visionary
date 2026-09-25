"""MRB #17: New-BobGitWebhook.ps1 must parse under Windows PowerShell 5.1 (ASCII-only)."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "New-BobGitWebhook.ps1"


def test_webhook_helper_is_ascii_only():
    raw = SCRIPT.read_bytes()
    assert raw, "script missing"
    # No UTF-8 BOM required; body must be pure ASCII (PS 5.1 + some editors choke on em-dash)
    try:
        raw.decode("ascii")
    except UnicodeDecodeError as e:
        raise AssertionError(f"New-BobGitWebhook.ps1 has non-ASCII at {e.start}: {raw[e.start:e.start+8]!r}") from e


def test_webhook_helper_has_no_em_dash_or_smart_quotes():
    text = SCRIPT.read_text(encoding="utf-8")
    for bad in ("\u2014", "\u2013", "\u2018", "\u2019", "\u201c", "\u201d", "\u2026"):
        assert bad not in text, f"forbidden unicode {bad!r} in New-BobGitWebhook.ps1"


def test_webhook_helper_parses_under_windows_powershell():
    """Parser-only check (no network). Prefer powershell.exe (5.1) when present."""
    ps = "powershell.exe"
    try:
        subprocess.run([ps, "-NoProfile", "-Command", "$PSVersionTable.PSVersion.Major"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        ps = "pwsh"
    cmd = (
        "$e=$null; $t=$null; "
        "[void][System.Management.Automation.Language.Parser]::ParseFile("
        f"'{SCRIPT.as_posix()}', [ref]$t, [ref]$e); "
        "if ($e) { $e | ForEach-Object { $_.ToString() }; exit 1 }; 'OK'"
    )
    r = subprocess.run([ps, "-NoProfile", "-Command", cmd], capture_output=True, text=True)
    assert r.returncode == 0, f"parse failed via {ps}: {r.stdout}\n{r.stderr}"


def test_webhook_helper_targets_bob_v1_git_not_report():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "/bob/v1/git" in text
    assert "plan-bob-webhooks" in text
    # Must not default hook URL to digest report
    assert re.search(r'HookUrl\s*=\s*[\'"]https://irc\.ntsa\.uk/bob/v1/git', text)


def test_harvest_cast_iron_same_turn_in_skills():
    h = (ROOT / ".grok/skills/harvest-agent-skills/SKILL.md").read_text(encoding="utf-8")
    assert "AUTOMATIC harvest" in h
    assert "same turn" in h.lower()
    assert "club-madeira-onboarding" in h
    v = (ROOT / ".grok/skills/visionary/SKILL.md").read_text(encoding="utf-8")
    assert "Harvest (AUTOMATIC)" in v

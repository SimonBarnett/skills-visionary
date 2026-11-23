# -*- coding: utf-8 -*-
"""VIS-D2 / FR #148: park dry-run / fixtures put Depends-on on issue body."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "format_depends_on_park_issue_body.py"
VISIONARY = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"
CATALOG = ROOT / "apps" / "mcp-catalog" / "catalog" / "visionary" / "SKILL.md"
EVIDENCE = ROOT / "docs" / "evidence" / "vis-d2-park-emits-depends-on.md"
FIXTURES = ROOT / "tests" / "fixtures" / "depends-on-park"

sys.path.insert(0, str(ROOT / "tools"))
import format_depends_on_park_issue_body as fmt  # noqa: E402


def _text(path: Path) -> str:
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), path
    return raw.decode("utf-8")


def test_fr148_format_puts_depends_on_first():
    body = fmt.format_park_issue_body(
        feature_id="VIS-D2",
        theme="Depends-on preconditions",
        vision_pack_url="https://example.invalid/v.md",
        index_url="https://example.invalid/i.md",
        depends_on="#147",
    )
    assert body.startswith("**Depends-on:** #147\n")
    assert "**Depends-on:** #147" in body[:500]
    assert "Feature request `VIS-D2`" in body
    # Vision URL alone is not the acceptance — stamp is on the body.
    assert body.index("**Depends-on:**") < body.index("Vision pack")


def test_fr148_normalize_none_and_cross_repo():
    assert fmt.normalize_depends_on(None) == "(none)"
    assert fmt.normalize_depends_on("(none)") == "(none)"
    assert fmt.normalize_depends_on("SimonBarnett/bobiverse#9147, #8807") == (
        "SimonBarnett/bobiverse#9147, #8807"
    )
    try:
        fmt.normalize_depends_on("BOB-D3")
        assert False, "backlog id should raise"
    except ValueError:
        pass


def test_fr148_dry_run_cli_matches_formatter():
    proc = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--feature-id",
            "VIS-D2",
            "--theme",
            "t",
            "--vision-pack-url",
            "https://example.invalid/v.md",
            "--index-url",
            "https://example.invalid/i.md",
            "--depends-on",
            "#99",
            "--dry-run",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.startswith("**Depends-on:** #99\n")


def test_fr148_fixtures_and_evidence_are_issue_bodies():
    assert EVIDENCE.is_file()
    evidence = _text(EVIDENCE)
    assert "Depends-on" in evidence
    assert "format_depends_on_park_issue_body" in evidence
    assert "intake" in evidence.lower() or "-Body" in evidence
    names = {
        "child-depends-on-digest.body.md",
        "none.body.md",
        "cross-repo.body.md",
    }
    found = {p.name for p in FIXTURES.glob("*.body.md")}
    assert names <= found
    for name in names:
        text = _text(FIXTURES / name)
        assert text.lstrip().startswith("**Depends-on:**"), name
        assert "**Depends-on:**" in text[:500]


def test_fr148_visionary_requires_issue_body_not_vision_only():
    text = _text(VISIONARY)
    assert "VIS-D2" in text or "FR #148" in text
    assert "format_depends_on_park_issue_body" in text
    low = text.lower()
    assert "issue body" in low
    assert "vision markdown" in low or "feature-request-*.md" in text
    catalog = _text(CATALOG)
    assert "VIS-D2" in catalog or "FR #148" in catalog

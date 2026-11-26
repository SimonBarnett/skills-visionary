# -*- coding: utf-8 -*-
"""VIS-G4 / FR #190: digest explains vision + docs link + Digest flag."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_fr_digest_explain_flag.py"
FMT = ROOT / "tools" / "format_fr_digest_explain_flag.py"
VISIONARY = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"
CATALOG = ROOT / "apps" / "mcp-catalog" / "catalog" / "visionary" / "SKILL.md"
FIXTURE = ROOT / "docs" / "fixtures" / "fr-digest-explain-flag"
PACK = ROOT / "docs" / "feature-request-fr-digest-explain-flag-2026-11-23.md"

sys.path.insert(0, str(ROOT / "tools"))
import check_fr_digest_explain_flag as chk  # noqa: E402
import format_fr_digest_explain_flag as fmt  # noqa: E402


def _text(path: Path) -> str:
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), path
    return raw.decode("utf-8")


def test_fr190_check_rejects_children_only():
    errs = chk.check_stamp(
        {
            "labels": ["fr-digest", "hold"],
            "body": "## Children\n\n| Issue | Title | Vision |\n|---|---|---|\n| #1 | A | v |\n",
        }
    )
    assert errs
    assert any("vision summary" in e or "Digest flag" in e or "docs link" in e for e in errs)


def test_fr190_check_rejects_missing_label():
    body = (
        "Kind: fr-digest\nDigest: true\n\n## Vision\n\n"
        "Intent success criteria out of scope enough words here for the gate.\n\n"
        "**Docs:** docs/x.md\n"
    )
    errs = chk.check_stamp({"labels": ["hold"], "body": body})
    assert any("Digest label" in e for e in errs)


def test_fr190_check_rejects_pr_labels():
    errs = chk.check_stamp(
        {"is_pr": True, "labels": ["digest", "hold"], "body": "n/a"}
    )
    assert errs
    assert any("PR-shaped" in e for e in errs)


def test_fr190_check_accepts_stamp():
    errs = chk.check_stamp(
        {
            "labels": ["fr-digest", "hold"],
            "body": (
                "Kind: fr-digest\n"
                "Digest: true\n\n"
                "## Vision\n\n"
                "Product intent and success criteria with out of scope noted clearly.\n\n"
                "**Docs:** https://example.test/docs/vision.md\n"
                "**Vision pack:** https://example.test/docs/vision.md\n"
            ),
        }
    )
    assert errs == []


def test_fr190_check_rejects_dual_digest_labels():
    errs = chk.check_stamp(
        {
            "labels": ["digest", "fr-digest", "hold"],
            "body": (
                "Kind: fr-digest\n"
                "Digest: true\n\n"
                "## Vision\n\n"
                "Product intent and success criteria with out of scope noted clearly.\n\n"
                "**Docs:** https://example.test/docs/vision.md\n"
            ),
        }
    )
    assert any("dual Digest labels" in e for e in errs)


def test_fr190_fixture_pack_passes_cli():
    assert (FIXTURE / "README.md").is_file()
    stamp = json.loads(_text(FIXTURE / "park-stamp.json"))
    assert "fr-digest" in stamp["labels"]
    assert "digest" not in stamp["labels"]
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE / "park-stamp.json")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_fr190_format_body_and_labels():
    body = fmt.format_digest_issue_body(
        theme="t",
        vision_summary=(
            "Intent: park digests with context. Success: flag + docs. "
            "Out of scope: child implementation."
        ),
        docs_url="docs/feature-request-fr-digest-explain-flag-2026-11-23.md",
        vision_pack_url="https://example.test/v.md",
        index_url="https://example.test/i.md",
        children_rows=[{"number": 3, "title": "c", "vision": "v.md"}],
    )
    assert "Kind: fr-digest" in body
    assert "Digest: true" in body
    assert "## Vision" in body
    assert "**Docs:**" in body
    assert "| #3 |" in body
    labels = fmt.digest_create_labels()
    assert "fr-digest" in labels
    assert "hold" in labels
    assert "digest" not in labels


def test_fr190_visionary_cast_iron_vis_g4():
    text = _text(VISIONARY)
    assert "VIS-G4" in text or "FR #190" in text
    assert "check_fr_digest_explain_flag" in text
    assert "docs/fixtures/fr-digest-explain-flag" in text
    low = text.lower()
    assert "vision" in low and "digest" in low
    catalog = _text(CATALOG)
    assert "VIS-G4" in catalog or "check_fr_digest_explain_flag" in catalog
    assert "VIS-G4" in _text(PACK)


def test_fr190_cli_format_labels():
    proc = subprocess.run(
        [sys.executable, str(FMT), "labels"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    labs = json.loads(proc.stdout)
    assert "digest" in labs and "fr-digest" in labs

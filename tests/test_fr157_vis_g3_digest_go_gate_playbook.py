"""VIS-G3 / FR #157: visionary skill documents digest go-gate playbook."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"
CATALOG = ROOT / "apps" / "mcp-catalog" / "catalog" / "visionary" / "SKILL.md"
PACK = ROOT / "docs" / "feature-request-fr-digest-skill-playbook-2026-11-21.md"


def test_fr157_skill_documents_digest_go_gate():
    text = SKILL.read_text(encoding="utf-8")
    assert "VIS-G3" in text or "digest go-gate" in text.lower()
    assert "fr-digest" in text
    assert "unhold" in text.lower()
    assert "CLOSED Depends-on" in text or "ordinary" in text.lower()
    assert "one digest per" in text.lower()
    # order cues
    assert "Create digest first" in text or "digest issue first" in text.lower()


def test_fr157_catalog_mirror_has_go_gate_bullet():
    canonical = SKILL.read_text(encoding="utf-8")
    catalog = CATALOG.read_text(encoding="utf-8")
    assert "digest go-gate" in catalog.lower()
    bullet = next(
        line
        for line in canonical.splitlines()
        if "digest go-gate playbook" in line.lower() or "VIS-G3" in line
    )
    # first line of the block should appear in catalog after sync
    assert "VIS-G3" in catalog or "digest go-gate" in catalog.lower()
    assert bullet in catalog or "FR digest go-gate playbook" in catalog


def test_fr157_vision_pack_present():
    text = PACK.read_text(encoding="utf-8")
    assert "VIS-G3" in text
    assert "digest go-gate" in text.lower()

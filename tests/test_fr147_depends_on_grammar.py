# -*- coding: utf-8 -*-
"""VIS-D1 / FR #147: Depends-on grammar in visionary skill + docs."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VISIONARY = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"
CATALOG = ROOT / "apps" / "mcp-catalog" / "catalog" / "visionary" / "SKILL.md"
DOCS = ROOT / "docs" / "depends-on-grammar.md"


def _text(path: Path) -> str:
    assert path.is_file(), path
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), path
    return raw.decode("utf-8")


def test_fr147_visionary_documents_depends_on_grammar():
    text = _text(VISIONARY)
    assert "VIS-D1" in text or "FR #147" in text
    assert "Depends-on: #N" in text or "Depends-on: `#N`" in text or "`Depends-on: #N`" in text
    assert "owner/repo#N" in text
    assert "(none)" in text
    # Any SimonBarnett product repo — fail-when Bobiverse-only.
    low = text.lower()
    assert "any simonbarnett product" in low or "any simonbarnett product repo" in low
    assert "bobiverse-only" in low or "not bobiverse-only" in low
    assert "hold" in low and "depends-on" in low
    assert "docs/depends-on-grammar.md" in text


def test_fr147_docs_depends_on_grammar_page():
    text = _text(DOCS)
    assert "Depends-on: #N" in text or "`Depends-on: #N`" in text
    assert "owner/repo#N" in text
    assert "(none)" in text
    low = text.lower()
    assert "any simonbarnett product" in low
    assert "bobiverse-only" in low or "not" in low and "bobiverse" in low
    assert "hold" in low


def test_fr147_catalog_mirror_carries_grammar():
    skill = _text(VISIONARY)
    catalog = _text(CATALOG)
    assert "FR #147" in catalog or "VIS-D1" in catalog
    assert "owner/repo#N" in catalog
    assert "(none)" in catalog
    assert skill.count("VIS-D1") == catalog.count("VIS-D1") or (
        "FR #147" in skill and "FR #147" in catalog
    )

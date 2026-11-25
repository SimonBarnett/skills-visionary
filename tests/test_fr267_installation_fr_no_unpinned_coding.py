"""FR #267: visionary CAST IRON — installation FRs must not mix unpinned coding."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"


def test_fr267_installation_fr_cast_iron_phrases():
    text = SKILL.read_text(encoding="utf-8")
    low = text.lower()
    assert "installation fr" in low
    assert "must not contain" in low
    assert "machine-pinned" in low or "machine pin" in low
    assert "FR #267" in text
    assert "separate" in low

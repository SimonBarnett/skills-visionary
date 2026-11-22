"""VIS-08 / FR #140: plan.ntsa.uk HTML/docs expose PlanAgent.msi download link."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MSI = (
    "https://github.com/SimonBarnett/skills-visionary/"
    "releases/latest/download/PlanAgent.msi"
)
PAGE = ROOT / "apps" / "mcp-catalog" / "app" / "page.tsx"
DOWNLOADS = ROOT / "apps" / "mcp-catalog" / "app" / "downloads" / "page.tsx"
LIB = ROOT / "apps" / "mcp-catalog" / "lib" / "downloads.ts"
MOCK_HOME = ROOT / "docs" / "mocks" / "plan-home.html"
MOCK_DL = ROOT / "docs" / "mocks" / "plan-downloads.html"


def test_fr140_landing_exposes_msi_link():
    text = PAGE.read_text(encoding="utf-8")
    assert "Downloads" in text
    assert "PlanAgent.msi" in text or "PLAN_AGENT_MSI_HREF" in text
    assert "/downloads" in text


def test_fr140_downloads_page_links_msi():
    assert DOWNLOADS.is_file()
    text = DOWNLOADS.read_text(encoding="utf-8")
    assert "PlanAgent.msi" in text or "PLAN_AGENT_MSI_HREF" in text
    assert 'data-role="msi"' in text


def test_fr140_downloads_lib_canonical_href():
    text = LIB.read_text(encoding="utf-8")
    assert MSI in text


def test_fr140_docs_mocks_link_msi():
    assert MSI in MOCK_HOME.read_text(encoding="utf-8")
    assert MSI in MOCK_DL.read_text(encoding="utf-8")

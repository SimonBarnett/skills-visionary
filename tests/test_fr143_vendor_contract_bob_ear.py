"""VIS-09 / FR #143: vendor contract doc for bob-ear (BOB-44 / BOB-49)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "vendor-contract-bob-ear.md"
JSON = ROOT / "docs" / "vendor" / "plan-agent-bob-ear.json"
MSI = (
    "https://github.com/SimonBarnett/skills-visionary/"
    "releases/latest/download/PlanAgent.msi"
)


def test_fr143_vendor_contract_doc_exists():
    assert DOC.is_file(), f"missing vendor contract: {DOC}"
    text = DOC.read_text(encoding="utf-8")
    assert "VIS-09" in text or "Vendor contract" in text
    assert "BOB-44" in text
    assert "BOB-49" in text
    assert "PlanAgent.msi" in text
    assert "PlanAgent.exe" in text
    assert MSI in text
    assert "plan-v" in text
    assert "https://plan.ntsa.uk" in text
    assert "contract version" in text.lower() or "Contract version" in text


def test_fr143_vendor_contract_json_urls_and_version():
    assert JSON.is_file(), f"missing vendor JSON: {JSON}"
    data = json.loads(JSON.read_text(encoding="utf-8"))
    assert data.get("contract_version")
    assert data.get("product") == "Plan Agent"
    assert "BOB-44" in data.get("consumers", [])
    assert "BOB-49" in data.get("consumers", [])
    urls = data.get("urls") or {}
    assert urls.get("msi_latest") == MSI
    assert urls.get("landing") == "https://plan.ntsa.uk"
    assert urls.get("mcp") == "https://plan.ntsa.uk/mcp"
    assert data.get("exe") == "PlanAgent.exe"
    assert data.get("msi") == "PlanAgent.msi"
    assert data.get("docs_path") == "docs/vendor-contract-bob-ear.md"


def test_fr143_ascii_bomless_contract_files():
    for path in (DOC, JSON):
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), path
        raw.decode("ascii")

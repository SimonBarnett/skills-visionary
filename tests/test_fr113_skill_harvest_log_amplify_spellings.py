"""FR #113: skill-harvest-log Amplify entries must keep a/n/t literals."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "docs" / "skill-harvest-log.md"


def test_fr113_amplify_harvest_log_spellings():
    raw = LOG.read_text(encoding="utf-8")
    assert "\x07" not in raw
    assert "Root mplify.yml" not in raw
    assert "monorepo ppRoot" not in raw
    # Corrupted tokens must not appear as whole path segments (apps contains pps).
    assert re.search(r"(?<![A-Za-z])pps/mcp-catalog", raw) is None
    assert re.search(r"(?<![A-Za-z])ests/smoke-live", raw) is None
    assert re.search(r"(?m)^\s*vm use 20", raw) is None
    assert re.search(r"(?m)^\s*pm ci ", raw) is None
    assert "amplify.yml" in raw
    assert "appRoot" in raw
    assert "nvm use 20" in raw
    assert "npm ci" in raw
    assert "npm run build" in raw
    assert "apps/mcp-catalog/tests/amplify-hosting.test.mjs" in raw
    assert "apps/mcp-catalog/scripts/smoke-mcp-live.mjs" in raw
    assert "apps/mcp-catalog/tests/smoke-live.test.mjs" in raw
    assert "## 2026-11-20 - FR #84 Amplify deploy contract for plan.ntsa.uk" in raw
    assert "## 2026-11-20 - FR #86 smoke:live against plan.ntsa.uk" in raw

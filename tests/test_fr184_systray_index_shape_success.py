"""FR #184: systray FR index must pass vision-pack validate with Shape + Success."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate-vision-pack.py"
INDEX = ROOT / "docs" / "feature-request-plan-agent-systray-index-2026-11-21.md"
MOCKS = ROOT / "docs" / "mocks"


def test_fr184_systray_index_has_shape_and_success_and_validates():
    assert INDEX.is_file(), f"missing {INDEX.name} (do not leave only fr-index-* rename)"
    text = INDEX.read_text(encoding="utf-8")
    assert re.search(r"^##\s+Shape\s*$", text, re.MULTILINE)
    assert re.search(r"^##\s+Success\s*$", text, re.MULTILINE)
    cmd = [sys.executable, str(VALIDATOR), str(INDEX), "--mocks-dir", str(MOCKS)]
    assert subprocess.run(cmd, cwd=ROOT, check=False).returncode == 0
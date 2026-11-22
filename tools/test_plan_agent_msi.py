"""VIS-07: PlanAgent.msi is a Windows Installer file named for Plan Agent."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_plan_agent_msi as bld  # noqa: E402


def test_msi_is_ole_and_names_plan_agent(tmp: Path):
    path = bld.build_msi(tmp / "PlanAgent.msi")
    raw = path.read_bytes()
    assert path.name == "PlanAgent.msi"
    assert raw[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
    # Summary info stores the product name as UTF-16LE.
    assert b"Plan Agent" in raw


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as folder:
        test_msi_is_ole_and_names_plan_agent(Path(folder))
    print("ok")

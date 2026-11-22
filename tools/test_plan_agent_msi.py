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


def test_msi_contains_installable_file(tmp: Path):
    """Hostile: a Plan standalone MSI must install at least one File (not an empty Product DB)."""
    import msilib

    path = bld.build_msi(tmp / "PlanAgent.msi")
    db = msilib.OpenDatabase(str(path), 0)
    try:
        view = db.OpenView("SELECT `File` FROM `File`")
        view.Execute(None)
        count = 0
        while view.Fetch():
            count += 1
    finally:
        try:
            view.Close()
        except Exception:
            pass
        db.Close()
    assert count >= 1, "PlanAgent.msi File table is empty; MSI installs nothing"


def test_msi_accepts_external_payload(tmp: Path):
    payload = tmp / "PlanAgent.exe"
    payload.write_bytes(b"MZ" + (b"\0" * 126) + b"PLAN")
    path = bld.build_msi(tmp / "out" / "PlanAgent.msi", payload=payload)
    assert path.is_file()
    import msilib

    db = msilib.OpenDatabase(str(path), 0)
    try:
        view = db.OpenView("SELECT `File` FROM `File`")
        view.Execute(None)
        assert view.Fetch() is not None
    finally:
        try:
            view.Close()
        except Exception:
            pass
        db.Close()


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        test_msi_is_ole_and_names_plan_agent(root)
        test_msi_contains_installable_file(root)
        test_msi_accepts_external_payload(root)
    print("ok")

"""VIS-07: write a standalone PlanAgent.msi (Windows Installer database).

Not a GitHub Release and not a plan.ntsa.uk upload. Those are the publish
step. This is the MSI the release asset is built from.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

import msilib
from msilib import schema

# Stable product / component codes so repeated builds stay the same product.
PRODUCT_CODE = "{8F3C2A10-4B6E-4D11-9C2A-0E5F1A7B1420}"
COMPONENT_CODE = "{B2C4E618-9A1D-4F70-8E3B-1D5A7C9E1420}"
PRODUCT_NAME = "Plan Agent"
MANUFACTURER = "SimonBarnett"
VERSION = "1.0.0"
PAYLOAD_NAME = "PlanAgent.exe"
# Minimal MZ stub so the File table has a real payload without needing a built exe.
_MZ_STUB = b"MZ" + (b"\0" * 126)


def _stage_payload(payload: Path | None, staging: Path) -> Path:
    staging.mkdir(parents=True, exist_ok=True)
    dest = staging / PAYLOAD_NAME
    if payload is not None:
        src = Path(payload)
        if not src.is_file():
            raise FileNotFoundError(src)
        shutil.copy2(src, dest)
    else:
        dest.write_bytes(_MZ_STUB)
    return dest


def build_msi(path: Path, payload: Path | None = None) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()

    with tempfile.TemporaryDirectory(prefix="plan-msi-") as tmp:
        staged = _stage_payload(payload, Path(tmp))
        db = msilib.init_database(
            str(path),
            schema,
            PRODUCT_NAME,
            PRODUCT_CODE,
            VERSION,
            MANUFACTURER,
        )
        cab = msilib.CAB("PlanAgent")
        feature = msilib.Feature(db, "DefaultFeature", "Plan Agent", "Complete", 0)
        root = msilib.Directory(db, cab, None, str(staged.parent), "TARGETDIR", "SourceDir", 0)
        app = msilib.Directory(db, cab, root, ".", "APPDIR", "PlanAgent", 1)
        app.start_component(
            "PlanAgentComp",
            feature=feature,
            flags=0,
            keyfile=PAYLOAD_NAME,
            uuid=COMPONENT_CODE,
        )
        app.add_file(PAYLOAD_NAME)
        cab.commit(db)
        db.Commit()
    return path


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "out" / "PlanAgent.msi"
    payload = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    written = build_msi(out, payload=payload)
    print(written)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

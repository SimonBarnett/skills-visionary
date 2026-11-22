"""VIS-07: write a standalone PlanAgent.msi (Windows Installer database).

Not a GitHub Release and not a plan.ntsa.uk upload. Those are the publish
step. This is the MSI the release asset is built from.
"""
from __future__ import annotations

import sys
from pathlib import Path

import msilib
from msilib import schema

# Stable product code so repeated builds stay the same product.
PRODUCT_CODE = "{8F3C2A10-4B6E-4D11-9C2A-0E5F1A7B1420}"
PRODUCT_NAME = "Plan Agent"
MANUFACTURER = "SimonBarnett"
VERSION = "1.0.0"


def build_msi(path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    db = msilib.init_database(
        str(path),
        schema,
        PRODUCT_NAME,
        PRODUCT_CODE,
        VERSION,
        MANUFACTURER,
    )
    db.Commit()
    return path


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "out" / "PlanAgent.msi"
    written = build_msi(out)
    print(written)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

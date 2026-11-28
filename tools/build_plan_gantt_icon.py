"""VIS-06 / FR #281: Plan Agent GANTT icon (ICO + PNG) from checked-in source art."""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "apps" / "plan_agent" / "assets"
SOURCE = OUT_DIR / "plan-gantt-source.png"
SIZES = (16, 24, 32, 48, 64, 128, 256)


def load_master() -> Image.Image:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"missing source art: {SOURCE} (FR #281)")
    with Image.open(SOURCE) as im:
        return im.convert("RGBA")


def resize_master(master: Image.Image, size: int) -> Image.Image:
    if master.size == (size, size):
        return master.copy()
    return master.resize((size, size), Image.Resampling.LANCZOS)


def main(argv: list[str] | None = None) -> int:
    del argv
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    master = load_master()
    images = [resize_master(master, s) for s in SIZES]
    ico = OUT_DIR / "plan-gantt.ico"
    png = OUT_DIR / "plan-gantt.png"
    images[-1].save(png)
    # BMP-style ICO so .NET ApplicationIcon (PlanAgent.exe) embeds RT_GROUP_ICON (FR #281).
    master.save(ico, format="ICO", sizes=[(s, s) for s in SIZES])
    print(f"source {SOURCE} ({SOURCE.stat().st_size} bytes)")
    print(f"wrote {ico} ({ico.stat().st_size} bytes)")
    print(f"wrote {png} ({png.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
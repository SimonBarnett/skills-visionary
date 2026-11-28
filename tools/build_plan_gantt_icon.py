"""VIS-06 / FR #281: Plan Agent GANTT icon (ICO + PNG) from checked-in source art."""
from __future__ import annotations

import io
import struct
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


def write_ico(path: Path, images: list[Image.Image]) -> None:
    """PNG-compressed multi-size ICO (Windows-friendly)."""
    entries: list[tuple[int, int, int, int, bytes]] = []
    offset = 6 + 16 * len(images)
    for im in images:
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        data = buf.getvalue()
        w, h = im.size
        entries.append((0 if w >= 256 else w, 0 if h >= 256 else h, len(data), offset, data))
        offset += len(data)
    out = bytearray()
    out += struct.pack("<HHH", 0, 1, len(entries))
    for w, h, size, off, _ in entries:
        out += struct.pack("<BBBBHHII", w, h, 0, 0, 1, 32, size, off)
    for *_, data in entries:
        out += data
    path.write_bytes(out)


def main(argv: list[str] | None = None) -> int:
    del argv
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    master = load_master()
    images = [resize_master(master, s) for s in SIZES]
    ico = OUT_DIR / "plan-gantt.ico"
    png = OUT_DIR / "plan-gantt.png"
    images[-1].save(png)
    write_ico(ico, images)
    print(f"source {SOURCE} ({SOURCE.stat().st_size} bytes)")
    print(f"wrote {ico} ({ico.stat().st_size} bytes)")
    print(f"wrote {png} ({png.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
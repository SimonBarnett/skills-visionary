"""VIS-06: rebuild Plan Agent GANTT icon (ICO + PNG)."""
from __future__ import annotations

import io
import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "apps" / "plan_agent" / "assets"
SIZES = (16, 24, 32, 48, 64, 128, 256)


def make_gantt(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    margin = max(1, size // 16)
    d.rounded_rectangle(
        [margin, margin, size - margin - 1, size - margin - 1],
        radius=max(2, size // 8),
        fill=(15, 76, 92, 255),
    )
    pad = max(2, size // 8)
    row_h = max(2, size // 7)
    gap = max(1, size // 16)
    top = pad + gap
    bars = (
        ((0.12, 0.62), (90, 200, 180, 255)),
        ((0.28, 0.82), (255, 196, 86, 255)),
        ((0.18, 0.72), (120, 180, 255, 255)),
    )
    inner_w = size - 2 * pad
    for i, ((start, end), color) in enumerate(bars):
        y0 = top + i * (row_h + gap)
        y1 = y0 + row_h
        x0 = pad + int(inner_w * start)
        x1 = pad + int(inner_w * end)
        if x1 <= x0:
            x1 = x0 + max(2, size // 10)
        d.rounded_rectangle(
            [x0, y0, x1, y1],
            radius=max(1, row_h // 3),
            fill=color,
        )
    return img


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
    images = [make_gantt(s) for s in SIZES]
    ico = OUT_DIR / "plan-gantt.ico"
    png = OUT_DIR / "plan-gantt.png"
    images[-1].save(png)
    write_ico(ico, images)
    print(f"wrote {ico} ({ico.stat().st_size} bytes)")
    print(f"wrote {png} ({png.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""VIS-D4 / FR #150: require an explicit Depends-on stamp (including (none)).

Silent omission of Depends-on fails. Backlog-id rejection is VIS-D3.
"""
from __future__ import annotations

import argparse
import re
import sys

# Match plain `Depends-on: …` and bold `**Depends-on:** …` (colon inside or outside **).
_DEPENDS_LINE = re.compile(
    r"(?im)^\s*\*{0,2}Depends-on\*{0,2}:\*{0,2}\s*(.+?)\s*$"
)
_NONE = re.compile(r"^\(none\)$", re.I)


def find_depends_on_values(text: str) -> list[str]:
    return [(m.group(1) or "").strip() for m in _DEPENDS_LINE.finditer(text or "")]


def has_depends_on_stamp(text: str) -> bool:
    return bool(find_depends_on_values(text))


def has_explicit_none(text: str) -> bool:
    for val in find_depends_on_values(text):
        if _NONE.match(val):
            return True
    return False


def check_text(text: str, *, require_none: bool = False) -> list[str]:
    """Return human error strings (empty = ok)."""
    errs: list[str] = []
    if not has_depends_on_stamp(text):
        errs.append("silent omission: no Depends-on line")
        return errs
    if require_none and not has_explicit_none(text):
        errs.append("expected Depends-on: (none) for no-preconditions pack")
    return errs


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path", nargs="+", help="Markdown / issue-body files to check")
    p.add_argument(
        "--require-none",
        action="store_true",
        help="Each file must include Depends-on: (none)",
    )
    args = p.parse_args(argv)
    failed = 0
    for raw in args.path:
        path = raw
        try:
            text = open(path, encoding="utf-8").read()
        except OSError as exc:
            print(f"FAIL {path}: {exc}", file=sys.stderr)
            failed += 1
            continue
        if text.startswith("\ufeff"):
            print(f"FAIL {path}: UTF-8 BOM", file=sys.stderr)
            failed += 1
            continue
        errs = check_text(text, require_none=args.require_none)
        if errs:
            failed += 1
            for e in errs:
                print(f"FAIL {path}: {e}", file=sys.stderr)
        else:
            print(f"ok {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

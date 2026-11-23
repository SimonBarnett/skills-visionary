#!/usr/bin/env python3
"""VIS-G2 / FR #156: children Depends-on digest; digest Children table lists them.

Fail-when: child missing Depends-on:#digest, or digest body empty of children.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_DEPENDS_LINE = re.compile(
    r"(?im)^\s*\*{0,2}Depends-on\*{0,2}:\*{0,2}\s*(.+?)\s*$"
)
_CHILD_ISSUE_CELL = re.compile(r"(?m)^\|\s*#?(\d+)\s*\|")
_HASH_REF = re.compile(r"#(\d+)\b")


def find_depends_on_values(text: str) -> list[str]:
    return [(m.group(1) or "").strip() for m in _DEPENDS_LINE.finditer(text or "")]


def depends_on_includes_digest(text: str, digest_number: int) -> bool:
    """True when any Depends-on value cites #digest or owner/repo#digest."""
    needle = f"#{int(digest_number)}"
    for val in find_depends_on_values(text):
        # split comma/semicolon lists
        parts = [p.strip() for p in re.split(r"[,;]", val) if p.strip()]
        for part in parts:
            if part == needle or part.endswith(needle):
                return True
            # bare number only when whole token is the digest id (rare)
            if part.isdigit() and int(part) == int(digest_number):
                return True
    return False


def children_listed_in_digest_body(digest_body: str, child_numbers: list[int]) -> list[int]:
    """Return child numbers missing from the digest Children table / body."""
    listed: set[int] = set()
    # Prefer markdown table rows "| #N |" or "| N |"
    for m in _CHILD_ISSUE_CELL.finditer(digest_body or ""):
        listed.add(int(m.group(1)))
    # Also accept plain "#N" mentions under a Children heading block
    if "children" in (digest_body or "").lower():
        for m in _HASH_REF.finditer(digest_body or ""):
            listed.add(int(m.group(1)))
    missing = [n for n in child_numbers if int(n) not in listed]
    return missing


def check_stamp(data: dict[str, Any]) -> list[str]:
    """Return human error strings (empty = ok)."""
    errs: list[str] = []
    digest = data.get("digest") or {}
    children = data.get("children") or []

    if not isinstance(digest, dict) or not digest:
        errs.append("digest body empty of children: park missing digest object")
        return errs

    try:
        digest_number = int(digest.get("number"))
    except (TypeError, ValueError):
        errs.append("digest missing integer number")
        return errs

    digest_body = digest.get("body") or ""
    if not str(digest_body).strip():
        errs.append("digest body empty of children: digest body is empty")
        return errs

    if not children:
        errs.append("digest body empty of children: no children in stamp pack")
        return errs

    child_numbers: list[int] = []
    for i, child in enumerate(children):
        if not isinstance(child, dict):
            errs.append(f"child[{i}] must be an object")
            continue
        try:
            num = int(child.get("number"))
        except (TypeError, ValueError):
            errs.append(f"child[{i}] missing integer number")
            continue
        child_numbers.append(num)
        body = child.get("body") or ""
        if not depends_on_includes_digest(str(body), digest_number):
            errs.append(
                f"child missing Depends-on digest: #{num} lacks Depends-on:#{digest_number}"
            )

    missing = children_listed_in_digest_body(str(digest_body), child_numbers)
    for num in missing:
        errs.append(
            f"digest body empty of children: digest #{digest_number} Children table missing #{num}"
        )

    return errs


def load_stamp(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        raise ValueError(f"{path}: UTF-8 BOM")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: stamp root must be a JSON object")
    # Optional: load body from sibling files when body_file set
    digest = data.get("digest")
    if isinstance(digest, dict) and digest.get("body_file") and not digest.get("body"):
        bp = path.parent / str(digest["body_file"])
        digest["body"] = bp.read_text(encoding="utf-8")
    for child in data.get("children") or []:
        if isinstance(child, dict) and child.get("body_file") and not child.get("body"):
            bp = path.parent / str(child["body_file"])
            child["body"] = bp.read_text(encoding="utf-8")
    return data


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "path",
        nargs="+",
        help="park-stamp.json files (digest number/body + children bodies)",
    )
    args = p.parse_args(argv)
    failed = 0
    for raw in args.path:
        path = Path(raw)
        try:
            data = load_stamp(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"FAIL {path}: {exc}", file=sys.stderr)
            failed += 1
            continue
        errs = check_stamp(data)
        if errs:
            failed += 1
            for e in errs:
                print(f"FAIL {path}: {e}", file=sys.stderr)
        else:
            print(f"ok {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

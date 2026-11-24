#!/usr/bin/env python3
"""VIS-G1 / FR #155 + CAST IRON digests-must-hold: every digest needs fr-digest + hold.

Fail-when: children with no digest, or any digest without hold (including
nested phase digests listed under digests[]).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_DIGEST_LABELS = frozenset({"fr-digest", "hold"})


def _norm_labels(raw: Any) -> set[str]:
    if raw is None:
        return set()
    if isinstance(raw, str):
        parts = [p.strip() for p in raw.replace(";", ",").split(",")]
        return {p for p in parts if p}
    if isinstance(raw, (list, tuple, set)):
        return {str(x).strip() for x in raw if str(x).strip()}
    return set()


def _check_one_digest(digest: dict[str, Any], *, label: str) -> list[str]:
    errs: list[str] = []
    if not isinstance(digest, dict) or not digest:
        errs.append(f"{label}: empty digest object")
        return errs
    labels = _norm_labels(digest.get("labels"))
    missing = REQUIRED_DIGEST_LABELS - labels
    if missing:
        errs.append(
            f"{label}: digest without hold/fr-digest: missing labels "
            + ", ".join(sorted(missing))
        )
    return errs


def check_manifest(data: dict[str, Any]) -> list[str]:
    """Return human error strings (empty = ok)."""
    errs: list[str] = []
    digest = data.get("digest")
    digests = data.get("digests") or []
    children = data.get("children") or []
    order = data.get("order") or []

    if digests and not isinstance(digests, list):
        errs.append("digests must be a JSON array when present")
        return errs

    if digest:
        errs.extend(_check_one_digest(digest, label="digest"))
    for i, d in enumerate(digests):
        name = str((d or {}).get("id") or (d or {}).get("title") or f"digests[{i}]")
        errs.extend(_check_one_digest(d if isinstance(d, dict) else {}, label=name))

    if not digest and not digests:
        errs.append("children with no digest: park missing digest object")
        return errs

    if children and not order:
        errs.append("park order missing: cannot prove digest created first")
    elif order:
        first = str(order[0]).strip().lower()
        if first not in {"digest", "fr-digest"} and not first.startswith("digest"):
            errs.append(
                f"digest not first: order starts with {order[0]!r} "
                "(create digest before children)"
            )

    return errs


def load_manifest(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        raise ValueError(f"{path}: UTF-8 BOM")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: manifest root must be a JSON object")
    return data


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "path",
        nargs="+",
        help="park-manifest.json files (digest first + fr-digest/hold)",
    )
    args = p.parse_args(argv)
    failed = 0
    for raw in args.path:
        path = Path(raw)
        try:
            data = load_manifest(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"FAIL {path}: {exc}", file=sys.stderr)
            failed += 1
            continue
        errs = check_manifest(data)
        if errs:
            failed += 1
            for e in errs:
                print(f"FAIL {path}: {e}", file=sys.stderr)
        else:
            print(f"ok {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

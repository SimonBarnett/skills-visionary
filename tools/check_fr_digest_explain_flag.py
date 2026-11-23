#!/usr/bin/env python3
"""VIS-G4 / FR #190: digest body explains vision + docs link + Digest flag.

Fail-when: digest is only a child list; missing Kind/Digest stamp; missing docs
URL; missing digest/fr-digest label; digest/hold labels on a PR-shaped stamp.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_KIND = re.compile(r"(?im)^\s*Kind:\s*(fr-digest|digest)\s*$")
_DIGEST_TRUE = re.compile(r"(?im)^\s*Digest:\s*true\s*$")
_DOCS_LINK = re.compile(
    r"(?im)(?:\*\*Docs?\*\*|Vision pack|Index):\s*(\S+)|"
    r"https?://\S+|docs/[A-Za-z0-9_./-]+\.md"
)
_VISION_HEAD = re.compile(r"(?im)^##\s*Vision\s*$")
_CHILDREN_HEAD = re.compile(r"(?im)^##\s*Children\s*$")


def _labels(data: dict[str, Any]) -> set[str]:
    raw = data.get("labels") or []
    if isinstance(raw, str):
        raw = [p.strip() for p in raw.split(",") if p.strip()]
    out: set[str] = set()
    for item in raw:
        if isinstance(item, dict):
            name = str(item.get("name") or "").strip().lower()
        else:
            name = str(item).strip().lower()
        if name:
            out.add(name)
    return out


def has_digest_flag_body(body: str) -> bool:
    text = body or ""
    return bool(_KIND.search(text) or _DIGEST_TRUE.search(text))


def has_docs_link(body: str) -> bool:
    return bool(_DOCS_LINK.search(body or ""))


def has_vision_summary(body: str) -> bool:
    """True when a Vision section exists with non-trivial prose before Children."""
    text = body or ""
    m = _VISION_HEAD.search(text)
    if not m:
        # Also accept a short epic/batch summary paragraph before Children
        # when Kind/Digest is present and Docs link exists (legacy parks).
        return False
    after = text[m.end() :]
    cut = _CHILDREN_HEAD.search(after)
    block = after[: cut.start()] if cut else after
    # strip markdown noise
    prose = re.sub(r"[|#*`\-]", " ", block)
    words = [w for w in prose.split() if w.strip()]
    return len(words) >= 8


def check_stamp(data: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    if not isinstance(data, dict):
        return ["stamp root must be an object"]

    if data.get("is_pr") or str(data.get("task") or "").upper() == "MRB":
        labs = _labels(data)
        bad = labs & {"digest", "fr-digest", "hold"}
        if bad:
            errs.append(
                f"digest/hold labels on PR-shaped stamp: {sorted(bad)} (issues-only)"
            )
        return errs

    body = str(data.get("body") or "")
    if data.get("body_file") and not body:
        # caller may resolve body_file before check
        pass

    if not body.strip():
        errs.append("digest body empty")
        return errs

    if not has_digest_flag_body(body):
        errs.append("missing Digest flag: need Kind: fr-digest or Digest: true")

    if not has_docs_link(body):
        errs.append("missing docs link: need Docs/Vision pack/Index URL or docs/*.md path")

    if not has_vision_summary(body):
        errs.append(
            "missing vision summary: need ## Vision with intent/success/out-of-scope prose"
        )

    labs = _labels(data)
    if not (labs & {"digest", "fr-digest"}):
        errs.append("missing Digest label: need label digest and/or fr-digest")

    return errs


def load_stamp(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        raise ValueError(f"{path}: UTF-8 BOM")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: stamp root must be a JSON object")
    if data.get("body_file") and not data.get("body"):
        bp = path.parent / str(data["body_file"])
        data["body"] = bp.read_text(encoding="utf-8")
    digest = data.get("digest")
    if isinstance(digest, dict):
        # allow nested digest object like G2 park-stamp
        if digest.get("body_file") and not digest.get("body"):
            bp = path.parent / str(digest["body_file"])
            digest["body"] = bp.read_text(encoding="utf-8")
        # flatten for check when top-level body/labels absent
        if not data.get("body") and digest.get("body"):
            data["body"] = digest["body"]
        if not data.get("labels") and digest.get("labels"):
            data["labels"] = digest["labels"]
    return data


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path", nargs="+", help="digest stamp JSON files")
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

#!/usr/bin/env python3
"""FR #243 / VIS-G6: default park is parallel under the digest.

Implementation children Depends-on the digest only. Extra #N / owner/repo#N
refs force a linear chain and need an explicit sequencing stamp in the child
body (**Sequencing (intra-batch):** or **Child-hold (intra-batch):**).

Fail-when: park docs force linear Depends-on chains for unrelated FRs with
no sequencing stamp.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SEQ_STAMP = re.compile(
    r"(?i)(\*\*)?\s*(Sequencing|Child-hold)\s*\(\s*intra-batch\s*\)\s*(\*\*)?\s*:",
)

# Depends-on line: capture refs after the label
DEPENDS_LINE = re.compile(r"(?im)^\s*Depends-on\s*:\s*(.+)$")
REF_TOKEN = re.compile(
    r"(?i)#\d+|([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#\d+)|\(none\)"
)


def _norm_depends(raw: Any) -> list[str]:
    if raw is None:
        return []
    text = str(raw).strip()
    if not text:
        return []
    # split commas
    parts = [p.strip() for p in text.replace(";", ",").split(",") if p.strip()]
    return parts


def _refs_from_child(child: dict[str, Any]) -> list[str]:
    refs = _norm_depends(child.get("depends_on"))
    body = str(child.get("body") or "")
    m = DEPENDS_LINE.search(body)
    if m:
        refs = _norm_depends(m.group(1))
    return refs


def _is_digest_only(refs: list[str], digest_nums: set[str]) -> bool:
    """True when every ref is the digest (or placeholder #DIGEST/#PHASE*)."""
    if not refs:
        return False
    for r in refs:
        rl = r.strip()
        if rl.lower() == "(none)":
            return False
        if re.fullmatch(r"(?i)#DIGEST|#EPIC|#PHASE\d*", rl):
            continue
        if re.fullmatch(r"#\d+", rl):
            if rl.lstrip("#") not in digest_nums and rl not in {f"#{n}" for n in digest_nums}:
                # numeric ref that is not a known digest number => sibling chain
                if rl.lstrip("#") not in digest_nums:
                    return False
            continue
        if "/" in rl and "#" in rl:
            # cross-repo: allow only if stamped as digest parent elsewhere; treat as chain
            return False
        # placeholder digest tokens already handled
        if rl.upper().startswith("#DIGEST") or rl.upper().startswith("#PHASE"):
            continue
        return False
    return True


def check_manifest(data: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    digest = data.get("digest") or {}
    digests = data.get("digests") or []
    children = data.get("children") or []

    digest_nums: set[str] = set()
    for d in [digest, *digests]:
        if not isinstance(d, dict):
            continue
        n = d.get("number")
        if n is not None:
            digest_nums.add(str(n).lstrip("#"))
        did = str(d.get("id") or "").strip().lower()
        if did:
            digest_nums.add(did)

    for child in children:
        if not isinstance(child, dict):
            continue
        cid = str(child.get("id") or child.get("title") or "child")
        refs = _refs_from_child(child)
        body = str(child.get("body") or "")
        if _is_digest_only(refs, digest_nums):
            continue
        # Has sibling / linear refs
        if SEQ_STAMP.search(body):
            continue
        errs.append(
            f"{cid}: linear Depends-on {refs!r} without "
            "**Sequencing (intra-batch):** or **Child-hold (intra-batch):** "
            "(FR #243 parallel default)"
        )
    return errs


def load_manifest(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        raise ValueError(f"{path}: UTF-8 BOM")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be object")
    return data


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("path", nargs="+", help="park-manifest JSON files")
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

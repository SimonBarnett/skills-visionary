#!/usr/bin/env python3
"""FR #244: cross-repo digest children park stamps + anti-false-chain.

- Cross-repo children must stamp ``Depends-on: owner/repo#digest`` (not bare ``#N``
  alone when the child repo differs from the digest repo).
- Digest Children table rows may list ``owner/repo#N``.
- Unrelated siblings forced into a Depends-on chain without an explicit
  sequencing stamp fail (anti-false-chain).

Fail-when: cross-repo child missing ``Depends-on: owner/repo#digest``;
unrelated siblings forced into a chain.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SEQ_STAMP = re.compile(
    r"(?i)(\*\*)?\s*(Sequencing|Child-hold|Order reason)\s*"
    r"(\(\s*intra-batch\s*\))?\s*(\*\*)?\s*:",
)
DEPENDS_LINE = re.compile(r"(?im)^\s*\*{0,2}Depends-on\*{0,2}:\*{0,2}\s*(.+?)\s*$")
QUALIFIED = re.compile(r"(?i)^([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)#(\d+)$")
BARE = re.compile(r"^#(\d+)$")
CHILD_ROW = re.compile(
    r"(?im)^\|\s*((?:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)?#?\d+)\s*\|"
)


def _norm_depends(raw: Any) -> list[str]:
    if raw is None:
        return []
    text = str(raw).strip()
    if not text:
        return []
    return [p.strip() for p in text.replace(";", ",").split(",") if p.strip()]


def refs_from_child(child: dict[str, Any]) -> list[str]:
    refs = _norm_depends(child.get("depends_on"))
    body = str(child.get("body") or "")
    m = DEPENDS_LINE.search(body)
    if m:
        refs = _norm_depends(m.group(1))
    return refs


def digest_repo_and_number(digest: dict[str, Any]) -> tuple[str, int]:
    repo = str(digest.get("repo") or "").strip()
    try:
        num = int(str(digest.get("number")).lstrip("#"))
    except (TypeError, ValueError):
        num = 0
    return repo, num


def has_qualified_digest_depends(refs: list[str], repo: str, num: int) -> bool:
    want = f"{repo}#{int(num)}".lower()
    for r in refs:
        rl = r.strip()
        if rl.lower() == want:
            return True
        qm = QUALIFIED.match(rl)
        if qm and qm.group(1).lower() == repo.lower() and int(qm.group(2)) == int(num):
            return True
    return False


def sibling_chain_refs(
    refs: list[str], digest_repo: str, digest_num: int, child_ids: set[str]
) -> list[str]:
    """Refs that point at sibling issues (not the digest)."""
    out: list[str] = []
    dig_q = f"{digest_repo}#{digest_num}".lower() if digest_repo else ""
    dig_bare = f"#{digest_num}"
    for r in refs:
        rl = r.strip()
        if rl.lower() in ("(none)", ""):
            continue
        if dig_q and rl.lower() == dig_q:
            continue
        if rl == dig_bare:
            continue
        if re.fullmatch(r"(?i)#DIGEST|#EPIC|#PHASE\d*", rl):
            continue
        # anything else is a potential sibling / false chain
        out.append(rl)
    return out


_QUALIFIED_ANY = re.compile(r"(?i)([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)#(\d+)")


def children_table_allows_qualified(digest_body: str) -> bool:
    """True when body already uses or documents owner/repo#N child rows."""
    body = digest_body or ""
    if _QUALIFIED_ANY.search(body):
        return True
    # table cells like | owner/repo#N |
    for m in CHILD_ROW.finditer(body):
        cell = m.group(1)
        if "/" in cell and "#" in cell:
            return True
    return "owner/repo#" in body.lower()


def check_park(data: dict[str, Any]) -> list[str]:
    errs: list[str] = []
    digest = data.get("digest") or {}
    if not isinstance(digest, dict) or not digest:
        return ["park missing digest object"]
    digest_repo, digest_num = digest_repo_and_number(digest)
    if digest_num < 1:
        return ["digest missing integer number"]
    if not digest_repo:
        errs.append("digest missing repo (owner/name) for cross-repo park")
        return errs

    children = data.get("children") or []
    if not children:
        errs.append("no children in cross-repo park pack")
        return errs

    child_nums: set[str] = set()
    for child in children:
        if isinstance(child, dict) and child.get("number") is not None:
            child_nums.add(str(child.get("number")).lstrip("#"))

    digest_body = str(digest.get("body") or "")
    # Optional body_file already inlined by loader
    if digest_body and not children_table_allows_qualified(digest_body):
        # Require at least one qualified child id in the table when any child is foreign
        foreign = [
            c
            for c in children
            if isinstance(c, dict)
            and str(c.get("repo") or "").strip()
            and str(c.get("repo")).strip().lower() != digest_repo.lower()
        ]
        if foreign:
            errs.append(
                "digest Children table must list foreign children as owner/repo#N "
                f"(digest {digest_repo}#{digest_num})"
            )

    for i, child in enumerate(children):
        if not isinstance(child, dict):
            errs.append(f"child[{i}] must be an object")
            continue
        cid = str(child.get("id") or child.get("title") or f"child[{i}]")
        crepo = str(child.get("repo") or "").strip()
        refs = refs_from_child(child)
        body = str(child.get("body") or "")
        foreign = bool(crepo) and crepo.lower() != digest_repo.lower()

        if foreign:
            if not has_qualified_digest_depends(refs, digest_repo, digest_num):
                errs.append(
                    f"{cid}: cross-repo child missing Depends-on: "
                    f"{digest_repo}#{digest_num}"
                )

        chain = sibling_chain_refs(refs, digest_repo, digest_num, child_nums)
        if chain and not SEQ_STAMP.search(body):
            # also allow depends_on field-only children to carry order_reason
            if not str(child.get("order_reason") or "").strip():
                errs.append(
                    f"{cid}: false-chain Depends-on {chain!r} without "
                    "Sequencing/Order reason stamp (FR #244)"
                )

    return errs


def load_park(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        raise ValueError(f"{path}: UTF-8 BOM")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be object")
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
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("park", type=Path, help="park JSON (stamp/manifest)")
    args = ap.parse_args(argv)
    try:
        data = load_park(args.park)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errs = check_park(data)
    if errs:
        for e in errs:
            print(e, file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""VIS-G5 / FR #220: do not double-park children with hold + Depends-on digest.

Default park: digest has hold; children use Depends-on:#digest only (no hold).
Child hold is allowed only when the child body stamps an explicit intra-batch
sequencing reason beyond waiting on the digest.

Fail-when: child has hold/on-hold while Depends-on includes only the digest
(and optional intra-batch #N) without an explicit child-hold reason stamp.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

HOLD_LABELS = frozenset({"hold", "on-hold"})
# Child body must say why hold is layered beyond Depends-on digest.
# Accept bold before/after the label and optional colon: **Child-hold (intra-batch):**
CHILD_HOLD_REASON_RE = re.compile(
    r"(?i)Child-hold\s*\(\s*(intra-batch|sequencing)\s*\)",
)
DEPENDS_ON_RE = re.compile(r"(?im)^\s*\*?\*?Depends-on\*?\*?\s*:\s*(.+)$")


def _norm_labels(raw: Any) -> set[str]:
    if raw is None:
        return set()
    if isinstance(raw, str):
        parts = [p.strip().lower() for p in raw.replace(";", ",").split(",")]
        return {p for p in parts if p}
    if isinstance(raw, (list, tuple, set)):
        return {str(x).strip().lower() for x in raw if str(x).strip()}
    return set()


def _depends_on_line(body: str) -> str:
    m = DEPENDS_ON_RE.search(body or "")
    return (m.group(1) if m else "").strip()


def _depends_on_digest_only(depends: str, digest_number: int | None) -> bool:
    """True when Depends-on refs are only the digest (and/or empty/none)."""
    blob = (depends or "").strip()
    if not blob or blob.lower() in {"(none)", "none"}:
        return True
    if digest_number is None:
        # Placeholder form from park manifests: #DIGEST / #<digest>
        tokens = re.split(r"[,;\s]+", blob)
        kept = [t for t in tokens if t]
        if not kept:
            return True
        return all(
            re.fullmatch(r"(?i)#?(?:DIGEST|<digest>|digest)", t) for t in kept
        )
    # Real numbers: every #N must be the digest number (no extra gates required
    # for this check — intra-batch #N alone is still "waiting on batch"; hold
    # still forbidden unless Child-hold reason is present).
    return True


def child_double_parked(
    *,
    labels: set[str],
    body: str,
    digest_number: int | None = None,
) -> str | None:
    """Return fail reason when child is double-parked; else None."""
    if not (labels & HOLD_LABELS):
        return None
    if CHILD_HOLD_REASON_RE.search(body or ""):
        return None
    depends = _depends_on_line(body)
    # Manifest may put depends_on on the child object; callers pass via body.
    if not depends:
        # still double-park if hold without reason (digest gate assumed)
        return "child hold without Child-hold (intra-batch) reason (double-park)"
    if _depends_on_digest_only(depends, digest_number):
        return (
            "double-park: child has hold while Depends-on digest is the go-gate; "
            "omit child hold or stamp **Child-hold (intra-batch):** reason"
        )
    return (
        "double-park: child has hold without **Child-hold (intra-batch):** reason"
    )


def check_manifest(data: dict[str, Any], *, root: Path | None = None) -> list[str]:
    errs: list[str] = []
    digest = data.get("digest") if isinstance(data.get("digest"), dict) else {}
    digest_number = digest.get("number")
    try:
        digest_number = int(digest_number) if digest_number is not None else None
    except (TypeError, ValueError):
        digest_number = None

    children = data.get("children") or []
    for i, child in enumerate(children):
        if not isinstance(child, dict):
            errs.append(f"children[{i}]: not an object")
            continue
        labels = _norm_labels(child.get("labels"))
        body = str(child.get("body") or "")
        body_file = str(child.get("body_file") or "").strip()
        if not body and body_file and root is not None:
            path = root / body_file
            try:
                body = path.read_text(encoding="utf-8-sig")
            except OSError as exc:
                errs.append(f"children[{i}]: cannot read body_file {body_file}: {exc}")
                continue
        depends_field = str(child.get("depends_on") or "").strip()
        if depends_field and "Depends-on:" not in body and "depends-on:" not in body.lower():
            body = f"Depends-on: {depends_field}\n{body}"
        why = child_double_parked(
            labels=labels, body=body, digest_number=digest_number
        )
        if why:
            cid = child.get("id") or child.get("number") or i
            errs.append(f"child {cid}: {why}")
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
        help="park-manifest.json / park-stamp.json files",
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
        errs = check_manifest(data, root=path.parent)
        if errs:
            failed += 1
            for e in errs:
                print(f"FAIL {path}: {e}", file=sys.stderr)
        else:
            print(f"ok {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

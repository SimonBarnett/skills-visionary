#!/usr/bin/env python3
"""VIS-G2 / FR #156: build digest Children table + child Depends-on:#digest bodies.

Dry-run helpers for Plan park: stamp children with Depends-on:#D and patch the
digest body Children table so every child #N appears.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Reuse VIS-D2 formatter when available.
_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from format_depends_on_park_issue_body import format_park_issue_body  # noqa: E402


_CHILDREN_SECTION = re.compile(
    r"(?ims)^##\s*Children\s*$\n.*?(?=^##\s|\Z)"
)


def format_children_table(rows: list[dict]) -> str:
    """Return a markdown Children table for digest body.

    Each row: {"number": int, "title": str, "vision": str}
    """
    lines = [
        "## Children",
        "",
        "| Issue | Title | Vision |",
        "|-------|-------|--------|",
    ]
    for row in rows:
        num = int(row["number"])
        title = str(row.get("title") or "").replace("|", "\\|")
        vision = str(row.get("vision") or "").replace("|", "\\|")
        lines.append(f"| #{num} | {title} | {vision} |")
    lines.append("")
    return "\n".join(lines)


def patch_digest_children_table(digest_body: str, rows: list[dict]) -> str:
    """Replace or append the ## Children section with a filled table."""
    table = format_children_table(rows)
    body = digest_body or ""
    if _CHILDREN_SECTION.search(body):
        return _CHILDREN_SECTION.sub(table.rstrip() + "\n\n", body, count=1)
    # append before trailing whitespace
    return body.rstrip() + "\n\n" + table


def format_child_body_for_digest(
    *,
    feature_id: str,
    theme: str,
    vision_pack_url: str,
    index_url: str,
    digest_number: int,
    extra_depends: list[str] | None = None,
) -> str:
    """Child park body with Depends-on:#digest (+ optional intra-batch refs)."""
    deps: list[str] = [f"#{int(digest_number)}"]
    for tok in extra_depends or []:
        t = str(tok).strip()
        if t and t not in deps:
            deps.append(t)
    return format_park_issue_body(
        feature_id=feature_id,
        theme=theme,
        vision_pack_url=vision_pack_url,
        index_url=index_url,
        depends_on=deps,
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("table", help="Print Children markdown table")
    t.add_argument(
        "--row",
        action="append",
        required=True,
        help="number|title|vision (repeatable)",
    )

    c = sub.add_parser("child-body", help="Print child issue body Depends-on:#digest")
    c.add_argument("--feature-id", required=True)
    c.add_argument("--theme", required=True)
    c.add_argument("--vision-pack-url", required=True)
    c.add_argument("--index-url", required=True)
    c.add_argument("--digest", type=int, required=True)
    c.add_argument("--extra-depends", default="", help="comma-separated #N refs")

    d = sub.add_parser("patch-digest", help="Patch digest body file Children table")
    d.add_argument("--digest-body", required=True, type=Path)
    d.add_argument(
        "--row",
        action="append",
        required=True,
        help="number|title|vision (repeatable)",
    )
    d.add_argument("-o", "--output", type=Path, help="Write result (default stdout)")

    args = p.parse_args(argv)

    if args.cmd == "table":
        rows = []
        for raw in args.row:
            num, title, vision = raw.split("|", 2)
            rows.append({"number": int(num), "title": title, "vision": vision})
        sys.stdout.write(format_children_table(rows))
        return 0

    if args.cmd == "child-body":
        extra = [x.strip() for x in args.extra_depends.split(",") if x.strip()]
        sys.stdout.write(
            format_child_body_for_digest(
                feature_id=args.feature_id,
                theme=args.theme,
                vision_pack_url=args.vision_pack_url,
                index_url=args.index_url,
                digest_number=args.digest,
                extra_depends=extra,
            )
        )
        return 0

    if args.cmd == "patch-digest":
        rows = []
        for raw in args.row:
            num, title, vision = raw.split("|", 2)
            rows.append({"number": int(num), "title": title, "vision": vision})
        body = args.digest_body.read_text(encoding="utf-8")
        out = patch_digest_children_table(body, rows)
        if args.output:
            args.output.write_text(out, encoding="utf-8", newline="\n")
        else:
            sys.stdout.write(out)
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

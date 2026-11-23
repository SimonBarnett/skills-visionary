#!/usr/bin/env python3
"""VIS-G4 / FR #190: build digest issue body with vision summary + docs + Digest flag.

Plan park uses this for the digest GitHub issue body (intake -Body / gh issue create).
Labels at create: digest + fr-digest + hold (+ feature-request when the repo uses it).
Never stamp digest/hold on PRs.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Reuse Children table helper when present.
_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
try:
    from format_fr_digest_children_stamp import format_children_table  # noqa: E402
except Exception:  # pragma: no cover - optional during partial trees
    format_children_table = None  # type: ignore


DIGEST_CREATE_LABELS = ("digest", "fr-digest", "hold", "feature-request")


def format_digest_issue_body(
    *,
    theme: str,
    vision_summary: str,
    docs_url: str,
    vision_pack_url: str,
    index_url: str,
    children_rows: list[dict] | None = None,
    depends_on: str = "(none)",
) -> str:
    """Return digest body: flag + vision + docs links + Children table."""
    summary = (vision_summary or "").strip()
    if not summary:
        raise ValueError("vision_summary is required")
    docs = (docs_url or vision_pack_url or "").strip()
    if not docs:
        raise ValueError("docs_url or vision_pack_url is required")
    lines = [
        f"**Depends-on:** {depends_on}",
        "",
        "Kind: fr-digest",
        "Digest: true",
        "",
        f"**Theme:** {theme}",
        "",
        "## Vision",
        "",
        summary,
        "",
        f"**Docs:** {docs}",
        f"**Vision pack:** {vision_pack_url}",
        f"**Index:** {index_url}",
        "",
        "Digest go-gate for this batch. Children are not assignable until this",
        "issue is **unheld**. Labels at create: `digest` + `fr-digest` + `hold`.",
        "",
    ]
    if children_rows is not None and format_children_table is not None:
        lines.append(format_children_table(children_rows).rstrip())
        lines.append("")
    elif children_rows is not None:
        lines.extend(
            [
                "## Children",
                "",
                "| Issue | Title | Vision |",
                "|-------|-------|--------|",
            ]
        )
        for row in children_rows:
            num = row.get("number", "pending")
            title = str(row.get("title") or "").replace("|", "\\|")
            vision = str(row.get("vision") or "").replace("|", "\\|")
            cell = f"#{num}" if str(num).isdigit() else "(pending)"
            lines.append(f"| {cell} | {title} | {vision} |")
        lines.append("")
    return "\n".join(lines)


def digest_create_labels() -> list[str]:
    return list(DIGEST_CREATE_LABELS)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("body", help="Print digest issue body")
    b.add_argument("--theme", required=True)
    b.add_argument("--vision-summary", required=True, help="intent / success / out of scope")
    b.add_argument("--docs-url", required=True)
    b.add_argument("--vision-pack-url", required=True)
    b.add_argument("--index-url", required=True)
    b.add_argument("--depends-on", default="(none)")
    b.add_argument(
        "--row",
        action="append",
        default=[],
        help="number|title|vision for Children table (repeatable; use pending|title|vision)",
    )

    l = sub.add_parser("labels", help="Print JSON label list for digest create")

    args = p.parse_args(argv)
    if args.cmd == "labels":
        sys.stdout.write(json.dumps(digest_create_labels()) + "\n")
        return 0

    rows: list[dict] = []
    for raw in args.row:
        num, title, vision = raw.split("|", 2)
        num = num.strip()
        row: dict = {"title": title, "vision": vision}
        if num.isdigit():
            row["number"] = int(num)
        else:
            row["number"] = num
        rows.append(row)

    body = format_digest_issue_body(
        theme=args.theme,
        vision_summary=args.vision_summary,
        docs_url=args.docs_url,
        vision_pack_url=args.vision_pack_url,
        index_url=args.index_url,
        children_rows=rows or None,
        depends_on=args.depends_on,
    )
    sys.stdout.write(body)
    if not body.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

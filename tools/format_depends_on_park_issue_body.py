#!/usr/bin/env python3
"""VIS-D2 / FR #148: build a Plan-park GitHub issue body with a Depends-on stamp.

Plan park must put Depends-on on the **issue body** passed to intake/`gh issue
create`, not only in vision markdown. Dry-run prints the body for fixtures.
"""
from __future__ import annotations

import argparse
import re
import sys

_NONE = "(none)"
_RELATIVE = re.compile(r"^#\d+$")
_QUALIFIED = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#\d+$")


def normalize_depends_on(raw: str | list[str] | None) -> str:
    """Return a single Depends-on value: ``(none)``, ``#N``, or ``owner/repo#N`` list."""
    if raw is None:
        return _NONE
    if isinstance(raw, str):
        parts = [p.strip() for p in re.split(r"[,;\s]+", raw) if p.strip()]
    else:
        parts = [str(p).strip() for p in raw if str(p).strip()]
    if not parts or (len(parts) == 1 and parts[0].lower() == _NONE):
        return _NONE
    out: list[str] = []
    for tok in parts:
        if tok.lower() == _NONE:
            continue
        if not (_RELATIVE.match(tok) or _QUALIFIED.match(tok)):
            raise ValueError(
                f"invalid Depends-on ref {tok!r}; use #N, owner/repo#N, or (none)"
            )
        if tok not in out:
            out.append(tok)
    return ", ".join(out) if out else _NONE


def format_park_issue_body(
    *,
    feature_id: str,
    theme: str,
    vision_pack_url: str,
    index_url: str,
    depends_on: str | list[str] | None = _NONE,
    implement_blurb: str = (
        "Plan must identify FR preconditions on the issue. "
        "Implement Success S1 in the vision pack. Open a PR against main. "
        "Do not merge. One acceptance row only."
    ),
) -> str:
    """Return issue body with ``Depends-on`` in the first lines (chair truncation)."""
    dep = normalize_depends_on(depends_on)
    # Keep Depends-on within the first ~500 characters of the body.
    lines = [
        f"**Depends-on:** {dep}",
        "",
        f"Feature request `{feature_id}` (parked).",
        "",
        f"**Theme:** {theme}",
        f"**Depends-on:** {dep}",
        f"**Vision pack:** {vision_pack_url}",
        f"**Index:** {index_url}",
        "",
        implement_blurb.strip(),
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--feature-id", required=True, help="e.g. VIS-D2 or BOB-D3")
    p.add_argument("--theme", required=True)
    p.add_argument("--vision-pack-url", required=True)
    p.add_argument("--index-url", required=True)
    p.add_argument(
        "--depends-on",
        default=_NONE,
        help="(none), #N, owner/repo#N, or comma-separated list",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the issue body to stdout (fixture / evidence)",
    )
    args = p.parse_args(argv)
    body = format_park_issue_body(
        feature_id=args.feature_id,
        theme=args.theme,
        vision_pack_url=args.vision_pack_url,
        index_url=args.index_url,
        depends_on=args.depends_on,
    )
    # Always print: Plan seats pipe this into intake -Body / evidence files.
    sys.stdout.write(body)
    if not body.endswith("\n"):
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

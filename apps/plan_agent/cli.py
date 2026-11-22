"""Plan Agent CLI: accept model/context/effort (VIS-02 / FR #136).

Aligned with bobiverse BOB-15 setting names (model, context, effort).
Effort values match VALID_EFFORTS low/medium/high. Context is accepted
on this Plan surface even when sibling CLIs mark it unsupported.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

VALID_EFFORTS = ("low", "medium", "high")
PRODUCT_NAME = "Plan Agent"


def normalize_effort(raw: object) -> str:
    s = str(raw or "").strip().lower()
    if s in VALID_EFFORTS:
        return s
    return ""


def cli_settings_args(
    *,
    model: str = "",
    context: str = "",
    effort: str = "",
) -> list[str]:
    """Build argv fragment for model/context/effort when set."""
    args: list[str] = []
    mid = str(model or "").strip()
    if mid:
        args.extend(["--model", mid])
    ctx = str(context or "").strip()
    if ctx:
        args.extend(["--context", ctx])
    eff = normalize_effort(effort)
    if eff:
        args.extend(["--effort", eff])
    return args


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="plan-agent",
        description=(
            f"{PRODUCT_NAME}: start with models webhook settings "
            "(model / context / effort)."
        ),
    )
    p.add_argument(
        "--model",
        default="",
        help="Model id from the models webhook / tray (e.g. grok-4).",
    )
    p.add_argument(
        "--context",
        default="",
        help="Context window / budget hint from the models webhook.",
    )
    p.add_argument(
        "--effort",
        default="",
        choices=VALID_EFFORTS,
        help="Reasoning effort: low, medium, or high.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print resolved settings as JSON and exit (no seat launch).",
    )
    return p


def dry_run_payload(
    *,
    model: str,
    context: str,
    effort: str,
) -> dict[str, Any]:
    args = cli_settings_args(model=model, context=context, effort=effort)
    return {
        "product": PRODUCT_NAME,
        "dry_run": True,
        "model": str(model or "").strip(),
        "context": str(context or "").strip(),
        "effort": normalize_effort(effort),
        "cli_settings_args": args,
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    model = str(args.model or "").strip()
    context = str(args.context or "").strip()
    effort = str(args.effort or "").strip()

    if args.dry_run:
        payload = dry_run_payload(model=model, context=context, effort=effort)
        sys.stdout.write(json.dumps(payload, sort_keys=True) + "\n")
        return 0

    # Full seat launch is VIS-01 (PlanAgent exe). This slice only proves
    # the settings flag surface; without --dry-run require at least one flag.
    if not (model or context or effort):
        parser.error("pass --model/--context/--effort, or use --dry-run / --help")
    payload = dry_run_payload(model=model, context=context, effort=effort)
    payload["dry_run"] = False
    payload["status"] = "settings-accepted"
    sys.stdout.write(json.dumps(payload, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

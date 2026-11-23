"""VIS-03 / FR #137: no-token dialog + quit when this box has no tokens.

Aligned with bobiverse FR #8814 (EXIT_OUT_OF_FUEL=10, dialog then quit).
Fuel-empty is proven by a fixture JSON (remaining_pct == 0).
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Callable

EXIT_OUT_OF_FUEL = 10  # match bob_worker FR #8814
PRODUCT_NAME = "Plan Agent"
DEFAULT_DIALOG_TITLE = "Plan Agent - no tokens"


def load_fuel_doc(path: str | Path | None) -> dict[str, Any] | None:
    if not path:
        return None
    p = Path(path)
    try:
        raw = p.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        doc = json.loads(raw)
    except ValueError:
        return None
    return doc if isinstance(doc, dict) else None


def is_fuel_empty(doc: dict[str, Any] | None) -> bool:
    """True when the box has no tokens (remaining_pct 0 or status empty/exhausted)."""
    if not isinstance(doc, dict):
        return False
    status = str(doc.get("status") or "").strip().lower()
    if status in ("empty", "exhausted", "out-of-fuel", "out_of_fuel"):
        return True
    for key in ("remaining_pct", "remaining", "tokens_remaining"):
        if key not in doc or doc.get(key) is None or doc.get(key) == "":
            continue
        try:
            return int(doc.get(key)) <= 0
        except (TypeError, ValueError):
            continue
    return False


def format_no_token_dialog_text(
    *,
    pool: str = "",
    remaining: str = "",
    evidence: str = "",
    nick: str = "",
) -> str:
    parts = [
        f"{PRODUCT_NAME}: this box has no tokens.",
        "The Plan seat will quit instead of starting without fuel.",
    ]
    if pool:
        parts.append(f"Pool: {pool}")
    if remaining:
        parts.append(f"Remaining: {remaining}")
    if evidence:
        parts.append(f"Evidence: {evidence}")
    if nick:
        parts.append(f"Seat: {nick}")
    return "\n".join(parts)


def _default_message_box(text: str, title: str) -> None:
    """Windows MessageBox when available; otherwise print to stderr."""
    if os.name == "nt":
        try:
            import ctypes

            ctypes.windll.user32.MessageBoxW(0, str(text), str(title), 0x10)  # MB_ICONERROR
            return
        except Exception:
            pass
    sys.stderr.write(f"{title}\n{text}\n")


def show_no_token_dialog(
    *,
    pool: str = "",
    remaining: str = "",
    evidence: str = "",
    nick: str = "",
    show_fn: Callable[[str, str], None] | None = None,
    env: dict[str, str] | None = None,
    log: Callable[[str], None] | None = None,
) -> bool:
    """Show the no-token dialog. Returns True when shown.

    Set BOB_PLAN_FUEL_DIALOG=0 to skip the GUI (tests / headless) while still quitting.
    """
    e = os.environ if env is None else env
    flag = str((e or {}).get("BOB_PLAN_FUEL_DIALOG") or "1").strip().lower()
    text = format_no_token_dialog_text(
        pool=pool, remaining=remaining, evidence=evidence, nick=nick
    )
    title = DEFAULT_DIALOG_TITLE
    if flag in ("0", "false", "no", "off"):
        if log:
            log("plan-agent fuel dialog skipped (BOB_PLAN_FUEL_DIALOG off)")
        # Still emit a machine-readable line for fixtures / CI.
        sys.stderr.write(f"out-of-fuel dialog: {text.splitlines()[0]}\n")
        return False
    fn = show_fn or _default_message_box
    fn(text, title)
    return True


def resolve_fuel_path(
    *,
    cli_path: str = "",
    env: dict[str, str] | None = None,
) -> Path | None:
    e = os.environ if env is None else env
    raw = str(cli_path or "").strip() or str((e or {}).get("BOB_PLAN_FUEL_FILE") or "").strip()
    if not raw:
        return None
    return Path(raw)


def enforce_fuel_or_quit(
    *,
    fuel_path: str | Path | None = None,
    show_fn: Callable[[str, str], None] | None = None,
    env: dict[str, str] | None = None,
    nick: str = "",
) -> int | None:
    """If fuel is empty: dialog + return EXIT_OUT_OF_FUEL. Else return None (continue)."""
    path = Path(fuel_path) if fuel_path else resolve_fuel_path(env=env)
    doc = load_fuel_doc(path) if path else None
    if not is_fuel_empty(doc):
        return None
    assert doc is not None
    pool = str(doc.get("pool") or "plan")
    rem = doc.get("remaining_pct")
    if rem is None:
        rem = doc.get("remaining")
    remaining = "0" if rem is None else str(rem)
    evidence = str(doc.get("evidence") or "fuel-empty")
    show_no_token_dialog(
        pool=pool,
        remaining=remaining,
        evidence=evidence,
        nick=nick,
        show_fn=show_fn,
        env=env,
    )
    sys.stderr.write(
        f"out-of-fuel: {PRODUCT_NAME} quitting (exit {EXIT_OUT_OF_FUEL}); "
        f"pool={pool} remaining={remaining} evidence={evidence}\n"
    )
    return EXIT_OUT_OF_FUEL

#!/usr/bin/env python3
"""Validate a visionary vision pack (shape, success, HTML mocks). Exit 1 on failure."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PRIMARY_SHAPES = ("service", "website", "app")
REQUIRED_MOCKS = ("home", "empty", "error")
POETRY_PHRASES = (
    "users will love it",
    "users love it",
    "a lot",
    "feelings",
)
OBSERVABLE_HOW_PATTERNS = (
    r"`[^`]+`",
    r"\bpython\b",
    r"\bpytest\b",
    r"\bpip\b",
    r"\bworkflow\b",
    r"\.github",
    r"GitHub Actions",
    r"\bGHA\b",
    r"\bCI\b",
    r"docs/",
    r"tests/",
    r"tools/",
    r"README",
    r"\bvalidator\b",
    r"\bfixture",
    r"file content",
    r"\bexit\s+[01]\b",
    r"\b\d+%\b",
    r"\b\d+\s+of\b",
    r"/",
    r"\\",
)

# FR #22: human-scale mermaid - hard ceiling ~12 nodes; caption required.
MERMAID_NODE_CEILING = 12
MERMAID_FENCE_RE = re.compile(
    r"(?ms)^(?P<indent>[ \t]*)```mermaid[ \t]*\r?\n(?P<body>.*?)(?P=indent)```[ \t]*$"
)
MERMAID_KW = frozenset(
    {
        "flowchart",
        "graph",
        "sequencediagram",
        "statediagram",
        "statediagram-v2",
        "classdiagram",
        "erdiagram",
        "gantt",
        "pie",
        "journey",
        "requirementdiagram",
        "gitgraph",
        "mindmap",
        "timeline",
        "participant",
        "actor",
        "as",
        "note",
        "over",
        "left",
        "right",
        "of",
        "end",
        "loop",
        "alt",
        "else",
        "opt",
        "par",
        "and",
        "rect",
        "activate",
        "deactivate",
        "state",
        "direction",
        "tb",
        "td",
        "bt",
        "rl",
        "lr",
        "subgraph",
        "class",
        "click",
        "style",
        "linkstyle",
        "classdef",
        "yes",
        "no",
    }
)


def section(text: str, name: str) -> str:
    pattern = rf"^##\s+{re.escape(name)}\s*$"
    match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
    if not match:
        return ""
    start = match.end()
    nxt = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + nxt.start() if nxt else len(text)
    return text[start:end]


def shape_is_unknown(shape: str) -> bool:
    if re.search(r"Primary:\s*UNKNOWN\b", shape, re.IGNORECASE):
        return True
    if re.search(r"^UNKNOWN\s*$", shape, re.MULTILINE | re.IGNORECASE):
        if not re.search(r"^LOCKED\s*$", shape, re.MULTILINE):
            return True
    return False


def shape_locked_primary(shape: str) -> str | None:
    for line in shape.splitlines():
        m = re.match(
            r"^\s*Primary(?:\s*\(one\))?:\s*(service|website|app)\s*\.?\s*$",
            line,
            re.IGNORECASE,
        )
        if m:
            return m.group(1).lower()
        m = re.match(
            r"^\s*Primary(?:\s*\(one\))?:\s*\*\*(service|website|app)\*\*\s*$",
            line,
            re.IGNORECASE,
        )
        if m:
            return m.group(1).lower()
        m = re.match(
            r"^\s*Reuse repo primary:\s*\*\*(service|website|app)\*\*",
            line,
            re.IGNORECASE,
        )
        if m:
            return m.group(1).lower()
    return None


def shape_has_locked(shape: str) -> bool:
    for line in shape.splitlines():
        if re.match(r"^\s*LOCKED\s*/\s*UNKNOWN\s*:?\s*$", line, re.IGNORECASE):
            continue
        if re.match(r"^\s*LOCKED\s*$", line, re.IGNORECASE):
            return True
    return False



DEPENDS_ON_LINE_RE = re.compile(
    r"(?im)^(?:\*\*Depends-on:\*\*|Depends-on:)\s*(.+?)\s*$"
)
# Enforceable refs: #N or owner/repo#N. (none) is explicit empty.
DEPENDS_ON_NONE_RE = re.compile(r"^\(none\)$", re.IGNORECASE)
DEPENDS_ON_ISSUE_RE = re.compile(
    r"^(?:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)?#\d+$"
)

def iter_depends_on_values(text: str) -> list[str]:
    """Return raw Depends-on values from pack header lines (may be empty)."""
    return [m.group(1).strip() for m in DEPENDS_ON_LINE_RE.finditer(text)]


def validate_depends_on(text: str, errors: list[str]) -> bool:
    """FR #149 / VIS-D3: refuse backlog-id-only Depends-on (e.g. bare BOB-06).

    Missing Depends-on is allowed (older packs). Present values must be
    `(none)`, `#N`, and/or `owner/repo#N` tokens — never sole/mixed
    bare backlog ids.
    """
    values = iter_depends_on_values(text)
    if not values:
        return True
    ok = True
    for raw in values:
        if not raw:
            errors.append("depends-on: empty value; use (none) or #N / owner/repo#N")
            ok = False
            continue
        if DEPENDS_ON_NONE_RE.match(raw):
            continue
        tokens = [t.strip() for t in raw.split(",") if t.strip()]
        if not tokens:
            errors.append("depends-on: empty value; use (none) or #N / owner/repo#N")
            ok = False
            continue
        bad: list[str] = []
        for tok in tokens:
            if DEPENDS_ON_ISSUE_RE.match(tok):
                continue
            bad.append(tok)
        if bad:
            errors.append(
                "depends-on: backlog-id-only or non-issue ref not allowed: "
                + ", ".join(bad)
                + " (use #N, owner/repo#N, or (none); VIS-D3 / FR #149)"
            )
            ok = False
    return ok


def validate_shape(shape: str, errors: list[str]) -> bool:
    if not shape.strip():
        errors.append("shape: missing ## Shape section")
        return False
    if shape_is_unknown(shape):
        return True
    primary = shape_locked_primary(shape)
    if primary is None:
        errors.append(
            "shape: set Primary to service, website, or app (or mark shape UNKNOWN)"
        )
        return False
    if primary not in PRIMARY_SHAPES:
        errors.append(f"shape: invalid primary '{primary}'")
        return False
    if not shape_has_locked(shape):
        errors.append("shape: primary chosen but Shape is not LOCKED")
        return False
    return True


def success_is_unknown(success: str) -> bool:
    if re.search(r"(?im)^\s*UNKNOWN\s*$", success):
        return True
    if re.search(r"(?i)success\s+(?:section\s+)?is\s+UNKNOWN", success):
        return True
    if re.search(r"(?i)whole\s+table\s+is\s+UNKNOWN", success):
        stripped = success.strip().lower()
        if "unknown" in stripped and "|" not in success:
            return True
    return False


def field_has_poetry(text: str) -> bool:
    lowered = text.strip().lower()
    return any(phrase in lowered for phrase in POETRY_PHRASES)


def how_measured_observable(how: str) -> bool:
    how = how.strip()
    if not how:
        return False
    for pattern in OBSERVABLE_HOW_PATTERNS:
        if re.search(pattern, how, re.IGNORECASE):
            return True
    return False


def row_is_measurable(metric: str, target: str, how: str) -> bool:
    if field_has_poetry(metric) or field_has_poetry(target) or field_has_poetry(how):
        return False
    return how_measured_observable(how)


def parse_success_rows(success: str) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    for line in success.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        if cells[0].lower() in ("id", "----"):
            continue
        if all(re.match(r"^-+$", c) for c in cells):
            continue
        metric, target, how, fail_when = cells[1], cells[2], cells[3], cells[4]
        rows.append((metric, target, how, fail_when))
    return rows


def validate_success(success: str, errors: list[str]) -> bool:
    if not success.strip():
        errors.append("success: missing ## Success section")
        return False
    if success_is_unknown(success):
        return True
    rows = parse_success_rows(success)
    complete = [
        r
        for r in rows
        if all(field and not re.match(r"^-+$", field) for field in r)
    ]
    if not complete:
        errors.append(
            "success: add a complete table row (metric, target, how measured, fail-when) "
            "or mark Success UNKNOWN"
        )
        return False
    measurable = [r for r in complete if row_is_measurable(*r[:3])]
    if measurable:
        return True
    if any(field_has_poetry(m) or field_has_poetry(t) or field_has_poetry(h) for m, t, h, _ in complete):
        errors.append(
            "success: poetry is not measurable (metric/target/how-measured must cite "
            "a command, path, workflow, or count)"
        )
    else:
        errors.append(
            "success: how-measured must cite an observable check "
            "(command, path, workflow, or count)"
        )
    return False


def iter_mermaid_blocks(text: str) -> list[tuple[int, str, str]]:
    """Return (1-based start line, caption_line, body) for each mermaid fence."""
    out: list[tuple[int, str, str]] = []
    for m in MERMAID_FENCE_RE.finditer(text):
        start = text[: m.start()].count("\n") + 1
        before = text[: m.start()].rstrip("\r\n")
        caption = ""
        if before:
            caption = before.splitlines()[-1].strip()
        out.append((start, caption, m.group("body")))
    return out


def count_mermaid_nodes(body: str) -> int:
    """Best-effort unique node/participant/state id count for FR #22 ceiling."""
    ids: set[str] = set()
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("%%"):
            continue
        low = line.lower()
        # sequenceDiagram participants
        m = re.match(r"(?i)^(participant|actor)\s+(\w+)", line)
        if m:
            ids.add(m.group(2))
            continue
        # stateDiagram: state Id or Id: label / [*]
        m = re.match(r"(?i)^state\s+(\w+)\b", line)
        if m:
            ids.add(m.group(1))
        # flowchart / graph node defs and edge endpoints
        for tok in re.findall(r"[A-Za-z][\w]*", line):
            if tok.lower() in MERMAID_KW:
                continue
            if tok.isdigit():
                continue
            # skip pure direction tokens already in KW
            ids.add(tok)
        # edge-only lines still contribute via findall above
        if re.search(r"\[\*\]", line):
            ids.add("*")
    return len(ids)


def caption_is_usable(caption: str) -> bool:
    if not caption:
        return False
    if caption.startswith("#"):
        return False
    if caption.startswith("```"):
        return False
    if re.match(r"^[-*|]{1,}\s*$", caption):
        return False
    # Require a short sentence, not a bare heading word.
    letters = sum(1 for c in caption if c.isalpha())
    return letters >= 8


def validate_mermaid(text: str, errors: list[str]) -> bool:
    """FR #22: every mermaid block needs a caption; nodes <= ceiling."""
    ok = True
    blocks = iter_mermaid_blocks(text)
    for idx, (line_no, caption, body) in enumerate(blocks, start=1):
        if not caption_is_usable(caption):
            errors.append(
                f"mermaid[{idx}]@{line_no}: missing one-sentence caption on the "
                "line immediately above the mermaid fence"
            )
            ok = False
        nodes = count_mermaid_nodes(body)
        if nodes > MERMAID_NODE_CEILING:
            errors.append(
                f"mermaid[{idx}]@{line_no}: {nodes} nodes exceeds ceiling "
                f"{MERMAID_NODE_CEILING} - split into smaller diagrams"
            )
            ok = False
    return ok


def validate_mocks(mocks_dir: Path, errors: list[str]) -> bool:
    if not mocks_dir.is_dir():
        errors.append(f"mocks: directory not found: {mocks_dir}")
        return False
    html_files = list(mocks_dir.glob("*.html"))
    png_files = list(mocks_dir.glob("*.png"))
    if not html_files and png_files:
        errors.append("mocks: PNG-only mocks are not allowed")
        return False
    missing: list[str] = []
    for key in REQUIRED_MOCKS:
        if not (mocks_dir / f"{key}.html").is_file():
            missing.append(f"{key}.html")
    if missing:
        errors.append(f"mocks: missing required HTML: {', '.join(missing)}")
        return False
    return True


def validate_pack(vision_path: Path, mocks_dir: Path, historical: bool = False) -> list[str]:
    if historical:
        return []
    errors: list[str] = []
    text = vision_path.read_text(encoding="utf-8")
    shape_sec = section(text, "Shape")
    success_sec = section(text, "Success")

    shape_ok = validate_shape(shape_sec, errors)
    validate_success(success_sec, errors)
    validate_mermaid(text, errors)
    validate_depends_on(text, errors)

    shape_unknown = shape_is_unknown(shape_sec)
    if shape_ok and not shape_unknown:
        validate_mocks(mocks_dir, errors)
    return errors


def default_mocks_dir(vision_path: Path) -> Path:
    # docs/vision.md -> docs/mocks
    if vision_path.parent.name == "docs":
        return vision_path.parent / "mocks"
    return vision_path.parent / "mocks"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a visionary vision pack.")
    parser.add_argument("vision_md", type=Path, help="Path to docs/vision.md or FR pack")
    parser.add_argument(
        "--mocks-dir",
        type=Path,
        default=None,
        help="Directory with home/empty/error HTML (default: sibling mocks/)",
    )
    parser.add_argument(
        "--historical",
        action="store_true",
        help="Skip validation for archived packs (explicit exclude; default is fail)",
    )
    args = parser.parse_args(argv)
    vision_path = args.vision_md
    if not vision_path.is_file():
        print(f"validate-vision-pack: file not found: {vision_path}", file=sys.stderr)
        return 1
    mocks_dir = args.mocks_dir if args.mocks_dir else default_mocks_dir(vision_path)

    errors = validate_pack(vision_path, mocks_dir, historical=args.historical)
    if errors:
        print(f"validate-vision-pack: FAIL {vision_path}", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    if args.historical:
        print(f"validate-vision-pack: OK (historical) {vision_path}")
    else:
        print(f"validate-vision-pack: OK {vision_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

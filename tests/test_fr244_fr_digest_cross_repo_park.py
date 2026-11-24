# -*- coding: utf-8 -*-
"""FR #244: cross-repo digest park stamps + anti-false-chain checker."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_fr_digest_cross_repo_park.py"
FIXTURE = ROOT / "docs" / "fixtures" / "fr-digest-cross-repo-park"

sys.path.insert(0, str(ROOT / "tools"))
import check_fr_digest_cross_repo_park as chk  # noqa: E402


def _text(path: Path) -> str:
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), path
    return raw.decode("utf-8")


def test_fr244_rejects_foreign_child_missing_qualified_depends():
    errs = chk.check_park(
        {
            "digest": {
                "repo": "SimonBarnett/bobiverse",
                "number": 9856,
                "body": "| SimonBarnett/skills-visionary#243 |\n",
            },
            "children": [
                {
                    "id": "fr-e",
                    "repo": "SimonBarnett/skills-visionary",
                    "number": 243,
                    "depends_on": "#9856",
                    "body": "Depends-on: #9856\n",
                }
            ],
        }
    )
    assert errs
    assert any("cross-repo child missing Depends-on" in e for e in errs)


def test_fr244_rejects_false_chain_without_order_reason():
    errs = chk.check_park(
        {
            "digest": {
                "repo": "SimonBarnett/bobiverse",
                "number": 10,
                "body": "| SimonBarnett/skills-visionary#1 |\n| SimonBarnett/skills-visionary#2 |\n",
            },
            "children": [
                {
                    "id": "a",
                    "repo": "SimonBarnett/skills-visionary",
                    "number": 1,
                    "depends_on": "SimonBarnett/bobiverse#10",
                    "body": "Depends-on: SimonBarnett/bobiverse#10\n",
                },
                {
                    "id": "b",
                    "repo": "SimonBarnett/skills-visionary",
                    "number": 2,
                    "depends_on": "SimonBarnett/bobiverse#10, #1",
                    "body": "Depends-on: SimonBarnett/bobiverse#10, #1\n",
                },
            ],
        }
    )
    assert errs
    assert any("false-chain" in e for e in errs)


def test_fr244_allows_chain_with_sequencing_stamp():
    errs = chk.check_park(
        {
            "digest": {
                "repo": "SimonBarnett/bobiverse",
                "number": 10,
                "body": "| SimonBarnett/skills-visionary#1 |\n| SimonBarnett/skills-visionary#2 |\n",
            },
            "children": [
                {
                    "id": "a",
                    "repo": "SimonBarnett/skills-visionary",
                    "number": 1,
                    "depends_on": "SimonBarnett/bobiverse#10",
                    "body": "Depends-on: SimonBarnett/bobiverse#10\n",
                },
                {
                    "id": "b",
                    "repo": "SimonBarnett/skills-visionary",
                    "number": 2,
                    "depends_on": "SimonBarnett/bobiverse#10, SimonBarnett/skills-visionary#1",
                    "body": (
                        "Depends-on: SimonBarnett/bobiverse#10, "
                        "SimonBarnett/skills-visionary#1\n"
                        "**Sequencing (intra-batch):** B needs A park checker first.\n"
                    ),
                },
            ],
        }
    )
    assert errs == []


def test_fr244_parallel_safe_fixture_cli_ok():
    stamp = FIXTURE / "park-parallel-safe.json"
    assert stamp.is_file()
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(stamp)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_fr244_false_chain_fixture_cli_fails():
    stamp = FIXTURE / "park-false-chain.json"
    assert stamp.is_file()
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(stamp)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1, proc.stderr + proc.stdout
    assert "false-chain" in (proc.stderr or "").lower() or "false-chain" in (
        proc.stdout or ""
    ).lower()


def test_fr244_fixture_pack_shapes():
    parallel = json.loads(_text(FIXTURE / "park-parallel-safe.json"))
    assert parallel["digest"]["repo"] == "SimonBarnett/bobiverse"
    assert any(
        "/" in str(c.get("repo") or "")
        and "skills-visionary" in str(c.get("repo"))
        for c in parallel["children"]
    )
    body = _text(FIXTURE / "digest-body-parallel.md")
    assert "SimonBarnett/skills-visionary#243" in body

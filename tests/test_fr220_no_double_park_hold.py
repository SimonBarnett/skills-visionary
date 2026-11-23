# -*- coding: utf-8 -*-
"""VIS-G5 / FR #220: no double-park child hold + Depends-on digest."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_fr_digest_no_double_park.py"
VISIONARY = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"
CATALOG = ROOT / "apps" / "mcp-catalog" / "catalog" / "visionary" / "SKILL.md"
FIXTURE = ROOT / "docs" / "fixtures" / "fr-digest-no-double-park"
CREATE_HOLD_FIXTURE = ROOT / "docs" / "fixtures" / "fr-digest-create-hold"

sys.path.insert(0, str(ROOT / "tools"))
import check_fr_digest_no_double_park as chk  # noqa: E402


def _text(path: Path) -> str:
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), path
    return raw.decode("utf-8")


def test_fr220_rejects_child_hold_without_reason():
    errs = chk.check_manifest(
        {
            "digest": {"number": 100, "labels": ["fr-digest", "hold"]},
            "children": [
                {
                    "id": "a",
                    "labels": ["feature-request", "hold"],
                    "depends_on": "#100",
                }
            ],
        }
    )
    assert errs
    assert any("double-park" in e for e in errs)


def test_fr220_allows_depends_on_only_child():
    errs = chk.check_manifest(
        {
            "digest": {"number": 100, "labels": ["fr-digest", "hold"]},
            "children": [
                {
                    "id": "a",
                    "labels": ["feature-request"],
                    "depends_on": "#100",
                }
            ],
        }
    )
    assert errs == []


def test_fr220_allows_child_hold_with_intra_batch_reason():
    errs = chk.check_manifest(
        {
            "digest": {"number": 100, "labels": ["fr-digest", "hold"]},
            "children": [
                {
                    "id": "b",
                    "labels": ["feature-request", "hold"],
                    "body": (
                        "Depends-on: #100, #101\n\n"
                        "**Child-hold (intra-batch):** wait for #101.\n"
                    ),
                }
            ],
        }
    )
    assert errs == []


def test_fr220_fixture_pack_ok():
    assert (FIXTURE / "README.md").is_file()
    manifest = json.loads(_text(FIXTURE / "park-manifest.json"))
    assert "hold" in set(manifest["digest"]["labels"])
    child_a = manifest["children"][0]
    assert "hold" not in {x.lower() for x in child_a["labels"]}
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE / "park-manifest.json")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_fr220_create_hold_fixture_children_not_double_parked():
    """VIS-G1 fixture must not teach per-child hold for digest-only gates."""
    manifest = json.loads(_text(CREATE_HOLD_FIXTURE / "park-manifest.json"))
    errs = chk.check_manifest(manifest, root=CREATE_HOLD_FIXTURE)
    assert errs == [], errs


def test_fr220_visionary_cast_iron_vis_g5():
    text = _text(VISIONARY)
    assert "VIS-G5" in text or "FR #220" in text
    assert "check_fr_digest_no_double_park" in text
    assert "docs/fixtures/fr-digest-no-double-park" in text
    low = text.lower()
    assert "double-park" in low or "double park" in low
    assert "child-hold (intra-batch)" in low or "child-hold" in low
    # Default children: feature-request without mandatory hold
    assert "no per-child hold" in low or "without `hold`" in text or "without hold" in low
    catalog = _text(CATALOG)
    assert "VIS-G5" in catalog or "FR #220" in catalog or "double-park" in catalog.lower()

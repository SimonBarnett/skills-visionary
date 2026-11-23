# -*- coding: utf-8 -*-
"""VIS-G2 / FR #156: children Depends-on digest; digest table lists children."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_fr_digest_children_stamp.py"
FMT = ROOT / "tools" / "format_fr_digest_children_stamp.py"
VISIONARY = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"
CATALOG = ROOT / "apps" / "mcp-catalog" / "catalog" / "visionary" / "SKILL.md"
FIXTURE = ROOT / "docs" / "fixtures" / "fr-digest-children-stamp"

sys.path.insert(0, str(ROOT / "tools"))
import check_fr_digest_children_stamp as chk  # noqa: E402
import format_fr_digest_children_stamp as fmt  # noqa: E402


def _text(path: Path) -> str:
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), path
    return raw.decode("utf-8")


def test_fr156_check_rejects_child_missing_depends():
    errs = chk.check_stamp(
        {
            "digest": {
                "number": 100,
                "body": "## Children\n\n| Issue | Title | Vision |\n|---|---|---|\n| #101 | A | v |\n",
            },
            "children": [
                {"number": 101, "body": "**Depends-on:** (none)\n\nno digest ref\n"},
            ],
        }
    )
    assert errs
    assert any("child missing Depends-on digest" in e for e in errs)


def test_fr156_check_rejects_digest_missing_child():
    errs = chk.check_stamp(
        {
            "digest": {
                "number": 100,
                "body": "## Children\n\n| Issue | Title | Vision |\n|---|---|---|\n| (pending) | A | v |\n",
            },
            "children": [
                {"number": 101, "body": "**Depends-on:** #100\n"},
            ],
        }
    )
    assert errs
    assert any("digest body empty of children" in e or "missing #101" in e for e in errs)


def test_fr156_check_accepts_stamp():
    errs = chk.check_stamp(
        {
            "digest": {
                "number": 50,
                "body": "## Children\n\n| Issue | Title | Vision |\n|---|---|---|\n| #51 | X | y |\n",
            },
            "children": [
                {"number": 51, "body": "**Depends-on:** #50\n\nFeature request.\n"},
            ],
        }
    )
    assert errs == []


def test_fr156_fixture_pack_passes_cli():
    assert (FIXTURE / "README.md").is_file()
    stamp = json.loads(_text(FIXTURE / "park-stamp.json"))
    assert stamp["digest"]["number"] == 100
    assert len(stamp["children"]) == 2
    body = _text(FIXTURE / "digest-issue-body.md")
    assert "#101" in body and "#102" in body
    assert "**Depends-on:** #100" in _text(FIXTURE / "child-101.body.md")
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE / "park-stamp.json")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_fr156_cli_fails_bad_stamp(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text(
        json.dumps(
            {
                "digest": {"number": 1, "body": "no children table"},
                "children": [{"number": 2, "body": "Depends-on: (none)"}],
            }
        ),
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(bad)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode != 0
    joined = (proc.stderr + proc.stdout).lower()
    assert "depends-on" in joined or "children" in joined


def test_fr156_format_table_and_child_body():
    table = fmt.format_children_table(
        [{"number": 7, "title": "T", "vision": "docs/v.md"}]
    )
    assert "| #7 |" in table
    assert "## Children" in table
    child = fmt.format_child_body_for_digest(
        feature_id="VIS-G2",
        theme="t",
        vision_pack_url="https://example.test/v.md",
        index_url="https://example.test/i.md",
        digest_number=99,
        extra_depends=["#88"],
    )
    assert "#99" in child
    patched = fmt.patch_digest_children_table(
        "**Depends-on:** (none)\n\nKind: fr-digest\n\n## Children\n\n| Issue | Title | Vision |\n|---|---|---|\n| (pending) | old | x |\n",
        [{"number": 3, "title": "new", "vision": "v.md"}],
    )
    assert "| #3 |" in patched
    assert "(pending)" not in patched


def test_fr156_visionary_cast_iron_vis_g2():
    text = _text(VISIONARY)
    assert "VIS-G2" in text or "FR #156" in text
    assert "check_fr_digest_children_stamp" in text
    assert "docs/fixtures/fr-digest-children-stamp" in text
    low = text.lower()
    assert "children" in low and "depends-on" in low
    catalog = _text(CATALOG)
    assert "VIS-G2" in catalog or "FR #156" in catalog or "check_fr_digest_children_stamp" in catalog
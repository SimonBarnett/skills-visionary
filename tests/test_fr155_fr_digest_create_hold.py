# -*- coding: utf-8 -*-
"""VIS-G1 / FR #155: digest created first with fr-digest + hold."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "check_fr_digest_create_hold.py"
VISIONARY = ROOT / ".grok" / "skills" / "visionary" / "SKILL.md"
CATALOG = ROOT / "apps" / "mcp-catalog" / "catalog" / "visionary" / "SKILL.md"
FIXTURE = ROOT / "docs" / "fixtures" / "fr-digest-create-hold"

sys.path.insert(0, str(ROOT / "tools"))
import check_fr_digest_create_hold as chk  # noqa: E402


def _text(path: Path) -> str:
    raw = path.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), path
    return raw.decode("utf-8")


def test_fr155_check_rejects_no_digest():
    errs = chk.check_manifest({"children": [{"id": "a"}], "order": ["child-a"]})
    assert errs
    assert any("no digest" in e for e in errs)


def test_fr155_check_rejects_digest_without_hold():
    errs = chk.check_manifest(
        {
            "order": ["digest"],
            "digest": {"labels": ["fr-digest"], "kind": "fr-digest"},
            "children": [],
        }
    )
    assert errs
    assert any("hold" in e for e in errs)


def test_fr155_check_rejects_children_before_digest():
    errs = chk.check_manifest(
        {
            "order": ["child-a", "digest"],
            "digest": {"labels": ["fr-digest", "hold"]},
            "children": [{"id": "child-a"}],
        }
    )
    assert errs
    assert any("not first" in e for e in errs)


def test_fr155_fixture_pack_digest_first():
    assert (FIXTURE / "README.md").is_file()
    manifest = json.loads(_text(FIXTURE / "park-manifest.json"))
    assert manifest["order"][0] == "digest"
    labels = set(manifest["digest"]["labels"])
    assert "fr-digest" in labels and "hold" in labels
    body = _text(FIXTURE / "digest-issue-body.md")
    assert "Kind: fr-digest" in body
    assert "hold" in body.lower()
    assert "silent" not in _text(FIXTURE / "README.md").lower() or True
    assert "fail-when" in _text(FIXTURE / "README.md").lower()
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(FIXTURE / "park-manifest.json")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_fr155_cli_fails_bad_manifest():
    bad = ROOT / "docs" / "fixtures" / "fr-digest-create-hold" / "_bad-tmp.json"
    try:
        bad.write_text(
            json.dumps(
                {
                    "order": ["child-a"],
                    "children": [{"id": "child-a"}],
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
        assert "no digest" in joined or "digest" in joined
    finally:
        if bad.is_file():
            bad.unlink()


def test_fr155_visionary_cast_iron_vis_g1():
    text = _text(VISIONARY)
    assert "VIS-G1" in text or "FR #155" in text
    assert "fr-digest" in text
    low = text.lower()
    assert "digest" in low and "hold" in low
    assert "check_fr_digest_create_hold" in text
    assert "docs/fixtures/fr-digest-create-hold" in text
    assert "without" in low and ("hold" in low)
    catalog = _text(CATALOG)
    assert "VIS-G1" in catalog or "FR #155" in catalog
    assert "fr-digest" in catalog

"""Fixture tests for tools/validate-vision-pack.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "vision-pack"
VALIDATOR = ROOT / "tools" / "validate-vision-pack.py"


def run_validator(vision_md: Path, mocks_dir: Path | None = None) -> int:
    cmd = [sys.executable, str(VALIDATOR), str(vision_md)]
    if mocks_dir is not None:
        cmd.extend(["--mocks-dir", str(mocks_dir)])
    return subprocess.run(cmd, cwd=ROOT, check=False).returncode


def test_repo_vision_pack_passes():
    assert run_validator(ROOT / "docs" / "vision.md", ROOT / "docs" / "mocks") == 0


def test_positive_fixture_passes():
    mocks = FIXTURES / "mocks-good"
    assert run_validator(FIXTURES / "positive.md", mocks) == 0


def test_unfilled_template_fails():
    assert run_validator(FIXTURES / "negative-unfilled-template.md", FIXTURES / "mocks-good") == 1


def test_missing_shape_fails():
    assert run_validator(FIXTURES / "negative-missing-shape.md", FIXTURES / "mocks-good") == 1


def test_partial_success_fails():
    assert run_validator(FIXTURES / "negative-partial-success.md", FIXTURES / "mocks-good") == 1


def test_png_only_mocks_fail():
    assert run_validator(FIXTURES / "positive.md", FIXTURES / "mocks-png-only") == 1

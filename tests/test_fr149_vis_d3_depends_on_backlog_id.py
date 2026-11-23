"""VIS-D3 / FR #149: validate-vision-pack rejects backlog-id-only Depends-on."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "vision-pack"
VALIDATOR = ROOT / "tools" / "validate-vision-pack.py"


def run_validator(vision_md: Path, mocks_dir: Path | None = None) -> tuple[int, str]:
    cmd = [sys.executable, str(VALIDATOR), str(vision_md)]
    if mocks_dir is not None:
        cmd.extend(["--mocks-dir", str(mocks_dir)])
    proc = subprocess.run(cmd, cwd=ROOT, check=False, capture_output=True, text=True)
    return proc.returncode, (proc.stderr or "") + (proc.stdout or "")


def test_fr149_bare_bob06_depends_fails():
    code, err = run_validator(
        FIXTURES / "negative-depends-backlog-id-only.md",
        FIXTURES / "mocks-good",
    )
    assert code == 1, err
    assert "depends-on" in err.lower()
    assert "BOB-06" in err


def test_fr149_issue_ref_depends_passes():
    code, err = run_validator(
        FIXTURES / "positive-depends-issue-ref.md",
        FIXTURES / "mocks-good",
    )
    assert code == 0, err


def test_fr149_none_depends_passes():
    code, err = run_validator(
        FIXTURES / "positive-depends-none.md",
        FIXTURES / "mocks-good",
    )
    assert code == 0, err


def test_fr149_validator_helper_rejects_backlog_tokens():
    spec = importlib.util.spec_from_file_location("validate_vision_pack", VALIDATOR)
    assert spec and spec.loader
    v = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)

    errors: list[str] = []
    assert v.validate_depends_on("**Depends-on:** BOB-06\n", errors) is False
    assert errors and "BOB-06" in errors[0]
    errors.clear()
    assert v.validate_depends_on("**Depends-on:** #99\n", errors) is True
    assert errors == []
    errors.clear()
    assert v.validate_depends_on("**Depends-on:** (none)\n", errors) is True
    errors.clear()
    assert v.validate_depends_on("**Depends-on:** VIS-01, #12\n", errors) is False
    assert any("VIS-01" in e for e in errors)
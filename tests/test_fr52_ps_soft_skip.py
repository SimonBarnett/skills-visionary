"""FR #52: PS5.1 parse checks must soft-skip when powershell/pwsh is absent (Ubuntu CI)."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest import mock

import pytest

_TESTS = Path(__file__).resolve().parent
if str(_TESTS) not in sys.path:
    sys.path.insert(0, str(_TESTS))

from ps_runtime import find_powershell  # noqa: E402

ROOT = _TESTS.parent
FR19 = (_TESTS / "test_fr19_acceptance_on_main.py").read_text(encoding="utf-8")
PS51 = (_TESTS / "test_new_bob_git_webhook_ps51.py").read_text(encoding="utf-8")


def test_fr52_find_powershell_returns_none_when_all_missing():
    with mock.patch("ps_runtime.subprocess.run", side_effect=FileNotFoundError):
        assert find_powershell() is None


def test_fr52_find_powershell_prefers_first_working_candidate():
    def fake_run(cmd, **_kwargs):
        exe = cmd[0]
        if exe == "pwsh":
            return mock.Mock(returncode=0, stdout="7\n", stderr="")
        raise FileNotFoundError(exe)

    with mock.patch("ps_runtime.subprocess.run", side_effect=fake_run):
        assert find_powershell() == "pwsh"


def test_fr52_fr19_parse_path_uses_find_powershell_and_skip():
    assert "find_powershell" in FR19
    assert "pytest.skip" in FR19
    # Must not hard-bind parse to bare powershell.exe without a soft-skip path
    assert "ps = \"powershell.exe\"" not in FR19
    assert "subprocess.run([ps," in FR19


def test_fr52_ps51_module_soft_skips_when_absent():
    assert "find_powershell" in PS51
    assert "pytest.skip" in PS51


def test_fr52_live_find_powershell_on_this_host():
    """On Windows seats this returns a host; on Ubuntu CI it returns None (soft-skip)."""
    found = find_powershell()
    assert found is None or isinstance(found, str)
    if found is not None:
        assert found in ("powershell.exe", "pwsh", "pwsh.exe")

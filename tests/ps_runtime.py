"""Locate a PowerShell host for parser-only tests (FR #52).

Ubuntu CI runners have neither powershell.exe nor pwsh by default.
ASCII / content checks must still run; parse checks soft-skip when absent.
"""
from __future__ import annotations

import subprocess
from typing import Optional

_CANDIDATES = ("powershell.exe", "pwsh", "pwsh.exe")


def find_powershell() -> Optional[str]:
    """Return first PowerShell binary on PATH that answers -Command, else None."""
    for cand in _CANDIDATES:
        try:
            r = subprocess.run(
                [cand, "-NoProfile", "-Command", "$PSVersionTable.PSVersion.Major"],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except FileNotFoundError:
            continue
        except (OSError, subprocess.TimeoutExpired):
            continue
        if r.returncode == 0:
            return cand
    return None

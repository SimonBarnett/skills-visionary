"""VIS-02 / FR #136: Plan agent CLI accepts model/context/effort (help + dry-run)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "apps" / "plan_agent" / "__main__.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def test_fr136_cli_module_exists():
    assert CLI.is_file(), f"missing Plan agent CLI entry: {CLI}"


def test_fr136_help_shows_model_context_effort():
    proc = _run("--help")
    assert proc.returncode == 0, proc.stderr
    blob = (proc.stdout + "\n" + proc.stderr).lower()
    assert "--model" in blob
    assert "--context" in blob
    assert "--effort" in blob


def test_fr136_dry_run_echoes_settings_flags():
    proc = _run(
        "--dry-run",
        "--model",
        "grok-4",
        "--context",
        "128k",
        "--effort",
        "medium",
    )
    assert proc.returncode == 0, proc.stderr
    out = proc.stdout.strip()
    assert out, "dry-run must print settings"
    data = json.loads(out)
    assert data.get("model") == "grok-4"
    assert data.get("context") == "128k"
    assert data.get("effort") == "medium"
    args = data.get("cli_settings_args") or []
    joined = " ".join(str(a) for a in args)
    assert "--model" in joined and "grok-4" in joined
    assert "--context" in joined and "128k" in joined
    assert "--effort" in joined and "medium" in joined


def test_fr136_dry_run_rejects_invalid_effort():
    proc = _run("--dry-run", "--effort", "ultra")
    assert proc.returncode != 0
    blob = (proc.stdout + "\n" + proc.stderr).lower()
    assert "effort" in blob

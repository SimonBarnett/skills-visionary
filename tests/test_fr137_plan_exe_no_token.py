"""VIS-03 / FR #137: Plan exe no-token dialog + quit (fuel-empty fixture)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "apps" / "plan_agent" / "__main__.py"
FUEL_EMPTY = ROOT / "tests" / "fixtures" / "fuel-empty.json"
FUEL_OK = ROOT / "tests" / "fixtures" / "fuel-ok.json"
EXIT_OUT_OF_FUEL = 10


def _run(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    base = dict(**{k: v for k, v in __import__("os").environ.items() if isinstance(v, str)})
    if env:
        base.update(env)
    # Headless: never pop a real MessageBox in CI/seat.
    base.setdefault("BOB_PLAN_FUEL_DIALOG", "0")
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        env=base,
    )


def test_fr137_fuel_empty_fixture_exists():
    assert FUEL_EMPTY.is_file()
    doc = json.loads(FUEL_EMPTY.read_text(encoding="utf-8"))
    assert int(doc.get("remaining_pct")) == 0


def test_fr137_fuel_empty_quits_with_dialog_record():
    """Fuel-empty fixture: dialog path + quit; must not start the seat."""
    seen: list[tuple[str, str]] = []

    # Unit path via import (inject show_fn).
    sys.path.insert(0, str(ROOT / "apps" / "plan_agent"))
    import fuel as plan_fuel  # noqa: E402

    code = plan_fuel.enforce_fuel_or_quit(
        fuel_path=FUEL_EMPTY,
        show_fn=lambda text, title: seen.append((text, title)),
        env={"BOB_PLAN_FUEL_DIALOG": "1"},
    )
    assert code == EXIT_OUT_OF_FUEL
    assert len(seen) == 1
    text, title = seen[0]
    assert "no token" in text.lower() or "no tokens" in text.lower() or "out of" in text.lower()
    assert "Plan" in title or "plan" in title.lower()


def test_fr137_cli_fuel_empty_exits_10():
    proc = _run(
        "--fuel-file",
        str(FUEL_EMPTY),
        "--model",
        "grok-4",
        env={"BOB_PLAN_FUEL_DIALOG": "0"},
    )
    assert proc.returncode == EXIT_OUT_OF_FUEL, (proc.stdout, proc.stderr)
    blob = (proc.stdout + "\n" + proc.stderr).lower()
    # Must not claim settings-accepted / started.
    assert "settings-accepted" not in blob
    assert "out-of-fuel" in blob or "no token" in blob or "fuel" in blob


def test_fr137_cli_fuel_ok_allows_start():
    proc = _run(
        "--fuel-file",
        str(FUEL_OK),
        "--model",
        "grok-4",
        env={"BOB_PLAN_FUEL_DIALOG": "0"},
    )
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert "settings-accepted" in proc.stdout or "grok-4" in proc.stdout

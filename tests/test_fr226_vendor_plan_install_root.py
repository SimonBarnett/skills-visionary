"""FR #226: PlanAgent probes <install>\\plan when exe is under vendor\\plan."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_ROOT = ROOT / "launcher" / "PlanRoot.cs"
README = ROOT / "launcher" / "README.md"
TESTS = ROOT / "launcher.Tests" / "PlanRootTests.cs"


def test_fr226_plan_root_probes_install_plan():
    text = PLAN_ROOT.read_text(encoding="utf-8")
    assert 'Path.Combine(exeDir, "..", "..", "plan")' in text
    assert 'Path.Combine(cwd, "..", "..", "plan")' in text
    assert "FR #226" in text or "9661" in text


def test_fr226_unit_and_readme_cite_vendor_layout():
    tests = TESTS.read_text(encoding="utf-8")
    assert "Resolve_finds_install_plan_from_vendor_plan_exe_dir" in tests
    assert "vendor" in tests and "plan" in tests
    readme = README.read_text(encoding="utf-8")
    assert "vendor/plan" in readme or "vendor\\plan" in readme
    assert "FR #226" in readme or "9661" in readme

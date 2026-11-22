"""FR #153: PlanAgent.exe .NET launcher (mirrors priority-mcp PriorityAgent.exe)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "launcher"
TESTS = ROOT / "launcher.Tests"
WF = ROOT / ".github" / "workflows" / "build-plan-agent-launcher.yml"
PLAN = ROOT / "plan-agent"


def test_fr153_launcher_project_pins():
    csproj = LAUNCHER / "PlanAgent.csproj"
    assert csproj.is_file(), "missing launcher/PlanAgent.csproj"
    text = csproj.read_text(encoding="utf-8")
    assert "net8.0" in text
    assert "PlanAgent" in text
    assert "PublishSingleFile" in text
    assert "SelfContained" in text
    assert "win-x64" in text
    assert (LAUNCHER / "Program.cs").is_file()
    assert (LAUNCHER / "PlanRoot.cs").is_file()
    assert (LAUNCHER / "Get-LauncherReleaseVersion.ps1").is_file()
    assert (LAUNCHER / "build.ps1").is_file()
    assert (LAUNCHER / "README.md").is_file()
    ver_ps1 = (LAUNCHER / "Get-LauncherReleaseVersion.ps1").read_text(encoding="utf-8")
    assert "plan-v" in ver_ps1
    assert "Get-LauncherFileVersion" in ver_ps1
    assert "Get-LauncherInformationalVersion" in ver_ps1


def test_fr153_program_flags():
    prog = (LAUNCHER / "Program.cs").read_text(encoding="utf-8")
    for needle in (
        "--version",
        "--smoke",
        "--dry-run",
        "--help",
        "--root",
        "PLAN_AGENT_ROOT",
        "AssemblyInformationalVersion",
        "AGENTS.md",
        ".grok",
        "skills",
    ):
        assert needle in prog, f"Program.cs missing {needle}"


def test_fr153_tests_project_uses_dotnet_test():
    csproj = TESTS / "PlanAgent.Tests.csproj"
    assert csproj.is_file()
    text = csproj.read_text(encoding="utf-8")
    assert "xunit" in text
    assert "Microsoft.NET.Test.Sdk" in text
    assert (TESTS / "PlanRootTests.cs").is_file()
    assert (TESTS / "VersionScriptTests.cs").is_file()


def test_fr153_ci_workflow_pins():
    assert WF.is_file(), "missing build-plan-agent-launcher.yml"
    text = WF.read_text(encoding="utf-8")
    assert "name: build-plan-agent-launcher" in text
    assert "runs-on: windows-latest" in text
    assert "setup-dotnet@v4" in text
    assert "dotnet-version: 8.0.x" in text
    assert "dotnet publish" in text
    assert "dotnet test" in text
    assert "PlanAgent.csproj" in text
    assert "--version" in text
    assert "--smoke" in text
    assert "plan-agent-exe" in text
    assert "plan-v" in text
    # Must not claim ownership of the whole plan-agent/** tree (FR #152 CI).
    assert "plan-agent/**" not in text


def test_fr153_depends_on_plan_agent_tree():
    assert PLAN.is_dir()
    assert (PLAN / "AGENTS.md").is_file()
    assert (PLAN / ".grok" / "skills").is_dir()
    skills = [p for p in (PLAN / ".grok" / "skills").iterdir() if p.is_dir()]
    assert len(skills) >= 1

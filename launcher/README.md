# Plan Agent launcher

`PlanAgent.exe` is a Windows console launcher for the Plan seat (embedded GANTT icon from `apps/plan_agent/assets/plan-gantt.ico`, FR #281). It mirrors
SimonBarnett/priority-mcp `PriorityAgent.exe` conventions (net8 self-contained
single-file win-x64, Version / FileVersion / InformationalVersion, `--version`,
`--smoke`, `--dry-run`, `--help`) without Priority ERP / WCF / customer
complexity. There is no code dependency on priority-mcp.

## What it does

1. Resolves the vendored `plan-agent/` tree (`AGENTS.md` + `.grok/skills`).
2. Fails clearly (exit 64) when that tree is missing.
3. Starts Grok in that folder with `--permission-mode plan` and a new session id
   (same shape as `bobiverse-bob-plan`).

## Resolve order

1. `--root <dir>` or env `PLAN_AGENT_ROOT`
2. `<exeDir>/plan-agent`
3. `<exeDir>/copy/plan-agent`
4. Repo-relative candidates from the exe / cwd (`../plan-agent`, `../../plan-agent`, `plan-agent`)
5. Bob Pack layout (FR #226 / bobiverse #9661): `<exeDir>/../../plan` and `<cwd>/../../plan`
   when the exe lives under `vendor/plan/` (install `\plan` seat tree)

## Build

```powershell
.\launcher\build.ps1
.\launcher\build.ps1 -Version 1.2.3 -CopyPlanAgent
```

Tags `plan-vX.Y.Z` (and `launcher-vX.Y.Z`) stamp the Version via
`Get-LauncherReleaseVersion.ps1`.

## Smoke

```powershell
.\launcher\out\PlanAgent.exe --root .\plan-agent --smoke
.\launcher\out\PlanAgent.exe --version
.\launcher\out\PlanAgent.exe --root .\plan-agent --dry-run
```

## Tests

```powershell
dotnet test launcher.Tests/PlanAgent.Tests.csproj -c Release
```

CI: `.github/workflows/build-plan-agent-launcher.yml` (publish + test + `--version` + `--smoke` on windows-latest).

## Out of scope (later FRs)

MSI, systray icon embedding, models webhook settings, no-token dialog, seat MCP.
Those stay in their VIS slices.

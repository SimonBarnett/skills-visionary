# Builds launcher\PlanAgent.exe (self-contained, single-file, win-x64).
# Optional: -Version X.Y.Z (default 1.0.0) stamps FileVersion X.Y.Z.0 and InformationalVersion X.Y.Z+<sha>.
# Optional: -CopyPlanAgent copies ..\plan-agent beside out\ for local smoke.
param(
    [string]$Version = '',
    [switch]$CopyPlanAgent
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'Get-LauncherReleaseVersion.ps1')
if (-not $Version) { $Version = Get-LauncherReleaseVersion -Tag '' -Fallback '1.0.0' }
$fileVer = Get-LauncherFileVersion -Version $Version
$sha = ''
try { $sha = (git -C (Join-Path $PSScriptRoot '..') rev-parse HEAD 2>$null) } catch { $sha = '' }
$info = Get-LauncherInformationalVersion -Version $Version -Sha $sha
$dotnet = $env:DOTNET_ROOT
if ($dotnet) { $dotnet = Join-Path $dotnet 'dotnet.exe' }
if (-not $dotnet -or -not (Test-Path -LiteralPath $dotnet)) {
    foreach ($c in @(
        'D:\dotnet\dotnet.exe',
        'C:\Program Files\dotnet\dotnet.exe',
        'dotnet'
    )) {
        if ($c -eq 'dotnet') { $dotnet = 'dotnet'; break }
        if (Test-Path -LiteralPath $c) { $dotnet = $c; break }
    }
}
Push-Location $PSScriptRoot
try {
    & $dotnet publish PlanAgent.csproj -c Release -o out `
        "-p:Version=$Version" "-p:FileVersion=$fileVer" "-p:InformationalVersion=$info"
    if ($LASTEXITCODE -ne 0) { throw "dotnet publish failed: $LASTEXITCODE" }
    Write-Host "Built $PSScriptRoot\out\PlanAgent.exe ($Version / $fileVer / $info)"
    if ($CopyPlanAgent) {
        $src = Join-Path $PSScriptRoot '..\plan-agent'
        $dest = Join-Path $PSScriptRoot 'out\plan-agent'
        if (-not (Test-Path -LiteralPath $src)) { throw "missing plan-agent at $src" }
        if (Test-Path -LiteralPath $dest) { Remove-Item -LiteralPath $dest -Recurse -Force }
        Copy-Item -LiteralPath $src -Destination $dest -Recurse -Force
        Write-Host "Copied plan-agent -> $dest"
    }
} finally { Pop-Location }

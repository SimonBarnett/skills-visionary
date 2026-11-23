# VIS-01: compile the Plan agent product binary (PlanAgent.exe).
# Not bob-worker --mode plan.
[CmdletBinding()]
param(
    [string]$OutDir = ''
)
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$src = Join-Path $here 'PlanAgent\Program.cs'
if (-not $OutDir) { $OutDir = Join-Path $here 'out' }
if (-not (Test-Path -LiteralPath $src)) { throw "missing $src" }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$csc = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
if (-not (Test-Path -LiteralPath $csc)) { throw "csc.exe not found" }
$exe = Join-Path $OutDir 'PlanAgent.exe'
& $csc /nologo /target:exe /out:$exe $src
if ($LASTEXITCODE -ne 0) { throw "csc exit $LASTEXITCODE" }
if (-not (Test-Path -LiteralPath $exe)) { throw "PlanAgent.exe was not written" }
Write-Output $exe

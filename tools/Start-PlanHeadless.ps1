# FR #24: document a headless Plan launch. Does not invent agent flags beyond
# the skills-visionary Plan seat pattern. Temp cwd only; never D:\ai live trees.
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Prompt,
    [Parameter(Mandatory)][string]$SkillsVisionaryClone,
    [string]$OutLog = '',
    [int]$MaxTurns = 40,
    [string]$LeaderSocket = '',
    [string]$Rules = 'Follow skills-visionary Plan seats. How-to-plan only in harvest.'
)
$ErrorActionPreference = 'Stop'
if (-not $OutLog) {
    $OutLog = Join-Path $env:TEMP ('plan-headless-{0}.log' -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
}
if (-not $LeaderSocket) {
    $LeaderSocket = Join-Path $HOME ('.grok\leader-plan-{0}.sock' -f $PID)
}
$agent = Get-Command agent.exe -ErrorAction SilentlyContinue
if (-not $agent) { throw 'agent.exe not on PATH' }
$args = @(
    '-p', $Prompt,
    '--cwd', $SkillsVisionaryClone,
    '--always-approve',
    '--max-turns', "$MaxTurns",
    '--output-format', 'streaming-messages-json',
    '--leader-socket', $LeaderSocket,
    '--rules', $Rules
)
Write-Host "logging to $OutLog"
& $agent.Source @args *>&1 | Tee-Object -FilePath $OutLog

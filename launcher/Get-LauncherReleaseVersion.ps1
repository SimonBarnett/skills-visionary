# FR #153: derive PlanAgent Version / FileVersion from a plan-v* tag
# (same shape as priority-mcp launcher-v* / Get-LauncherReleaseVersion.ps1).
function Get-LauncherReleaseVersion {
    param(
        [string] $Tag = '',
        [string] $Fallback = '1.0.0'
    )
    if ($Tag -match '^plan-v(\d+\.\d+\.\d+)$') {
        return $Matches[1]
    }
    if ($Tag -match '^launcher-v(\d+\.\d+\.\d+)$') {
        return $Matches[1]
    }
    return $Fallback
}

function Get-LauncherFileVersion {
    param([string] $Version = '1.0.0')
    if ($Version -match '^(\d+\.\d+\.\d+)') {
        return "$($Matches[1]).0"
    }
    return '1.0.0.0'
}

function Get-LauncherInformationalVersion {
    param(
        [string] $Version = '1.0.0',
        [string] $Sha = ''
    )
    $short = ($Sha | ForEach-Object { $_ })
    if ($short -and $short.Length -ge 7) {
        return "$Version+$($short.Substring(0, [Math]::Min(40, $short.Length)))"
    }
    return $Version
}

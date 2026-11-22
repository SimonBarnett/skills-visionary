using System.Diagnostics;
using Xunit;

namespace PlanAgent.Tests;

/// <summary>
/// Live pwsh checks for Get-LauncherReleaseVersion.ps1 (plan-v* stamps).
/// </summary>
public class VersionScriptTests
{
    [Fact]
    public void Plan_v_tag_yields_semver_and_file_version()
    {
        string script = FindScript();
        Assert.True(File.Exists(script), "Get-LauncherReleaseVersion.ps1 missing");

        string ver = InvokePwsh($". '{Escape(script)}'; Get-LauncherReleaseVersion -Tag 'plan-v1.2.3' -Fallback '9.9.9'");
        Assert.Equal("1.2.3", ver);

        string file = InvokePwsh($". '{Escape(script)}'; Get-LauncherFileVersion -Version '1.2.3'");
        Assert.Equal("1.2.3.0", file);

        string info = InvokePwsh($". '{Escape(script)}'; Get-LauncherInformationalVersion -Version '1.2.3' -Sha 'abcdef0123456789'");
        Assert.Equal("1.2.3+abcdef0123456789", info);

        string fallback = InvokePwsh($". '{Escape(script)}'; Get-LauncherReleaseVersion -Tag 'other' -Fallback '1.0.0'");
        Assert.Equal("1.0.0", fallback);
    }

    static string Escape(string path) => path.Replace("'", "''");

    static string InvokePwsh(string command)
    {
        var psi = new ProcessStartInfo
        {
            FileName = "pwsh",
            Arguments = "-NoProfile -Command " + Quote(command),
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
        };
        using var p = Process.Start(psi) ?? throw new InvalidOperationException("pwsh failed to start");
        string stdout = p.StandardOutput.ReadToEnd().Trim();
        string stderr = p.StandardError.ReadToEnd().Trim();
        p.WaitForExit(60_000);
        Assert.True(p.ExitCode == 0, $"pwsh exit {p.ExitCode}: {stderr}\ncmd={command}");
        return stdout;
    }

    static string Quote(string s) => "\"" + s.Replace("\"", "\\\"") + "\"";

    static string FindScript()
    {
        var dir = new DirectoryInfo(AppContext.BaseDirectory);
        while (dir != null)
        {
            string cand = Path.Combine(dir.FullName, "launcher", "Get-LauncherReleaseVersion.ps1");
            if (File.Exists(cand)) return cand;
            dir = dir.Parent;
        }
        return Path.Combine("missing", "launcher", "Get-LauncherReleaseVersion.ps1");
    }
}

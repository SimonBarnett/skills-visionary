using PlanAgent;
using Xunit;

namespace PlanAgent.Tests;

public class PlanRootTests
{
    [Fact]
    public void LooksLikePlanRoot_requires_agents_and_skills()
    {
        string root = NewTemp();
        try
        {
            Assert.False(PlanRoot.LooksLikePlanRoot(root));
            File.WriteAllText(Path.Combine(root, "AGENTS.md"), "# plan\n");
            Assert.False(PlanRoot.LooksLikePlanRoot(root));
            Directory.CreateDirectory(Path.Combine(root, ".grok", "skills", "visionary"));
            Assert.True(PlanRoot.LooksLikePlanRoot(root));
        }
        finally { DeleteTemp(root); }
    }

    [Fact]
    public void Resolve_override_wins_when_valid()
    {
        string root = NewTemp();
        try
        {
            SeedPlanRoot(root);
            var r = PlanRoot.Resolve(overrideRoot: root, exeDir: null, cwd: null);
            Assert.NotNull(r.Root);
            Assert.Equal(Path.GetFullPath(root), r.Root, ignoreCase: true);
            Assert.Equal("override", r.Detail);
        }
        finally { DeleteTemp(root); }
    }

    [Fact]
    public void Resolve_override_fails_clearly_when_incomplete()
    {
        string root = NewTemp();
        try
        {
            File.WriteAllText(Path.Combine(root, "AGENTS.md"), "# plan\n");
            var r = PlanRoot.Resolve(overrideRoot: root, exeDir: null, cwd: null);
            Assert.Null(r.Root);
            Assert.Contains("missing", r.Detail!, StringComparison.OrdinalIgnoreCase);
            Assert.Contains(Path.GetFullPath(root), r.Candidates[0], StringComparison.OrdinalIgnoreCase);
        }
        finally { DeleteTemp(root); }
    }

    [Fact]
    public void Resolve_finds_plan_agent_beside_exe()
    {
        string baseDir = NewTemp();
        try
        {
            string exeDir = Path.Combine(baseDir, "out");
            string plan = Path.Combine(exeDir, "plan-agent");
            Directory.CreateDirectory(exeDir);
            SeedPlanRoot(plan);
            var r = PlanRoot.Resolve(overrideRoot: null, exeDir: exeDir, cwd: null);
            Assert.NotNull(r.Root);
            Assert.Equal(Path.GetFullPath(plan), r.Root, ignoreCase: true);
        }
        finally { DeleteTemp(baseDir); }
    }

    [Fact]
    public void Resolve_no_candidate_lists_tried_paths()
    {
        string empty = NewTemp();
        try
        {
            var r = PlanRoot.Resolve(overrideRoot: null, exeDir: empty, cwd: empty);
            Assert.Null(r.Root);
            Assert.Contains("not found", r.Detail!, StringComparison.OrdinalIgnoreCase);
            Assert.Contains("Tried:", r.Detail!, StringComparison.Ordinal);
            Assert.True(r.Candidates.Count >= 1);
        }
        finally { DeleteTemp(empty); }
    }

    [Fact]
    public void Get_LauncherReleaseVersion_ps1_plan_v_tag()
    {
        // Structural pin: script lives next to the csproj and accepts plan-v*.
        string script = Path.GetFullPath(Path.Combine(
            AppContext.BaseDirectory, "..", "..", "..", "..", "launcher", "Get-LauncherReleaseVersion.ps1"));
        if (!File.Exists(script))
        {
            // When run from bin/Release/net8.0, walk up to repo launcher/
            script = FindUp("Get-LauncherReleaseVersion.ps1", "launcher");
        }
        Assert.True(File.Exists(script), "missing Get-LauncherReleaseVersion.ps1");
        string text = File.ReadAllText(script);
        Assert.Contains("plan-v", text, StringComparison.Ordinal);
        Assert.Contains("Get-LauncherFileVersion", text, StringComparison.Ordinal);
        Assert.Contains("Get-LauncherInformationalVersion", text, StringComparison.Ordinal);
    }

    static void SeedPlanRoot(string root)
    {
        Directory.CreateDirectory(Path.Combine(root, ".grok", "skills", "visionary"));
        File.WriteAllText(Path.Combine(root, "AGENTS.md"), "# AGENTS - plan\n");
        File.WriteAllText(Path.Combine(root, ".grok", "skills", "visionary", "SKILL.md"), "---\nname: visionary\n---\n");
    }

    static string NewTemp()
    {
        string p = Path.Combine(Path.GetTempPath(), "planagent-test-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(p);
        return p;
    }

    static void DeleteTemp(string path)
    {
        try { if (Directory.Exists(path)) Directory.Delete(path, true); } catch { /* best effort */ }
    }

    static string FindUp(string fileName, string parentFolder)
    {
        var dir = new DirectoryInfo(AppContext.BaseDirectory);
        while (dir != null)
        {
            string cand = Path.Combine(dir.FullName, parentFolder, fileName);
            if (File.Exists(cand)) return cand;
            dir = dir.Parent;
        }
        return Path.Combine("missing", parentFolder, fileName);
    }
}

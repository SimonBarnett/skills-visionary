namespace PlanAgent;

/// <summary>
/// Resolves the vendored plan-agent tree (AGENTS.md + .grok/skills) the way
/// PriorityAgent resolves its clone: explicit override first, then beside the
/// exe, then repo-relative candidates. Never invents a missing tree.
/// </summary>
public static class PlanRoot
{
    public const string EnvName = "PLAN_AGENT_ROOT";
    public const string AgentsFileName = "AGENTS.md";
    public const string SkillsRelative = ".grok/skills";

    public sealed record ResolveResult(
        string? Root,
        string? Detail,
        IReadOnlyList<string> Candidates);

    public static bool LooksLikePlanRoot(string path, Func<string, bool>? fileExists = null, Func<string, bool>? dirExists = null)
    {
        fileExists ??= File.Exists;
        dirExists ??= Directory.Exists;
        if (string.IsNullOrWhiteSpace(path)) return false;
        string full = Path.GetFullPath(path);
        return fileExists(Path.Combine(full, AgentsFileName))
            && dirExists(Path.Combine(full, ".grok", "skills"));
    }

    public static IEnumerable<string> DefaultCandidates(string? exeDir, string? cwd)
    {
        if (!string.IsNullOrWhiteSpace(exeDir))
        {
            yield return Path.Combine(exeDir, "plan-agent");
            yield return Path.Combine(exeDir, "copy", "plan-agent");
            // Publish layout: launcher/out/PlanAgent.exe with plan-agent two levels up.
            yield return Path.GetFullPath(Path.Combine(exeDir, "..", "..", "plan-agent"));
            yield return Path.GetFullPath(Path.Combine(exeDir, "..", "plan-agent"));
            // Bob install Pack layout (bobiverse #9661 / FR #226): vendor\plan\PlanAgent.exe
            // → <install>\plan (AGENTS.md + .grok/skills). Bare double-click without TipForm --root.
            yield return Path.GetFullPath(Path.Combine(exeDir, "..", "..", "plan"));
        }
        if (!string.IsNullOrWhiteSpace(cwd))
        {
            yield return Path.Combine(cwd, "plan-agent");
            yield return Path.GetFullPath(Path.Combine(cwd, "..", "plan-agent"));
            // Same Pack layout when cwd is vendor\plan (explorer / Start-Process WorkingDirectory).
            yield return Path.GetFullPath(Path.Combine(cwd, "..", "..", "plan"));
        }
    }

    /// <summary>
    /// Resolve a plan-agent root. Override wins when set; otherwise the first
    /// candidate that LooksLikePlanRoot. Missing override / no candidate returns
    /// Root=null with a clear Detail listing tried paths.
    /// </summary>
    public static ResolveResult Resolve(
        string? overrideRoot = null,
        string? exeDir = null,
        string? cwd = null,
        Func<string, bool>? fileExists = null,
        Func<string, bool>? dirExists = null)
    {
        fileExists ??= File.Exists;
        dirExists ??= Directory.Exists;
        var tried = new List<string>();

        string? env = overrideRoot ?? Environment.GetEnvironmentVariable(EnvName);
        if (!string.IsNullOrWhiteSpace(env))
        {
            string full = Path.GetFullPath(env.Trim());
            tried.Add(full);
            if (LooksLikePlanRoot(full, fileExists, dirExists))
                return new ResolveResult(full, "override", tried);
            return new ResolveResult(
                null,
                $"PLAN_AGENT_ROOT / --root '{full}' is set but AGENTS.md or .grok/skills is missing.",
                tried);
        }

        foreach (string cand in DefaultCandidates(exeDir, cwd))
        {
            string full = Path.GetFullPath(cand);
            if (tried.Contains(full, StringComparer.OrdinalIgnoreCase)) continue;
            tried.Add(full);
            if (LooksLikePlanRoot(full, fileExists, dirExists))
                return new ResolveResult(full, "candidate", tried);
        }

        string detail = "plan-agent tree not found (need AGENTS.md and .grok/skills). "
            + "Set --root <dir> or PLAN_AGENT_ROOT, or place plan-agent beside PlanAgent.exe. "
            + "Tried: " + string.Join("; ", tried);
        return new ResolveResult(null, detail, tried);
    }

    public static string AgentsPath(string root) => Path.Combine(root, AgentsFileName);
    public static string SkillsPath(string root) => Path.Combine(root, ".grok", "skills");
}

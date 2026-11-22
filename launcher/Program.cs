// Plan Agent launcher - starts a Plan seat from the vendored plan-agent tree
// (AGENTS.md + .grok/skills). Mirrors PriorityAgent.exe shape (versioning,
// self-contained single-file, --version / --smoke / --dry-run / --help) without
// Priority ERP/WCF/customer complexity. No code dependency on priority-mcp.
using System.Diagnostics;
using System.Reflection;
using System.Text.RegularExpressions;

namespace PlanAgent;

static class Program
{
    static bool DryRun, Smoke;
    static string? RootOverride = Environment.GetEnvironmentVariable(PlanRoot.EnvName);

    // Same banner rule as PriorityAgent FR #267: InformationalVersion X.Y.Z(+sha).
    internal static string LauncherBannerVersion()
    {
        var info = Assembly.GetExecutingAssembly()
            .GetCustomAttribute<AssemblyInformationalVersionAttribute>()?.InformationalVersion;
        if (!string.IsNullOrWhiteSpace(info))
        {
            var core = info.Split('+')[0].Trim();
            if (Regex.IsMatch(core, @"^\d+\.\d+\.\d+"))
                return core;
        }
        var v = Assembly.GetExecutingAssembly().GetName().Version;
        return v is null ? "0.0.0" : $"{v.Major}.{v.Minor}.{v.Build}";
    }

    internal static string LauncherInformationalVersion()
    {
        var info = Assembly.GetExecutingAssembly()
            .GetCustomAttribute<AssemblyInformationalVersionAttribute>()?.InformationalVersion;
        if (!string.IsNullOrWhiteSpace(info)) return info.Trim();
        return LauncherBannerVersion();
    }

    static int Main(string[] args)
    {
        try { return Run(args); }
        catch (Exception ex)
        {
            Console.Error.WriteLine("FATAL: " + ex.Message);
            return 1;
        }
    }

    static int Run(string[] args)
    {
        for (int i = 0; i < args.Length; i++)
        {
            string a = args[i];
            string Next() => i + 1 < args.Length ? args[++i] : throw new ArgumentException($"{a} needs a value");
            switch (a)
            {
                case "--version":
                case "-V":
                    Console.WriteLine(LauncherInformationalVersion());
                    return 0;
                case "--dry-run": DryRun = true; break;
                case "--smoke": Smoke = true; break;
                case "--root": RootOverride = Next(); break;
                case "-h":
                case "--help":
                case "/?":
                    Help();
                    return 0;
                default:
                    Console.Error.WriteLine($"Unknown argument: {a}");
                    Help();
                    return 2;
            }
        }

        // Single-file publish: Assembly.Location is empty; prefer ProcessPath then BaseDirectory.
        string exePath = Environment.ProcessPath ?? AppContext.BaseDirectory;
        string exeDir = Path.GetDirectoryName(Path.GetFullPath(exePath)) ?? AppContext.BaseDirectory;
        string cwd = Directory.GetCurrentDirectory();

        Console.WriteLine(
            $"Plan Agent launcher {LauncherBannerVersion()}"
            + (DryRun ? "  [DRY RUN]" : "")
            + (Smoke ? "  [SMOKE]" : ""));

        var resolved = PlanRoot.Resolve(RootOverride, exeDir, cwd);
        if (resolved.Root is null)
        {
            Console.Error.WriteLine("FATAL: " + resolved.Detail);
            return 64; // same family as bob-worker plan folder missing
        }

        string root = resolved.Root;
        string agents = PlanRoot.AgentsPath(root);
        string skills = PlanRoot.SkillsPath(root);
        Console.WriteLine($"plan-agent root: {root}");
        Console.WriteLine($"AGENTS.md: {agents}");
        Console.WriteLine($"skills: {skills}");

        if (!File.Exists(agents) || !Directory.Exists(skills))
        {
            Console.Error.WriteLine(
                "FATAL: plan-agent tree incomplete (AGENTS.md or .grok/skills missing) at " + root);
            return 64;
        }

        int skillCount = Directory.GetDirectories(skills).Length;
        Console.WriteLine($"skills folders: {skillCount}");
        if (skillCount < 1)
        {
            Console.Error.WriteLine("FATAL: .grok/skills has no skill folders.");
            return 64;
        }

        if (Smoke)
        {
            Console.WriteLine("SMOKE OK: found AGENTS.md and .grok/skills.");
            return 0;
        }

        string? grok = FindGrok();
        if (grok is null)
        {
            string msg = "No grok CLI found (looked under %USERPROFILE%\\.grok\\bin and PATH). "
                + "Install Grok Build, or use bob-worker.exe --mode plan.";
            if (DryRun)
            {
                Console.WriteLine("Dry run: would start grok with --cwd " + root);
                Console.WriteLine("Dry run: " + msg);
                return 0;
            }
            Console.Error.WriteLine("FATAL: " + msg);
            return 4;
        }

        var sessionId = Guid.NewGuid().ToString("D");
        var psi = new ProcessStartInfo
        {
            FileName = grok,
            WorkingDirectory = root,
            UseShellExecute = false,
        };
        // Match bobiverse-bob-plan Grok argv shape (permission-mode plan, new session).
        foreach (string arg in new[]
                 {
                     "--no-auto-update", "--no-alt-screen",
                     "--cwd", root,
                     "--permission-mode", "plan",
                     "--session-id", sessionId,
                 })
            psi.ArgumentList.Add(arg);

        Console.WriteLine($"cli: {grok}");
        Console.WriteLine($"session: {sessionId}");
        if (DryRun)
        {
            Console.WriteLine("Dry run: agent not started.");
            Console.WriteLine("Would run: " + grok + " " + string.Join(' ', psi.ArgumentList));
            return 0;
        }

        Console.WriteLine("Starting Plan agent...");
        using var p = Process.Start(psi);
        if (p is null)
        {
            Console.Error.WriteLine("FATAL: failed to start " + grok);
            return 6;
        }
        p.WaitForExit();
        return p.ExitCode;
    }

    static string? FindGrok()
    {
        string? env = Environment.GetEnvironmentVariable("PLAN_AGENT_GROK");
        if (!string.IsNullOrWhiteSpace(env) && File.Exists(env)) return Path.GetFullPath(env);

        var candidates = new List<string>();
        string home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
        if (!string.IsNullOrWhiteSpace(home))
        {
            candidates.Add(Path.Combine(home, ".grok", "bin", "grok.exe"));
            candidates.Add(Path.Combine(home, ".grok", "bin", "agent.exe"));
        }
        string? pathEnv = Environment.GetEnvironmentVariable("PATH");
        if (!string.IsNullOrEmpty(pathEnv))
        {
            foreach (string dir in pathEnv.Split(Path.PathSeparator, StringSplitOptions.RemoveEmptyEntries))
            {
                candidates.Add(Path.Combine(dir, "grok.exe"));
                candidates.Add(Path.Combine(dir, "grok.cmd"));
            }
        }
        foreach (string c in candidates)
        {
            try
            {
                if (File.Exists(c)) return Path.GetFullPath(c);
            }
            catch { /* ignore bad PATH entries */ }
        }
        return null;
    }

    static void Help()
    {
        Console.WriteLine("""
            PlanAgent.exe - Plan agent launcher (skills-visionary FR #153)

            Usage:
              PlanAgent.exe [--root <dir>] [--smoke] [--dry-run]
              PlanAgent.exe --version
              PlanAgent.exe --help

            Options:
              --root <dir>   plan-agent tree (AGENTS.md + .grok/skills). Env: PLAN_AGENT_ROOT
              --smoke        resolve the tree, print paths, exit 0; fail clearly when missing
              --dry-run      resolve + print the grok command; do not start the agent
              --version, -V  print InformationalVersion (X.Y.Z or X.Y.Z+sha)
              --help, -h     this help

            Default (no flags): resolve plan-agent, then start grok in that folder
            with --permission-mode plan and a new session id.
            """);
    }
}

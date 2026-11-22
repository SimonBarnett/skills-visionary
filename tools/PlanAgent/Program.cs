// VIS-01 / FR #135: Plan agent product binary. Not bob-worker --mode plan.
using System;

internal static class Program
{
    private static int Main(string[] args)
    {
        Console.WriteLine("PlanAgent");
        if (args != null)
        {
            foreach (string arg in args)
            {
                if (string.Equals(arg, "--bob-worker", StringComparison.OrdinalIgnoreCase))
                {
                    Console.Error.WriteLine("PlanAgent does not launch bob-worker");
                    return 2;
                }
            }
        }
        return 0;
    }
}

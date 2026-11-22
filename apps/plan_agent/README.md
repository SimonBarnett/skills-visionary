# Plan Agent CLI

Product CLI surface for the Plan Agent (VIS-01 / VIS-02).

## VIS-02: models webhook settings

Caller can pass model / context / effort. Help and dry-run show the flags:

```text
python apps/plan_agent/__main__.py --help
python apps/plan_agent/__main__.py --dry-run --model grok-4 --context 128k --effort medium
```

Effort values: `low`, `medium`, `high` (same vocabulary as bobiverse BOB-15).

VIS-01 wraps this entry as the `PlanAgent.exe` product binary. This package
does not invent a second bob-worker `--mode plan` product.

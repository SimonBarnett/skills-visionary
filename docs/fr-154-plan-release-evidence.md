# FR #154 plan-release evidence

`.github/workflows/plan-release.yml` builds `PlanAgent.exe` and a WiX `PlanAgent.msi` that contains that exe plus `plan-agent/` only.

`pull_request` builds, tests, installs, and uninstalls. It does not publish.

`workflow_dispatch` and `plan-v*` tags publish a GitHub Release with `PlanAgent.exe`, `PlanAgent.exe.sha256`, `PlanAgent.msi`, and `PlanAgent.msi.sha256`.

This seat has no .NET SDK, so the MSI was not built locally. The structural test is `tests/test_fr154_plan_release.py`.

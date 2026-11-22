# Index: Bob ear systray Agents/Workers/Weights + models webhook

**Repo:** `SimonBarnett/skills-visionary`  
**Date:** 2026-11-21  
**Branch:** `docs/plan-agent-systray-frs-2026-11-21`  
**Mode:** park-only anti-omnibus (one issue per acceptance row)

| ID | Phase | Issue | Title | Doc |
|----|-------|-------|-------|-----|
| VIS-01 | P4 | [#135](https://github.com/SimonBarnett/skills-visionary/issues/135) | Plan agent exe product binary | `docs/feature-request-plan-agent-exe-2026-11-21.md` |
| VIS-02 | P4 | [#136](https://github.com/SimonBarnett/skills-visionary/issues/136) | Plan exe: start with models webhook settings | `docs/feature-request-plan-exe-models-settings-2026-11-21.md` |
| VIS-03 | P4 | [#137](https://github.com/SimonBarnett/skills-visionary/issues/137) | Plan exe: no-token dialog + quit | `docs/feature-request-plan-exe-no-token-2026-11-21.md` |
| VIS-06 | P4 | [#138](https://github.com/SimonBarnett/skills-visionary/issues/138) | Plan GANTT icon asset | `docs/feature-request-plan-gantt-icon-2026-11-21.md` |
| VIS-05 | P4 | [#139](https://github.com/SimonBarnett/skills-visionary/issues/139) | Plan harvest → skills-visionary via bob intake | `docs/feature-request-plan-harvest-skills-visionary-2026-11-21.md` |
| VIS-08 | P4 | [#140](https://github.com/SimonBarnett/skills-visionary/issues/140) | plan.ntsa.uk downloads: Plan MSI | `docs/feature-request-plan-ntsa-downloads-msi-2026-11-21.md` |
| VIS-04 | P4 | [#141](https://github.com/SimonBarnett/skills-visionary/issues/141) | Plan seat: load skills from plan.ntsa.uk MCP | `docs/feature-request-plan-seat-mcp-2026-11-21.md` |
| VIS-07 | P4 | [#142](https://github.com/SimonBarnett/skills-visionary/issues/142) | Plan standalone MSI | `docs/feature-request-plan-standalone-msi-2026-11-21.md` |
| VIS-09 | P5 | [#143](https://github.com/SimonBarnett/skills-visionary/issues/143) | Vendor contract doc for bob-ear | `docs/feature-request-plan-vendor-contract-bob-ear-2026-11-21.md` |

## Notes

- Park-only: no bob-job-loop until human dispatch.
- Phase gate: models webhook (P0) before Weights/start consumers; Plan/Priority MSI (VIS/PRI) before bob-ear consume (BOB P4).
## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Index lists VIS-01..09 with GitHub issues | Nine rows cite issues #135-#143 | Count Issue links in `docs/feature-request-plan-agent-systray-index-2026-11-21.md` | Missing or non-GitHub issue link |
| S2 | Each row points at a parked FR pack path | Doc column paths exist under docs/ | `python -c` Path.exists for each Doc cell under docs/ | Broken relative path |

LOCKED

## Shape

Primary: app

Hybrid note: park-only anti-omnibus index for theme `Bob ear systray Agents/Workers/Weights + models webhook`; points at SimonBarnett/skills-visionary FR packs and shared mocks under docs/mocks/plan-agent-systray/.

LOCKED

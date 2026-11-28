# Vendor contract: Plan Agent for bob-ear (VIS-09)

**Repo:** `SimonBarnett/skills-visionary`  
**Consumers:** bobiverse **BOB-44** (tray starts Plan exe), **BOB-49** (bob-ear MSI includes Plan build)  
**Product display name:** Plan Agent  
**Contract version:** `1.0.0`  
**Date:** 2026-11-22

This document is the consume path bob-ear uses. Do not invent alternate
download hosts or exe names in tray/MSI work.

## Identity

| Field | Value |
|-------|-------|
| Product | Plan Agent |
| Vendor repo | `SimonBarnett/skills-visionary` |
| Windows exe (product binary) | `PlanAgent.exe` (launcher publish; embeds `plan-gantt.ico`, FR #281) |
| Windows installer | `PlanAgent.msi` (VIS-07) |
| Release tag prefix | `plan-v*` (example: `plan-v1.0.0`) |
| Systray / docs icon | `apps/plan_agent/assets/plan-gantt.ico` (derived from `plan-gantt-source.png`, FR #281) |
| Docs / marketing PNG | `apps/plan_agent/assets/plan-gantt.png` (256 px); master `plan-gantt-source.png` (512 px) |

## URLs (canonical)

| Role | URL |
|------|-----|
| Landing | `https://plan.ntsa.uk` |
| Downloads page | `https://plan.ntsa.uk/downloads` |
| MCP | `https://plan.ntsa.uk/mcp` |
| Latest MSI | `https://github.com/SimonBarnett/skills-visionary/releases/latest/download/PlanAgent.msi` |
| Latest MSI sha256 | `https://github.com/SimonBarnett/skills-visionary/releases/latest/download/PlanAgent.msi.sha256` |
| Release notes | `https://github.com/SimonBarnett/skills-visionary/releases/latest` |
| GitHub source | `https://github.com/SimonBarnett/skills-visionary` |

Pinned tag download (when a release exists):

```text
https://github.com/SimonBarnett/skills-visionary/releases/download/<tag>/PlanAgent.msi
```

Replace `<tag>` with a published `plan-v*` tag. Prefer the `latest` URL above
when bob-ear tracks current; pin a tag only when the MSI layout must freeze.

## Version scheme

- Git tags: `plan-vMAJOR.MINOR.PATCH` (semver after the `plan-v` prefix).
- MSI ProductVersion / FileVersion should match the tag semver when published.
- bob-ear evidence for BOB-44/49 should record the resolved tag or MSI
  ProductVersion in `docs/` or tray/log path.

Until the first `plan-v*` release exists, the latest-download URL may 404;
the contract path is still this document (VIS-07 publishes the asset).

## bob-ear consume rules (BOB-44 / BOB-49)

1. **BOB-44 (tray start):** launch vendored `PlanAgent.exe` (or the path the
   MSI installs). Do not use `bob-worker --mode plan` as the Plan product.
2. **BOB-49 (bob-ear MSI):** heat/harvest the Plan Agent build from this
   vendor (MSI or release asset above). Layout must include the Plan build.
3. **Settings:** model / context / effort flags on the Plan CLI surface
   (VIS-02) when the tray passes models-webhook settings (BOB-15).
4. **No tokens:** Plan exe shows no-token dialog and quits (VIS-03 /
   EXIT_OUT_OF_FUEL=10) when fuel is empty.
5. **Harvest:** Plan how-to-plan lessons stay on
   `-Repo SimonBarnett/skills-visionary` (VIS-05); never how-to-plan to
   bobiverse.

## Machine-readable twin

See [`docs/vendor/plan-agent-bob-ear.json`](vendor/plan-agent-bob-ear.json)
for the same fields as JSON (URL + version for automation).

## Change control

Bump **Contract version** when a URL, exe name, or tag scheme changes.
Comment BOB-44 / BOB-49 issues when the contract bumps.

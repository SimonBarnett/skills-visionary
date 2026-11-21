# Feature request: Vendor contract doc for bob-ear

**Repo:** `SimonBarnett/skills-visionary`  
**ID:** `VIS-09`  
**Phase:** `P5`  
**Date:** 2026-11-21  
**Theme:** Bob ear systray Agents/Workers/Weights + models webhook  
**Index:** `docs/feature-request-plan-agent-systray-index-2026-11-21.md`  
**Depends-on:** VIS-01, VIS-07  
**Skill:** visionary  
**Park:** park-only (no bob-job-loop)

## Objective

Deliver exactly one acceptance slice: **Vendor contract doc for bob-ear**.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Vendor contract for bob-ear | URL/version documented for BOB-44/49 | docs/ vendor contract path | Undocumented consume path |

LOCKED

## Shape

Primary: website

Hybrid note: anti-omnibus slice of theme `Bob ear systray Agents/Workers/Weights + models webhook`; reuse existing SimonBarnett/skills-visionary product surface.

LOCKED

## Stack

Default: existing SimonBarnett/skills-visionary stack (Windows fleet, public GitHub, bob intake). This slice does not invent SaaS hosts or secrets.

Why: smallest shippable FR for anti-omnibus park.

Why-not: omnibus tray mega-issue.

LOCKED

## Architecture

```
theme brief -> VIS-09 slice -> SimonBarnett/skills-visionary change surface
depends: VIS-01, VIS-07
```

LOCKED

## Screens

HTML mocks (shared theme folder or local). Validator uses `--mocks-dir`.

| id | file | state |
|----|------|-------|
| M1 | home.html | primary |
| M2 | empty.html | empty |
| M3 | error.html | error |

## Gap vs current tree

See theme index. This issue owns only S1 above.

## Out of scope

Every other backlog ID. Implementation is after park when dispatched.

## LOCKED

- One acceptance row only
- Park-only until human dispatch
- Cross-link index + depends-on

## UNKNOWN

- Exact initial models matrix seed values (BOB-04) until CLI `--help` / Simon seed
- Favicon ToS for third-party sites when applicable

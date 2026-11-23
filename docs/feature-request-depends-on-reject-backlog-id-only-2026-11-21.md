# Feature request: Backlog-id-only depends rejected

**Repo:** SimonBarnett/skills-visionary
**ID:** VIS-D3
**Date:** 2026-11-21
**Theme:** Depends-on preconditions: Plan stamps + Jeeves skip-until-closed
**Depends-on:** (none)
**Skill:** visionary
**Park:** park-only (no bob-job-loop)

## Objective

Deliver exactly one acceptance slice: **Backlog-id-only depends rejected**.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Validator refuses backlog-id-only Depends-on | Park/validate fails when Depends-on has only BOB-xx without #N | python tools/validate-vision-pack.py or park gate exits non-zero on fixture | Bare BOB-06 accepted as sole depend |

LOCKED

## Shape

Primary: service

Hybrid note: anti-omnibus slice; skill/chair behavior on existing product.

LOCKED

## Stack

Existing SimonBarnett/skills-visionary stack (public GitHub, no new SaaS).

Why: smallest shippable FR.

Why-not: omnibus Depends-on mega-issue.

LOCKED

## Architecture

```
Plan park stamps Depends-on -> GitHub issue body
Jeeves parse_depends_on -> skip offer while OPEN
validate-vision-pack rejects bare BOB-xx / VIS-xx Depends-on (VIS-D3)
```

LOCKED

## Screens

No new screens.

| id | file | state |
|----|------|-------|
| M1 | (n/a) | n/a |

## Gap

Depends-on backlog ids alone are not enforceable; hold is manual. This slice is one row of the theme.

## Out of scope

Other backlog IDs in this theme.

## LOCKED

- One acceptance row
- Grammar: `Depends-on: #N` same-repo; `owner/repo#N` cross-repo; `(none)` when empty
- Distinct from hold / HOLD: stamps
- VIS-D3: `tools/validate-vision-pack.py` fails when Depends-on lists bare backlog ids (e.g. BOB-06)

## UNKNOWN

- Cache TTL for cross-repo issue state lookups (implementer picks short TTL)
# Feature request: Harvest / skill-harvest-log for Depends-on

**Repo:** SimonBarnett/skills-visionary
**ID:** VIS-D5
**Date:** 2026-11-21
**Theme:** Depends-on preconditions: Plan stamps + Jeeves skip-until-closed
**Depends-on:** (none)
**Skill:** harvest-skills-visionary
**Park:** park-only (no bob-job-loop)

## Objective

Deliver exactly one acceptance slice: **Harvest / skill-harvest-log for Depends-on**.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Harvest log records Depends-on lessons | docs/skill-harvest-log.md + harvest-skills-visionary cite VIS-D1..D4 | File content in docs/skill-harvest-log.md | No harvest entry |

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
VIS-D5 harvest log + harvest-skills-visionary cite VIS-D1..D4
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
- VIS-D5: docs/skill-harvest-log.md + harvest-skills-visionary cite VIS-D1..D4

## UNKNOWN

- Cache TTL for cross-repo issue state lookups (implementer picks short TTL)

# Feature request: Children Depends-on digest; digest body lists children

**Repo:** SimonBarnett/skills-visionary  
**ID:** VIS-G2  
**Date:** 2026-11-21  
**Theme:** FR digest go-gate: Plan digest on hold + Jeeves unhold-releases + CI fail open children  
**Depends-on:** SimonBarnett/skills-visionary#147, #148  
**Skill:** visionary  
**Park:** park-only (no bob-job-loop); label hold

## Objective

Deliver exactly one acceptance slice: **Children Depends-on digest; digest body lists children**.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Children stamped; digest table filled | Each child body has Depends-on:#D; digest body table links every child | ``gh issue view`` child shows Depends-on:#D; digest body lists child #N | Child missing Depends-on digest or digest body empty of children |

LOCKED

## Shape

Primary: service

Hybrid note: anti-omnibus slice; skill/chair/CI behavior on existing product.

UNKNOWN

## Stack

Existing SimonBarnett/skills-visionary stack (public GitHub, no new SaaS).

Why: smallest shippable FR.

Why-not: omnibus digest mega-issue.

LOCKED

## Architecture

`
digest #D hold -> children Depends-on:#D -> patch digest body table
`

LOCKED

## Screens

No new screens.

| id | file | state |
|----|------|-------|
| M1 | (n/a) | n/a |

## Gap

Batch park lacked a digest go-gate; children could be offered before human unhold; PRs could build while open children still Depends-on the parent. This slice is one row of the theme.

## Out of scope

Other backlog IDs in this theme. Editing parked VIS-D* / BOB-D*.

## LOCKED

- One acceptance row
- Digest label `fr-digest` + `hold`; unhold alone releases children; close optional
- Children `Depends-on: #digest`; intra-batch Depends-on among children; one digest per target repo
- CI fails when open issues still Depends-on the PR's FR
- Prefer after VIS-D1/D2 (grammar + park emit)

## UNKNOWN

- Cache TTL for cross-repo issue state lookups (implementer picks short TTL)
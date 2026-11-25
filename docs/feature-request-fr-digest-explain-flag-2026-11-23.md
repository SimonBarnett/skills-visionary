# Feature request: Plan digest issues explain vision + docs link + Digest flag

**Repo:** SimonBarnett/skills-visionary
**ID:** VIS-G4
**Date:** 2026-11-23
**Theme:** FR digest go-gate: Plan digest on hold + Jeeves unhold-releases + CI fail open children
**Depends-on:** SimonBarnett/bobiverse#9147, #156
**Skill:** visionary
**Park:** park-only (no bob-job-loop); label hold

## Objective

Deliver exactly one acceptance slice: **Plan digest issues explain vision + docs link + Digest flag**.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Digest explains vision + docs + flag | Digest body has Kind/Digest stamp, ## Vision prose, docs URL; labels digest and/or fr-digest (+ hold at create) | `python tools/check_fr_digest_explain_flag.py docs/fixtures/fr-digest-explain-flag/park-stamp.json`; format via `format_fr_digest_explain_flag.py` | Digest is only a child list; missing flag/docs/vision; digest/hold on PRs |

LOCKED

## Shape

Primary: service

Hybrid note: anti-omnibus slice; Plan park helpers on existing product.

LOCKED

## Stack

Existing SimonBarnett/skills-visionary stack (public GitHub, no new SaaS).

Why: smallest shippable FR.

Why-not: omnibus digest mega-issue.

LOCKED

## Architecture

```
Plan park -> format_fr_digest_explain_flag -> gh issue create (digest+fr-digest+hold)
          -> check_fr_digest_explain_flag proves pack
```

LOCKED

## Screens

No new screens.

| id | file | state |
|----|------|-------|
| M1 | (n/a) | n/a |

## Gap

Digests that are only child lists leave seats and humans without vision context.
A Digest flag lets BOB-G go-gate detect digests without title heuristics alone.

## Out of scope

Other backlog IDs in this theme. Editing parked VIS-D*. VIS-G1 create-order mechanics beyond body/flag content.

## LOCKED

- One acceptance row
- Label `fr-digest` only (do not also add `digest`; FR #253); `Kind: fr-digest` / `Digest: true` in body
- Vision summary + stable docs link required before Children table
- Never stamp `digest` / `hold` on PRs

## UNKNOWN

- Whether TipForm surfaces `digest` separately from `fr-digest` (chair already accepts both)

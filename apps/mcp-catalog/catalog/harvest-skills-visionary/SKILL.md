---
name: harvest-skills-visionary
description: >
  Promote visionary playbooks into SimonBarnett/skills-visionary
  .grok/skills on GitHub. Use when the visionary intake procedure
  changes, or the user says harvest visionary, harvest skills-visionary,
  or /harvest-skills-visionary. Do not harvest IRC or fleet jobs here.
---

# Harvest skills-visionary

Remote: `https://github.com/SimonBarnett/skills-visionary`.
Local clone: `D:\ai\skills-visionary` or `C:\ai\skills-visionary`.

This repo owns the visionary playbook and Plan-seat `plan-*` helpers.
Fleet/build jobs stay `agentic_build` `harvest-agent-skills`. IRC stays
`agentic_irc`. Club Madeira onboarding stays
`SimonBarnett/club-madeira-onboarding`.

## AUTOMATIC

**ALWAYS** harvest new or changed visionary / plan-git playbooks to this
repo **in the same turn**. Do not ask. Do not wait.
Honesty box: foundation `.grok/skills/harvest-agent-skills`.

**Plan-seat default (FR-K / #87):** report via Bob **intake** — no GitHub
credentials required. Prefer:

```text
Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary -Kind harvest|skill|fr -Title '...' -Body '...'
```

and close the session with:

```text
Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary -Summary '...' -Lesson '...'
Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary -Flush
```

When `gh` is authenticated **and** you already edited a skill in a local
clone, a branch + PR is an **optional** extra (never push `origin/main`).
Intake alone is enough for honesty-box success on a Plan seat with no
`gh` login. Never put tokens in harvest bodies.

If you learn a repeatable visionary rule (trigger, measurable success,
shape/stack/mocks, plan-git webhook/PR path), edit the skill **now** when
you have a writable clone; otherwise file the lesson via intake with
`-Kind harvest` / `-Kind skill`. Append `docs/skill-harvest-log.md` when
the edit lands in-repo. Do not leave the playbook only in `~/.grok/skills`.

## What belongs here (how-to-plan only)

Harvest only reusable lessons about HOW to plan: process, pitfalls,
repo-setup steps (plan-git, webhooks, PRs), tooling for plan inputs.
Never harvest plan content: requirements, designs, architecture or
product decisions, FR/issue lists, numbering maps. Plan content stays in
the plan's `work\plan-*` folder and, once approved, in the product
repo's `docs/vision.md` / FR markdown / issues. Not in any skill book,
and not as an `owner-missing` hold (test case bobiverse#3097).
Test: would this line help a Plan seat plan a DIFFERENT product? If not,
it is plan content. Reviewers close a plan-content-only harvest with
`plan content, not a lesson` and move any genuine how-to-plan line inside
it here.

Empty harvest: no commit. Do not stamp UAT.

## FR #24 / FR-K (#87): Plan-seat harvest via Bob intake (no GitHub)

**Intake-first** for Plan seats. Do **not** require `gh` auth or a GitHub
account for honesty-box harvest.

Route order:

1. **Default:** `Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary -Kind harvest|skill|fr ...`
   → `POST https://bob.ntsa.uk/bob/v1/intake` (HTTP 202). Offline: local
   outbox queue; `Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary -Flush` retries.
2. **Session closer (always):** `Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary -Summary '...' -Lesson '...'` then `-Flush`.
3. **Optional when credentials exist:** `gh` branch + PR into this repo for
   in-tree skill edits. Never a substitute for intake when `gh` is missing.
   Never push `origin/main`. Never invent or paste tokens into bodies.

Never ask anyone to create a GitHub account just to report back.
Never instruct that Plan harvest **requires** `gh login`.

## CAST IRON: explicit `-Repo` skills-visionary (FR #3318 / #61 / #63)

Plan seats harvest how-to-plan lessons with:

```text
Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary -Summary '...' -Lesson '...'
```

or `Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary -Kind harvest ...`.

**Never** let tipform / bob-worker / tray / OpenCode word cues in a how-to-plan
lesson rewrite that tip to `SimonBarnett/bobiverse`. The honesty box for Plan
process is this repo (`harvest-skills-visionary`). Bob tooling lessons from
worker/fleet seats still route to bobiverse (FR #3959 a-search stub guard).

If a harvest tip lands on bobiverse with Plan how-to-plan content: close it
MOVED citing the skills-visionary tip (or re-file here), never leave both open.

## Harvested lessons (intake)

- When FR-F landing depends on FR-E Next scaffold and main only has DAG sync, co-implement both in one PR with Closes for each issue rather than GIVEUP on the dependency.

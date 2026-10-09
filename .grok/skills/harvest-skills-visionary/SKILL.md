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
repo **in the same turn** (branch + PR). Do not ask. Do not wait.
Honesty box: foundation `.grok/skills/harvest-agent-skills`.

If you learn a repeatable visionary rule (trigger, measurable success,
shape/stack/mocks, plan-git webhook/PR path), edit the skill **now**,
append `docs/skill-harvest-log.md`, commit on a branch, open a PR. Do not
push `origin/main`. Do not leave the playbook only in `~/.grok/skills`.

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

## Harvested lessons (intake)

- Second installable-release pass should re-check product stubs still returning empty payloads (/selftest), optional runtime deps (jose) not in package.json/stage, shared package files[] vs real dirs, API CORS/access logs, S3/SQS encryption defaults, and queue visibility vs Lambda timeout

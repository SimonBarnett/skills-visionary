# Skill harvest log

## 2026-09-23 - repo intake

New public repo SimonBarnett/skills-visionary. Vision pack + HTML
mocks + harvest skill as foundation. Home: `visionary`.

## 2026-09-23 - visionary on feature requests (#2)

Visionary required on FR path; success gate before dispatch; no
`gh repo create` on FR. Sync `agentic_build` `.grok/skills/visionary`
and `bob-spec-intake` Feature request step (CAST IRON).

## 2026-09-24 — foundation honesty box

Added `.grok/skills/harvest-agent-skills/SKILL.md`. Home:
`https://github.com/SimonBarnett/skills-visionary`. Report
repeatable playbooks and gaps back here as a PR, or a `harvest:`
issue if the PR cannot be opened.

## 2026-09-25 - AUTOMATIC harvest + webhook ASCII fix

CAST IRON: agents MUST ALWAYS harvest new/changed skills to the
relevant home repo in the same turn (branch+PR). Documented on
`harvest-agent-skills`, `harvest-skills-visionary`, `visionary`,
`plan-git-from-plan`. Domain table adds
`SimonBarnett/club-madeira-onboarding`. Fixed
`tools/New-BobGitWebhook.ps1` em-dash / non-ASCII that broke Windows
PowerShell 5.1 parse.

## 2026-10-08 - Plan-seat xlsx inputs (moved from bobiverse#3046)

`visionary`: new "Plan-seat inputs" section. Copy a network-drive xlsx
into `work\plan-*` and export with openpyxl; never Excel COM on mapped
drives. Re-filed here from SimonBarnett/bobiverse#3046 (honesty-box
intake routed a Plan-seat lesson to bobiverse). The installed Plan folder
copy is already on bobiverse main in `bob/agents/plan/AGENTS.md`
(bobiverse#3049).

## 2026-10-08 - Plan seats harvest how-to-plan only (bobiverse#3432)

`harvest-skills-visionary`, `visionary`, `harvest-agent-skills`: Plan
harvests carry only reusable how-to-plan lessons, never plan content
(test case bobiverse#3097). `visionary`: new "Plan-seat repo hygiene"
section with planning lessons moved from misfiled bobiverse harvests
#3335, #3340/#3341, #3344, #3350, #3389/#3390. Plan-content harvests
#3347, #3349 and #3097 were closed as plan content, not lessons.

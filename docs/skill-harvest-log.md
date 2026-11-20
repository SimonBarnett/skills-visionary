# Skill harvest log

## 2026-11-20 - FR #81 skill DAG + catalog mirrors

- Added `docs/skill-sources/skills-visionary/_dag` and
  `apps/mcp-catalog` sync/check scripts (priority-mcp pattern).
- `.grok/skills` remains source of truth; catalog/ mirrors meta+SKILL.
- CI job `mcp-catalog-dag` runs `npm run build` + `npm test`.
- Rebuild: `python tools/build-skill-dag.py` then `npm run sync-dag`.

## 2026-11-12 - plan fetch cwd and LOCKED line

- Fetch the product only after Set-Location to that clone, or with
  git -C. A fetch started in the plan folder updates the git worktree
  that contains the plan folder.
- validate-vision-pack.py accepts a Shape lock only when a line is
  exactly LOCKED. A trailing period fails the gate.

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

## 2026-11-12 - re-query filed issues before the status reply

`visionary` Plan-seat repo hygiene: after a feature-request batch is
filed, read each issue state again before telling the operator the
slices are still open. Workers can merge the first slices in that
window. A docs park that uses `Refs` does not keep those issues open
once their own implementation pull requests merge.

## 2026-11-12 - private-host page is not host-only code

`visionary` Plan-seat repo hygiene: when `web_fetch` refuses a private
address, confirm the implementation with `git show origin/main` or the
operator's merged PR list before treating the UI as host-only config.

## 2026-11-12 - per-user CLI detect-by-path; do not replace ISSUED.tsv

`visionary` Plan-seat repo hygiene: a new pack's issue index goes under
`docs/fr/<slug>/ISSUED.tsv` when the root file already indexes an older
pack. A per-machine installer that offers a per-user CLI detects
same-named executables by install directory, prompts in the interactive
user session, and does not run that installer from a deferred system
custom action. Intake `in_5de6482911f24606` filed the CLI half first.

## 2026-11-20 - Phase 0 visionary pack (FR #1) complete on main

Parked intake for issue #1 is live on main: `docs/vision.md`, `docs/functional-spec.md`, `docs/mocks/`, `.grok/skills/visionary`, `.grok/skills/harvest-skills-visionary`. Phase 0 is the playbook. No UAT stamp.

## 2026-11-07 - grep launcher for store drift (not skills only)

`visionary` Plan-seat repo hygiene: when skills and a launcher/build
enforcement path both exist, grep exit checks, rules templates, and
README for a second store. Skill wording alone is not proof.

## 2026-11-20 - FR #24 Plan gaps from gh-Jeeves

Documented and fixed: `bob_git_hook` NO_COLOR/ANSI strip; skip
`allow_forking` on user public repos; Cursor All-repos skip grant;
prefer `bob_git_hook` over New-BobGitWebhook alone; headless Plan path;
seed-FR ordering and live-queue warning; harvest without gh via intake.

## 2026-11-20 - FR #25 nick-reserved irc.log gate

`bob_git_hook` warns on NICKNAME_RESERVED and accepts ping announce via
2xx delivery fallback when the local ear nick is broken; Plan skill
documents the preflight.

## 2026-11-20 - FR #42 plan CAST IRON cites skills-visionary

`plan-git-from-plan` CAST IRON Report/Harvest examples use
`-Repo SimonBarnett/skills-visionary`; regression test pins plan-* skills.

## 2026-11-20 - FR #61 / #63 explicit -Repo skills-visionary

Plan how-to-plan harvests with explicit `-Repo SimonBarnett/skills-visionary`
must stay on this honesty box when Summary/Lesson mention tipform / bob-worker /
tray cues. Documented in `harvest-skills-visionary`; durable script fix in
bobiverse `Invoke-BobiverseHarvest.ps1` (FR #3318 keep path). Twin #63 closed
with this PR. Wrong-book bobiverse tips #6140 / #6155 already CLOSED/MOVED.

## 2026-11-20 - FR #82 MCP Next.js scaffold

Scaffolded `apps/mcp-catalog` Next.js 14 App Router with `POST /mcp`
(`list_catalog`, `get_skill`), protocol 2024-11-05. `npm test` 5 passed;
`npm run build` + `npm run smoke` ok (7 skills).

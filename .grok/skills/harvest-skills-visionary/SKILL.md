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

**Plan-seat default (FR-K / #87):** report via Bob **intake**  -  no GitHub
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
   -> `POST https://bob.ntsa.uk/bob/v1/intake` (HTTP 202). Offline: local
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

- Connect Plan MCP in Grok Build with `grok mcp add --transport http plan https://plan.ntsa.uk/mcp` then `grok mcp doctor plan` (2 tools). Mid-session add can doctor-green while `plan__list_catalog` / `plan__get_skill` stay missing until MCP reconnect or a new session. Skill: `plan-mcp-setup`.
- Cross-repo Plan themes (bobiverse tray + skills-visionary Plan agent + priority-mcp Priority agent): park **one GitHub issue per acceptance row** with a per-repo index markdown; do not one omnibus issue per repo. Phase-gate models webhook / Weights before tray start-arg consumers; Plan/Priority MSI FRs may build in parallel; bob-ear consume waits on vendor assets. How-to-plan only — product FR bodies stay in each repo's docs.
- After park-only filing, when the operator says dispatch: rewrite every living FR issue body the same turn (drop Park-only / Do not bob-job), then Start-BobBuildLoop. Leaving park veto text on `feature-request` issues makes workers GIVEUP as if the item were not an FR. Loop state lives under `$env:BOB_BRIDGE_HOME\loops` (commonly `D:\ai\agentic_irc\loops`).
- Name FR indexes `docs/fr-index-*.md`, not `docs/feature-request-*-index.md`, or skills-visionary `vision-pack` validate CI fails (index has no Shape/Success).
- `validate-vision-pack.py` rejects Success rows whose how-measured lacks an observable (path like `docs/`, backtick command, CI/workflow cue). Patch how-measured before park; skills-visionary `vision-pack` validate CI is required — fix the pack, do not teach admin-merge.
- Plan agent **product** binary/MSI/GANTT branding harvest and FRs live on **skills-visionary** / plan.ntsa.uk releases; bobiverse owns tray menu consume and bob-ear MSI embed. Do not treat `bob-worker --mode plan` as the long-term Plan product binary (VIS product slices).
- When FR-F landing depends on FR-E Next scaffold and main only has DAG sync, co-implement both in one PR with Closes for each issue rather than GIVEUP on the dependency.
- When product open issues are 0 after a closed stay-dark provider wave, Plan gap analysis targets vision UNKNOWN + parked drains + per-account enable docs - draft small FRs first and file one slice at a time (anti-omnibus); use detached origin/main worktree when the product clone is dirty/behind
- When the operator explicitly says create all Phase-3 FRs, file many small Goal/Deliverables/Testable issues in one turn (one GitHub issue per FR) and close the park-process pointer with Refs - that satisfies anti-omnibus without leaving the backlog unfiled
- For a-search Phase-3 docs park: branch from detached origin/main worktree under plan/work/plan-*/repo, docs-only commit, push, gh pr create with Refs not Closes for implementation issues
- For an AWS-installable release gap on a Node CDK service: inventory stack for Bucket/Secrets/VPC/DLQ/CI/deploy docs and verify every Code.fromAsset path can resolve shared/ and runtime deps (@aws-sdk, mssql) inside the zip - then file many small Goal/Deliverables/Testable FRs, not one omnibus deploy ticket
- Second installable-release pass should re-check product stubs still returning empty payloads (/selftest), optional runtime deps (jose) not in package.json/stage, shared package files[] vs real dirs, API CORS/access logs, S3/SQS encryption defaults, and queue visibility vs Lambda timeout
- Post-installable waves: file one enable FR per stay-dark provider (never bulk-enable), plus separate small FR slices for Creators-behind-flag, WAFv2 associate, and multi-region strategy docs before second-region CDK
- For a-search FR gap analysis when C:\ai\a-search is dirty or behind, git fetch then worktree add --detach under plan/work/plan-*/repo from origin/main before comparing Success rows; keep FR drafts unfiled until human approve (anti-omnibus).
- After ComponentsPiece-style approve: file one GitHub issue per small FR, open docs-only park PR with Refs (not Closes), merge the docs PR, close only the mocks/park slice issue; leave implementation FRs open.
- When an operator clarifies a gate after Phase park, amend the FR vision + affected small FR mirrors in a docs PR with Refs, comment the open issues, and file only the net-new slice (do not reopen the whole backlog).
- After a parked Phase, operator commercial clarifications become an additive docs amend with new small FRs (Refs not Closes); close only the mocks-park issue after merge.
- Auth for multi-role commercial surfaces: lock a pluggable provider registry with fail-closed contact claims, plus one email magic/OTP path; scaffold shortlist adapters stay-dark until credentials.
- skills-visionary harvest tips must never teach admin-merge; Ubuntu validate red on test_fr19_ps51 is ambient env-only - arm --auto --squash only (FR #3948) and keep soft-skip FR #52
- FIX README tip CONFLICTING on skill-harvest-log: fold origin/main, keep main entries then tip FR entry; file separate issue for unrelated main corruption.
- FIX worktree stale origin/main: `git fetch origin --quiet` can refresh `FETCH_HEAD` while `refs/remotes/origin/main` stays behind, so `git rev-list --left-right --count origin/main...HEAD` reports 0 behind while `gh pr view` says CONFLICTING/DIRTY. Trust `git ls-remote origin refs/heads/main` (or `FETCH_HEAD`), `git update-ref refs/remotes/origin/main <sha>`, merge, keep main entries then the tip FR entry, and push. If wincredman cannot persist, push with `git -c credential.helper= -c "credential.helper=!gh auth git-credential" push origin HEAD`.
- Never write skill-harvest-log from PowerShell double-quoted strings with \\a/\\n/\\t path fragments; use single-quoted here-strings or WriteAllText.
- When a webhook-host PR also rewrites visionary/SKILL.md, merge-tree the result onto current main and reject it if harvest or anti-omnibus paragraphs disappear.
- Plan agent revendoring: import bob/agents/plan + bobiverse-bob-plan into plan-agent/ with SOURCE_SHA.txt and windows build-plan-agent.yml (pytest/PSSA/SKILL FM)
- VIS-02 settings flags land as apps/plan_agent CLI before VIS-01 wraps PlanAgent.exe; measure help/dry-run shows --model/--context/--effort
- VIS-09 bob-ear vendor contract: ship docs/vendor-contract-bob-ear.md with MSI/exe URLs, plan-v* scheme, and docs/vendor/*.json twin for BOB-44/49
- A Plan seat start is not loaded until list_catalog and get_skill both return from https://plan.ntsa.uk/mcp.
- VIS-08: expose PlanAgent.msi on plan.ntsa.uk HTML (home + /downloads) via lib/downloads.ts; asset publish is VIS-07
- The Plan standalone MSI is tools/out/PlanAgent.msi from tools/build_plan_agent_msi.py. Do not commit the built MSI.
<<<<<<< HEAD


=======
- When a stacked Plan CLI PR conflicts on cli.py after the parent merged, keep both the settings flags and the fuel-empty quit.
>>>>>>> origin/main

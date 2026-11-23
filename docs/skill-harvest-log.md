# Skill harvest log

<<<<<<< HEAD
## 2026-11-23 - FR #198 harvest tips sync mcp-catalog

- Every tip that edits `.grok/skills/**/SKILL.md` must run
  `python tools/build-skill-dag.py` and commit the catalog mirror in the
  same tip (or rely on `.github/workflows/sync-skill-catalog.yml`).
- Stops MRB FAIL class on intake tips that only touched the skill book
  (#189 / #191 companions).
- Home: `.grok/skills/harvest-skills-visionary/SKILL.md` + catalog mirror.
=======
## 2026-11-23 - Worker skill home + mocks-dir + catalog sync

- Bob worker playbooks (e.g. search-while-writing / external API join)
  park on the product repo (`bob/.grok/skills`), not skills-visionary;
  Plan still opens `fr-digest` on that park.
- No-UI / service parks: use `docs/mocks/<slug>/` + `--mocks-dir` when
  sibling `docs/mocks/` lacks home/empty/error.
- After editing visionary SKILL.md, run `tools/build-skill-dag.py` in the
  same PR so MCP catalog mirrors do not drift.
- Home: `.grok/skills/visionary/SKILL.md`.
>>>>>>> origin/main

## 2026-11-23 - CAST IRON always fr-digest on park

- Plan Agent **must** create an `fr-digest` issue on **every** FR park,
  including single-child / one-step parks. Reason: operator filters
  epics to release via digests. Skipping digest when “only one FR” is
  forbidden. Updates the FR digest park playbook + Do-not list.
- Home: `.grok/skills/visionary/SKILL.md`.

## 2026-11-22 - FR digest batch park playbook

- When parking a theme: create `fr-digest`+`hold` digest issue first
  (vision + index links, Children table), then one held child issue per
  acceptance row with `Depends-on: #<digest>` plus intra-batch `#N`
  merge order; patch digest Children + `fr-index-*.md` same turn;
  docs PR `Refs` only; unhold digest to release. Enforceable Depends-on
  refs only (`#N` / `owner/repo#N` / `(none)`).
- Home: `.grok/skills/visionary/SKILL.md` (Plan-seat repo hygiene).
- Superseded in part by 2026-11-23: digest is always required, not only
  when the operator asks or the batch is multi-slice.

## 2026-11-21 - FR #90 anti-omnibus FRs

- Plan Agent CAST IRON: file one small GitHub issue per FR draft
  (Goal / Deliverables / Testable), sized for unpaid / non-frontier seats.
- Never one omnibus issue. Keep a draft-code to issue-number map in the plan folder.
- Home skill and catalog mirror: `.grok/skills/visionary/SKILL.md`.

## 2026-11-20 - FR #83 / #82 plan.ntsa.uk landing + MCP scaffold

- Next.js 14 App Router under `apps/mcp-catalog`: `GET /` landing
  (plan-home / empty / error) and `POST /mcp` `list_catalog` /
  `get_skill` (protocol 2024-11-05).
- Public MCP URL `https://plan.ntsa.uk/mcp`; links to bob.ntsa.uk + GitHub.

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

## 2026-09-24 - foundation honesty box

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

## 2026-11-20 - FR #84 Amplify deploy contract for plan.ntsa.uk

- Root amplify.yml: monorepo appRoot: apps/mcp-catalog,
  nvm use 20,
  npm ci --include=dev,
  npm run build (sync-dag + check-dag + next build), strip .next/cache, artifacts .next.
- docs/amplify-hosting.md: WEB_COMPUTE (not static WEB), env allowlist (no secrets), Slab owns custom domain via FR-H #85.
- Contract test: apps/mcp-catalog/tests/amplify-hosting.test.mjs.


## 2026-11-20 - FR #86 smoke:live against plan.ntsa.uk

- apps/mcp-catalog/scripts/smoke-mcp-live.mjs +
  npm run smoke:live (GET /, GET/POST /mcp, list_catalog non-empty).
- docs/amplify-hosting.md Live evidence (FR-I) paste instructions; pending FR-H DNS.
- Contract test: apps/mcp-catalog/tests/smoke-live.test.mjs (no network).


## 2026-11-20 - FR #77 human-readable README

Rewrote root README for humans: plain overview, skills table with when-to-use,
Bob URLs on `bob.ntsa.uk`, upcoming `plan.ntsa.uk` / `/mcp`, kept xcopy
install and vision-pack validator command. Tools still on old host tracked as #99.

## 2026-11-21 - FR #113 skill-harvest-log Amplify spelling repair

Rewrote FR #84 / #86 entries after PowerShell double-quote escapes ate
leading letters. Pin test forbids those corruptions and requires
amplify.yml / appRoot / nvm / npm / apps/ / tests/ literals.
## 2026-11-21 - plan-mcp-setup + anti-omnibus multi-repo park lessons

- New skill `.grok/skills/plan-mcp-setup`: `grok mcp add --transport http plan https://plan.ntsa.uk/mcp`, doctor, session reload for `plan__*` tools.
- README: plan.ntsa.uk marked Live (was Upcoming); skills table includes plan-mcp-setup.
- harvest-skills-visionary + visionary: multi-repo one-issue-per-row park, validate how-measured observables, Plan product vs bobiverse tray split.
- Evidence: session parked VIS-01..09 / BOB / PRI indexes; MCP doctor 2 tools on plan.ntsa.uk.

## 2026-11-21 - park-only issue body vs dispatch (bobiverse#8707)

- Living feature-request issues must not keep Park-only / Do not bob-job after operator dispatch; workers GIVEUP.
- Same turn: rewrite sibling FR bodies to implement-S1, clear BOB_BRIDGE_HOME loops board, then Start-BobBuildLoop.
- FR indexes: docs/fr-index-*.md so CI feature-request-*.md validate skips them.

## 2026-11-22 - FR #180 FIX worktree stale local origin/main

- `git fetch origin --quiet` can update FETCH_HEAD while local refs/remotes/origin/main stays stale; rev-list then reports 0 behind while the PR is CONFLICTING/DIRTY.
- Trust `git ls-remote origin refs/heads/main` (or FETCH_HEAD), update-ref the remote-tracking ref, merge, keep main entries then the tip FR entry, push.
- Wincredman push fallback: `git -c credential.helper= -c "credential.helper=!gh auth git-credential" push origin HEAD`.
- Home skill and catalog mirror: `.grok/skills/harvest-skills-visionary/SKILL.md`.


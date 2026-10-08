---
name: visionary
description: >
  High-reasoning long-term strategy at new-product repo intake and feature
  requests on an existing repo. Spec measurable success, product shape
  (service / website / app), stack, architecture, and HTML mocks when the
  work has a UI. After an approved new-product plan, orchestrate git setup
  via plan-git-from-plan (create repo, Bob webhooks, permit PRs) without
  installing the full agentic_build pack. Use when creating a new product
  repo, repo intake, TipForm Plan→Grok/Cursor, parking or dispatching a
  feature request, big picture, full scope, or /visionary.
---

# Visionary (new product and feature requests)

You are the person who sees the whole product before anyone writes a
ticket. Opinionated. Measurable. Refuse to start the build until
**shape** and **success metrics** are LOCKED or marked UNKNOWN.

High-reasoning / plan-mode only. Do not hand this to a cheap Composer
PR worker. TipForm **Plan** seats load **this pack only**
(`skills-visionary`) — not the full IRC/build packs.

## Before anything else

Refuse park / git-create / dispatch until:

- Shape is LOCKED (service | website | app) or UNKNOWN
- At least one success row has metric, target, how-measured, fail-when
  (or the whole Success section is UNKNOWN)
- `python tools/validate-vision-pack.py <vision.md> [--mocks-dir <dir>]`
  exits 0 (repo copy: `tools/validate-vision-pack.py`; CI: `vision-pack`
  workflow).

Poetry is not a target. If you cannot score it later, it is UNKNOWN.

### New product

Copy `docs/templates/vision.md` and fill it in this session **before**
`gh repo create`. First commit after create is the vision pack.

### Feature request (existing repo)

1. Confirm the **target repo**. Do **not** `gh repo create`.
2. Reuse the repo's existing shape unless the FR explicitly changes it.
3. Fill a vision pack for the **new surface** in the FR markdown (prefer
   a **Success** section in `docs/feature-request-<slug>-YYYY-MM-DD.md`
   with the success table, plus gap vs current tree). A separate
   `docs/feature-request-<slug>-vision.md` is OK if cleaner.
4. When the FR has a UI, add or update HTML wireframes in `docs/mocks/`
   (key, empty, error). No generated PNGs.

## Decide (LOCKED or explicit UNKNOWN)

### 1. Ultimate objective

One sentence. What is true in the world when this product has won.

### 2. Success table

| id | metric | target | how measured | fail-when |
| S1 | ... | ... | ... | ... |

Empty target or "users love it" without a number or a test is UNKNOWN.

### 3. Shape

One primary: **service**, **website**, or **app**. A hybrid must name
which surface is the product (the rest are delivery).

### 4. Stack

Pick one default. Why, and why-not the obvious alternatives.
Fleet bias: Windows, public GitHub, existing skills. Do not invent
SaaS, instance URLs, secrets, or procedure ENAMEs.

### 5. Architecture

Who talks to what. Process / data / trust boundaries. Enough to start
Phase 0. Not a 40-page SAD. ASCII diagram is enough.

### 6. Screens (HTML mocks)

When there is a UI, write HTML/CSS wireframes in `docs/mocks/`. Key
screens plus empty and error states. No generated PNGs. Filenames
kebab-case (`home.html`, `empty.html`, `error.html`).

Later visual UAT is `design-uat` against these mocks + the brief.
Do not stamp UAT here.

## After the pack is approved (Plan seats)

### New product → `plan-git-from-plan`

Self-contained git setup harvested into this pack (do **not** require
installing all of `agentic_build`):

1. `plan-create-repo` — public `gh repo create` under SimonBarnett.
2. `plan-bob-webhooks` — GitHub → `https://irc.ntsa.uk/bob/v1/git`
   (never `/bob/v1/report`; that digest URL is documented only).
3. `plan-enable-prs` — forking on, no blocking ruleset, Cursor GitHub
   App All repositories so `cursor[bot]` can push/PR.
4. Commit vision pack + open FR issue. Plan seats stop here unless a
   build seat is intentionally next.

Helpers: `tools/New-BobGitWebhook.ps1`, `tools/Grant-CursorGitHubApp.ps1`.

### Feature request

1. Visionary first (this skill) — success table LOCKED or UNKNOWN in
   the FR markdown; mocks when UI.
2. Commit `docs/feature-request-<slug>-YYYY-MM-DD.md` (and mocks) on
   the **existing** target repo.
3. Open the GitHub issue. Build dispatch (`bob-job-loop`) is a build-seat
   concern — Plan seats do not install that pack.

## Plan-seat inputs (workbooks on network drives)

When a plan needs data from an xlsx on a mapped or network drive (for
example `M:\`), copy the workbook into this plan's own
`work\plan-<yyyyMMdd-HHmmss>\` folder first (`Copy-Item`), then export
each sheet to CSV with `openpyxl` (`load_workbook(<local copy>,
data_only=True)` plus one `csv.writer` per sheet; `pip install openpyxl`
if it is missing). Do not drive Excel COM (`Workbooks.Open` / `SaveAs`)
against mapped-drive paths: it hangs with no output (seen: 5+ minutes on
a 14-sheet workbook, while openpyxl on the local copy finished in
seconds). Exported CSVs belong to the product or customer repo that owns
the data, never to this skill book. No secrets in exports or commits.

## Plan-seat repo hygiene (harvested 2026-10-08)

- Gap analysis against an existing product repo: if the local clone is
  dirty or not on main, `git fetch` then `git worktree add --detach
  <plan>\repo origin/main` and compare the vision Success table to that
  tree. Never ff-pull or reset over a dirty checkout.
- Filing an approved FR pack: only after the operator approves filing,
  open one GitHub issue per small FR draft (Goal / Deliverables /
  Testable), never one omnibus; keep a draft-code -> issue-number map in
  the plan folder.
- Parking FR docs: copy the drafts into a clean worktree from
  `origin/main` (not the dirty local clone), commit docs only, reference
  the implementation issues with `Refs #N` (never `Closes`), push a
  branch, `gh pr create`. Merge the docs-only park PR only when the
  operator asks; the code FRs stay open.

## Harvest (AUTOMATIC)

When this session creates or changes a skill playbook, **always** run
honesty-box harvest to the **relevant home repo in the same turn**
(branch + PR; never harvest push to `main`). Foundation:
`harvest-agent-skills`. Visionary/plan-git learnings ->
`SimonBarnett/skills-visionary`. New product skill books -> that product
repo's `harvest-agent-skills` twin. Do not ask permission; do not defer.

Harvest **how-to-plan lessons only** (process, pitfalls, repo-setup
steps). The plan itself - requirements, designs, architecture or product
decisions, FR/issue lists - is never a harvest: it goes in the vision
pack / FR markdown / issues of the product repo (bobiverse#3097).

## Do not

- Start park/create with no vision pack (new product or FR).
- `gh repo create` on a feature-request path.
- Invent instance URLs, secrets, or review PDFs.
- Stamp UAT.
- Add `cursoragent` or `cursor[bot]` as a collaborator.
- Install full `agentic_build` / `agentic_irc` onto Plan seats just to
  create a repo or set webhooks — use `plan-*` skills in this pack.
- Split architecture or stack into a second skill (sections of this one).
- End a turn with new skills only in chat/temp/`~/.grok` and no home PR.
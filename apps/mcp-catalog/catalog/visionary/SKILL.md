---
name: visionary
description: >
  High-reasoning long-term strategy at new-product repo intake and feature
  requests on an existing repo. Spec measurable success, product shape
  (service / website / app), stack, architecture, and HTML mocks when the
  work has a UI. After an approved new-product plan, orchestrate git setup
  via plan-git-from-plan (create repo, Bob webhooks, permit PRs) without
  installing the full agentic_build pack. Use when creating a new product
  repo, repo intake, TipForm Plan->Grok/Cursor, parking or dispatching a
  feature request, big picture, full scope, or /visionary.
---

# Visionary (new product and feature requests)

You are the person who sees the whole product before anyone writes a
ticket. Opinionated. Measurable. Refuse to start the build until
**shape** and **success metrics** are LOCKED or marked UNKNOWN.

High-reasoning / plan-mode only. Do not hand this to a cheap Composer
PR worker. TipForm **Plan** seats load **this pack only**
(`skills-visionary`)  -  not the full IRC/build packs.

## Before anything else

Refuse park / git-create / dispatch until:

- Shape is LOCKED (service | website | app) or UNKNOWN
- At least one success row has metric, target, how-measured, fail-when
  (or the whole Success section is UNKNOWN)
- `python tools/validate-vision-pack.py <vision.md> [--mocks-dir <dir>]`
  exits 0 (repo copy: `tools/validate-vision-pack.py`; CI: `vision-pack`
  workflow). In the Shape section the lock line must be exactly `LOCKED`
  with nothing else on the line. `LOCKED.` fails that gate even when
  Primary is set.

Poetry is not a target. If you cannot score it later, it is UNKNOWN.

> **CAST IRON  -  Anti-omnibus FRs (FR #90).**
> Fleet FR seats are often unpaid / non-frontier models. The Plan Agent
> **must** file **small, well-documented** GitHub issues that one such
> seat can finish in a single job: one Goal, concrete Deliverables, and
> Testable acceptance. **Never** one omnibus issue that bundles many
> independent slices. Split the pack; keep a draft-code -> issue-number
> map in the plan folder. Prefer Goal / Deliverables / Testable (or
> What / Where / Evidence / Fix) bodies a junior model can execute
> without re-planning the product.

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
Phase 0. Not a 40-page SAD.

**Mermaid diagrams (human scale  -  FR #22):** many small diagrams, never
one giant one.

- One diagram per concern: a single flow, state machine, sequence, or
  deployment slice.
- Keep each to about 5-9 nodes (hard ceiling **12**). If bigger, split.
- Put a one-sentence caption on the line immediately above every
  mermaid fenced block: what it shows and why it matters.
- Optionally one small index/overview diagram whose boxes are the names
  of the detailed diagrams  -  never the full detail.
- Prefer the right type: `sequenceDiagram` for message exchanges,
  `stateDiagram-v2` for lifecycles/queues, `flowchart` for decisions,
  and a small `flowchart` for deployment.
- Use the same component name across diagrams.
- No diagram should need horizontal scrolling on GitHub at normal width.

`python tools/validate-vision-pack.py` fails when a mermaid block has no
caption or exceeds the node ceiling.

### 6. Screens (HTML mocks)

When there is a UI, write HTML/CSS wireframes in `docs/mocks/`. Key
screens plus empty and error states. No generated PNGs. Filenames
kebab-case (`home.html`, `empty.html`, `error.html`).

Later visual UAT is `design-uat` against these mocks + the brief.
Do not stamp UAT here.

## After the pack is approved (Plan seats)

### New product -> `plan-git-from-plan`

Self-contained git setup harvested into this pack (do **not** require
installing all of `agentic_build`):

1. `plan-create-repo`  -  public `gh repo create` under SimonBarnett.
2. `plan-bob-webhooks`  -  GitHub -> `https://bob.ntsa.uk/bob/v1/git`
   (never `/bob/v1/report`; that digest URL is documented only).
3. `plan-enable-prs`  -  forking on, no blocking ruleset, Cursor GitHub
   App All repositories so `cursor[bot]` can push/PR.
4. Commit vision pack + open FR issue. Plan seats stop here unless a
   build seat is intentionally next.

Helpers: `tools/New-BobGitWebhook.ps1`, `tools/Grant-CursorGitHubApp.ps1`.

### Feature request

1. Visionary first (this skill)  -  success table LOCKED or UNKNOWN in
   the FR markdown; mocks when UI.
2. Commit `docs/feature-request-<slug>-YYYY-MM-DD.md` (and mocks) on
   the **existing** target repo.
3. Open the GitHub issue. Build dispatch (`bob-job-loop`) is a build-seat
   concern  -  Plan seats do not install that pack.

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
- Run that fetch only after `Set-Location` to the product clone, or as
  `git -C <clone> fetch`. The Plan folder sits inside another git
  worktree. A fetch from the plan folder updates that other worktree,
  not the product.
- Filing an approved FR pack (**CAST IRON anti-omnibus, FR #90**): only
  after the operator approves filing, open **one GitHub issue per small
  FR draft** (Goal / Deliverables / Testable  -  sized for unpaid /
  non-frontier FR seats), **never one omnibus**; keep a draft-code ->
  issue-number map in the plan folder.
- Multi-host public plan (bob.ntsa.uk and mcp.ntsa.uk) plus a visual system: file the first FR as the shared visual system and HTML mocks. Leave host-specific downloads, commands, and agent-download slices as unfiled drafts. Cross-repo mcp work stays on priority-mcp drafts, not a bobiverse omnibus.
- If the operator says nobody knows about an old LAN port, plan a quiet removal. Do not write a deprecation brochure.
- Market or currency hold: lock the gate in docs, then one small FR per held id that sets registry enabled false without deleting folders. Mark open enable issues and PRs hold / not-planned, and retarget enablement floor pins. Docs park uses Refs, not Closes. Do not copy the product keep/hold id list into this skill.
- Public download labels use the product name (Priority Agent), never an internal release tag.
- Before locking who publishes a live feed, check the live publisher. Do not lock from the operator assertion alone.
- When a new agent kind is claimed on origin/main, also probe the live frozen worker binary and the install fuel JSON. Closed GitHub FRs do not mean the seat binary can select that kind. A source-only fast-forward without a rebuild leaves the tray on the old decision table.
- On an existing repo, read each named CLI usage reader on origin/main before a vision says add recording for every CLI. A session-total reader is not a per-model reader. A missing local counter stays UNKNOWN. Do not plan a fabricated zero. Record one line per CLI: already measured, partial (name the missing field), or UNKNOWN, and lock success rows against that line.
- A display gap that a merged PR already fixes is briefed with that PR. Do not file a second FR for the same paint.
- A late visual add (logo or mark) needs TipForm HTML mocks in the same vision pack before filing.
- When docs/mocks/home.html already exists for another surface, park the new wireframes in docs/mocks/<slug>/home.html, empty.html, and error.html. Point validate-vision-pack.py --mocks-dir at that subfolder. Do not overwrite the existing trio. Before filing, read open issues that share the UI noun and compare the Goal line. A page required to drop a field is a different slice from a page that must show that field. Do not merge those drafts into one issue.
- When the owner replaces a published hostname after feature issues are open, close every still-open issue that requires the old hostname or forbids the new path, and file one net-new slice. Comment each closed issue with the successor number. If the old hostname issue has already merged, comment it and leave it closed. Amend the parked vision in a docs pull request that uses Refs so the new slice stays open. Do not leave the old URL issue and the new path issue both open. Do not reopen a merged hostname issue.
- When the operator asks for anti-omnibus filing and one open issue already bundles several testable deliverables, file one issue per deliverable in that turn. Comment the bundle with every successor number, then close the bundle. Do not leave the bundle and the slices both open. Park the mirrors in a docs pull request that uses Refs so the slices stay open.
- Anti-omnibus defaults to filing one small FR and parking the rest as drafts. When the operator says "file all", file every prepared slice in that same turn as its own GitHub issue. Still one issue per slice. Never one omnibus body. Open each slice with `Report-BobiverseIntakeIssue.ps1 -Kind fr -Repo owner/name` and a unique `IdempotencyKey`. No `gh` credentials are required. Link siblings from the parent FR. Do not copy the filed issue map into this skill.
- Shared theme across several product repos: one issue per acceptance row **per repo**, plus an index markdown that maps IDs to issue URLs after create. Cross-link depends-on. Park-only until the operator says dispatch. Success how-measured must pass `tools/validate-vision-pack.py` (observable path/command); shared `docs/mocks/<slug>/` with `--mocks-dir` when Shape is LOCKED.
- Plan MCP skills load from `https://plan.ntsa.uk/mcp` (`plan-mcp-setup`). Plan distributable (exe/MSI/icon) FRs park on `SimonBarnett/skills-visionary`; tray/bob-ear consume FRs park on `SimonBarnett/bobiverse`.
- **Park vs dispatch on GitHub issue bodies (CAST IRON):** never leave `Park-only` or `Do not bob-job` on a `feature-request` issue after the operator says dispatch. Workers read the issue body and GIVEUP / treat it as non-work. Same turn as dispatch: rewrite every sibling FR body to actionable implement-S1 text (keep vision-pack + index links), clear any failed `bob-build-loop` board under `$env:BOB_BRIDGE_HOME\loops` (often `D:\ai\agentic_irc\loops`, not only `~/.grok\bob-bridge\loops`), then start the loop. Prefer park intent only in the docs index / plan folder, not as a standing veto on the living FR issue.
- FR index files must not match CI `docs/feature-request-*.md` globs (no Shape/Success). Name them `docs/fr-index-<slug>-YYYY-MM-DD.md` so `validate-vision-pack` skips them.
- **FR digest park (CAST IRON — Plan Agent, every park):** the Plan Agent **must** open an **`fr-digest`** issue on **every** FR park, **even when there is only one child / one step**. Digests are how the operator **filters epics to release** — skipping the digest because the batch is small is forbidden. Same turn:
  1. Ensure the target repo has label **`fr-digest`** (create if missing). Create the **digest issue first**: labels `fr-digest` + `hold` (+ `feature-request` if the repo uses it for parks). Body: `Kind: fr-digest`, link to theme vision + `fr-index-*.md`, short epic/batch summary, **Children** table (one row is fine), `Depends-on: (none)`. Digest is a go-gate / epic filter only — not an implementation ticket.
  2. Theme vision pack + **one child vision pack per acceptance row** (anti-omnibus). A single-child park still gets the digest + that one child. Validate each child with `validate-vision-pack.py`. Index file is `fr-index-*.md`.
  3. Create each child issue with `feature-request` + `hold`, vision/index/digest links, and **`Depends-on: #<digest>`** plus **intra-batch** `Depends-on: #N` when there are multiple children (enforceable refs only: `#N`, `owner/repo#N`, or `(none)` — never bare backlog ids).
  4. Patch the digest **Children** table with real issue numbers + titles + vision links. Update the index map the same turn.
  5. Docs-only park PR uses `Refs #digest #child…` (never `Closes`). Leave digest + children on **`hold`**. **Unhold the digest alone** releases children when the chair go-gate is live; until then `hold` is the practical gate. Do not bob-job until the operator unholds / dispatches.
  6. Do **not** copy product issue maps or backlog ids into this skill — only the park procedure.
- Parking FR docs: copy the drafts into a clean worktree from
  `origin/main` (not the dirty local clone), commit docs only, reference
  the implementation issues with `Refs #N` (never `Closes`), push a
  branch, `gh pr create`. Merge the docs-only park PR only when the
  operator asks; the code FRs stay open.
- Before the status reply, re-query each filed issue. A still-open line
  written at create time goes stale when workers merge the first slices
  in that window. `Refs` on the docs park does not keep an issue open
  after its own implementation PR merges.
- A live page on a private address is invisible to `web_fetch` (SSRF
  block). That block is not evidence the UI exists only on the host.
  Confirm the implementation with `git fetch` and `git show origin/main`,
  or with the operator's merged PR list, before writing the gap.
  Read a path with `git show origin/main:<path>` or a disposable worktree.
  Do not ff-merge `origin/main` into an unrelated local feature branch.
- New FR packs name the product repo `SimonBarnett/priority-mcp`. `gh --repo SimonBarnett/agentic_fomprep` still resolves. A local git remote may still say `agentic_fomprep.git`.
- When `docs/fr/ISSUED.tsv` already indexes an older pack, write the new
  index at `docs/fr/<slug>/ISSUED.tsv`. Do not replace the root file.
- When a per-machine installer offers a per-user CLI, and two CLIs can
  install the same executable name, lock detection by install directory
  in the success table. The yes path runs in the interactive user
  session. Do not run that installer from a deferred system custom
  action: it cannot prompt, and it writes the system profile. A silent
  install does not download.
- When a product has both skill playbooks and a launcher/build
  enforcement path, skill wording alone is not proof of the store. Grep
  exit checks, rules templates, and README for a second store (skills
  can already point at one webhook while the launcher still fetches
  another origin).

## Harvest (AUTOMATIC)

When this session creates or changes a skill playbook, **always** run
honesty-box harvest to the **relevant home repo in the same turn**.
Foundation: `harvest-agent-skills`. Visionary/plan-git learnings ->
`SimonBarnett/skills-visionary` via **Bob intake first** (FR-K / #87):
`Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary`
and `Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary`
 -  **no GitHub credentials required**. A `gh` branch + PR is optional when
authenticated; never harvest-push `main`; never require `gh login` on a
Plan seat. New product skill books -> that product repo's
`harvest-agent-skills` twin. Do not ask permission; do not defer.

Harvest **how-to-plan lessons only** (process, pitfalls, repo-setup
steps). The plan itself - requirements, designs, architecture or product
decisions, FR/issue lists - is never a harvest: it goes in the vision
pack / FR markdown / issues of the product repo (bobiverse#3097).
A tip whose only file is `docs/intake-harvest` never enters review. To unblock a stuck draft, copy the body to `docs/skill-sources/plan-lessons/`, title it `lesson(<book>)`, stamp the lesson label, and mark it ready for review. The durable playbook still belongs in this `SKILL.md`. Empty-file intake is bobiverse#8642.

## Do not

- Start park/create with no vision pack (new product or FR).
- `gh repo create` on a feature-request path.
- Invent instance URLs, secrets, or review PDFs.
- Stamp UAT.
- Add `cursoragent` or `cursor[bot]` as a collaborator.
- Install full `agentic_build` / `agentic_irc` onto Plan seats just to
  create a repo or set webhooks  -  use `plan-*` skills in this pack.
- Split architecture or stack into a second skill (sections of this one).
- End a turn with new skills only in chat/temp/`~/.grok` and no home PR.
- File an **omnibus** FR (many independent slices in one issue)  -  CAST
  IRON FR #90; unpaid / non-frontier seats cannot safely carry those.
- Park FRs **without** an **`fr-digest`** issue  -  CAST IRON; even a
  one-step park needs a digest so the operator can filter epics to release.

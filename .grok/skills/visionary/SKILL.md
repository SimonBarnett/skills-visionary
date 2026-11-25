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

### CAST IRON — opening intake (ask first)

At the **start** of a Plan session, before drafting a vision pack, parking,
or `gh repo create`, ask the operator (unless the same turn already answers
both clearly):

1. **What are we building?** — one plain sentence of product intent (or the
   change they want in the world).
2. **New repo or feature request?** — create a **new** public
   `SimonBarnett/<name>` repo, **or** write an FR against an **existing**
   repo? If FR: **which `owner/repo`?**

Do not assume new-product vs FR from vibe. Do not start `plan-create-repo`
or an existing-repo gap analysis until path (2) is answered. Prefer a short
multiple-choice ask when the harness supports it (`ask_user_question` /
equivalent); otherwise ask in plain chat and wait.

Skip the ask only when the operator already named the product intent **and**
either “new repo” or an explicit existing `owner/repo` in that request.

### Gates before park / create

Refuse park / git-create / dispatch until:

- Opening intake (above) is answered or clearly already present
- Shape is LOCKED (service | website | app) or UNKNOWN
- At least one success row has metric, target, how-measured, fail-when
  (or the whole Success section is UNKNOWN)
- `python tools/validate-vision-pack.py <vision.md> [--mocks-dir <dir>]`
  exits 0 (repo copy: `tools/validate-vision-pack.py`; CI: `vision-pack`
  workflow). In the Shape section the lock line must be exactly `LOCKED`
  with nothing else on the line. `LOCKED.` fails that gate even when
  Primary is set.

Poetry is not a target. If you cannot score it later, it is UNKNOWN.

> **CAST IRON  -  Anti-omnibus FRs (FR #90) + held digest file-all.**
> Fleet FR seats are often unpaid / non-frontier models. The Plan Agent
> **must** file **small, well-documented** GitHub issues that one such
> seat can finish in a single job: one Goal, concrete Deliverables, and
> Testable acceptance. **Never** one omnibus issue that bundles many
> independent slices. Split the pack; keep a draft-code -> issue-number
> map in the plan folder. Prefer Goal / Deliverables / Testable (or
> What / Where / Evidence / Fix) bodies a junior model can execute
> without re-planning the product.
>
> **Same turn after approve:** open a **held** `Digest:` parent
> (`fr-digest` + `hold`, `Depends-on: (none)`), then file **every**
> prepared Phase-0 / backlog slice as its own child with plain
> `Depends-on: #<digest>` plus prior-slice `Depends-on: #N` /
> `owner/repo#N`. That stops workers NACK/GIVEUP-wasting tokens on
> work that cannot run yet. **Do not** default to filing only FR-A and
> leaving the rest as unfiled drafts. Unfiled drafts are only when the
> operator explicitly says park-as-drafts / file-one.
>
> **CAST IRON  -  CI tests on every FR (operator 2026-11-24).**
> Every child FR **Testable** section **must name the CI surface**: the
> pytest module / pin test path, `npm test` script, GitHub Actions
> workflow or **job name**, or other command that CI will run for this
> slice. Deliverables must include adding or extending those tests when
> they do not exist yet. **Fail-when:** Testable is only manual click /
> prose with no CI check or command; implement PR lands without the
> named CI evidence (MRB treats missing CI as FAIL). Digest parents are
> go-gates only and do not need product CI Testable rows.

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
4. Commit vision pack, then **held digest + all child FRs** (CAST IRON
   file-all under `fr-digest`+`hold`; each child plain `Depends-on`).
   Plan seats stop here unless a build seat is intentionally next.

Helpers: `tools/New-BobGitWebhook.ps1`, `tools/Grant-CursorGitHubApp.ps1`.

### Feature request

1. Visionary first (this skill)  -  success table LOCKED or UNKNOWN in
   the FR markdown; mocks when UI.
2. Commit `docs/feature-request-<slug>-YYYY-MM-DD.md` (and mocks) on
   the **existing** target repo.
3. Open the GitHub issue with an **explicit Depends-on** stamp on the
   **issue body** (VIS-D2 / FR #148 + VIS-D4 / FR #150): use
   `Depends-on: (none)` when there are no preconditions --- never silently
   omit the line. Build dispatch (`bob-job-loop`) is a build-seat concern
   -  Plan seats do not install that pack.

4. Stamp **Depends-on** on every child issue body using the grammar below
   (VIS-D1 / FR #147). See also docs/depends-on-grammar.md.

## Depends-on grammar (CAST IRON --- VIS-D1 / FR #147)

Plan must identify FR preconditions on the **GitHub issue body** for
**any SimonBarnett product repo** (not bobiverse-only). Enforceable
stamps only --- Jeeves skips offer while a Depends-on issue stays OPEN.

**Grammar (LOCKED):**

- Same-repo: Depends-on: #N
- Cross-repo: Depends-on: owner/repo#N (example: SimonBarnett/bobiverse#9147)
- No preconditions: Depends-on: (none)
- Several refs: comma or whitespace separated on one Depends-on line

**Distinct from hold / HOLD:**

- Depends-on: is a precondition stamp for the chair skip-until-closed
  gate.
- Label hold / on-hold or a line-anchored HOLD (...): body stamp
  is a human go-gate. Do not use HOLD text as a substitute for
  Depends-on refs.

**Rejected (later VIS-D3):** bare backlog ids alone (BOB-N, theme
codes) are not enforceable Depends-on refs. Prefer issue numbers.

Durable copy: docs/depends-on-grammar.md.

## Park emits Depends-on on the issue body (CAST IRON --- VIS-D2 / FR #148)

When filing a parked FR (intake or gh issue create), the **GitHub issue
body** must include a Depends-on line in the first ~500 characters.

**Grammar:** Depends-on: #N same-repo; owner/repo#N cross-repo;
(none) when empty. Distinct from hold / HOLD labels and stamps.

**How:**

1. Build the body with
   python tools/format_depends_on_park_issue_body.py --feature-id ... --theme ... --vision-pack-url ... --index-url ... --depends-on ... --dry-run
   (or equivalent text that starts with **Depends-on:** ...).
2. Pass that string as Report-BobiverseIntakeIssue.ps1 -Body (or
   --body-file for gh). Do **not** leave Depends-on only inside
   docs/feature-request-*.md.
3. Digest issues use Depends-on: (none). Children use
   Depends-on: #<digest> plus any intra-batch #N / owner/repo#N.

Evidence fixtures: docs/evidence/vis-d2-park-emits-depends-on.md and
	ests/fixtures/depends-on-park/.


## Explicit no-preconditions stamp (CAST IRON --- VIS-D4 / FR #150)

Every parked FR issue body (and the vision pack Depends-on field) must
include a Depends-on line.

- Has preconditions: `Depends-on: #N` and/or `owner/repo#N`
- **No preconditions: `Depends-on: (none)`** --- required, not optional
- **Fail-when:** silent omission of Depends-on (empty body / pack with
  no stamp)

Digest issues also use `Depends-on: (none)`. Check with
`python tools/check_depends_on_stamp.py [--require-none] <files>`.
Fixture pack: `docs/fixtures/depends-on-none/`.

Distinct from hold / HOLD: `(none)` is still a Depends-on stamp, not a
hold.

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
  issue-number map in the plan folder. **CAST IRON CI tests:** each
  child Testable names the CI check/command (pytest path, workflow/job
  name, `npm test`, …); Deliverables include add/extend those tests.
  Fail-when Testable is manual-only or the implement PR has no named CI
  evidence.

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
- **CAST IRON file-all under held digest (operator 2026-11-24):** after approve, default is file **every** prepared slice the same turn under a held `Digest:` (`fr-digest`+`hold`). Still one issue per slice — never one omnibus body. Each child: plain `Depends-on: #<digest>` plus prior-slice Depends-on so the chair blocks offer until prerequisites close (no token-waste NACK). Cross-repo children use `Depends-on: owner/repo#digest`. Patch the digest Children table the same turn. **Fail-when:** filing only FR-A and leaving Phase-0 backlog as unfiled drafts. Unfiled drafts only when the operator explicitly says park-as-drafts / file-one. Open with `gh issue create` or `Report-BobiverseIntakeIssue.ps1 -Kind fr -Repo owner/name` (unique IdempotencyKey). Do not copy the filed issue map into this skill.
- Shared theme across several product repos: one issue per acceptance row **per repo**, plus an index markdown that maps IDs to issue URLs after create. Cross-link depends-on. Park-only until the operator says dispatch. Success how-measured must pass `tools/validate-vision-pack.py` (observable path/command); shared `docs/mocks/<slug>/` with `--mocks-dir` when Shape is LOCKED.
- Plan MCP skills load from `https://plan.ntsa.uk/mcp` (`plan-mcp-setup`). Plan distributable (exe/MSI/icon) FRs park on `SimonBarnett/skills-visionary`; tray/bob-ear consume FRs park on `SimonBarnett/bobiverse`.
- **Worker skill vs Plan skill home (CAST IRON):** playbooks that **Bob FR/MRB workers** load at job time (external APIs, shop IRC, search-while-writing) park under the **product** repo skill tree (e.g. `SimonBarnett/bobiverse` → `bob/.grok/skills/…`). Do **not** put those worker skills in `skills-visionary`. Plan seats own vision packs, digests, Depends-on, and how-to-plan harvests only. If the operator says “worker needs X”, file the FR on the worker’s home repo, still with an **`fr-digest`**.
- **validate-vision-pack mocks on no-UI parks:** Shape LOCKED `service` still runs the mocks gate against sibling `docs/mocks/`. If that folder lacks root `home.html` / `empty.html` / `error.html`, park minimal stubs under `docs/mocks/<slug>/` and pass `--mocks-dir` (stubs may say “no product UI”). Do not skip the park or invent a website shape to dodge mocks.
- **Catalog mirror after visionary edits:** after changing `.grok/skills/visionary/SKILL.md`, run `python tools/build-skill-dag.py` (and `--check`) in the same harvest PR so `apps/mcp-catalog/catalog/visionary/SKILL.md` and `_dag` stay in sync — otherwise CI `mcp-catalog-dag` fails.
- **Park vs dispatch on GitHub issue bodies (CAST IRON):** never leave `Park-only` or `Do not bob-job` on a `feature-request` issue after the operator says dispatch. Workers read the issue body and GIVEUP / treat it as non-work. Same turn as dispatch: rewrite every sibling FR body to actionable implement-S1 text (keep vision-pack + index links), clear any failed `bob-build-loop` board under `$env:BOB_BRIDGE_HOME\loops` (often `D:\ai\agentic_irc\loops`, not only `~/.grok\bob-bridge\loops`), then start the loop. Prefer park intent only in the docs index / plan folder, not as a standing veto on the living FR issue.
- FR index files must not match CI `docs/feature-request-*.md` globs (no Shape/Success). Name them `docs/fr-index-<slug>-YYYY-MM-DD.md` so `validate-vision-pack` skips them.
- **FR digest park (CAST IRON — Plan Agent, every park):** the Plan Agent **must** open an **`fr-digest`** issue on **every** FR park, **even when there is only one child / one step**. Digests are how the operator **filters epics to release** — skipping the digest because the batch is small is forbidden. Same turn:
  1. Ensure the target repo has label **`fr-digest`** (create if missing). Create the **parent digest issue first**: labels **`fr-digest` only** + `hold` (+ `feature-request` if the repo uses it for parks). **Do not** also add label `digest` (duplication; FR #253). Body: `Kind: fr-digest`, link to theme vision + `fr-index-*.md`, short epic/batch summary, **Children** table (one row is fine), `Depends-on: (none)`. Digest is a go-gate / epic filter only — not an implementation ticket. Digest body should say **Unhold this digest to release children.**
  2. Theme vision pack + **one child vision pack per acceptance row** (anti-omnibus). A single-child park still gets the digest + that one child. Validate each child with `validate-vision-pack.py`. Index file is `fr-index-*.md`.
  3. Create each **dependent** issue (implementation children **and** nested/phase digests) with **`feature-request` only** — **no `hold`** by default — plus plain `Depends-on: #<parent-digest>` and any intra-batch `Depends-on: #N` / `owner/repo#N`. Nested digests may carry **`fr-digest` only** (never also `digest`) for epic filtering, but **must not** get `hold`; the parent digest hold + Depends-on is what stops Jeeves dispatch. Put Depends-on on the **GitHub issue body** via intake `-Body` / `format_depends_on_park_issue_body.py` (VIS-D2). **VIS-G5 / FR #220 + operator 2026-11-25:** do **not** put `hold` on dependents when they already `Depends-on` a held parent digest.
  4. Patch the digest **Children** table with real issue numbers + titles + vision links. Update the index map the same turn.
  5. Docs-only park PR uses `Refs #digest #child…` (never `Closes`). Leave **only the parent digest** on **`hold`**. Dependents stay offer-blocked via `Depends-on: #<digest>` while that parent is held/OPEN (BOB-G1). **Unhold the parent digest alone** releases dependents. Do not bob-job until the operator unholds / dispatches.
  6. Do **not** copy product issue maps or backlog ids into this skill — only the park procedure.

- **CAST IRON — fr-digest label only (FR #253 / operator 2026-11-25):** Plan digest issues use label **`fr-digest` only**. Do **not** also add `digest` (duplication). Parent: `fr-digest` + `hold` (+ `feature-request` when used). Nested digests: `fr-digest` without `hold`. Same-turn repair: if both labels were stamped, remove `digest` and keep `fr-digest`. Prove with `python tools/check_fr_digest_explain_flag.py` (requires `fr-digest`, rejects dual `digest`+`fr-digest`). Fail-when: Plan dual-stamps `digest` and `fr-digest` on a digest issue.
- **CAST IRON — merge all docs PRs automatically (FR #252 / operator 2026-11-25):** After Plan opens a **docs** PR (vision park, FR index, mocks, skill-doc park, README/docs-only amend), Plan **merges it automatically** without creating or waiting for MRB. Applies to **every** Plan docs PR in the session. Non-docs product/code PRs keep normal MRB when required. Fail-when: Plan leaves docs park PRs open for MRB, or claims the no-MRB exception for non-docs tips.
- **CAST IRON — hold only on the parent digest (operator 2026-11-25):**
 Plan **must** set `hold` **only** on the **parent** `fr-digest`. Dependent issues (implementation FRs **and** nested/phase digests) **do not** get `hold`. Plain `Depends-on: #<parent-digest>` is the dispatch gate — Jeeves must not offer/assign while that Depends-on target is OPEN/held. Fail-when: Plan stamps `hold` on every child or on nested digests “because they are digests”; or removes Depends-on and relies on child `hold` alone.
- **Create parent fr-digest on hold first (VIS-G1 / FR #155):** at every batch park, open the **parent** digest with labels `fr-digest` + `hold` **before** any child issue. Prove with `python tools/check_fr_digest_create_hold.py docs/fixtures/fr-digest-create-hold/park-manifest.json` (fixture under `docs/fixtures/fr-digest-create-hold/`). Fail-when: children before digest, or **parent** digest without hold/fr-digest. Nested digests created later are dependents: `fr-digest` OK, **`hold` forbidden** by default.
- **No double-park dependent hold (VIS-G5 / FR #220):** default dependents = `feature-request` (+ `fr-digest` if nested) + `Depends-on: #<parent-digest>` **without** `hold`. Extra `hold` / `on-hold` only when true intra-batch sequencing needs a second gate beyond the parent — then stamp `**Child-hold (intra-batch):** <reason>` in the body. Prove with `python tools/check_fr_digest_no_double_park.py docs/fixtures/fr-digest-no-double-park/park-manifest.json`. Fail-when: every dependent gets `hold` solely because the parent is held; unhold-parent alone cannot release them.
- **Digest explains vision + docs link + Digest flag (VIS-G4 / FR #190):** when Plan creates the digest issue, the body must open with `Kind: fr-digest` / `Digest: true`, a `## Vision` summary (product intent, success criteria, out of scope), and a stable docs link (**Docs:** / vision pack / index URL) before the Children table. Apply labels **`fr-digest` only** plus `hold` on the parent at create (issues-only; never on PRs). **Do not** dual-stamp `digest` + `fr-digest` (FR #253). Format with `format_fr_digest_explain_flag.py`; prove with `python tools/check_fr_digest_explain_flag.py docs/fixtures/fr-digest-explain-flag/park-stamp.json` (fixture under `docs/fixtures/fr-digest-explain-flag/`). Fail-when: digest is only a child list; missing flag/docs/vision; digest/hold labels on PRs.
- **Children Depends-on digest; digest body lists children (VIS-G2 / FR #156):** after the digest exists, every child issue body must carry `Depends-on: #<digest>` (plus intra-batch `#N` as needed) via `format_depends_on_park_issue_body.py` / `format_fr_digest_children_stamp.py`. Same turn, patch the digest **Children** table so each child `#N` appears (no leftover `(pending)` rows). Prove the pack with `python tools/check_fr_digest_children_stamp.py docs/fixtures/fr-digest-children-stamp/park-stamp.json` (fixture under `docs/fixtures/fr-digest-children-stamp/`). Fail-when: child missing Depends-on digest, or digest body empty of children.
- **FR digest go-gate playbook (VIS-G3):** how Plan parks a batch so children
  stay off the offer queue until a human releases the epic. Distinct from a
  lone `hold` on one FR (that blocks only that issue) and from ordinary
  **CLOSED Depends-on** (child waits until the parent issue is *closed*).
  Digest go-gate = labels `fr-digest` + `hold` on the **parent** digest
  (one held parent per theme); **unhold that parent alone** releases
  dependents (closing the digest is optional; BOB-G1). Nested/phase digests
  are dependents: they may be `fr-digest` but stay **unheld** and use
  `Depends-on: #<parent>`. Order every park:
  1. Create **parent** digest first (`fr-digest`+`hold`, Children table, `Depends-on: (none)`).
  2. Create dependents with `Depends-on: #<digest>` (+ intra-batch `#N` as needed) and **no dependent hold** by default (VIS-G5 / operator 2026-11-25).
  3. Patch digest Children table + `fr-index-*.md` the same turn; docs PR `Refs` only.
  4. Leave **only the parent digest** on `hold` until the operator unholds / dispatches; do not stack dependent `hold` unless `**Child-hold (intra-batch):**` applies.
  Chair/CI: product repos should fail or skip offer when an open child still
  `Depends-on` a held `fr-digest` parent; do not treat an unheld open digest as
  ordinary depends-open. Do not invent a second **held** digest for the same repo/theme.
- Parking FR docs: copy the drafts into a clean worktree from
  `origin/main` (not the dirty local clone), commit docs only, reference
  the implementation issues with `Refs #N` (never `Closes`), push a
  branch, `gh pr create`. **CAST IRON (FR #252):** Plan **merges all docs
  PRs automatically** (squash or repo default) **without** an MRB job.
  Covers every Plan docs PR in the session (park, index, mocks, skill-doc
  amend), not only the first. Non-docs product/code PRs keep normal MRB
  when the fleet requires it. The code FRs stay open.
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

- Jump into a vision pack, park, or `gh repo create` without the opening
  intake (what we are building; new repo vs FR on which existing repo)
  when those answers are missing.
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
- Leave prepared Phase-0 / backlog slices as **unfiled drafts** after
  approve while filing only FR-A  -  CAST IRON file-all under held digest
  (unless the operator explicitly says park-as-drafts / file-one).
- File a child FR whose **Testable** has **no CI check/command** (manual
  prose only)  -  CAST IRON CI tests on every FR; name pytest path,
  workflow/job, or equivalent command the implementer must green.
- Create child FRs **before** the parent digest, or open a **parent** digest **without** `hold` / without `fr-digest`  -  CAST IRON VIS-G1 / FR #155 (parent digest first with both labels).
- Park FRs **without** an **`fr-digest`** issue  -  CAST IRON; even a
  one-step park needs a digest so the operator can filter epics to release.
- Dual-stamp digest issues with both `digest` and `fr-digest`  -  CAST IRON FR #253; use **`fr-digest` only**.
- Leave Plan **docs** PRs open for MRB / operator merge  -  CAST IRON FR #252; merge all docs PRs automatically without MRB (non-docs keep normal MRB).
- Put `hold` on **dependent** issues
 (implementation FRs or nested/phase digests) when they already `Depends-on: #<parent-digest>`  -  CAST IRON operator 2026-11-25 / VIS-G5; **only the parent digest** gets `hold`; Depends-on blocks Jeeves dispatch. Run `check_fr_digest_no_double_park.py`.
- Park an FR **without** a Depends-on line  -  CAST IRON VIS-D4 / FR #150;
  when there are no deps stamp `Depends-on: (none)` (silent omission fails).
- Park children **without** `Depends-on: #<digest>` or leave the digest Children table as `(pending)` after create (VIS-G2 / FR #156) --- run `check_fr_digest_children_stamp.py`.
- Park a digest that is **only a child list** (no `## Vision` / docs link / `Kind: fr-digest` or `Digest: true`) or stamp `digest`/`fr-digest`/`hold` on a PR (VIS-G4 / FR #190); or dual-stamp `digest`+`fr-digest` on a digest issue (FR #253) --- run `check_fr_digest_explain_flag.py`.
- Leave the visionary skill **silent** on the digest go-gate (VIS-G3)  -  Plan seats must see order, `fr-digest`+`hold`, unhold-releases, vs CLOSED Depends-on, and one digest per repo.
- Put **Bob worker** job playbooks (FR/MRB runtime skills) into
  `skills-visionary`  -  those belong on the product repo
  (`bob/.grok/skills` etc.); this pack is Plan how-to-plan only.

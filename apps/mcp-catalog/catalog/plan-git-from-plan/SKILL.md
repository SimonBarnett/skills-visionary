---
name: plan-git-from-plan
description: >
  After an approved TipForm Plan (vision pack LOCKED), create the product
  git repo, point Bob git webhooks, and enable PR workflow — without
  installing the full agentic_build or agentic_irc skill packs. Use when
  Plan → Grok/Cursor seats finish a new-product plan, park new product,
  or /plan-git-from-plan. Steps: plan-create-repo, plan-bob-webhooks,
  plan-enable-prs. Vision content: visionary. Feature requests on an
  existing repo skip create.
---

# Plan → git setup (orchestrator)

> **CAST IRON RULE - HARVEST AND FILE EVERYTHING (read this first, every time).**
> 1. ALWAYS harvest skills you learn and file EVERY issue / FR / bug / gap you find to the intake webhook in the
>    SAME turn. Never leave a finding unfiled, never "note it for later", never skip it because it is small.
> 2. File with the intake webhook (no secret or login needed; `POST https://bob.ntsa.uk/bob/v1/intake`; offline it is
>    queued locally and retried):
>    `..\scripts\Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary -Kind issue -Title "short title" -Body "what / where / evidence / fix"`
>    (`-Kind issue|fr|skill|harvest`; always pass an explicit `-Repo owner/name`).
>    How-to-plan / Plan process lessons use **`-Repo SimonBarnett/skills-visionary`** (FR #42 / #3318 / #3506 / #3667).
>    Use `-Repo SimonBarnett/bobiverse` only for fleet-tooling docs (worker, Jeeves, tray, intake), never for Plan playbooks.
> 3. BEFORE finishing ANY debugging session run the harvest step:
>    `..\scripts\Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary -Summary "what broke / what fixed it" -Lesson "one learned playbook line"`
>    then `..\scripts\Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary -Flush` to resend anything that was queued while offline.
> 4. Never put a token, password, SASL/NickServ secret, key or private hostname in a filing, a skill or a log.

TipForm **Plan** seats load **skills-visionary only**. This skill is the
self-contained bridge that used to live inside `agentic_build`
`bob-spec-intake` (create + webhook + Cursor app). Fleet build/IRC jobs
stay in their packs; Plan does not install them.

## When to run

**New product** — vision pack approved this session, validator green,
no target repo yet.

**Feature request** — do **not** run create. Confirm target repo; commit
FR markdown + mocks there; open the GitHub issue. Webhook/Cursor app
should already exist on that repo.

## New-product sequence (same turn)

0. **Visionary** — skill `visionary`. Fill `docs/templates/vision.md`.
   Refuse until shape + success LOCKED or UNKNOWN **and**

```
python tools/validate-vision-pack.py docs/vision.md --mocks-dir docs/mocks
```

   exits 0 (product `tools/` else sister clone of this repo).

1. **Create repo** — skill `plan-create-repo`.
   `gh repo create SimonBarnett/<name> --public`.

2. **Bob git webhook** — skill `plan-bob-webhooks`.
   Hook URL `https://bob.ntsa.uk/bob/v1/git` only.
   Digest `https://bob.ntsa.uk/bob/v1/report` is not a GitHub hook.
   **Gate:** `python tools/bob_git_hook.py SimonBarnett/<name>` must exit 0
   (exact hook config, ping 2xx, Jeeves `GIT ping` seen) **before step 4**.
   No push and no issue until it does. Anything earlier is never delivered.

3. **Permit PRs** — skill `plan-enable-prs`.
   Forking on; no blocking ruleset; Cursor GitHub App All repositories
   (Contents + Pull requests Read and write).
   Auto-merge on (`gh api -X PATCH repos/SimonBarnett/<name> -F allow_auto_merge=true`),
   and the `required-ci-3948` ruleset (CI checks only, not strict,
   admin bypass) once a CI workflow runs on every PR (bobiverse#3948).

4. **First commit** (still this seat / orchestrator):

   - `docs/vision.md`
   - `docs/mocks/*.html` (when UI)
   - `docs/functional-spec.md` (LOCKED pulled from vision)
   - If the product is a skill pack: **honesty box foundation**
     `.grok/skills/harvest-agent-skills/SKILL.md` with frontmatter
     `github:` set to **this new product repo** (same pattern as
     agentic_build). AUTOMATIC harvest of later learnings is PR-only.

5. **CAST IRON — held digest + all child FRs** (visionary file-all):
   - Ensure labels `feature-request`, `fr-digest`, `hold` exist
     (`gh label create … --force`).
   - Push the vision commit first (webhook already green).
   - Create **Digest:** parent with labels `feature-request` +
     `fr-digest` + `hold`, body `Depends-on: (none)`, Children table,
     “Unhold this digest to release children.”
   - File **every** prepared Phase-0 / backlog slice as its own issue
     (anti-omnibus: one Goal/Deliverables/Testable each). Each child
     starts with plain `Depends-on: #<digest>` plus prior-slice
     `Depends-on: #N` / `owner/repo#N` so workers never NACK blocked
     work. Cross-repo children (e.g. bobiverse vendor) use
     `Depends-on: SimonBarnett/<product>#<digest>`.
   - Patch the digest Children table with real numbers the same turn.
   - Confirm Jeeves announced digest + children on `#bobiverse`
     (gitannounce / `bob_git_hook.py --replay-missed` if needed).
   - **Fail-when:** only FR-A filed and the rest left as unfiled drafts
     (unless the operator explicitly said park-as-drafts / file-one).

6. **Stop for Plan seats.** Do not run `bob-job-loop` /
   `bob-build-dispatch` unless a build seat with the build pack is
   intentionally next. Plan's job ends when git + hooks + PR path are
   ready, the vision pack is on the remote, and the **held digest +
   all child FRs** are filed. Operator unholds the digest to release.

## Quick command checklist

```
# 0 validator
python tools/validate-vision-pack.py docs/vision.md --mocks-dir docs/mocks

# 1 create
gh repo create SimonBarnett/<name> --public --description "<objective>"

# 2 webhook + verify (gate: before ANY push/issue)
python tools/bob_git_hook.py SimonBarnett/<name>

# 3 auto-merge (bobiverse#3948); required-ci-3948 ruleset once CI runs on PRs (see plan-enable-prs)
gh api -X PATCH repos/SimonBarnett/<name> -F allow_auto_merge=true

# 4 Cursor app pages (Simon clicks All repositories if needed)
powershell -NoProfile -ExecutionPolicy Bypass -File tools\Grant-CursorGitHubApp.ps1
```

## Honesty / harvest

These playbooks were harvested from `agentic_build` (and webhook URL
docs shared with `agentic_irc` / bobiverse). Changes land as PRs on
`SimonBarnett/skills-visionary` via `harvest-skills-visionary`. Do not
leave Plan-only git setup only in `~/.grok/skills`.

**FR #42:** every `Report-BobiverseIntakeIssue` / `Invoke-BobiverseHarvest`
example in this Plan skill uses `-Repo SimonBarnett/skills-visionary`.
Never cite `-Repo SimonBarnett/bobiverse` for how-to-plan harvest.

## Do not

- Install all of `agentic_build` or `agentic_irc` onto Plan seats.
- `gh repo create` on an FR path.
- Point GitHub at `/bob/v1/report`.
- Put secrets in git.
- Restart IRC.
- Stamp UAT.
- Add `cursoragent` / `cursor[bot]` as collaborators.

## FR #24: headless Plan, seed FRs, stubs

### Headless Plan (non-interactive)

The tray Plan menu launches interactive `agent.exe --permission-mode plan`.
For headless runs use a **temp working folder** (never the live `D:\ai`
trees), for example:

```text
agent.exe -p "<prompt>" --cwd <skills-visionary clone> --always-approve --max-turns N --output-format streaming-messages-json --leader-socket ~/.grok/leader-<name>.sock --rules "<plan rules>"
```

Redirect stdout to a file (a pipe owned by a short-lived shell gets
orphaned). Optional helper: `tools/Start-PlanHeadless.ps1`.

### Seed FRs from a brief

After the webhook gate exits 0:

1. Create issues **before** committing stubs that cite them (or open a
   follow-up PR that links the numbers). Do not leave `TODO: seed FR #N`
   in the first commit when the issues do not exist yet.
2. Title pattern + labels (`known-issue` / `gate-blocking` as needed);
   pin the headline acceptance FR as #1 when that is the product intent.
3. Space issue creation; keep bodies small (anti-omnibus).
4. **Warning:** new issues go straight into the live fleet unaccepted
   queue and are claimable by workers. Prefer a backlog-only label /
   queue opt-out when seeding a large known-issue list, or warn the
   operator that seeds are live.

### Mermaid

Many small human-scale diagrams (node ceiling + captions). See FR #22 /
PR #92 for the validator/template ceiling; do not ship one huge mermaid
in the vision pack.

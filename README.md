# skills-visionary

Skill pack for **Plan seats**: agents (and humans) who turn a new-product
idea into a measurable vision pack, then create the GitHub repo and wire
Bob webhooks so the fleet can build it.

This pack is **only** the Plan / vision surface. It is not the full IRC
fleet (`agentic_irc`) or the full build pack (`agentic_build`). TipForm
**Plan → Grok/Cursor** seats load these skills so they can lock shape and
success metrics, then run `plan-git-from-plan` without installing
everything else.

Remote: https://github.com/SimonBarnett/skills-visionary  
Vision: [`docs/vision.md`](docs/vision.md)

## What you get

1. **Vision gate** — refuse park / create until shape and success metrics
   are LOCKED (or marked UNKNOWN), with HTML mocks when there is a UI.
2. **Plan-git helpers** — create a public SimonBarnett repo, point Bob at
   git events, and enable outside PRs (including Cursor).
3. **Harvest** — send how-to-plan lessons back here (not plan content).

## Skills

| Skill | Role | When to use |
|-------|------|-------------|
| `visionary` | Measurable vision pack (shape, success, stack, mocks) | New product or large FR; before any park / git-create |
| `plan-git-from-plan` | Orchestrator: create → webhooks → enable PRs | After the vision pack is approved / LOCKED |
| `plan-create-repo` | Public `gh repo create` under SimonBarnett | Step 1 of plan-git (or alone when only the empty repo is needed) |
| `plan-bob-webhooks` | GitHub hook → Bob `/bob/v1/git` | Step 2 of plan-git; any new product repo that needs fleet git events |
| `plan-enable-prs` | Forking / no blocking ruleset / Cursor app | Step 3 of plan-git; when `cursor[bot]` cannot open PRs |
| `harvest-skills-visionary` | PR learnings back to this repo | After a Plan session teaches a reusable how-to-plan rule |

## Install (copy into agent home)

No secrets. Copy the skill folders into the agent skills tree:

```text
xcopy /E /I /Y .grok\skills %USERPROFILE%\.grok\skills
```

Or copy individual folders under `%USERPROFILE%\.grok\skills\`.
For the full plan-git path, copy `visionary`, `plan-git-from-plan`,
`plan-create-repo`, `plan-bob-webhooks`, and `plan-enable-prs` (or copy
the whole `.grok/skills` tree).

## Bob URLs (no secrets)

Use the Bob fleet host **`bob.ntsa.uk`**:

| Role | URL |
|------|-----|
| GitHub webhook | `https://bob.ntsa.uk/bob/v1/git` |
| Digest report (not a GitHub hook) | `https://bob.ntsa.uk/bob/v1/report` |

Never point a GitHub webhook at `/bob/v1/report`. That path is for fleet /
TipForm digest merge (`reportUrl` in the build pack
`agentic_build/config/bobiverse.json`).

Helpers in this repo:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File tools\New-BobGitWebhook.ps1 -Repo SimonBarnett/<name> -HookUrl https://bob.ntsa.uk/bob/v1/git
powershell -NoProfile -ExecutionPolicy Bypass -File tools\Grant-CursorGitHubApp.ps1
```

## Upcoming: plan.ntsa.uk

A public Plan landing page and MCP are planned:

| Surface | URL | Status |
|---------|-----|--------|
| Landing | `https://plan.ntsa.uk` | Upcoming (Amplify + DNS via Slab) |
| MCP | `https://plan.ntsa.uk/mcp` | Upcoming (catalog of these skills) |

Until that is live, use this GitHub repo and the copy/xcopy install above.
Sibling FRs cover the DAG, Next.js MCP app, Amplify, and smoke tests.

## Vision-pack gate

Before create or park, run the validator (no need to open `SKILL.md`).
From a product repo, invoke the script from a checkout of this pack;
keep `docs/vision.md` and `--mocks-dir` relative to the product repo:

```text
python /path/to/skills-visionary/tools/validate-vision-pack.py docs/vision.md --mocks-dir docs/mocks
```

CI: `.github/workflows/vision-pack.yml`.

## Harvest honesty

Reusable how-to-plan playbooks land here as PRs — see
[`docs/skill-harvest-log.md`](docs/skill-harvest-log.md). Plan content
(requirements, designs, FR lists) stays in the plan folder / product
`docs/vision.md`, not in skill books.

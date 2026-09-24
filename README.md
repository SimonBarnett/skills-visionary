# skills-visionary

High-reasoning new-product intake skill pack for TipForm **Plan →
Grok/Cursor** seats. See `docs/vision.md`.

Plan seats load **this pack only** (not the full `agentic_build` /
`agentic_irc` packs). Enough build surface to create git from a plan is
harvested here as self-contained `plan-*` skills.

## Skills

| Skill | Role |
|-------|------|
| `visionary` | Measurable vision pack (shape, success, stack, mocks) |
| `plan-git-from-plan` | Orchestrator: after plan approved → create → webhooks → PRs |
| `plan-create-repo` | Public `gh repo create` under SimonBarnett |
| `plan-bob-webhooks` | GitHub hook → `https://irc.ntsa.uk/bob/v1/git` |
| `plan-enable-prs` | Forking / no blocking ruleset / Cursor app for `cursor[bot]` |
| `harvest-skills-visionary` | PR learnings back to this repo |

Copy into the agent home (example):

```
xcopy /E /I /Y .grok\skills %USERPROFILE%\.grok\skills
```

Or copy individual skill folders under `%USERPROFILE%\.grok\skills\`.

## Bob URLs (no secrets)

| Role | URL |
|------|-----|
| GitHub webhook | `https://irc.ntsa.uk/bob/v1/git` |
| Digest report (not a GitHub hook) | `https://irc.ntsa.uk/bob/v1/report` |

`reportUrl` source in the build pack: `agentic_build/config/bobiverse.json`.

Helpers:

```
powershell -NoProfile -ExecutionPolicy Bypass -File tools\New-BobGitWebhook.ps1 -Repo SimonBarnett/<name>
powershell -NoProfile -ExecutionPolicy Bypass -File tools\Grant-CursorGitHubApp.ps1
```

## Vision-pack gate

Before create or park, run the validator:

```
python tools/validate-vision-pack.py docs/vision.md --mocks-dir docs/mocks
```

CI: `.github/workflows/vision-pack.yml`.

## Harvest honesty

Playbooks stolen from `agentic_build` (`bob-spec-intake`,
`setup-github-webhooks`, `setup-github-cursor`, digest URL notes) land
as PRs here — see `docs/skill-harvest-log.md`.

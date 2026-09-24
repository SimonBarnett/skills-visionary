# Skill harvest log

## 2026-09-23 - repo intake

New public repo SimonBarnett/skills-visionary. Vision pack + HTML
mocks + harvest skill as foundation. Home: `visionary`.

## 2026-09-23 - visionary on feature requests (#2)

Visionary required on FR path; success gate before dispatch; no
`gh repo create` on FR. Sync `agentic_build` `.grok/skills/visionary`
and `bob-spec-intake` Feature request step (CAST IRON).

## 2026-09-24 - plan-git from build (Plan seats)

Harvest minimal git-setup surface into this pack so TipForm Plan->Grok/Cursor
seats load **visionary only** (no full agentic_build / agentic_irc install).

Added skills:

- `plan-git-from-plan` - orchestrator after approved plan
- `plan-create-repo` - from `agentic_build` `bob-spec-intake` New GitHub repo (create half)
- `plan-bob-webhooks` - from `agentic_build` `setup-github-webhooks` (+ digest URL table from `bob-digest-webhook` / `config/bobiverse.json`)
- `plan-enable-prs` - from `agentic_build` `setup-github-cursor` + public-PR rules in `bob-spec-intake`

Helpers: `tools/New-BobGitWebhook.ps1`, `tools/Grant-CursorGitHubApp.ps1`
(adapted from `agentic_build/tools/Grant-CursorGitHubApp.ps1`).

Updated `visionary` Park path to call `plan-git-from-plan` instead of
depending on build-pack `bob-spec-intake` for create/webhook/Cursor.

URLs (no secrets): git `https://irc.ntsa.uk/bob/v1/git`, report
`https://irc.ntsa.uk/bob/v1/report`.

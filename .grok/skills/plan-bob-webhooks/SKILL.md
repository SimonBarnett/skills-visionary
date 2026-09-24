---
name: plan-bob-webhooks
description: >
  Point a SimonBarnett GitHub repo at Bob fleet webhooks (git events to
  /bob/v1/git). Use when a new plan-created repo needs hooks, set up
  webhooks on git, GitHub hook, or /plan-bob-webhooks. Digest report URL
  is documented here for Plan seats but is NOT the GitHub hook target.
  Orchestrator: plan-git-from-plan. Source harvest: agentic_build
  setup-github-webhooks + bobiverse.json reportUrl.
---

# Bob webhooks from plan (Plan seats)

Self-contained harvest from `agentic_build` skills
`setup-github-webhooks` and `bob-digest-webhook` (URL table only).
No IRC restart. No digest producer code.

## Two different Bob URLs (do not mix)

| Role | URL | Who uses it |
|------|-----|-------------|
| **GitHub webhook** (this skill) | `https://irc.ntsa.uk/bob/v1/git` | GitHub → Jeeves `GIT ...` on `#bobiverse` |
| **Digest report** (document only) | `https://irc.ntsa.uk/bob/v1/report` | Fleet / TipForm GET+POST `op=merge`; `config/bobiverse.json` `reportUrl` |

Never point a GitHub hook at `/bob/v1/report` (that path expects
`X-Bob-Secret` digest merges). Never HMAC/webhook secret in git,
issues, or channel.

Source of truth for reportUrl in the build pack:
`agentic_build/config/bobiverse.json` → `"reportUrl": "https://irc.ntsa.uk/bob/v1/report"`.

## Events

`push`, `pull_request`, `issues`. JSON body. `insecure_ssl` = `0`
(receiver must already be HTTPS).

## One repo

Write `hook.json` UTF-8 **without BOM**:

```
{"name":"web","active":true,"events":["push","pull_request","issues"],"config":{"url":"https://irc.ntsa.uk/bob/v1/git","content_type":"json","insecure_ssl":"0"}}
```

PowerShell `ConvertTo-Json` often adds a BOM and GitHub returns 400
"Problems parsing JSON". Prefer:

```powershell
$json = '{"name":"web","active":true,"events":["push","pull_request","issues"],"config":{"url":"https://irc.ntsa.uk/bob/v1/git","content_type":"json","insecure_ssl":"0"}}'
[IO.File]::WriteAllText("$PWD\hook.json", $json, [Text.UTF8Encoding]::new($false))
gh api repos/SimonBarnett/<name>/hooks -X POST --input hook.json
```

Or use this pack's helper:

```
powershell -NoProfile -ExecutionPolicy Bypass -File tools\New-BobGitWebhook.ps1 -Repo SimonBarnett/<name>
```

## List / skip if present

```
gh api repos/SimonBarnett/<name>/hooks --jq '.[].config.url'
```

If `https://irc.ntsa.uk/bob/v1/git` is already there, do not create a
second hook. Leave other hooks (Amplify, etc.) in place.

## Check

- Hook `config.url` is `https://irc.ntsa.uk/bob/v1/git`
- `insecure_ssl` is `0`
- Create sends a `ping`; delivery `status_code` 204 is OK
- GET `https://irc.ntsa.uk/bob/v1/git` is 405 (POST only)

```
gh api repos/SimonBarnett/<name>/hooks/<id>/deliveries --jq '.[0] | {event,status,status_code}'
```

## Do not

- Point GitHub at `/bob/v1/report`.
- Put hook secrets in git.
- Replace unrelated hooks.
- Restart IRC / touch chair.
- Stamp UAT.
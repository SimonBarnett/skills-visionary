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

> **CAST IRON RULE - HARVEST AND FILE EVERYTHING (read this first, every time).**
> 1. ALWAYS harvest skills you learn and file EVERY issue / FR / bug / gap you find to the intake webhook in the
>    SAME turn. Never leave a finding unfiled, never "note it for later", never skip it because it is small.
> 2. File with the intake webhook (no secret or login needed; `POST https://bob.ntsa.uk/bob/v1/intake`; offline it is
>    queued locally and retried):
>    `..\scripts\Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary -Kind issue -Title "short title" -Body "what / where / evidence / fix"`
>    (`-Kind issue|fr|skill|harvest`; always pass an explicit `-Repo owner/name`).
>    How-to-plan / Plan process lessons use **`-Repo SimonBarnett/skills-visionary`** (FR #42).
>    Use `-Repo SimonBarnett/bobiverse` only for fleet-tooling docs, never for Plan playbooks.
> 3. BEFORE finishing ANY debugging session run the harvest step:
>    `..\scripts\Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary -Summary "what broke / what fixed it" -Lesson "one learned playbook line"`
>    then `..\scripts\Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary -Flush`.
> 4. Never put a token, password, SASL/NickServ secret, key or private hostname in a filing, a skill or a log.

Self-contained harvest from `agentic_build` skills
`setup-github-webhooks` and `bob-digest-webhook` (URL table only).
No IRC restart. No digest producer code.

## Two different Bob URLs (do not mix)

| Role | URL | Who uses it |
|------|-----|-------------|
| **GitHub webhook** (this skill) | `https://bob.ntsa.uk/bob/v1/git` | GitHub → Jeeves `GIT ...` on `#bobiverse` |
| **Digest report** (document only) | `https://bob.ntsa.uk/bob/v1/report` | Fleet / TipForm GET+POST `op=merge`; `config/bobiverse.json` `reportUrl` |

Never point a GitHub hook at `/bob/v1/report` (that path expects
`X-Bob-Secret` digest merges). Never HMAC/webhook secret in git,
issues, or channel.

Source of truth for reportUrl in the build pack:
`agentic_build/config/bobiverse.json` → `"reportUrl": "https://bob.ntsa.uk/bob/v1/report"`.

## Gate: hook BEFORE any push or issue (required)

Tracks FR **#19** (and closes the club-madeira-onboarding miss): Plan
must leave a new repo fully wired into Bob Fleet before any issue or PR.

GitHub never backfills: anything pushed or opened before the hook exists
is never delivered, so Jeeves never announces it and the FR issue never
reaches the unaccepted queue. (club-madeira-onboarding 25/09: repo 08:03:30Z,
first commit 08:03:43Z, issue #1 08:04:00Z, hook 08:04:21Z, so repo and
issue #1 were silent on `#bobiverse`.)

Run this right after `gh repo create`, before the first push, and
before `gh issue create`:

```
python tools/bob_git_hook.py SimonBarnett/<name>
```

It is the single source of truth for the hook and exits 0 only when:

1. The hook matches the fleet config **exactly** (creates it if absent, PATCHes
   drift, never adds a second one, leaves unrelated hooks alone):
   url `https://bob.ntsa.uk/bob/v1/git`, `content_type` `json`,
   `insecure_ssl` `0`, events `issues`,`pull_request`,`push`,`issue_comment`,
   active (FR #4711 when the receiver supports comment events).
2. A `ping` delivery returned **2xx** (the receiver answers 204).
3. Items opened before the hook existed are replayed as `opened` events
   (automatic when this run created the hook; else `--replay-missed`).
4. Jeeves' `GIT ping SimonBarnett/<name>` (and each replayed
   `GIT issues|pull_request ... opened #N`) line is seen in a local
   `#bobiverse` `irc.log` (default candidates include
   `~/.agentic-irc-gitannounce/irc.log` and
   `~/.agentic-irc-bobiverse/irc.log`), or the replayed item is in the
   digest unaccepted queue.

Exit 1 = hook or ping failed; exit 2 = Jeeves announce not seen. Either
way, **webhook setup is NOT done**. Do not tell the human it is, and do
not push or open the issue yet. **Do not weaken this gate.**

Fix for a repo that was already set up late (after the fact):

```
python tools/bob_git_hook.py SimonBarnett/<name> --replay-missed
```

## Secret handling

Fleet hooks (agentic_build, agentic_irc, AgentMonitor, skills-visionary)
carry **no** webhook secret; the `/bob/v1/git` receiver does not check
HMAC. Match that. `--secret-file <path>` exists only for a future signed
receiver. The value is read from the file and never printed. Never type
a secret on a command line, in chat, in git, or in an issue.

## Events

`push`, `pull_request`, `issues`. JSON body. `insecure_ssl` = `0`
(receiver must already be HTTPS).

## One repo

Write `hook.json` UTF-8 **without BOM**:

```
{"name":"web","active":true,"events":["push","pull_request","issues"],"config":{"url":"https://bob.ntsa.uk/bob/v1/git","content_type":"json","insecure_ssl":"0"}}
```

PowerShell `ConvertTo-Json` often adds a BOM and GitHub returns 400
"Problems parsing JSON". Prefer:

```powershell
$json = '{"name":"web","active":true,"events":["push","pull_request","issues"],"config":{"url":"https://bob.ntsa.uk/bob/v1/git","content_type":"json","insecure_ssl":"0"}}'
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

If `https://bob.ntsa.uk/bob/v1/git` is already there, do not create a
second hook. Leave other hooks (Amplify, etc.) in place.

## Check

`python tools/bob_git_hook.py SimonBarnett/<name>` is the check (see Gate).
Manual spot-checks:

```
gh api repos/SimonBarnett/<name>/hooks/<id>/deliveries --jq '.[0] | {event,status,status_code}'
```

- GET `https://bob.ntsa.uk/bob/v1/git` is 405 (POST only)

## Do not

- Push, commit to the remote, or open an issue/PR before `bob_git_hook.py` exits 0.
- Declare setup done on a 2xx ping alone; the Jeeves announce is required too.

- Point GitHub at `/bob/v1/report`.
- Put hook secrets in git.
- Replace unrelated hooks.
- Restart IRC / touch chair.
- Stamp UAT.

## FR #24: prefer bob_git_hook; ANSI; filtered 400

- Prefer `python tools/bob_git_hook.py SimonBarnett/<name>` (exit 0) as
  the gate. `New-BobGitWebhook.ps1` is a fallback for creating the hook
  JSON only; it does not replace the announce/ping gate.
- When calling `gh api` from Python without a TTY, set `NO_COLOR=1`
  and `GH_FORCE_TTY=0` (`bob_git_hook.default_gh` does this and strips
  ANSI). Otherwise colored `[]` breaks `json.loads`.
- Receiver secret filter (agentic_irc #206): issue/PR/commit text with
  certain marker strings is rejected by `/bob/v1/git` with HTTP 400 and
  never announced. Avoid those markers until #206 lands. Treat a 400
  delivery as **filtered**, not as a missing hook.

## FR #25: irc.log nick reserved preflight

Before `gh repo create` / the webhook gate:

1. Confirm a local `#bobiverse` `irc.log` is receiving Jeeves
   `PRIVMSG #bobiverse` lines (not only `NICKNAME_RESERVED`). Nick
   compare is case-insensitive (`:Jeeves!` or `:jeeves!` — FR #228).
2. If the local ear nick is reserved, fix the nick (or use another
   machine's log via `--irc-log`) so announce_seen can work.
3. Fallback: when GitHub records a **2xx ping** delivery and the local
   log shows nick-reserved, `bob_git_hook.py` accepts the **ping**
   announce via that delivery (still exit 0 only when all needles clear).
   Replay items still use the digest-queue fallback.
4. Keep **refuse-to-push / refuse-to-open-issue** until the gate exits 0.

## FR #88: gitannounce listen when ircBob holds the ear nick

When `ircBob` is Running as `Bob-<machine>` (NickServ `bob-<machine>`), a
second client that tries `bob-<machine>` / `bob-<machine>_l` without that
SASL gets `NICKNAME_RESERVED` and never joins. Then
`~/.agentic-irc-bobiverse/irc.log` only shows 433 loops and
`bob_git_hook.py` stays **exit 2** even after ping 204. **Do not weaken
the announce gate.**

Repair (keep the gate):

1. Seed Ergo guest PASS once (never print or commit the value):

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.grok\ergo" | Out-Null
# Copy from the local bob install only when the guest PASS file is missing:
#   Copy-Item -Force <ai root>\bob\config\ergo.password "$env:USERPROFILE\.grok\ergo\connect.password"
# Prefer an existing ~/.grok/ergo/connect.password. Never invent an Ergo PASS.
```

2. Start a free-nick listener into a dedicated home:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools\Start-BobiverseGitAnnounceListen.ps1
# wait until ~/.agentic-irc-gitannounce/irc.log shows JOIN #bobiverse
python tools/bob_git_hook.py SimonBarnett/<name> --irc-log $env:USERPROFILE\.agentic-irc-gitannounce\irc.log
```

Use nick `gitannounce-<machine>` with **server PASS only** (no ear
NickServ). Prefer `C:\ai\bob\scripts\irc_agent.py` with `BOB_IRC_PASSWORD`
from `~/.grok\ergo\connect.password`. Never mint a fresh NickServ GUID
for a registered `bob-*` account. Pack copy of the helper:
`tools/Start-BobiverseGitAnnounceListen.ps1` (also under `plan-agent/tools/`).

Default log candidates already include
`~/.agentic-irc-gitannounce/irc.log` then
`~/.agentic-irc-bobiverse/irc.log`.

If the listen log shows `JOIN #bobiverse` and no `NICKNAME_RESERVED`, but
`bob_git_hook.py` still exits 2 with zero Jeeves PRIVMSG lines, the chair
is not draining `chair-outbox.txt` — fix the chair; do not weaken this
gate.

`gh pr create` from a non-default branch needs `--head <branch>` when
GitHub cannot infer the head.

## FR #42: harvest repo for Plan process

How-to-plan harvest / intake examples use `-Repo SimonBarnett/skills-visionary`.
Do not cite `-Repo SimonBarnett/bobiverse` for Plan playbooks (fleet tooling only).

**Plan-seat sync:** after a skills-visionary harvest merges, copy tip
`.grok/skills/*` onto `<ai root>\bob\plan\.grok\skills\` (include
`plan-mcp-setup` when missing). Never promote a stale seat copy that
still shows honesty-box `-Repo SimonBarnett/bobiverse` for Plan process
lessons back onto tip.

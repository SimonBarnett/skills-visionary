# Feature request: Plan wires Bob webhooks before first issue/PR

**Issue:** [#19](https://github.com/SimonBarnett/skills-visionary/issues/19)  
**Related:** [#18](https://github.com/SimonBarnett/skills-visionary/pull/18) (implementation), [#17](https://github.com/SimonBarnett/skills-visionary/issues/17) (PS 5.1 webhook script)

## Ultimate objective

When Plan creates a new `SimonBarnett` product repo, the Bob GIT webhook
must be live and verified **before** any push, issue, or PR. Otherwise
GitHub never delivers those events and Jeeves never announces them on
`#bobiverse` (club-madeira-onboarding 2026-09-25).

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Hook gate before first push/issue | `python tools/bob_git_hook.py SimonBarnett/<name>` exits 0 after `gh repo create` and before any push or issue | `plan-create-repo` / `plan-bob-webhooks` / `plan-git-from-plan` skill order; `python -m pytest tests/test_bob_git_hook.py` | Skills allow first commit/issue before tool exit 0 |
| S2 | Exact fleet hook shape | URL `https://irc.ntsa.uk/bob/v1/git`; events `issues,pull_request,push`; JSON; `insecure_ssl=0`; active; no secret | `tools/bob_git_hook.py` create/PATCH; unit tests | Wrong URL, missing events, or secret set |
| S3 | Ping delivery 2xx | latest ping delivery status 2xx before exit 0 | tool `_require_ping`; tests | Exit 0 with failed/missing ping |
| S4 | Pre-hook items replayed | open issues/PRs older than hook get synthetic `opened` replay | `--replay-missed` / auto on create; tests | Pre-hook FR silent forever |
| S5 | Jeeves announce required | `GIT ...` on `#bobiverse` (or digest unaccepted for replays) before exit 0 | tool announce wait; exit 2 on timeout; tests | Exit 0 while Jeeves silent |
| S6 | PR path + label | forking on; no blocking ruleset; Cursor app path; `feature-request` label before first issue | `plan-enable-prs` + orchestrator; pytest skill assertions | Label missing; fork blocked |
| S7 | CI validates this FR pack | `python tools/validate-vision-pack.py docs/feature-request-plan-bob-webhooks-before-first-issue-2026-09-25.md --mocks-dir docs/mocks` exits 0 | local CLI + GHA vision-pack workflow | Pack missing Shape/Success; CI red |

LOCKED

## Shape

Reuse repo primary: **service** (skill-pack playbook). This FR tightens Plan
intake tooling and skills. No website or app.

LOCKED

## Stack

- `tools/bob_git_hook.py` + `tests/test_bob_git_hook.py`
- Skills: `plan-bob-webhooks`, `plan-create-repo`, `plan-git-from-plan`, `plan-enable-prs`
- Validator: `tools/validate-vision-pack.py` (existing)

## Gap vs tree before this FR

- Skills described hook setup but allowed first commit/issue first.
- No verified gate (exact fleet hook + ping 2xx + Jeeves announce).
- No replay path for items opened before the hook existed.
- `feature-request` label often missing on brand-new repos.
- Parked FR markdown omitted Shape/Success so vision-pack CI failed.

## Acceptance (LOCKED)

| ID | Criterion |
|----|-----------|
| A1 | After `gh repo create`, `python tools/bob_git_hook.py SimonBarnett/<name>` exits 0 before any push/issue |
| A2 | Hook URL `https://irc.ntsa.uk/bob/v1/git`, events `issues,pull_request,push`, JSON, `insecure_ssl=0`, active, no secret (fleet standard) |
| A3 | Ping delivery 2xx required |
| A4 | Pre-hook open issues/PRs replayed as `opened` when needed (`--replay-missed` or auto on create) |
| A5 | Jeeves `GIT ...` on `#bobiverse` required (or digest unaccepted for replays); else exit 2 — setup not done |
| A6 | `plan-enable-prs`: forking on, no blocking ruleset, Cursor app path, `feature-request` label created |
| A7 | Tests cover hook create/PATCH, ping, replay, announce-timeout, and skill gate order |
| A8 | This FR pack passes `validate-vision-pack.py` (Shape + Success LOCKED) |

## Implementation

- `tools/bob_git_hook.py` + `tests/test_bob_git_hook.py`
- Skills: `plan-bob-webhooks`, `plan-create-repo`, `plan-git-from-plan`, `plan-enable-prs`

# Feature request: Plan wires Bob webhooks before first issue/PR

**Issue:** [#19](https://github.com/SimonBarnett/skills-visionary/issues/19)  
**Related:** [#18](https://github.com/SimonBarnett/skills-visionary/pull/18) (implementation), [#17](https://github.com/SimonBarnett/skills-visionary/issues/17) (PS 5.1 webhook script)

## Summary

When Plan creates a new `SimonBarnett` product repo, the Bob GIT webhook
must be live and verified **before** any push, issue, or PR. Otherwise
GitHub never delivers those events and Jeeves never announces them on
`#bobiverse` (club-madeira-onboarding 2026-09-25).

## Gap vs tree before this FR

- Skills described hook setup but allowed first commit/issue first.
- No verified gate (exact fleet hook + ping 2xx + Jeeves announce).
- No replay path for items opened before the hook existed.
- `feature-request` label often missing on brand-new repos.

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

## Implementation

- `tools/bob_git_hook.py` + `tests/test_bob_git_hook.py`
- Skills: `plan-bob-webhooks`, `plan-create-repo`, `plan-git-from-plan`, `plan-enable-prs`

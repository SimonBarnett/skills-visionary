# FR: executable vision-pack gate and CI

**GitHub issue:** https://github.com/SimonBarnett/skills-visionary/issues/6
**Date:** 2026-09-23
**Source:** `cursor[bot]` visionary review of `main` (body cites `20617e4`; flamingo parks from `b9913fc`).
**Repo:** `SimonBarnett/skills-visionary`
**Skill:** `visionary` (this pack). Separate from #1 (pack park), #2/#4 (FR required).

## Ultimate objective

Every SimonBarnett vision pack fails a repeatable command (and CI) when shape or success is missing, so intake cannot rely on each agent reading the prose gate.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Vision pack has a local validator | one command, exit 0/1 | documented command in README + this FR; `bob-spec-intake` called out as the call site | Gate remains prose-only in SKILL.md |
| S2 | Shape gate is deterministic | fail unless valid primary shape + LOCKED, or explicit UNKNOWN | validator on fixtures | Copied-unfilled template or missing shape still exits 0 |
| S3 | Success gate is deterministic | fail unless Success is UNKNOWN, or >=1 row with metric, target, how-measured, fail-when | validator on fixtures | Partial/empty success row exits 0 |
| S4 | Mock gate | required key/empty/error HTML present; reject PNG-only | validator on fixtures | Missing HTML or PNG-only exits 0 |
| S5 | Untouched template fails | `docs/templates/vision.md` copy is a negative fixture | CI + local | Untouched template exits 0 |
| S6 | CI runs the validator | GHA on this repo's pack + fixtures | workflow file | No workflow, or only lint |
| S7 | S1 in `docs/vision.md` names the command | how-measured cites validator/CI | file content | S1 still says "check file contents" only |

LOCKED

## Shape

Reuse repo primary: **service** (skill-pack playbook). This FR adds a CLI/CI gate, not a website or app.

LOCKED

## Stack

Default: small validator in-repo (Python already used by fleet, or PowerShell if Windows-only hermetic), GitHub Actions on `ubuntu-latest` + fixtures under `tests/` or `docs/fixtures/`.

Why: no new SaaS; public repo already has Actions.

Why-not: do not invent a web UI, PNG pipeline, or extra runtime.

LOCKED

## Architecture

```
vision.md / FR vision pack
  --> validate-vision-pack (local CLI)
        fail: shape / success / mocks
  --> GitHub Actions (same CLI on pack + fixtures)
  --> bob-spec-intake refuses park/dispatch unless CLI exit 0
```

No secrets. No instance URLs.

LOCKED

## Screens

No new UI. Existing `docs/mocks/*.html` stay. Do not add generated PNGs.

## Gap vs current tree (`b9913fc`)

- Gate is prose in `.grok/skills/visionary/SKILL.md` only.
- No validator command, no fixtures, no GHA.
- `docs/vision.md` S1 how-measured is file-content inspection, not a command.
- `bob-spec-intake` (agentic_build) is not documented as calling a validator.

## LOCKED (implementation)

1. Do not gut the visionary skill or existing mocks.
2. Untouched `docs/templates/vision.md` must fail the validator.
3. Harvest remaining agentic_build intake hook as a **PR** later if needed; this repo owns the CLI/CI.
4. No UAT stamp. No `git push origin main` from implementer.

## Acceptance (from #6)

- A1: Local validation command for a vision pack.
- A2: Fail when shape is neither valid primary + LOCKED nor explicit UNKNOWN.
- A3: Fail when Success is neither UNKNOWN nor one complete row.
- A4: Fail when required key/empty/error HTML mocks are missing; reject PNG-only.
- A5: Positive + negative fixtures, including untouched template copy that must fail.
- A6: GitHub Actions runs the validator on this pack and fixtures.
- A7: Document local command + `bob-spec-intake` integration point.
- A8: Update product `docs/vision.md` S1 how-measured to name validator/CI.

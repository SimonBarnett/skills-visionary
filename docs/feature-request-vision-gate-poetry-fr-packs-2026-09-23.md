# FR: vision gate rejects poetry and covers parked FR packs

**GitHub issue:** https://github.com/SimonBarnett/skills-visionary/issues/11
**Date:** 2026-09-23
**Source:** `cursor[bot]` visionary review of `main` `2c98dfd`.
**Repo:** `SimonBarnett/skills-visionary`
**Skill:** `visionary`. Separate from #1 (pack park) and #6 (validator exists; six fixtures pass).

## Ultimate objective

A vision pack that is poetry, or an FR pack that the skill requires but CI never runs, cannot park or dispatch.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Poetry success row exits 1 | fixture `users will love it` / `a lot` / `feelings` | `python tools/validate-vision-pack.py tests/fixtures/vision-pack/negative-poetry.md` (or same wording) | That fixture exits 0 |
| S2 | how-measured must cite an observable | command, path, workflow, or count | validator on fixtures; `docs/vision.md` S1–S3 still exit 0 | Row with only `feelings` / empty check exits 0 |
| S3 | Parked FR packs are in-scope | both `docs/feature-request-*.md` on main exit 0, or `--historical` / explicit exclude | local CLI + GHA | Silent fail (exit 1 with no exclude) while CI is green |
| S4 | CI runs every in-scope pack | workflow lists product + FR packs + fixtures | `.github/workflows/vision-pack.yml` | CI only runs `docs/vision.md` |
| S5 | Product S1 covers FRs | `docs/vision.md` objective + S1 fail-when includes FR park/dispatch without a passing pack | file content | S1 remains new-product-only |

LOCKED

## Shape

Primary: service

Skill-pack playbook. This FR tightens the existing CLI/CI gate. No website or app.

LOCKED

## Stack

Same as #6: `tools/validate-vision-pack.py`, pytest fixtures, GitHub Actions.

LOCKED

## Architecture

```
FR / product vision.md
  --> validate-vision-pack.py
        fail: poetry / unmeasurable how-measured
        fail: FR pack missing Primary/Success unless --historical
  --> GHA on all in-scope packs
  --> bob-spec-intake refuses park unless exit 0
```

No secrets. No instance URLs. No new UI.

LOCKED

## Screens

No new mocks. Existing `docs/mocks/*.html` stay (error mock remains the refuse-poetry illustration).

## Gap vs `2c98dfd`

- CLI only checks four non-empty success cells; poetry exits 0.
- CI only validates `docs/vision.md`.
- Parked FR packs fail the command the skill requires (`Primary:` wording / missing Success table).
- `docs/vision.md` S1 fail-when is new-product-only.

## Acceptance (from #11)

- A1: Poetry fixture exits 1.
- A2: Pass only when how-measured cites command, path, workflow, or count; current S1–S3 still exit 0.
- A3: Both parked FR packs exit 0, or marked historical with an explicit flag (not a silent fail).
- A4: CI runs the validator on every in-scope pack.
- A5: Product objective and S1 fail when an FR parks/dispatches without a passing vision pack.

No UAT stamp. Implementer opens a PR; do not push `main`.

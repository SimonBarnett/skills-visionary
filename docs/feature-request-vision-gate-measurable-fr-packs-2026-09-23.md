# FR: vision gate rejects poetry and scores parked FR packs

**GitHub issue:** https://github.com/SimonBarnett/skills-visionary/issues/11
**Date:** 2026-09-23
**Source:** `cursor[bot]` visionary review of `main` at `2c98dfd` (after #6 / PR #7).
**Repo:** `SimonBarnett/skills-visionary`
**Skill:** `visionary` (this pack). Separate from #1 (pack park) and #6 (CLI exists; six fixtures pass).

## Ultimate objective

A vision pack cannot park or dispatch when success is unmeasurable poetry, and every in-scope pack on this repo (product + parked FRs) fails the same command unless it is explicitly historical.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Unmeasurable success row fails | poetry fixture exits 1 | `python tools/validate-vision-pack.py` on a fixture whose cells are `users will love it` / `a lot` / `feelings` / `never` | That fixture exits 0 |
| S2 | how-measured must be observable | pass only when how-measured cites a command, path, workflow, or count | validator on fixtures; current `docs/vision.md` S1–S3 still exit 0 | Empty-looking poetry in how-measured exits 0 |
| S3 | Parked FR packs are in scope | both `docs/feature-request-*.md` packs exit 0, or an explicit historical exclude flag | validator + CI on those paths | Silent exit 1 on a parked FR while CI stays green |
| S4 | CI covers every in-scope pack | workflow runs the CLI on product pack and in-scope FR packs / fixtures | `.github/workflows/vision-pack.yml` | Workflow still only `docs/vision.md` + the #6 fixture set |
| S5 | Product S1 includes FR park | objective + S1 fail-when cover FR park/dispatch without a passing pack | `docs/vision.md` content | S1 still only names new-product `functional-spec` parks |

LOCKED

## Shape

Primary: service

Hybrid note: same skill-pack CLI/CI surface as #6. No website or app.

LOCKED

## Stack

Default: extend `tools/validate-vision-pack.py`, fixtures under `tests/fixtures/vision-pack/`, GitHub Actions `vision-pack` on `ubuntu-latest`.

Why: the gate already exists; this FR tightens success quality and pack scope.

Why-not: no new SaaS, no PNG pipeline, no second validator.

LOCKED

## Architecture

```
vision.md / FR vision pack
  --> validate-vision-pack (local CLI)
        fail: shape / success (including poetry) / mocks
        fail: parked FR dialect unless historical-exclude
  --> GitHub Actions (same CLI on product pack + in-scope FR packs + fixtures)
  --> bob-spec-intake refuses park/dispatch unless CLI exit 0
```

No secrets. No instance URLs.

LOCKED

## Screens

No new UI. Existing `docs/mocks/*.html` stay. Do not add generated PNGs.

## Gap vs current tree (`2c98dfd` / #6 head `db8d362`)

- CLI accepts any non-empty success cells. `users will love it` / `a lot` / `feelings` / `never` exits 0.
- Skill says poetry is not a target; mocks `error.html` is that refuse state; the command does not enforce it.
- Parked FR packs fail the command the skill requires:
  - `docs/feature-request-vision-pack-gate-ci-2026-09-23.md` — `Reuse repo primary: **service**` is not `Primary: service`
  - `docs/feature-request-visionary-also-on-fr-2026-09-23.md` — no `## Shape`, no `## Success` table
- CI runs the CLI on `docs/vision.md` only (plus pytest fixtures). `main` stays green while those FR packs exit 1.
- `docs/vision.md` S1 fail-when is new-product `functional-spec` only.

## LOCKED (implementation)

1. Do not gut the #6 fixtures or make `docs/vision.md` fail the current gate.
2. Current product S1–S3 rows must still exit 0 (they already cite observable checks).
3. Historical exclude, if used, must be an explicit validator flag or front-matter — a silent fail is not a pass.
4. Harvest remaining `bob-spec-intake` call-site work as a later agentic_build PR if needed; this repo owns the CLI/CI.
5. No UAT stamp. No `git push origin main` from implementer.

## Acceptance (from #11)

- A1: A fixture copied from the error-mock wording (`users will love it` / `a lot` / `feelings`) exits 1.
- A2: A row passes only when `how measured` cites an observable check (command, path, workflow, or count). Current S1–S3 in `docs/vision.md` still exit 0.
- A3: Both parked `docs/feature-request-*.md` packs exit 0, or they are marked historical and excluded by an explicit validator flag.
- A4: CI runs the validator on every in-scope pack, not only `docs/vision.md`.
- A5: Product objective and S1 fail when an FR parks or dispatches without a passing vision pack.

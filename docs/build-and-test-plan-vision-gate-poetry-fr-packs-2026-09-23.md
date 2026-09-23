# Build/test plan: poetry gate + FR packs (#11)

FR: `docs/feature-request-vision-gate-poetry-fr-packs-2026-09-23.md`.

## Build

1. `tools/validate-vision-pack.py`
   - Fail success rows whose target/how-measured are poetry (`users will love it`, `a lot`, `feelings`, no command/path/workflow/count).
   - Keep current S1–S3 in `docs/vision.md` exiting 0.
   - Accept FR shape `Primary: service` (and existing `Reuse repo primary` if we keep those packs live).
   - `--historical` (or allow-list) for packs that stay as history; default is fail, not silent.
2. Fixture `tests/fixtures/vision-pack/negative-poetry.md` (error-mock wording). Must exit 1.
3. Fix or exclude both parked `docs/feature-request-*.md` so each is exit 0 or explicit historical.
4. `.github/workflows/vision-pack.yml` — run validator on product pack, in-scope FR packs, and fixtures (not only `docs/vision.md`).
5. Update `docs/vision.md` objective + S1 so FR park/dispatch without a passing pack is fail-when.
6. Open a PR. Do not push `main`. No UAT.

## Test

- Local: poetry fixture exit 1; `docs/vision.md` exit 0; FR packs exit 0 or `--historical`.
- `pytest tests/ -q`
- GHA green on the PR.

## Do not

- Stamp UAT. Push origin/main. Second 11904 harvest #275/#276.

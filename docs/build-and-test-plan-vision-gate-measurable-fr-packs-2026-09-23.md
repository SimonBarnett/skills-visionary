# Build/test plan: vision gate measurable success + FR packs (#11)

FR: `docs/feature-request-vision-gate-measurable-fr-packs-2026-09-23.md`.

## Build

1. Extend `tools/validate-vision-pack.py` success gate:
   - Fail a row whose metric/target/how-measured/fail-when is poetry (`users will love it`, `a lot`, `feelings`, or equivalent empty-of-measurement wording).
   - Pass a row only when how-measured cites an observable check (command, path, workflow, or count).
   - Keep `docs/vision.md` S1–S3 exiting 0.
2. Fixtures: add a negative poetry row copied from the error-mock wording; keep #6 positives/negatives green.
3. FR pack scope:
   - Make both parked `docs/feature-request-*.md` packs exit 0 (widen `Primary:` matcher and add missing Shape/Success), **or** mark them historical with an explicit validator flag. Silent exit 1 is not a pass.
4. `.github/workflows/vision-pack.yml` — run the CLI on the product pack and every in-scope FR pack (plus existing pytest).
5. Update `docs/vision.md` objective + S1 so FR park/dispatch without a passing pack is a fail-when.
6. Open a PR. Do not push `main`. No UAT.

## Test

- Local: product `docs/vision.md` still exit 0.
- Poetry fixture exit 1.
- In-scope FR packs exit 0, or historical-exclude is explicit and documented.
- `pytest tests/ -q` includes the new fixture; #6 cases still pass.
- GHA green on the PR.

## Do not

- Stamp UAT. Push origin/main. Re-open #6 MUSTs as if the CLI did not exist.

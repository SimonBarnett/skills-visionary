# Build/test plan: vision-pack gate and CI (#6)

FR: `docs/feature-request-vision-pack-gate-ci-2026-09-23.md`.

## Build

1. Add `tools/validate-vision-pack` (Python preferred; one entrypoint, exit 1 on fail).
   - Args: path to vision markdown (and optional mocks dir).
   - Shape: valid `service|website|app` + LOCKED, or explicit UNKNOWN.
   - Success: section UNKNOWN, or >=1 table row with metric, target, how-measured, fail-when.
   - Mocks: `home`/`empty`/`error` (or key/empty/error) `.html` required when pack is not UNKNOWN-shape-without-UI; reject `.png` as the only mocks.
2. Fixtures under `tests/fixtures/vision-pack/` (or similar):
   - positive: copy of a valid filled pack.
   - negative: untouched copy of `docs/templates/vision.md` (must fail).
   - negative: missing shape, partial success row, PNG-only mocks.
3. `.github/workflows/vision-pack.yml` — run validator on `docs/vision.md` + fixtures.
4. README + visionary skill: name the command; `bob-spec-intake` must invoke it before park/dispatch (document the hook; harvest to agentic_build as a PR if the call site is not this repo).
5. Update `docs/vision.md` S1 how-measured to the validator/CI.
6. Open a PR. Do not push `main`. No UAT.

## Test

- Local: validator exit 0 on this repo's `docs/vision.md`; exit 1 on untouched template fixture.
- `pytest` or scripted fixture loop if added.
- GHA green on the PR.

## Do not

- Stamp UAT. Push origin/main. Second 11904 lanes (#1 pack-only).

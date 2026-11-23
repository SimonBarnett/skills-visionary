# VIS-D2 evidence: park dry-run issue bodies include Depends-on

**FR:** SimonBarnett/skills-visionary#148  
**Tool:** `python tools/format_depends_on_park_issue_body.py --dry-run ...`

Plan park must pass this body (or equivalent) to
`Report-BobiverseIntakeIssue.ps1 -Body` / `gh issue create --body-file`.
Vision markdown alone is not enough (S1 fail-when).

## Dry-run: child Depends-on digest

```text
**Depends-on:** #147

Feature request `VIS-D2` (parked).

**Theme:** Depends-on preconditions: Plan stamps + Jeeves skip-until-closed
**Depends-on:** #147
**Vision pack:** https://github.com/SimonBarnett/skills-visionary/blob/docs/depends-on-plan-stamp-frs-2026-11-21/docs/feature-request-depends-on-park-emits-issue-body-2026-11-21.md
**Index:** https://github.com/SimonBarnett/skills-visionary/blob/docs/depends-on-plan-stamp-frs-2026-11-21/docs/fr-index-depends-on-plan-stamp-2026-11-21.md

Plan must identify FR preconditions on the issue. Implement Success S1 in the vision pack. Open a PR against main. Do not merge. One acceptance row only.


```

## Dry-run: explicit (none)

```text
**Depends-on:** (none)

Feature request `VIS-D4` (parked).

**Theme:** Depends-on preconditions: Plan stamps + Jeeves skip-until-closed
**Depends-on:** (none)
**Vision pack:** https://example.invalid/vision.md
**Index:** https://example.invalid/index.md

Plan must identify FR preconditions on the issue. Implement Success S1 in the vision pack. Open a PR against main. Do not merge. One acceptance row only.


```

## Dry-run: cross-repo + same-repo

```text
**Depends-on:** SimonBarnett/bobiverse#9147, #8807

Feature request `BOB-D3` (parked).

**Theme:** Depends-on preconditions
**Depends-on:** SimonBarnett/bobiverse#9147, #8807
**Vision pack:** https://example.invalid/vision.md
**Index:** https://example.invalid/index.md

Plan must identify FR preconditions on the issue. Implement Success S1 in the vision pack. Open a PR against main. Do not merge. One acceptance row only.


```

Each fixture file under `tests/fixtures/depends-on-park/` starts with
`**Depends-on:**` so chair truncation of the first 500 characters still sees the stamp.

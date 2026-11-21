# Index: Depends-on preconditions: Plan stamps + Jeeves skip-until-closed

**Repo:** SimonBarnett/skills-visionary  
**Date:** 2026-11-21  
**Mode:** park-only anti-omnibus

| ID | Issue | Title | Doc |
|----|-------|-------|-----|
| VIS-D1 | [#147](https://github.com/SimonBarnett/skills-visionary/issues/147) | Depends-on grammar in visionary skill | docs/feature-request-depends-on-grammar-visionary-2026-11-21.md |
| VIS-D2 | [#148](https://github.com/SimonBarnett/skills-visionary/issues/148) | Plan park emits Depends-on on GitHub issue body | docs/feature-request-depends-on-park-emits-issue-body-2026-11-21.md |
| VIS-D3 | [#149](https://github.com/SimonBarnett/skills-visionary/issues/149) | Backlog-id-only depends rejected | docs/feature-request-depends-on-reject-backlog-id-only-2026-11-21.md |
| VIS-D4 | [#150](https://github.com/SimonBarnett/skills-visionary/issues/150) | Explicit no-preconditions stamp | docs/feature-request-depends-on-explicit-none-2026-11-21.md |
| VIS-D5 | [#151](https://github.com/SimonBarnett/skills-visionary/issues/151) | Harvest / skill-harvest-log for Depends-on | docs/feature-request-depends-on-harvest-log-2026-11-21.md |

## Notes

- Park-only: no bob-job-loop until asked.
- Grammar: `Depends-on: #N` same-repo; `owner/repo#N` cross-repo; `(none)` when empty.
- Pair with bobiverse BOB-D1..D9 (Jeeves skip-until-closed) and retarget #8754.

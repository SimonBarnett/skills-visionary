# Fixture pack: explicit Depends-on: (none)

**VIS-D4 / FR #150.** When an FR has no preconditions, Plan park still stamps
`Depends-on: (none)` on the **GitHub issue body** (and may mirror it in the
vision pack). Silent omission of the Depends-on line fails S1.

## Files

| File | Role |
|------|------|
| `issue-body.md` | Sample intake / `gh issue create` body with `(none)` |
| `vision-pack-snippet.md` | Vision pack / FR markdown also shows the stamp |

## Fail-when

An issue or pack that never mentions `Depends-on` (even when there are no
deps) is a silent omission — reject that park.

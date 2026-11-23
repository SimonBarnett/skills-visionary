# Depends-on grammar (Plan stamps)

**Repo:** SimonBarnett/skills-visionary  
**ID:** VIS-D1 / FR #147  
**Skill:** `.grok/skills/visionary/SKILL.md`

Plan seats stamp FR preconditions on GitHub issue bodies so Jeeves can
skip offer until those issues are closed. This grammar applies to
**any SimonBarnett product repo** (bobiverse, skills-visionary,
priority-mcp, a-search, and other SimonBarnett products) — not
bobiverse-only.

## Grammar (LOCKED)

| Form | Meaning | Example |
|------|---------|---------|
| `Depends-on: #N` | Same-repo issue N must be closed | `Depends-on: #9147` |
| `Depends-on: owner/repo#N` | Cross-repo issue must be closed | `Depends-on: SimonBarnett/bobiverse#9147` |
| `Depends-on: (none)` | Explicitly no preconditions | `Depends-on: (none)` |

Several refs may appear on one line, separated by commas or whitespace.

Place the stamp near the top of the issue body (within the first 500
characters) so chair queue rows that truncate the body still see it.

## Distinct from hold / HOLD

| Mechanism | Role |
|-----------|------|
| `Depends-on:` stamp | Precondition: skip offer while listed issues are OPEN |
| Label `hold` / `on-hold` or line-anchored `HOLD (...):` | Human go-gate / park; not a Depends-on substitute |

Unhold alone can release a digest batch when the chair go-gate is live;
Depends-on still blocks children whose listed issues remain OPEN.

## Out of scope here

- Emitting the stamp from park automation (VIS-D2)
- Rejecting backlog-id-only depends (VIS-D3)
- Harvest / skill-harvest-log coverage (VIS-D5)
- Jeeves parse/skip implementation (bobiverse BOB-D*)

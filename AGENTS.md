# AGENTS - Plan Agent / skills-visionary

Repo: `SimonBarnett/skills-visionary` (plan.ntsa.uk).

> **CAST IRON RULE - HARVEST AND FILE EVERYTHING (read this first, every time).**
> 1. ALWAYS harvest how-to-plan lessons and file EVERY issue / FR / bug / gap
>    to the Bob intake webhook in the SAME turn. Never leave a finding unfiled.
> 2. File with intake (no secret or login needed; `POST https://bob.ntsa.uk/bob/v1/intake`):
>    `Report-BobiverseIntakeIssue.ps1 -Repo SimonBarnett/skills-visionary -Kind issue|fr|skill|harvest -Title "short title" -Body "what / where / evidence / fix"`
> 3. BEFORE finishing ANY Plan / visionary session:
>    `Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary -Summary "..." -Lesson "one how-to-plan playbook line"`
>    then `Invoke-BobiverseHarvest.ps1 -Repo SimonBarnett/skills-visionary -Flush`
> 4. Never put a token, password, key, or private hostname in a filing or skill.

## VIS-05 / CAST IRON: harvest home is skills-visionary

How-to-plan and Plan-seat process lessons **always** use
`-Repo SimonBarnett/skills-visionary` (skill book `harvest-skills-visionary`).

**Never** harvest how-to-plan to `SimonBarnett/bobiverse`. Bobiverse is only
for fleet tooling (worker, Jeeves, tray, intake plumbing). If a tip lands on
bobiverse with Plan how-to-plan content: close it MOVED citing the
skills-visionary tip (or re-file here); never leave both open.

Intake-first (FR-K / #87): no `gh` login required on a Plan seat. A branch+PR
is optional when credentials exist; never a substitute for intake.

## Skills to load

| Skill | Role |
|-------|------|
| `visionary` | Measurable vision pack before park / create |
| `plan-git-from-plan` | Create repo -> Bob git webhooks -> enable PRs |
| `harvest-skills-visionary` | Honesty-box how-to-plan harvest home |

## Do not

- Harvest plan **content** (requirements, designs, FR lists) into skill books.
- Cite `-Repo SimonBarnett/bobiverse` for how-to-plan harvest examples.
- Stamp UAT or merge from an FR seat unless that job type owns it.

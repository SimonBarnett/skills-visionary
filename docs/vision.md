# Vision: skills-visionary

Skill: `visionary`. New-product intake for this repo.

## Objective

Every new SimonBarnett product and every feature request on an existing
repo starts with a scored long-term plan (shape, stack, architecture,
HTML mocks when there is a UI) before anyone parks a ticket or dispatches
a build.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Parks include a passing vision pack | 100% of new products and FRs on SimonBarnett repos | `python tools/validate-vision-pack.py` on the pack exits 0 locally; GitHub Actions `vision-pack` workflow on this repo (product + in-scope FR packs); `bob-spec-intake` must run the same command before park/dispatch | A new product parks `functional-spec` only and dispatches, or an FR parks/dispatches without a vision pack that exits 0 |
| S2 | Mocks are HTML wireframes | Key + empty + error | `docs/mocks/*.html` present; no generated PNG mocks | Intake ships PNG-only or skips empty/error |
| S3 | Harvest home is this repo | Learnings land on a PR here | `.grok/skills/harvest-skills-visionary` used; no playbook-only in `~/.grok` | Visionary playbook edited only on agentic_build or home disk |

## Shape

Primary: service

Hybrid note: the product is an agent playbook (skill pack). Delivery is
public git markdown plus HTML mocks, not a website or installable app.

LOCKED

## Stack

Default: Markdown `SKILL.md` in `.grok/skills/visionary`, HTML/CSS mocks
in `docs/mocks/`, public GitHub (`SimonBarnett/skills-visionary`).

Why: fleet already loads `.grok/skills`; HTML mocks are reviewable
without an image model; public repo lets anyone open a PR.

Why-not: no web app, no SaaS, no generated PNG pipeline, no extra
runtime. Windows + `gh` + existing intake skills are enough.

LOCKED

## Architecture

Who talks to what. Phase 0 only.

```
brief --> visionary (high-reasoning seat)
       --> docs/vision.md + docs/mocks/*.html   [new product]
       --> FR markdown success + mocks          [feature request]
       --> plan-git-from-plan (Plan seats; no full build pack)
       --> public repo + Bob git webhook + permit PRs  [new product only]
       --> FR commit on existing repo                  [FR; no create]
       --> FR issue --> bob-job-loop
design-uat later reads mocks + brief (does not stamp UAT here)
harvest-skills-visionary PRs learnings back to this repo
```

Trust: no secrets, no instance URLs. This pack owns the visionary
playbook **and** Plan-seat git setup (`plan-git-from-plan` /
`plan-create-repo` / `plan-bob-webhooks` / `plan-enable-prs`),
harvested from agentic_build so Plan seats do not install the full
build pack. Fleet build/IRC jobs stay in their packs.

LOCKED

## Screens

| id | file | state |
|----|------|-------|
| M1 | docs/mocks/home.html | primary Ã¢â‚¬â€ vision pack filled |
| M2 | docs/mocks/empty.html | empty Ã¢â‚¬â€ refuse dispatch |
| M3 | docs/mocks/error.html | error Ã¢â‚¬â€ poetry / unmeasurable |

## LOCKED

- Shape is a skill-pack service.
- Success S1-S3 as above.
- Stack is SKILL.md + HTML mocks + public git.
- Harvest skill is foundation.

## UNKNOWN

- Whether agentic_build keeps a stub pointer or copies this skill on
  Install-BobFleet only.
- Visual UAT of the HTML mocks (Bob stamps; not this intake).

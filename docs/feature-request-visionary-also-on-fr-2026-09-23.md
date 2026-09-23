# FR: visionary should also run on feature requests

https://github.com/SimonBarnett/skills-visionary/issues/2

Simon: "Should als be on FR" (also on FR). Empty body. Existing A3 says FRs skip visionary.

## Gap vs current tree

`.grok/skills/visionary/SKILL.md` and `docs/functional-spec.md` A3:
feature requests on an existing repo skip this skill (gap-vs-current
stays `bob-spec-intake` only).

## LOCKED

1. Visionary runs on **feature requests** as well as new-product intake.
2. An FR does **not** create a new repo. Confirm target repo. Fill a
   vision pack for the new surface: success table (metric / target /
   how-measured / fail-when) LOCKED or UNKNOWN; mocks in `docs/mocks/`
   when the FR has a UI. Reuse existing shape unless the FR changes it.
3. `bob-spec-intake` Feature request step must call `visionary` before
   park/dispatch (same refuse gate: shape + at least one success row,
   or Success UNKNOWN).
4. Flip spec A3. Description / triggers include FR, not only new repo.
5. Harvest as PR, not `main`. Also harvest the same rule into
   `SimonBarnett/agentic_build` `.grok/skills/visionary` + `bob-spec-intake`
   (CAST IRON). No UAT. No secrets.

## UNKNOWN

Whether an FR vision pack is `docs/vision.md` append vs
`docs/feature-request-<slug>-vision.md`. Prefer a section in the FR
markdown plus mocks when UI, unless the worker has a cleaner split.

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Visionary runs on feature requests | 100% of FRs on SimonBarnett repos | `.grok/skills/visionary/SKILL.md` and `docs/functional-spec.md` A3; `python tools/validate-vision-pack.py` on FR pack before park | Skill or spec still says FRs skip visionary |
| S2 | FR path does not create a repo | 0 new repos per FR | `bob-spec-intake` FR path; no `gh repo create` in FR flow | FR runs `gh repo create` |

LOCKED

## Shape

Primary: service

Skill-pack and intake rule change only. No new website or app.

LOCKED

## Acceptance

| ID | Gate |
|---|---|
| A1 | Visionary skill no longer says FRs skip it. |
| A2 | FR intake refuses dispatch until success metrics LOCKED or UNKNOWN. |
| A3 | FR path does not `gh repo create`. |
| A4 | Functional spec A3 updated (FRs run visionary). |

# FR-A: Human-readable README for skills-visionary

**Repo:** SimonBarnett/skills-visionary  
**Label:** feature-request  
**Parent plan:** docs/feature-request-plan-dag-mcp-2026-11-15.md

## Goal

Rewrite the root README so a human (not only an agent) can understand what this pack is, which skills it contains, how to install/copy them, which Bob URLs to use (`bob.ntsa.uk`), and that a public MCP at `plan.ntsa.uk` is coming.

## Deliverables

1. Replace agent-only tone with a short plain-English overview (Plan seats, vision gate, plan-git helpers).
2. Keep the skills table; add one-line “when to use” for each.
3. Fix webhook/digest URLs from `irc.ntsa.uk` to `https://bob.ntsa.uk/bob/v1/git` and `https://bob.ntsa.uk/bob/v1/report`.
4. Document upcoming `https://plan.ntsa.uk` and `https://plan.ntsa.uk/mcp` (may note “pending Amplify/DNS — Slab”).
5. Keep copy/xcopy install instructions; no secrets.

## Testable

- [ ] README contains `bob.ntsa.uk` and does **not** contain `irc.ntsa.uk`
- [ ] README names `visionary`, `plan-git-from-plan`, `plan-create-repo`, `plan-bob-webhooks`, `plan-enable-prs`, `harvest-skills-visionary`
- [ ] README mentions `plan.ntsa.uk` (MCP or landing)
- [ ] A reader can find the vision-pack validator command without opening SKILL.md

## Out of scope

DAG sync, Next.js MCP app, Amplify console, bob.ntsa.uk home link (those are FR-C…J).

## Success row

Supports plan Success **S1**.

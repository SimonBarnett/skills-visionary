# Vision: skills-visionary

Skill: `visionary`. Product vision for this repo.

## Objective

Plan seats and humans discover and pull visionary / plan skills via a
public surface at **https://plan.ntsa.uk** (landing + MCP), with a clear
human README and a discoverable link from **https://bob.ntsa.uk**. Skill
markdown under `.grok/skills` remains the source of truth.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Public README is human-readable | Non-agent reader can state purpose, skills list, MCP URL, install/copy path in ≤2 min | Manual read of root `README.md`; links use `bob.ntsa.uk` / `plan.ntsa.uk` | README is agent-only jargon only, or still points at the old fleet host |
| S2 | Skill DAG builds clean | `check-dag` (or twin) exit 0 on CI | CI job on PR; catalog↔DAG sync, no cycles on skill nodes, no secrets in public catalog | Drift between `.grok/skills` and catalog/DAG |
| S3 | MCP tools work on Amplify | `list_catalog` + `get_skill` over `POST https://plan.ntsa.uk/mcp` | `npm run smoke` locally + `smoke:live` after Slab DNS | 404 / wrong transport / empty catalog |
| S4 | plan.ntsa.uk resolves | HTTPS 200 on `/` and MCP path | curl/Invoke-WebRequest after Slab attach | NXDOMAIN or Amplify default-only forever |
| S5 | bob.ntsa.uk links Plan | Home page has visible `plan.ntsa.uk` link | Fetch `https://bob.ntsa.uk/` HTML contains href | Home ships without Plan link |
| S6 | Vision pack stays green | `python tools/validate-vision-pack.py docs/vision.md --mocks-dir docs/mocks` exits 0 | Local + GitHub Actions `vision-pack` workflow | Pack parks with poetry rows or missing mocks |

LOCKED

## Shape

Primary: website

Hybrid note: product surface is plan.ntsa.uk landing + MCP HTTP.
`.grok/skills` markdown remains source of truth; Amplify serves catalog
+ DAG read API. Explicit change from prior vision shape skill-pack
service.

LOCKED

## Stack

Default: Markdown skills in `.grok/skills` → sync into `apps/mcp-catalog`
(Next.js 14 App Router), Node 20, Amplify **WEB_COMPUTE**, public DAG
under `data/`, no secrets on Amplify. Pattern:
`SimonBarnett/priority-mcp` `v2/apps/mcp-catalog` / live
`https://mcp.ntsa.uk`.

Why: proven MCP host; Plan seats already load this pack; one repo owns
playbook + public surface.

Why-not: Amplify static `WEB` only; new empty host repo; execute-plane
tools on Amplify.

LOCKED

## Architecture

Who talks to what. Amplify WEB_COMPUTE + Slab DNS for plan.ntsa.uk.

```
.grok/skills/*  (source of truth SKILL.md)
       |
       v
 sync-skill-dag + catalog mirrors + check-dag  (CI / amplify preBuild)
       |
       v
 apps/mcp-catalog  Next.js  --POST /mcp-->  list_catalog, get_skill
       |
       v
 Amplify WEB_COMPUTE  <--- Slab agent: app + DNS plan.ntsa.uk + cert
       |
       +--> public landing HTML (human)
       |
bob.ntsa.uk home  -->  link to plan.ntsa.uk
```

Trust: public skills only; no tokens on Amplify; how-to-plan harvest
stays this repo (`harvest-skills-visionary`). Fleet build/IRC jobs stay
in their packs. Plan-seat git helpers remain
`plan-git-from-plan` / `plan-create-repo` / `plan-bob-webhooks` /
`plan-enable-prs`.

LOCKED

## Screens

| id | file | state |
|----|------|-------|
| M1 | docs/mocks/plan-home.html | Landing: what Plan is + MCP connect snippet |
| M2 | docs/mocks/plan-empty.html | Empty catalog / not deployed |
| M3 | docs/mocks/plan-error.html | MCP/DAG build failure message |

Required validator trio (`home.html` / `empty.html` / `error.html`)
remains in `docs/mocks/` for `validate-vision-pack`; product UI mocks
above are the plan.ntsa.uk wireframes.

## LOCKED

- Shape Primary is website (plan.ntsa.uk landing + MCP).
- Success S1-S6 as above (README, DAG, MCP, DNS, bob link, vision gate).
- Stack is `.grok/skills` → Amplify WEB_COMPUTE catalog; no secrets.
- Harvest skill is foundation.

## UNKNOWN

- Exact Amplify app id / custom-domain attach timing (Slab FR-H).
- Whether agentic_build keeps a stub pointer or copies this skill on
  Install-BobFleet only.
- Visual UAT of the HTML mocks (Bob stamps; not this intake).

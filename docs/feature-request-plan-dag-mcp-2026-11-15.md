# Feature request: skills-visionary DAG MCP + plan.ntsa.uk

**Repos:** `SimonBarnett/skills-visionary` (primary), `SimonBarnett/bobiverse` (FR-J front door)  
**Plan folder:** `C:\ai\bob\plan\work\plan-20261115-112332`  
**Date:** 2026-11-15  
**Skill:** visionary

## Objective

Plan seats and humans discover and pull visionary/plan skills via a public DAG MCP at **https://plan.ntsa.uk**, with a clear human README and a discoverable link from **https://bob.ntsa.uk**.

LOCKED

## Success

| id | metric | target | how measured | fail-when |
|----|--------|--------|--------------|-----------|
| S1 | Public README is human-readable | Non-agent reader can state purpose, skills list, MCP URL, install/copy path in ≤2 min | Manual read of root `README.md`; links use `bob.ntsa.uk` / `plan.ntsa.uk` | README is agent-only jargon only, or still points at `irc.ntsa.uk` |
| S2 | Skill DAG builds clean | `check-dag` (or twin) exit 0 on CI | CI job on PR; catalog↔DAG sync, no cycles on skill nodes, no secrets in public catalog | Drift between `.grok/skills` and catalog/DAG |
| S3 | MCP tools work on Amplify | `list_catalog` + `get_skill` over `POST https://plan.ntsa.uk/mcp` | `npm run smoke` locally + `smoke:live` after Slab DNS | 404 / wrong transport / empty catalog |
| S4 | plan.ntsa.uk resolves | HTTPS 200 on `/` and MCP path | curl/Invoke-WebRequest after Slab attach | NXDOMAIN or Amplify default-only forever |
| S5 | bob.ntsa.uk links Plan | Home page has visible `plan.ntsa.uk` link | Fetch `https://bob.ntsa.uk/` HTML contains href | Home ships without Plan link |

LOCKED

## Shape

Primary: website

Hybrid note: product surface is plan.ntsa.uk landing + MCP HTTP. `.grok/skills` markdown remains source of truth; Amplify serves catalog + DAG read API. Explicit change from prior vision shape skill-pack service.

LOCKED

## Stack

Default: Markdown skills in `.grok/skills` → sync into `apps/mcp-catalog` (Next.js 14 App Router), Node 20, Amplify **WEB_COMPUTE**, public DAG under `data/`, no secrets on Amplify. Pattern: `SimonBarnett/priority-mcp` `v2/apps/mcp-catalog` / live `https://mcp.ntsa.uk`.

Why: proven MCP host; Plan seats already load this pack; one repo owns playbook + public surface.

Why-not: Amplify static `WEB` only; new empty host repo; execute-plane tools on Amplify.

LOCKED

## Architecture

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
bob.ntsa.uk jeeves/www/irc-ntsa/index.html  -->  link to plan.ntsa.uk
```

Trust: public skills only; no tokens on Amplify; how-to-plan harvest stays this repo.

LOCKED

## Screens

| id | file | state |
|----|------|-------|
| M1 | docs/mocks/plan-home.html | Landing: what Plan is + MCP connect snippet |
| M2 | docs/mocks/plan-empty.html | Empty catalog / not deployed |
| M3 | docs/mocks/plan-error.html | MCP/DAG build failure message |

Mocks live in this plan folder first; product PR copies under `docs/mocks/`.

## Gap vs origin/main

- No DAG, no MCP app, no Amplify, `plan.ntsa.uk` NXDOMAIN
- README exists but agent-oriented; cites stale `irc.ntsa.uk`
- bob.ntsa.uk `jeeves/www/irc-ntsa/index.html` has no Plan link

## Anti-omnibus slices

See `drafts/backlog.md`. Do not open one omnibus issue.

## Out of scope

Full agentic_build/IRC on Plan seats; Amplify secrets/WCF; rename repo; stamp UAT.

---
name: plan-mcp-setup
description: >
  Connect an MCP client to the public Plan Agent catalog at
  https://plan.ntsa.uk/mcp. Use when the user says plan MCP, load
  plan.ntsa.uk, plan__list_catalog, plan__get_skill, or /plan-mcp-setup.
---

# Plan MCP setup

Foundation: harvest-skills-visionary -> report back to
https://github.com/SimonBarnett/skills-visionary.

Public catalog (no secrets): **https://plan.ntsa.uk**  
MCP transport: **https://plan.ntsa.uk/mcp**  
Tools: `list_catalog`, `get_skill` (DAG-aware).

Sibling pattern: Priority catalog at `https://mcp.ntsa.uk` /
`priority-mcp-setup`. This skill is Plan-only.

## When

First-time Plan MCP connect, empty `plan__*` tools in a Grok session,
or confirming the live catalog after Amplify/DNS changes.

## Grok Build (HTTP)

```powershell
grok mcp add --transport http plan https://plan.ntsa.uk/mcp
grok mcp doctor plan
grok mcp list
```

Expect doctor: handshake OK, **2 tools** discovered. Config lands in
`~/.grok/config.toml` as `[mcp_servers.plan]` with
`url = "https://plan.ntsa.uk/mcp"` and `enabled = true`.

**Session reload:** adding the server mid-session does not always expose
`plan__list_catalog` / `plan__get_skill` until MCP reconnect or a new
Grok session. `grok mcp doctor plan` can be healthy while the live tool
catalog still omits `plan__*`.

## Smoke (no secrets)

```powershell
curl.exe -sS https://plan.ntsa.uk/
# Landing JSON/HTML notes tools list_catalog + get_skill
curl.exe -sS -o NUL -w "%{http_code}" https://plan.ntsa.uk/mcp
# Expect 200 on the MCP path (POST JSON-RPC for real tool calls)
```

Live npm smoke (when present in this repo): `npm run smoke:live` under
`apps/mcp-catalog` (see `docs/amplify-hosting.md`).

## Skills on the host

Catalog mirrors `.grok/skills` in this repo (visionary, plan-*, harvest*).
How-to-plan harvest still targets **SimonBarnett/skills-visionary** via
Bob intake (`harvest-skills-visionary`). Never park how-to-plan under
bobiverse.

## Do not

- Commit secrets, PATs, or Authorization headers (catalog is public)
- Point Plan seats at on-prem IIS and treat 404 as a Plan bug
- Invent a second Plan MCP URL
- Teach admin-merge of docs PRs when `vision-pack` validate is red —
  fix how-measured / mocks so validate exits 0

## Related

- Vision gate: `visionary`
- Plan git path: `plan-git-from-plan`
- Harvest: `harvest-skills-visionary`
- Live host: https://plan.ntsa.uk

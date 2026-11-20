# mcp-catalog (skills-visionary)

Public skill catalog + DAG + MCP host for **plan.ntsa.uk** (FR-C / FR-D / FR-E).

## Source of truth

`.grok/skills/*/SKILL.md` is the source of truth. `catalog/<id>/` mirrors
`meta.json` + `SKILL.md` for the MCP host. Regenerate mirrors when skills
change; do not edit catalog copies as the primary store.

## MCP (FR-E)

- Next.js 14 App Router, Node 20, Amplify **WEB_COMPUTE**-ready
- `POST /mcp` — JSON-RPC protocol `2024-11-05`, one object per POST
- Tools: `list_catalog`, `get_skill` (returns `skillMd` + `required[]` from DAG)
- No ERP / execute plane; no secrets in env
- Local: `npm run dev` / `npm run build && npm start`
- Smoke: `npm run smoke` (after build)
- Optional local stdio: `npm run stdio` (not on Amplify)

## DAG

- Source: `docs/skill-sources/skills-visionary/_dag/{dag.json,dag-index.json}`
- Sync: `npm run sync-dag` copies into `data/`
- Gate: `npm run check-dag` fails on catalog↔DAG drift, dangling edges,
  skill-node cycles (topic↔topic loops OK), or secret-like blobs in DAG nodes
- `npm run build` = sync + check + `next build`

## Pattern

`SimonBarnett/priority-mcp` `v2/apps/mcp-catalog` (tools subset: catalog only).

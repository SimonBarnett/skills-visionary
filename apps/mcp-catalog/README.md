# mcp-catalog (skills-visionary)

Public skill catalog + DAG for **plan.ntsa.uk** (FR-C / FR-D).

## Source of truth

`.grok/skills/*/SKILL.md` is the source of truth. `catalog/<id>/` mirrors
`meta.json` + `SKILL.md` for the MCP host. Regenerate mirrors when skills
change; do not edit catalog copies as the primary store.

## DAG

- Source: `docs/skill-sources/skills-visionary/_dag/{dag.json,dag-index.json}`
- Sync: `npm run sync-dag` copies into `data/`
- Gate: `npm run check-dag` fails on catalog↔DAG drift, dangling edges,
  skill-node cycles (topic↔topic loops OK), or secret-like blobs in DAG nodes

## Next.js (FR-E / FR-F)

- Landing `GET /` matches `docs/mocks/plan-home.html` (empty/error branches too)
- MCP `POST /mcp` JSON-RPC 2024-11-05: `list_catalog`, `get_skill`
- Public MCP URL: `https://plan.ntsa.uk/mcp`
- `npm run build` = sync + check-dag + `next build`
- `npm run smoke` = local catalog non-empty check
- No secrets in env; stdio is local-only (not served)

## Pattern

`SimonBarnett/priority-mcp` `v2/apps/mcp-catalog`.

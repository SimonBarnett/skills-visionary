# skill-sources

Public DAG sources for plan.ntsa.uk MCP (FR #81).

- `skills-visionary/_dag/dag.json` — skill nodes + depends_on edges
- Rebuild from `.grok/skills`: `python tools/build-skill-dag.py`
- Sync into the app: `cd apps/mcp-catalog && npm run sync-dag`
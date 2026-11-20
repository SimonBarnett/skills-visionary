# Amplify Hosting for https://plan.ntsa.uk

The Next.js catalog at `apps/mcp-catalog` is meant for Amplify Hosting compute
(`WEB_COMPUTE`). The full deploy contract (`amplify.yml`, console settings, env
allowlist, no secrets) is **FR-G**
(https://github.com/SimonBarnett/skills-visionary/issues/84). Custom domain +
cert is **FR-H**
(https://github.com/SimonBarnett/skills-visionary/issues/85).

This document’s **Live evidence (FR-I)** section is where operators paste the
output of `npm run smoke:live` after production is up.

## Live smoke how-to (FR-I)

From `apps/mcp-catalog` (Node 20+):

```bash
npm ci --include=dev --no-audit --fund=false
npm run smoke:live
```

Override origin when testing a default Amplify hostname before DNS:

```bash
SMOKE_MCP_ORIGIN=https://<appId>.amplifyapp.com npm run smoke:live
```

The script asserts:

1. `GET /` returns HTTP 200 (Plan landing HTML).
2. `GET /mcp` returns HTTP 200 and tool names `list_catalog`, `get_skill`.
3. `POST /mcp` `initialize` returns protocol `2024-11-05` and
   `serverInfo.name` `mcp-skills-visionary`.
4. `tools/call` `list_catalog` returns a non-empty `skills` array.

Exit 0 prints a JSON evidence block. Paste that block under **Live evidence
(FR-I)** below (replace the pending stub).

Local catalog-only check (no network): `npm run smoke`.

## Live evidence (FR-I)

**Status (2026-11-20):** pending FR-H. `plan.ntsa.uk` does not resolve yet
(Cloudflare DNS + Amplify app not attached). After FR-H deploys and DNS
propagates, run `npm run smoke:live` and replace this stub with the printed
JSON (keep the heading).

```json
{
  "origin": "https://plan.ntsa.uk",
  "when": null,
  "note": "pending FR-H — re-run npm run smoke:live and paste PASS JSON here"
}
```

### Expected after FR-H

| Check | Expect |
| --- | --- |
| `https://plan.ntsa.uk/` | HTTP 200 |
| `https://plan.ntsa.uk/mcp` | HTTP 200, tools include `list_catalog` + `get_skill` |
| `list_catalog` | non-empty `skills` |

# Amplify Hosting for https://plan.ntsa.uk

The only component Amplify can host from this repository is the Plan skill
**catalog** at `apps/mcp-catalog`. It is a Next.js 14 App Router server. It
reads `catalog/` and `data/` from disk and answers stateless JSON-RPC.

This document is the **deploy contract** (FR-G). It does not create the
Amplify app, change DNS, or attach a certificate. Those steps belong to
**FR-H** (Slab-owned): Amplify console app + custom domain `plan.ntsa.uk` +
cert. See sibling issue
https://github.com/SimonBarnett/skills-visionary/issues/85.

Pattern source: `SimonBarnett/priority-mcp` `docs/amplify-hosting.md`
(`appRoot` there is `v2/apps/mcp-catalog`; here it is `apps/mcp-catalog`).

## What is hosted

| Piece | Runtime | On Amplify |
| --- | --- | --- |
| `apps/mcp-catalog` landing (`GET /`) and `POST /mcp` | Node, Next.js route handlers, filesystem reads of `catalog/` + `data/` | Yes, Hosting compute (`WEB_COMPUTE`) |
| Local `next start` / agent stdio MCP | Long-lived process on a seat | No. Amplify compute is HTTP request/response. |
| `.grok/skills` edit / harvest / Plan seat tooling | Local agent machine | No. |

There is no Amplify Gen 2 backend (`amplify/` auth, data, or functions) in
this repo. Do not add one.

## Console settings

| Setting | Value |
| --- | --- |
| Repository | `SimonBarnett/skills-visionary` |
| Branch | `main` (repository default) |
| Monorepo | Yes |
| App root | `apps/mcp-catalog` |
| Platform | `WEB_COMPUTE` (Hosting compute / SSR). Not `WEB` (static). |
| Build image | Amazon Linux 2023 |
| Build spec | Repository root `amplify.yml` (overrides a console spec) |
| Service role | The role Amplify offers for Hosting compute logs. Do not add secret permissions. |

`WEB` static hosting publishes files. It does not run `POST /mcp`. Create the
app as Next.js SSR / Web compute. Amplify does not offer a reliable in-place
switch from `WEB` to `WEB_COMPUTE`; a static app has to be recreated.

Connecting the monorepo in the console sets `AMPLIFY_MONOREPO_APP_ROOT`. If
the app is created outside that flow, set it yourself to `apps/mcp-catalog`.
The Next.js process does not read it.

## Build, start, artifacts

`amplify.yml` runs with its working directory at the app root.

| Phase | Command |
| --- | --- |
| preBuild | `nvm use 20` |
| preBuild | `node -v` |
| preBuild | `npm ci --include=dev --no-audit --fund=false` |
| build | `npm run build` |
| build | `rm -rf .next/cache` |

`npm run build` is `node scripts/sync-skill-dag.mjs` (copy
`docs/skill-sources/skills-visionary/_dag` into `data/`),
`node scripts/check-dag.mjs` (catalog↔DAG sync + public-safe scan), and
`next build`. The check fails the build on catalog-DAG drift, dangling
edges, skill-node cycles, or secret-like blobs in DAG nodes.

The spec then deletes `.next/cache`. That cache is not used at runtime.

| Artifact field | Value |
| --- | --- |
| `baseDirectory` | `.next` (relative to `apps/mcp-catalog`) |
| `files` | `**/*` |
| Cache | `node_modules/**/*` only. Do not cache `.next/cache`. |

There is no start command in `amplify.yml`. Hosting compute starts the
Next.js server itself. Do not set a custom start command and do not point it
at `node .next/standalone/server.js`. Amplify no longer deploys Next
standalone output (aws-amplify/amplify-hosting#3682). Do not set
`output: 'standalone'` in `next.config.mjs`.

Local equivalents, from `apps/mcp-catalog`:

```bash
nvm use 20
npm ci --include=dev --no-audit --fund=false
npm test
npm run build
npm run smoke
```

`npm start` is `next start` and listens on port 3000.

Node 20, 22, and 24 are the Amplify SSR runtimes. Node 14, 16, and 18 fail
the SSR build. `package.json` `engines.node` is `>=20`. Prefer `nvm use 20`
so the Amplify build matches local.

## Environment variable names (allowlist - no secrets)

The running app needs no secrets. Do not store tokens, passwords, PATs, or
SASL material on the Amplify app.

| Name | Required | Purpose |
| --- | --- | --- |
| `AMPLIFY_MONOREPO_APP_ROOT` | Yes, in the Amplify console when the console did not set it | Must be `apps/mcp-catalog`. Build wiring only. |
| `CATALOG_PUBLIC_ORIGIN` | No | Fallback origin when the request Host is not allowlisted. Allowlisted hosts: `plan.ntsa.uk`, `*.amplifyapp.com`, and local `localhost` / `127.0.0.1`. https only, except localhost. No userinfo, path, query, or hash. |

Amplify injects its own names (`AWS_BRANCH`, `AWS_APP_ID`, and others). The
catalog code does not read them.

## Custom domain (FR-H / Slab)

Custom domain `plan.ntsa.uk` and the certificate are **Slab-owned** (FR-H
#85). This FR only documents the contract so FR-H can attach DNS after a
successful `main` deploy:

1. Domain management → Add domain → `ntsa.uk`.
2. Subdomain `plan` → branch `main`. Do not attach the apex in this step.
3. Use the certificate Amplify requests in ACM (us-east-1 for CloudFront).
4. Copy the DNS records the console shows (validation CNAME +
   `plan.ntsa.uk` → `*.amplifyapp.com`). Do not guess the target.
5. Leave other `ntsa.uk` records alone except the records Amplify lists for
   `plan`.

## HTTP surface

| Method | Path | Behavior |
| --- | --- | --- |
| GET | `/` | HTML Plan skill landing. |
| GET | `/mcp` | Discovery JSON. Not an event stream. |
| POST | `/mcp` | One JSON-RPC 2.0 object. `Content-Type: application/json`. |
| OPTIONS | `/mcp` | CORS preflight. |

`POST /mcp` methods that are implemented:

| Method | Result |
| --- | --- |
| `initialize` | Protocol `2024-11-05`, tools capability only |
| `notifications/initialized`, `initialized` | empty / ack |
| `ping` | empty result |
| `tools/list` | `list_catalog`, `get_skill` |
| `tools/call` | those two tools |

A JSON array (batched JSON-RPC) is rejected. There is no SSE `GET` and no
stdio on Amplify.

Client URL: `https://plan.ntsa.uk/mcp`.

```bash
curl -sS https://plan.ntsa.uk/mcp
curl -sS -X POST https://plan.ntsa.uk/mcp \
  -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_catalog","arguments":{}}}'
```

## Authentication and exposure

The catalog is public on purpose. The GitHub repository is already public.
Amplify does not add a login.

- `Access-Control-Allow-Origin` is `*`.
- Anyone who can POST can read every published `SKILL.md` under `catalog/`.
- Do not put live secrets, cookie jars, or private hostnames into `catalog/`
  or the DAG. The build ships those trees.

No application auth header is required or checked.

## Limits that are real on Amplify

| Limit | Effect here |
| --- | --- |
| SSR response body about 5.72 MB | Skill markdown bodies stay small. |
| Compute bundle about 220 MB uncompressed | Delete `.next/cache` in the build spec. Keep `catalog/` and `data/` so the server can read them. |
| Compute writable path is `/tmp` only | The catalog is read-only. That matches the app. |
| No Edge runtime | Keep Node.js runtime on `/` and `/mcp`. |
| Request rate | Amplify returns 429 when the app exceeds its request-token quota. `POST /mcp` is uncached. |

## Verification after FR-H deploys

Run these against the default `*.amplifyapp.com` URL before changing DNS,
then again at `https://plan.ntsa.uk` after the certificate is issued
(FR-I smoke:live can own the live gate).

1. `GET /mcp` returns HTTP 200 and tool names `list_catalog`, `get_skill`.
2. `POST /mcp` `initialize` returns `protocolVersion` `2024-11-05`.
3. `tools/call` `list_catalog` returns a non-empty `skills` array and an
   allowlisted `host` (`https://plan.ntsa.uk` or the amplifyapp.com host).
4. `GET /` shows the Plan landing and links to `bob.ntsa.uk` + GitHub.

Local pre-flight (this FR):

```bash
cd apps/mcp-catalog
npm test
npm run build
```

## Live smoke how-to (FR-I)

From `apps/mcp-catalog` (Node 20+):

```bash
npm ci --include=dev --no-audit --fund=false
npm run smoke:live
```

Override origin when testing a default Amplify hostname before DNS. Copy the
exact deployment URL from the Amplify console (it includes the branch prefix),
or set:

```bash
SMOKE_MCP_ORIGIN=https://<main-branch>.<appId>.amplifyapp.com npm run smoke:live
```

Do not invent only `https://<appId>.amplifyapp.com` unless that is the URL the
console shows for the deployed branch.

The script asserts:

1. `GET /` returns HTTP 200 (Plan landing HTML).
2. `GET /mcp` returns HTTP 200 and tool names `list_catalog`, `get_skill`.
3. `POST /mcp` `initialize` returns protocol `2024-11-05` and
   `serverInfo.name` `Plan Agent` (FR #89 display name).
4. `tools/call` `list_catalog` returns a non-empty `skills` array.

Exit 0 prints a JSON evidence block. Paste that block under **Live evidence
(FR-I)** below.

Local catalog-only check (no network): `npm run smoke`.

Also listed under **Verification after FR-H deploys** above; `smoke:live` is
the paste-ready harness for that gate.

## Live evidence (FR-I)

**Status (2026-11-23):** live. FR-H (#85) deployed. Refreshed for FR #222
(`plan-mcp-setup` in catalog + committed DAG; `listCatalogCount` 8).

| Item | Value |
| --- | --- |
| Amplify app id | `d2ae27jt2feuj7` (eu-west-2, `WEB_COMPUTE`, branch `main`) |
| Default domain | `main.d2ae27jt2feuj7.amplifyapp.com` |
| Custom domain | `plan.ntsa.uk` -> `main`, domain status `AVAILABLE`, Amplify-managed certificate |
| DNS | Cloudflare, DNS-only (not proxied): `plan` CNAME + ACM validation CNAME |
| First good build | job 4, 2026-11-21 13:39 UTC, BUILD/DEPLOY/VERIFY SUCCEED (Node 20.20.2) |
| Amplify env | `AMPLIFY_MONOREPO_APP_ROOT=apps/mcp-catalog`, `AMPLIFY_DIFF_DEPLOY=false`, `NPM_CONFIG_PRODUCTION=false`. No secrets. |

`npm run smoke:live` (origin `https://plan.ntsa.uk`) printed `smoke-mcp-live PASS`:

```json
{
  "origin": "https://plan.ntsa.uk",
  "when": "2026-11-23T20:25:08.853Z",
  "homeStatus": 200,
  "mcpGetTools": [
    "list_catalog",
    "get_skill"
  ],
  "serverInfo": {
    "name": "Plan Agent",
    "version": "0.1.0"
  },
  "protocolVersion": "2024-11-05",
  "listCatalogCount": 8,
  "listCatalogHost": "https://plan.ntsa.uk",
  "sampleSkillNames": [
    "harvest-agent-skills",
    "harvest-skills-visionary",
    "plan-bob-webhooks",
    "plan-create-repo",
    "plan-enable-prs",
    "plan-git-from-plan",
    "plan-mcp-setup",
    "visionary"
  ]
}
```

### Expected after FR-H

| Check | Expect |
| --- | --- |
| https://plan.ntsa.uk/ | HTTP 200 |
| https://plan.ntsa.uk/mcp | HTTP 200, tools include list_catalog + get_skill |
| list_catalog | non-empty skills |

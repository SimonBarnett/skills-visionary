/**
 * Live hosting smoke against plan.ntsa.uk (FR-I).
 * Default origin: https://plan.ntsa.uk  Override: SMOKE_MCP_ORIGIN
 *
 * Usage (from apps/mcp-catalog):
 *   npm run smoke:live
 *   # or: node scripts/smoke-mcp-live.mjs
 *
 * Exit 0 on PASS; prints a short evidence block for docs/amplify-hosting.md.
 * Run after FR-H (Amplify + DNS). Until then DNS/HTTPS failures are expected.
 */
import assert from 'node:assert/strict';

const origin = String(process.env.SMOKE_MCP_ORIGIN || 'https://plan.ntsa.uk').replace(
  /\/$/,
  '',
);
const mcpUrl = `${origin}/mcp`;
const homeUrl = `${origin}/`;
const timeoutMs = Number(process.env.SMOKE_MCP_TIMEOUT_MS || 60000);

async function fetchText(url, init = {}) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, { ...init, signal: ctrl.signal });
    const text = await res.text();
    return { res, text };
  } finally {
    clearTimeout(t);
  }
}

async function rpc(method, params, id = 1) {
  const { res, text } = await fetchText(mcpUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id, method, params: params || {} }),
  });
  assert.equal(res.status, 200, `HTTP ${res.status} for ${method}: ${text.slice(0, 200)}`);
  return JSON.parse(text);
}

function toolText(envelope) {
  const c = envelope?.result?.content;
  assert.ok(Array.isArray(c) && c[0]?.type === 'text', 'tool result content');
  return c[0].text;
}

const evidence = {
  origin,
  when: new Date().toISOString(),
  homeStatus: null,
  mcpGetTools: null,
  serverInfo: null,
  protocolVersion: null,
  listCatalogCount: null,
  listCatalogHost: null,
  sampleSkillNames: null,
};

const home = await fetchText(homeUrl, { method: 'GET' });
assert.equal(home.res.status, 200, `GET / expected 200, got ${home.res.status}`);
evidence.homeStatus = home.res.status;
assert.ok(
  /plan|skill|mcp|visionary/i.test(home.text),
  'GET / body should look like the Plan landing',
);

const disc = await fetchText(mcpUrl, { method: 'GET' });
assert.equal(disc.res.status, 200, `GET /mcp expected 200, got ${disc.res.status}`);
const discJson = JSON.parse(disc.text);
assert.ok(Array.isArray(discJson.tools), 'GET /mcp tools array');
assert.ok(discJson.tools.includes('list_catalog'), 'GET /mcp lists list_catalog');
assert.ok(discJson.tools.includes('get_skill'), 'GET /mcp lists get_skill');
evidence.mcpGetTools = discJson.tools;

const init = await rpc('initialize', { protocolVersion: '2024-11-05', capabilities: {} }, 1);
evidence.serverInfo = init.result?.serverInfo || null;
evidence.protocolVersion = init.result?.protocolVersion || null;
assert.equal(init.result?.protocolVersion, '2024-11-05');
assert.equal(init.result?.serverInfo?.name, 'mcp-skills-visionary');

const listEnv = await rpc('tools/call', { name: 'list_catalog', arguments: {} }, 2);
const listPayload = JSON.parse(toolText(listEnv));
const skills = Array.isArray(listPayload.skills) ? listPayload.skills : [];
assert.ok(skills.length > 0, 'list_catalog returns non-empty skills');
evidence.listCatalogCount = skills.length;
evidence.listCatalogHost = listPayload.host || null;
evidence.sampleSkillNames = skills.slice(0, 8).map((s) => s.name || s.id);

console.log('smoke-mcp-live PASS');
console.log(JSON.stringify(evidence, null, 2));
console.log(
  '\nPaste the JSON block above into docs/amplify-hosting.md under ## Live evidence (FR-I).',
);

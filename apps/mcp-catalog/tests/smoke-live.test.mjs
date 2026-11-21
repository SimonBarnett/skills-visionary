/**
 * FR-I: smoke:live harness contract (no network).
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const appRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(appRoot, '..', '..');
const script = fs.readFileSync(path.join(appRoot, 'scripts', 'smoke-mcp-live.mjs'), 'utf8');
const pkg = JSON.parse(fs.readFileSync(path.join(appRoot, 'package.json'), 'utf8'));
const hostingDoc = fs.readFileSync(path.join(repoRoot, 'docs', 'amplify-hosting.md'), 'utf8');
const readme = fs.readFileSync(path.join(appRoot, 'README.md'), 'utf8');

test('package.json exposes smoke:live', () => {
  assert.equal(pkg.scripts['smoke:live'], 'node scripts/smoke-mcp-live.mjs');
});

test('smoke-mcp-live.mjs targets plan.ntsa.uk and checks GET / + list_catalog', () => {
  assert.match(script, /plan\.ntsa\.uk/);
  assert.match(script, /SMOKE_MCP_ORIGIN/);
  assert.match(script, /list_catalog/);
  assert.match(script, /GET \//);
  assert.match(script, /homeUrl|GET \//);
  assert.match(script, /Plan Agent/);
  assert.match(script, /2024-11-05/);
});

test('docs/amplify-hosting.md has Live evidence (FR-I) paste instructions', () => {
  assert.match(hostingDoc, /Live evidence \(FR-I\)/);
  assert.match(hostingDoc, /npm run smoke:live/);
  assert.match(hostingDoc, /plan\.ntsa\.uk/);
});

test('app README documents smoke:live', () => {
  assert.match(readme, /smoke:live/);
  assert.match(readme, /plan\.ntsa\.uk/);
});

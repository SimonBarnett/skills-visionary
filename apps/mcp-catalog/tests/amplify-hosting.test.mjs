/**
 * FR-G: Amplify deploy contract for plan.ntsa.uk (amplify.yml + docs).
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const appRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(appRoot, '..', '..');
const amplifyYml = fs.readFileSync(path.join(repoRoot, 'amplify.yml'), 'utf8');
const hostingDoc = fs.readFileSync(path.join(repoRoot, 'docs', 'amplify-hosting.md'), 'utf8');
const pkg = JSON.parse(fs.readFileSync(path.join(appRoot, 'package.json'), 'utf8'));

test('amplify.yml uses apps/mcp-catalog appRoot and Node 20 preBuild', () => {
  assert.match(amplifyYml, /appRoot:\s*apps\/mcp-catalog/);
  assert.match(amplifyYml, /nvm use 20/);
  assert.match(amplifyYml, /npm ci --include=dev/);
  assert.match(amplifyYml, /npm run build/);
  assert.match(amplifyYml, /rm -rf \.next\/cache/);
  assert.match(amplifyYml, /baseDirectory:\s*\.next/);
});

test('docs/amplify-hosting.md names WEB_COMPUTE, app root, and forbids secrets', () => {
  assert.match(hostingDoc, /WEB_COMPUTE/);
  assert.match(hostingDoc, /apps\/mcp-catalog/);
  assert.match(hostingDoc, /plan\.ntsa\.uk/);
  assert.match(hostingDoc, /no secrets|Do not store tokens|forbid/i);
  assert.match(hostingDoc, /FR-H|Slab/);
  assert.match(hostingDoc, /Not `WEB` \(static\)|Not WEB \(static\)|Not `WEB`/);
});

test('build script matches amplify.yml npm run build contract', () => {
  assert.match(pkg.scripts.build, /sync-skill-dag/);
  assert.match(pkg.scripts.build, /check-dag/);
  assert.match(pkg.scripts.build, /next build/);
  assert.ok(pkg.engines?.node?.includes('20') || pkg.engines?.node === '>=20');
});

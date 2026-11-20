/**
 * FR #89: user-visible name is always "Plan Agent" (matches bobiverse #7458).
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const appRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(appRoot, '..', '..');

/** Old product display names that must not appear in served UI / MCP display. */
const FORBIDDEN = [
  /Plan skills \(visionary\)/i,
  /\bPlan skills\b/i,
  /mcp-skills-visionary/,
  /Plan \/ visionary skills/i,
  /Plan skills MCP/i,
];

function scan(label, text) {
  for (const re of FORBIDDEN) {
    assert.equal(re.test(text), false, `${label} matches forbidden ${re}`);
  }
  assert.match(text, /Plan Agent/);
}

test('landing page + layout use Plan Agent', () => {
  scan('page.tsx', fs.readFileSync(path.join(appRoot, 'app', 'page.tsx'), 'utf8'));
  scan('layout.tsx', fs.readFileSync(path.join(appRoot, 'app', 'layout.tsx'), 'utf8'));
});

test('MCP serverInfo display name is Plan Agent', () => {
  const mcp = fs.readFileSync(path.join(appRoot, 'lib', 'mcp.ts'), 'utf8');
  assert.match(mcp, /name:\s*['\"]Plan Agent['\"]/);
  scan('mcp.ts', mcp);
  const route = fs.readFileSync(path.join(appRoot, 'app', 'mcp', 'route.ts'), 'utf8');
  scan('route.ts', route);
});

test('plan mocks use Plan Agent', () => {
  scan('plan-home.html', fs.readFileSync(path.join(repoRoot, 'docs', 'mocks', 'plan-home.html'), 'utf8'));
  const err = fs.readFileSync(path.join(repoRoot, 'docs', 'mocks', 'plan-error.html'), 'utf8');
  assert.match(err, /Plan Agent/);
  assert.equal(/Plan MCP unavailable/i.test(err), false);
});

test('README leads with Plan Agent', () => {
  const readme = fs.readFileSync(path.join(repoRoot, 'README.md'), 'utf8');
  assert.match(readme, /^# Plan Agent/m);
  assert.equal(/^# skills-visionary\s*$/m.test(readme), false);
});

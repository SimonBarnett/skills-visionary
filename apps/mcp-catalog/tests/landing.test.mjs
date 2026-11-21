/**
 * FR-F: landing page source matches plan-home wireframe contract.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const appRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const page = fs.readFileSync(path.join(appRoot, 'app', 'page.tsx'), 'utf8');
const mock = fs.readFileSync(
  path.join(appRoot, '..', '..', 'docs', 'mocks', 'plan-home.html'),
  'utf8',
);

test('landing names Plan Agent and plan.ntsa.uk/mcp', () => {
  assert.match(page, /Plan Agent/);
  assert.match(page, /plan\.ntsa\.uk|mcpUrl|\/mcp/);
  assert.match(page, /list_catalog/);
  assert.match(page, /get_skill/);
  assert.match(page, /bob\.ntsa\.uk/);
  assert.match(page, /github\.com\/SimonBarnett\/skills-visionary/);
});

test('landing has empty and error UX branches', () => {
  assert.match(page, /Catalog empty|plan-empty/);
  assert.match(page, /Plan Agent unavailable|plan-error/);
});

test('mock wireframe still documents MCP URL', () => {
  assert.match(mock, /https:\/\/plan\.ntsa\.uk\/mcp/);
  assert.match(mock, /Plan Agent/);
});

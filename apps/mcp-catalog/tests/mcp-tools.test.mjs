/**
 * FR-E: catalog + required[] helpers (no Next server).
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const appRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function listSkillsFs() {
  const root = path.join(appRoot, 'catalog');
  const skills = [];
  for (const name of fs.readdirSync(root)) {
    const dir = path.join(root, name);
    if (!fs.statSync(dir).isDirectory()) continue;
    const metaPath = path.join(dir, 'meta.json');
    if (!fs.existsSync(metaPath)) continue;
    const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
    skills.push(meta.name || name);
  }
  return skills.sort();
}

function requiredFromDag(skillId) {
  const dag = JSON.parse(fs.readFileSync(path.join(appRoot, 'data', 'dag.json'), 'utf8'));
  const from = `skill:${skillId}`;
  return (dag.edges || [])
    .filter((e) => e.from === from && e.rel === 'depends_on')
    .map((e) => String(e.to || '').replace(/^skill:/, ''))
    .filter(Boolean);
}

test('catalog has public Plan Agent skills', () => {
  const ids = listSkillsFs();
  assert.ok(ids.includes('visionary'));
  assert.ok(ids.includes('plan-git-from-plan'));
  assert.ok(ids.length >= 5);
});

test('DAG required[] for plan-git-from-plan includes create/webhooks/enable', () => {
  const req = requiredFromDag('plan-git-from-plan');
  assert.ok(req.includes('plan-create-repo'));
  assert.ok(req.includes('plan-bob-webhooks'));
  assert.ok(req.includes('plan-enable-prs'));
});

test('mcp route exposes list_catalog and get_skill', () => {
  const route = fs.readFileSync(path.join(appRoot, 'app', 'mcp', 'route.ts'), 'utf8');
  const mcp = fs.readFileSync(path.join(appRoot, 'lib', 'mcp.ts'), 'utf8');
  assert.match(route, /handleMcp/);
  assert.match(mcp, /list_catalog/);
  assert.match(mcp, /get_skill/);
  assert.match(mcp, /2024-11-05/);
});

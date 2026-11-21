/**
 * FR-E local smoke: catalog non-empty (list_catalog contract).
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const appRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const root = path.join(appRoot, 'catalog');
assert.ok(fs.existsSync(root), 'catalog/ missing');
const ids = [];
for (const name of fs.readdirSync(root)) {
  const dir = path.join(root, name);
  if (!fs.statSync(dir).isDirectory()) continue;
  if (!fs.existsSync(path.join(dir, 'meta.json'))) continue;
  const meta = JSON.parse(fs.readFileSync(path.join(dir, 'meta.json'), 'utf8'));
  ids.push(meta.name || name);
}
assert.ok(ids.length > 0, 'list_catalog expected non-empty skill ids');
assert.ok(fs.existsSync(path.join(appRoot, 'data', 'dag.json')), 'data/dag.json missing');
process.stdout.write(`smoke-mcp: ok skills=${ids.length} ids=${ids.slice(0, 8).join(',')}\n`);

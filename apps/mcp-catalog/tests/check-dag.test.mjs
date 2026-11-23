/**
 * FR #81: clean tree passes check-dag; intentional catalog↔DAG drift fails.
 */
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const appRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const syncScript = path.join(appRoot, 'scripts', 'sync-skill-dag.mjs');
const checkScript = path.join(appRoot, 'scripts', 'check-dag.mjs');

function runNode(script, cwd = appRoot) {
  return spawnSync(process.execPath, [script], {
    cwd,
    encoding: 'utf8',
    env: process.env,
  });
}

// FR #222: committed data/dag.json must already match catalog.
// Amplify/CI run sync during build, which hid stale commits (plan-mcp-setup).
test('committed check-dag exits 0 without re-sync (FR #222)', () => {
  const check = runNode(checkScript);
  assert.equal(check.status, 0, check.stderr || check.stdout);
  assert.match(check.stdout, /check-dag: ok/);
});

test('sync + check-dag exit 0 on clean tree', () => {
  const sync = runNode(syncScript);
  assert.equal(sync.status, 0, sync.stderr || sync.stdout);
  const check = runNode(checkScript);
  assert.equal(check.status, 0, check.stderr || check.stdout);
  assert.match(check.stdout, /check-dag: ok/);
});

test('intentional catalog↔DAG drift fails check-dag', () => {
  const sync = runNode(syncScript);
  assert.equal(sync.status, 0, sync.stderr || sync.stdout);

  const tmpName = `_drift_${Date.now()}`;
  const driftDir = path.join(appRoot, 'catalog', tmpName);
  fs.mkdirSync(driftDir, { recursive: true });
  fs.writeFileSync(
    path.join(driftDir, 'meta.json'),
    JSON.stringify({ name: tmpName, title: 'drift', version: '0.0.0' }, null, 2),
    'utf8',
  );
  try {
    const check = runNode(checkScript);
    assert.notEqual(check.status, 0, 'expected non-zero on drift');
    assert.match(check.stderr, /missing from DAG|check-dag:/);
  } finally {
    fs.rmSync(driftDir, { recursive: true, force: true });
  }
});

/**
 * VIS-08 / FR #140: plan.ntsa.uk landing + downloads page link PlanAgent.msi.
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const appRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(appRoot, '..', '..');
const MSI =
  'https://github.com/SimonBarnett/skills-visionary/releases/latest/download/PlanAgent.msi';

test('lib/downloads exports PlanAgent.msi href', () => {
  const src = fs.readFileSync(path.join(appRoot, 'lib', 'downloads.ts'), 'utf8');
  assert.match(src, /PlanAgent\.msi/);
  assert.ok(src.includes(MSI));
});

test('landing page exposes MSI download link', () => {
  const page = fs.readFileSync(path.join(appRoot, 'app', 'page.tsx'), 'utf8');
  assert.match(page, /Downloads/);
  assert.match(page, /PlanAgent\.msi/);
  assert.match(page, /PLAN_AGENT_MSI_HREF|releases\/latest\/download\/PlanAgent\.msi/);
  assert.match(page, /href=\"\/downloads\"|href=\{\s*[\"']\/downloads[\"']\s*\}|\"\/downloads\"/);
});

test('downloads page links MSI', () => {
  const page = fs.readFileSync(path.join(appRoot, 'app', 'downloads', 'page.tsx'), 'utf8');
  assert.match(page, /PlanAgent\.msi/);
  assert.match(page, /data-role=\"msi\"/);
  assert.match(page, /PLAN_AGENT_MSI_HREF|releases\/latest\/download\/PlanAgent\.msi/);
});

test('docs mocks include MSI download links', () => {
  const home = fs.readFileSync(path.join(repoRoot, 'docs', 'mocks', 'plan-home.html'), 'utf8');
  const dl = fs.readFileSync(path.join(repoRoot, 'docs', 'mocks', 'plan-downloads.html'), 'utf8');
  assert.ok(home.includes(MSI), 'plan-home mock missing MSI href');
  assert.ok(dl.includes(MSI), 'plan-downloads mock missing MSI href');
});

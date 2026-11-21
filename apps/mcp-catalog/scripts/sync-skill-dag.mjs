/**
 * FR #81: copy docs/skill-sources/skills-visionary/_dag into apps/mcp-catalog/data.
 * Pattern: SimonBarnett/priority-mcp v2/apps/mcp-catalog/scripts/sync-skill-dag.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const appRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(appRoot, '..', '..');
const srcDir = path.join(repoRoot, 'docs', 'skill-sources', 'skills-visionary', '_dag');
const destDir = path.join(appRoot, 'data');

function fail(msg) {
  process.stderr.write(`sync-skill-dag: ${msg}\n`);
  process.exit(1);
}

for (const name of ['dag.json', 'dag-index.json']) {
  const src = path.join(srcDir, name);
  if (!fs.existsSync(src)) fail(`missing source ${src}`);
  const text = fs.readFileSync(src, 'utf8');
  if (text.includes('=======') || text.includes('<<<<<<<') || text.includes('>>>>>>>')) {
    fail(`${name} still has conflict markers — fix docs/_dag before sync`);
  }
  JSON.parse(text);
}

fs.mkdirSync(destDir, { recursive: true });
for (const name of ['dag.json', 'dag-index.json']) {
  fs.copyFileSync(path.join(srcDir, name), path.join(destDir, name));
}
const dag = JSON.parse(fs.readFileSync(path.join(destDir, 'dag.json'), 'utf8'));
process.stdout.write(
  `sync-skill-dag: ok nodes=${(dag.nodes || []).length} edges=${(dag.edges || []).length} built=${dag.built}\n`,
);

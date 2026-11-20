/**
 * FR #82: MCP handler contract without booting Next (tsx loads lib/*.ts).
 */
import assert from 'node:assert/strict';
import test from 'node:test';
import { handleMcp } from '../lib/mcp.ts';
import { listSkills } from '../lib/catalog.ts';

test('list_catalog returns non-empty skill ids', () => {
  const skills = listSkills();
  assert.ok(skills.length >= 1, 'catalog should have skills from FR-C');
  const res = handleMcp(
    {
      jsonrpc: '2.0',
      id: 1,
      method: 'tools/call',
      params: { name: 'list_catalog', arguments: {} },
    },
    'http://127.0.0.1:9',
  );
  const catalog = JSON.parse(res.result.content[0].text);
  assert.equal(catalog.host, 'http://127.0.0.1:9');
  assert.ok(Array.isArray(catalog.skills) && catalog.skills.length >= 1);
  assert.ok(catalog.skills.every((s) => typeof s.name === 'string' && s.name));
});

test('get_skill returns name/title/version/skillMd/required', () => {
  const first = listSkills()[0];
  assert.ok(first);
  const res = handleMcp(
    {
      jsonrpc: '2.0',
      id: 2,
      method: 'tools/call',
      params: { name: 'get_skill', arguments: { name: first.id } },
    },
    'https://plan.ntsa.uk',
  );
  const skill = JSON.parse(res.result.content[0].text);
  assert.equal(skill.name, first.id);
  assert.equal(typeof skill.title, 'string');
  assert.equal(typeof skill.version, 'string');
  assert.equal(typeof skill.skillMd, 'string');
  assert.ok(skill.skillMd.length > 20);
  assert.ok(Array.isArray(skill.required));
});

test('tools/list exposes only list_catalog and get_skill', () => {
  const res = handleMcp(
    { jsonrpc: '2.0', id: 3, method: 'tools/list', params: {} },
    'http://127.0.0.1:9',
  );
  const names = res.result.tools.map((t) => t.name);
  assert.deepEqual(names, ['list_catalog', 'get_skill']);
});

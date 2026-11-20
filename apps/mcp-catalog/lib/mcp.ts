import { getSkill, listSkills, requiredSkillIds, type SkillRecord } from './catalog';
import { catalogPublicOrigin } from './public-origin';

const PROTOCOL = '2024-11-05';
const SERVER = { name: 'Plan Agent', version: '0.1.0' };

const TOOLS = [
  {
    name: 'list_catalog',
    description:
      'List Plan Agent skills published on plan.ntsa.uk. Folders under catalog/ with meta.json register skills. No secrets; markdown only.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  },
  {
    name: 'get_skill',
    description:
      'Return a catalog skill leaflet plus required[] from the skills DAG. JSON: name, title, version, skillMd, required[], topic. Pass name when more than one skill exists.',
    inputSchema: {
      type: 'object',
      properties: { name: { type: 'string', description: 'Skill folder / meta.name' } },
      additionalProperties: false,
    },
  },
];

export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'content-type, authorization',
};

function textResult(text: string) {
  return { content: [{ type: 'text', text }] };
}

function jsonResult(obj: unknown) {
  return textResult(JSON.stringify(obj, null, 2));
}

function needSkill(name?: string): { ok: true; skill: SkillRecord } | { ok: false; error: string } {
  const skill = getSkill(name);
  if (skill) return { ok: true, skill };
  const all = listSkills();
  if (!name && all.length > 1) {
    return { ok: false, error: `name required; catalog has: ${all.map((s) => s.id).join(', ')}` };
  }
  return { ok: false, error: `unknown skill '${name || ''}'` };
}

function callTool(name: string, args: Record<string, unknown> | undefined, origin: string) {
  const a = args || {};
  const skillName = typeof a.name === 'string' ? a.name : undefined;

  if (name === 'list_catalog') {
    return jsonResult({
      host: origin,
      addSkill: 'add apps/mcp-catalog/catalog/<name>/meta.json + SKILL.md',
      skills: listSkills().map((s) => ({
        name: s.id,
        title: s.meta.title || s.id,
        description: s.meta.description || '',
        version: s.meta.version || '1.0.0',
        topic: s.meta.topic || null,
      })),
    });
  }

  if (name === 'get_skill') {
    const got = needSkill(skillName);
    if (!got.ok) return { isError: true, ...textResult(got.error) };
    return jsonResult({
      name: got.skill.id,
      title: got.skill.meta.title || got.skill.id,
      version: got.skill.meta.version || '1.0.0',
      skillMd: got.skill.skillMd,
      required: requiredSkillIds(got.skill.id),
      topic: got.skill.meta.topic || null,
    });
  }

  return { isError: true, ...textResult(`unknown tool '${name}'`) };
}

export function handleMcp(body: unknown, origin = catalogPublicOrigin()): unknown | null {
  if (!body || typeof body !== 'object') {
    return { jsonrpc: '2.0', error: { code: -32600, message: 'invalid request' }, id: null };
  }
  const req = body as { jsonrpc?: string; id?: unknown; method?: string; params?: unknown };
  const id = 'id' in req ? req.id : null;
  const method = String(req.method || '');

  if (method === 'initialize') {
    return {
      jsonrpc: '2.0',
      id,
      result: {
        protocolVersion: PROTOCOL,
        capabilities: { tools: {} },
        serverInfo: SERVER,
      },
    };
  }
  if (method === 'notifications/initialized' || method === 'initialized') {
    return null;
  }
  if (method === 'tools/list') {
    return {
      jsonrpc: '2.0',
      id,
      result: {
        tools: TOOLS,
        note: 'Plan Agent MCP: list_catalog / get_skill only (no ERP execute plane).',
      },
    };
  }
  if (method === 'tools/call') {
    const params = (req.params || {}) as { name?: string; arguments?: Record<string, unknown> };
    const name = String(params.name || '');
    const result = callTool(name, params.arguments, origin);
    return { jsonrpc: '2.0', id, result };
  }
  if (method === 'ping') {
    return { jsonrpc: '2.0', id, result: {} };
  }
  return {
    jsonrpc: '2.0',
    id,
    error: { code: -32601, message: `method not found: ${method}` },
  };
}

export function listedToolNames(): string[] {
  return TOOLS.map((t) => t.name);
}

import { getSkill, listSkills } from './catalog';
import { getDagTopic, getRequiredSkillIds } from './skill-dag';

const PROTOCOL = '2024-11-05';
const SERVER = { name: 'Plan MCP (skills-visionary)', version: '0.1.0' };

export const corsHeaders: Record<string, string> = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
  'Access-Control-Allow-Headers': 'content-type',
};

const TOOLS = [
  {
    name: 'list_catalog',
    description:
      'List Plan / visionary skills published for plan.ntsa.uk. .grok/skills is source of truth; catalog/ mirrors.',
    inputSchema: { type: 'object', properties: {}, additionalProperties: false },
  },
  {
    name: 'get_skill',
    description:
      'Return a catalog skill leaflet plus required[] from the skills DAG when present. JSON: name, title, version, skillMd, required[], topic.',
    inputSchema: {
      type: 'object',
      properties: { name: { type: 'string', description: 'Skill folder / meta.name' } },
      additionalProperties: false,
    },
  },
];

function textResult(text: string) {
  return { content: [{ type: 'text', text }] };
}

function jsonResult(obj: unknown) {
  return textResult(JSON.stringify(obj, null, 2));
}

function needSkill(name?: string) {
  const skill = getSkill(name);
  if (skill) return { ok: true as const, skill };
  const all = listSkills();
  if (!name && all.length > 1) {
    return {
      ok: false as const,
      error: `name required; catalog has: ${all.map((s) => s.id).join(', ')}`,
    };
  }
  return { ok: false as const, error: `unknown skill '${name || ''}'` };
}

function callTool(name: string, args: Record<string, unknown> | undefined, origin: string) {
  const a = args || {};
  const skillName = typeof a.name === 'string' ? a.name : undefined;

  if (name === 'list_catalog') {
    return jsonResult({
      host: origin,
      note: 'No execute plane on this host. Copy skills into agent home or use get_skill.',
      skills: listSkills().map((s) => ({
        name: s.id,
        title: s.meta.title,
        description: s.meta.description,
        version: s.meta.version,
        topic: s.meta.topic,
      })),
    });
  }

  if (name === 'get_skill') {
    const got = needSkill(skillName);
    if (!got.ok) return { isError: true, ...textResult(got.error) };
    let required: string[] = [];
    let topic: string | null = got.skill.meta.topic || null;
    try {
      required = getRequiredSkillIds(got.skill.id);
      topic = getDagTopic(got.skill.id) || topic;
    } catch {
      required = [];
    }
    return jsonResult({
      name: got.skill.id,
      title: got.skill.meta.title,
      version: got.skill.meta.version,
      skillMd: got.skill.skillMd,
      required,
      topic,
    });
  }

  return { isError: true, ...textResult(`unknown tool '${name}'`) };
}

type JsonRpc = {
  jsonrpc?: string;
  id?: string | number | null;
  method?: string;
  params?: Record<string, unknown>;
};

export function handleMcp(body: unknown, origin: string): unknown | null {
  const msg = (body || {}) as JsonRpc;
  const id = msg.id ?? null;
  const method = String(msg.method || '');

  if (method.startsWith('notifications/')) {
    return null;
  }

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

  if (method === 'tools/list') {
    return { jsonrpc: '2.0', id, result: { tools: TOOLS } };
  }

  if (method === 'tools/call') {
    const params = (msg.params || {}) as Record<string, unknown>;
    const name = String(params.name || '');
    const args = (params.arguments || {}) as Record<string, unknown>;
    const result = callTool(name, args, origin);
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

export function mcpDiscoverPayload(origin: string) {
  return {
    ok: true,
    origin,
    transport: 'POST JSON-RPC to /mcp',
    protocolVersion: PROTOCOL,
    tools: TOOLS.map((t) => t.name),
    note: 'Plan skills only. No ERP/execute plane. stdio is local-only via npm run stdio.',
  };
}

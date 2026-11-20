import fs from 'node:fs';
import path from 'node:path';

type DagEdge = { from?: string; to?: string; type?: string };
type DagNode = { id?: string; type?: string; topic?: string; title?: string };

type DagFile = {
  nodes?: DagNode[];
  edges?: DagEdge[];
};

function loadDag(): DagFile {
  const p = path.join(process.cwd(), 'data', 'dag.json');
  if (!fs.existsSync(p)) return { nodes: [], edges: [] };
  return JSON.parse(fs.readFileSync(p, 'utf8')) as DagFile;
}

/** Required skill ids for a catalog skill from depends_on-style edges. */
export function getRequiredSkillIds(skillId: string): string[] {
  const dag = loadDag();
  const self = `skill:${skillId}`;
  const required = new Set<string>();
  for (const e of dag.edges || []) {
    const from = String(e.from || '');
    const to = String(e.to || '');
    // skill A depends_on skill B => edge from A to B (or reverse); accept either.
    if (from === self && to.startsWith('skill:')) {
      required.add(to.slice('skill:'.length));
    }
    if (to === self && from.startsWith('skill:') && String(e.type || '').includes('depend')) {
      required.add(from.slice('skill:'.length));
    }
  }
  required.delete(skillId);
  return [...required].sort();
}

export function getDagTopic(skillId: string): string | null {
  const dag = loadDag();
  const node = (dag.nodes || []).find((n) => String(n.id || '') === `skill:${skillId}`);
  if (!node) return null;
  return typeof node.topic === 'string' ? node.topic : null;
}

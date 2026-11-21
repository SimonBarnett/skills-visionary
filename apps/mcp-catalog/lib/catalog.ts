import fs from 'node:fs';
import path from 'node:path';

export type SkillMeta = {
  name: string;
  title?: string;
  description?: string;
  version?: string;
  topic?: string;
};

export type SkillRecord = {
  id: string;
  dir: string;
  meta: SkillMeta;
  skillMd: string;
};

export function catalogRoot(): string {
  return path.join(process.cwd(), 'catalog');
}

export function dagPath(): string {
  return path.join(process.cwd(), 'data', 'dag.json');
}

export function catalogHealth(): 'ok' | 'empty' | 'error' {
  const root = catalogRoot();
  if (!fs.existsSync(root) || !fs.existsSync(dagPath())) return 'error';
  const skills = listSkills();
  if (skills.length === 0) return 'empty';
  return 'ok';
}

export function listSkills(): SkillRecord[] {
  const root = catalogRoot();
  if (!fs.existsSync(root)) return [];
  const skills: SkillRecord[] = [];
  for (const name of fs.readdirSync(root)) {
    const dir = path.join(root, name);
    if (!fs.statSync(dir).isDirectory()) continue;
    const metaPath = path.join(dir, 'meta.json');
    if (!fs.existsSync(metaPath)) continue;
    const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8')) as SkillMeta;
    const id = meta.name || name;
    const skillPath = path.join(dir, 'SKILL.md');
    const skillMd = fs.existsSync(skillPath) ? fs.readFileSync(skillPath, 'utf8') : '';
    skills.push({
      id,
      dir,
      meta: { ...meta, name: id },
      skillMd,
    });
  }
  skills.sort((a, b) => a.id.localeCompare(b.id));
  return skills;
}

export function getSkill(name?: string): SkillRecord | null {
  const all = listSkills();
  if (!name) return all.length === 1 ? all[0] : null;
  const key = name.trim().toLowerCase();
  return all.find((s) => s.id.toLowerCase() === key) || null;
}

/** depends_on targets for skill:<id> from data/dag.json (FR-E get_skill required[]). */
export function requiredSkillIds(skillId: string): string[] {
  const p = dagPath();
  if (!fs.existsSync(p)) return [];
  try {
    const dag = JSON.parse(fs.readFileSync(p, 'utf8')) as {
      edges?: { from?: string; to?: string; rel?: string }[];
    };
    const from = `skill:${skillId}`;
    const out: string[] = [];
    for (const e of dag.edges || []) {
      if (e.from !== from) continue;
      if ((e.rel || '') !== 'depends_on') continue;
      const to = String(e.to || '');
      if (to.startsWith('skill:')) out.push(to.slice('skill:'.length));
    }
    return out;
  } catch {
    return [];
  }
}

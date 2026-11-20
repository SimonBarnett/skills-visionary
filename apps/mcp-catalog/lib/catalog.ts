import fs from 'node:fs';
import path from 'node:path';

export type SkillMeta = {
  name: string;
  title: string;
  description?: string;
  version: string;
  topic?: string;
  source?: string;
};

export type SkillRecord = {
  id: string;
  dir: string;
  meta: SkillMeta;
  skillMd: string;
};

function catalogRoot(): string {
  return path.join(process.cwd(), 'catalog');
}

export function listSkills(): SkillRecord[] {
  const root = catalogRoot();
  if (!fs.existsSync(root)) return [];
  const skills: SkillRecord[] = [];
  for (const name of fs.readdirSync(root)) {
    const dir = path.join(root, name);
    if (!fs.statSync(dir).isDirectory()) continue;
    const metaPath = path.join(dir, 'meta.json');
    const skillPath = path.join(dir, 'SKILL.md');
    if (!fs.existsSync(metaPath) || !fs.existsSync(skillPath)) continue;
    const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8')) as SkillMeta;
    const id = String(meta.name || name);
    skills.push({
      id,
      dir,
      meta: { ...meta, name: id },
      skillMd: fs.readFileSync(skillPath, 'utf8'),
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

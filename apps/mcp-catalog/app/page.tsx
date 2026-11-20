import { headers } from 'next/headers';
import { listSkills } from '../lib/catalog';
import { catalogPublicOrigin } from '../lib/public-origin';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

/** Minimal stub landing; polished public page is FR-F. */
export default function Home() {
  const h = headers();
  const origin = catalogPublicOrigin({
    host: h.get('host'),
    forwardedHost: h.get('x-forwarded-host'),
    proto: h.get('x-forwarded-proto'),
  });
  const skills = listSkills();
  return (
    <main>
      <h1>Plan MCP (skills-visionary)</h1>
      <p>
        Stateless JSON-RPC at <code>{origin}/mcp</code> (protocol 2024-11-05). Tools:{' '}
        <code>list_catalog</code>, <code>get_skill</code>. No execute plane.
      </p>
      <p>
        <code>grok mcp add --transport http plan-catalog {origin}/mcp</code>
      </p>
      <h2>Skills ({skills.length})</h2>
      <ul>
        {skills.map((s) => (
          <li key={s.id}>
            <strong>
              {s.meta.title} (<code>{s.id}</code>) v{s.meta.version}
            </strong>
          </li>
        ))}
      </ul>
      <p>
        Source of truth: <code>.grok/skills</code>. Catalog mirrors under{' '}
        <code>apps/mcp-catalog/catalog/</code>.
      </p>
    </main>
  );
}

import { headers } from 'next/headers';
import { catalogHealth, listSkills } from '../lib/catalog';
import { PLAN_AGENT_MSI_HREF } from '../lib/downloads';
import { catalogPublicOrigin } from '../lib/public-origin';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

export default function Home() {
  const requestHeaders = headers();
  const origin = catalogPublicOrigin({
    host: requestHeaders.get('host'),
    forwardedHost: requestHeaders.get('x-forwarded-host'),
    proto: requestHeaders.get('x-forwarded-proto'),
  });
  const mcpUrl = `${origin}/mcp`;
  const health = catalogHealth();
  const skills = listSkills();

  if (health === 'error') {
    return (
      <>
        <p className="meta">
          <span className="badge badge-error">error</span> plan-error
        </p>
        <h1>Plan Agent unavailable</h1>
        <p>DAG check failed or the catalog data is missing. Typical causes:</p>
        <ul>
          <li>
            <code>check-dag</code> failed (catalog↔DAG drift)
          </li>
          <li>App created as static WEB instead of WEB_COMPUTE</li>
          <li>
            Custom domain <code>plan.ntsa.uk</code> not attached yet (tell Slab)
          </li>
        </ul>
        <pre>{`npm run build   # must exit 0
npm run smoke   # local MCP`}</pre>
        <p>
          MCP URL (when healthy): <code>{mcpUrl}</code>
        </p>
      </>
    );
  }

  if (health === 'empty') {
    return (
      <>
        <p className="meta">
          <span className="badge badge-empty">empty</span> plan-empty
        </p>
        <h1>Catalog empty</h1>
        <p>
          No skills published yet, or Amplify build has not synced the DAG. Check{' '}
          <code>apps/mcp-catalog/catalog/</code> and the last Amplify build log.
        </p>
        <p>
          MCP endpoint: <code>{mcpUrl}</code>
        </p>
      </>
    );
  }

  return (
    <>
      <p className="meta">
        <a href="https://bob.ntsa.uk">bob.ntsa.uk</a> · <span className="badge">plan-home</span>
      </p>
      <h1>Plan Agent</h1>
      <p>
        Public catalog for TipForm <strong>Plan</strong> seats: measurable vision packs, then create
        repo → Bob git webhooks → permit PRs — without the full build pack.
      </p>
      <h2>MCP</h2>
      <p>Connect an MCP client to:</p>
      <pre>{mcpUrl}</pre>
      <p>
        Tools: <code>list_catalog</code>, <code>get_skill</code> (DAG-aware). Skills stay public
        markdown; no secrets on this host.
      </p>
      <h2>Skills ({skills.length})</h2>
      <ul className="skill-list">
        {skills.map((s) => (
          <li key={s.id}>
            <strong>{s.id}</strong>
            {s.meta.title ? ` - ${s.meta.title}` : ''}
          </li>
        ))}
      </ul>
      <h2>Downloads</h2>
      <p>
        Windows installer:{' '}
        <a href={PLAN_AGENT_MSI_HREF} data-role="msi">
          Download PlanAgent.msi
        </a>{' '}
        - <a href="/downloads">Downloads page</a>
      </p>
      <h2>Also</h2>
      <ul>
        <li>
          <a href="https://github.com/SimonBarnett/skills-visionary">GitHub: skills-visionary</a>
        </li>
        <li>
          <a href="https://bob.ntsa.uk">bob.ntsa.uk</a>
        </li>
        <li>
          <a href="https://mcp.ntsa.uk">Sibling: Priority catalog mcp.ntsa.uk</a>
        </li>
      </ul>
    </>
  );
}

import {
  PLAN_AGENT_MSI_HREF,
  PLAN_AGENT_MSI_SHA_HREF,
  PLAN_AGENT_RELEASES_HREF,
} from '../../lib/downloads';

export const runtime = 'nodejs';
export const dynamic = 'force-static';

/** VIS-08: plan.ntsa.uk/downloads links PlanAgent.msi */
export default function DownloadsPage() {
  return (
    <>
      <p className="meta">
        <a href="/">Plan Agent</a> - <span className="badge">downloads</span>
      </p>
      <h1>Downloads</h1>
      <p>
        Windows installer for Plan Agent. The MSI is published on GitHub Releases (
        <code>plan-v*</code> tags; VIS-07).
      </p>
      <h2>Plan Agent MSI</h2>
      <ul>
        <li>
          <a href={PLAN_AGENT_MSI_HREF} data-role="msi">
            Download PlanAgent.msi
          </a>
        </li>
        <li>
          <a href={PLAN_AGENT_MSI_SHA_HREF} data-role="sha256">
            PlanAgent.msi.sha256
          </a>
        </li>
        <li>
          <a href={PLAN_AGENT_RELEASES_HREF}>Release notes</a>
        </li>
      </ul>
      <p className="meta">
        Also listed on <a href="https://bob.ntsa.uk/downloads">bob.ntsa.uk/downloads</a>.
      </p>
    </>
  );
}

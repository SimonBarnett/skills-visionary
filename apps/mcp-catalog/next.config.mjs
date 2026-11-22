/** @type {import('next').NextConfig} */
const PLAN_AGENT_MSI_HREF =
  'https://github.com/SimonBarnett/skills-visionary/releases/latest/download/PlanAgent.msi';

const nextConfig = {
  reactStrictMode: true,
  // Amplify WEB_COMPUTE (FR-G) can host the Node server; keep output default for now.
  async redirects() {
    return [
      {
        source: '/PlanAgent.msi',
        destination: PLAN_AGENT_MSI_HREF,
        permanent: false,
      },
      {
        source: '/PlanAgent.msi.sha256',
        destination: `${PLAN_AGENT_MSI_HREF}.sha256`,
        permanent: false,
      },
    ];
  },
};

export default nextConfig;
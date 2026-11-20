/** @type {import('next').NextConfig} */
const nextConfig = {
  // Amplify WEB_COMPUTE traces catalog/ + data/ into the server bundle.
  experimental: {
    outputFileTracingIncludes: {
      '/': ['./catalog/**/*', './data/**/*'],
      '/mcp': ['./catalog/**/*', './data/**/*'],
    },
  },
  async headers() {
    return [
      {
        source: '/mcp',
        headers: [{ key: 'Cache-Control', value: 'no-store' }],
      },
    ];
  },
};

export default nextConfig;

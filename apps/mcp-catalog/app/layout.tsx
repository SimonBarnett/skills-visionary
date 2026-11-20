import type { ReactNode } from 'react';

export const metadata = {
  title: 'plan.ntsa.uk - Plan MCP',
  description: 'skills-visionary Plan MCP catalog (list_catalog / get_skill)',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'system-ui, sans-serif', margin: '2rem', lineHeight: 1.5 }}>
        {children}
      </body>
    </html>
  );
}

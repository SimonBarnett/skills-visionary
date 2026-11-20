import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Plan Agent',
  description: 'Plan Agent — public skill catalog and MCP for TipForm Plan seats (plan.ntsa.uk).',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

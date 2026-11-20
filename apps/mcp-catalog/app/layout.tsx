import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'plan.ntsa.uk — Plan skills',
  description: 'Public Plan / visionary skill catalog and MCP for TipForm Plan seats.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

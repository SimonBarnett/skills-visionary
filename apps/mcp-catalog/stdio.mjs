/**
 * Optional local-only stdio MCP bridge (not served on Amplify).
 * Usage: npm run stdio
 */
import readline from 'node:readline';
import { handleMcp } from './lib/mcp.ts';

const origin = process.env.CATALOG_PUBLIC_ORIGIN || 'https://plan.ntsa.uk';
const rl = readline.createInterface({ input: process.stdin, terminal: false });
for await (const line of rl) {
  const trimmed = line.trim();
  if (!trimmed) continue;
  let body;
  try {
    body = JSON.parse(trimmed);
  } catch {
    process.stdout.write(
      `${JSON.stringify({ jsonrpc: '2.0', error: { code: -32700, message: 'parse error' } })}\n`,
    );
    continue;
  }
  const result = handleMcp(body, origin);
  if (result !== null) {
    process.stdout.write(`${JSON.stringify(result)}\n`);
  }
}

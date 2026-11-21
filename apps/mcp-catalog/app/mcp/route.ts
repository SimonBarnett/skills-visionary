import { NextRequest, NextResponse } from 'next/server';
import { corsHeaders, handleMcp, listedToolNames } from '../../lib/mcp';
import { catalogPublicOrigin } from '../../lib/public-origin';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

const responseHeaders = {
  ...corsHeaders,
  'Cache-Control': 'no-store',
};

function requestOrigin(req: NextRequest): string {
  return catalogPublicOrigin({
    host: req.headers.get('host'),
    forwardedHost: req.headers.get('x-forwarded-host'),
    proto: req.headers.get('x-forwarded-proto'),
  });
}

export async function OPTIONS() {
  return new NextResponse(null, { status: 204, headers: responseHeaders });
}

export async function GET(req: NextRequest) {
  return NextResponse.json(
    {
      ok: true,
      origin: requestOrigin(req),
      transport: 'POST JSON-RPC to /mcp',
      protocolVersion: '2024-11-05',
      tools: listedToolNames(),
      note: 'Plan Agent catalog. No secrets. stdio is not served here.',
    },
    { headers: responseHeaders },
  );
}

export async function POST(req: NextRequest) {
  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json(
      { jsonrpc: '2.0', error: { code: -32700, message: 'parse error' } },
      { status: 400, headers: responseHeaders },
    );
  }
  const result = handleMcp(body, requestOrigin(req));
  if (result === null) {
    return new NextResponse(null, { status: 204, headers: responseHeaders });
  }
  return NextResponse.json(result, { headers: responseHeaders });
}

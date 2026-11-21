const DEFAULT_ORIGIN = 'https://plan.ntsa.uk';
const EXACT_HOSTS = new Set(['plan.ntsa.uk']);

function firstToken(value: string | null | undefined): string {
  return (value || '').split(',')[0].trim();
}

export function catalogPublicOrigin(opts?: {
  host?: string | null;
  forwardedHost?: string | null;
  proto?: string | null;
  envOrigin?: string | null;
}): string {
  const fromEnv = (opts?.envOrigin || process.env.CATALOG_PUBLIC_ORIGIN || '').trim();
  if (fromEnv) {
    try {
      const url = new URL(fromEnv);
      if (!url.username && !url.password) return url.origin;
    } catch {
      /* fall through */
    }
  }

  const hostHeader = firstToken(opts?.forwardedHost || opts?.host);
  if (!hostHeader || hostHeader.startsWith('[')) return DEFAULT_ORIGIN;

  let hostname = hostHeader;
  let port = '';
  const colon = hostHeader.lastIndexOf(':');
  if (colon > -1 && hostHeader.indexOf(':') === colon) {
    hostname = hostHeader.slice(0, colon);
    port = hostHeader.slice(colon + 1);
    if (!/^\d+$/.test(port)) return DEFAULT_ORIGIN;
  }
  hostname = hostname.toLowerCase().replace(/\.$/, '');
  const local = hostname === 'localhost' || hostname === '127.0.0.1';
  const amplify = hostname.endsWith('.amplifyapp.com') && hostname !== 'amplifyapp.com';
  if (!local && !amplify && !EXACT_HOSTS.has(hostname)) return DEFAULT_ORIGIN;

  const protoRaw = firstToken(opts?.proto).toLowerCase().replace(/:$/, '');
  let scheme: string;
  if (protoRaw === 'http') {
    if (!local) return DEFAULT_ORIGIN;
    scheme = 'http';
  } else if (protoRaw === 'https') {
    scheme = 'https';
  } else {
    scheme = local ? 'http' : 'https';
  }
  if (port && local) return `${scheme}://${hostname}:${port}`;
  return `${scheme}://${hostname}`;
}

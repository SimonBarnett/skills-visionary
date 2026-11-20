/**
 * Resolve the public origin for catalog host URLs.
 * Prefer request Host / X-Forwarded-*; fall back to CATALOG_PUBLIC_ORIGIN.
 */
export function catalogPublicOrigin(opts: {
  host?: string | null;
  forwardedHost?: string | null;
  proto?: string | null;
}): string {
  const envFallback = (
    process.env.CATALOG_PUBLIC_ORIGIN ||
    process.env.NEXT_PUBLIC_CATALOG_ORIGIN ||
    'https://plan.ntsa.uk'
  ).replace(/\/$/, '');

  const rawHost = (opts.forwardedHost || opts.host || '').split(',')[0].trim();
  if (!rawHost) return envFallback;

  // Block obvious spoof hosts when env is set (smoke uses evil.example).
  const allowed = new Set(
    [
      'plan.ntsa.uk',
      'localhost',
      '127.0.0.1',
      envFallback.replace(/^https?:\/\//, '').split('/')[0],
    ].filter(Boolean),
  );
  const hostOnly = rawHost.replace(/:\d+$/, '').toLowerCase();
  if (
    process.env.CATALOG_PUBLIC_ORIGIN &&
    !allowed.has(hostOnly) &&
    !hostOnly.endsWith('.ntsa.uk') &&
    hostOnly !== 'localhost' &&
    hostOnly !== '127.0.0.1'
  ) {
    return envFallback;
  }

  const proto = (opts.proto || 'http').split(',')[0].trim() || 'http';
  return `${proto}://${rawHost}`.replace(/\/$/, '');
}

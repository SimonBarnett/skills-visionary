/**
 * FR #82 local smoke: next start + list_catalog / get_skill over POST /mcp.
 * Requires prior `npm run build`.
 */
import http from 'node:http';
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const appRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const port = 3460;
const nextBin = path.join(appRoot, 'node_modules/next/dist/bin/next');

function raw(method, urlPath, { body } = {}) {
  return new Promise((resolve, reject) => {
    const payload = body == null ? null : Buffer.from(body);
    const headers = { host: `127.0.0.1:${port}` };
    if (payload) {
      headers['content-type'] = 'application/json';
      headers['content-length'] = String(payload.length);
    }
    const req = http.request(
      { hostname: '127.0.0.1', port, path: urlPath, method, headers },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          resolve({
            status: res.statusCode,
            text: Buffer.concat(chunks).toString('utf8'),
          });
        });
      },
    );
    req.on('error', reject);
    if (payload) req.end(payload);
    else req.end();
  });
}

function rpc(method, params) {
  return raw('POST', '/mcp', {
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params: params || {} }),
  });
}

function assert(cond, message, detail) {
  if (!cond) {
    const extra = detail == null ? '' : `\n${typeof detail === 'string' ? detail : JSON.stringify(detail)}`;
    throw new Error(`${message}${extra}`);
  }
}

async function waitForReady() {
  const deadline = Date.now() + 60000;
  let last = '';
  while (Date.now() < deadline) {
    try {
      const res = await raw('GET', '/mcp');
      if (res.status === 200) return;
      last = `status ${res.status}`;
    } catch (e) {
      last = e instanceof Error ? e.message : String(e);
    }
    await new Promise((r) => setTimeout(r, 300));
  }
  throw new Error(`server did not become ready: ${last}`);
}

const child = spawn(process.execPath, [nextBin, 'start', '-p', String(port)], {
  cwd: appRoot,
  env: { ...process.env, CATALOG_PUBLIC_ORIGIN: 'https://plan.ntsa.uk' },
  stdio: ['ignore', 'pipe', 'pipe'],
});
let logs = '';
child.stdout.on('data', (c) => {
  logs += c.toString();
});
child.stderr.on('data', (c) => {
  logs += c.toString();
});

try {
  await waitForReady();

  const discover = await raw('GET', '/mcp');
  assert(discover.status === 200, 'GET /mcp', discover.status);
  const discoverBody = JSON.parse(discover.text);
  assert(
    JSON.stringify(discoverBody.tools) === JSON.stringify(['list_catalog', 'get_skill']),
    'tools',
    discoverBody.tools,
  );

  const listed = JSON.parse(
    (await rpc('tools/call', { name: 'list_catalog', arguments: {} })).text,
  );
  const catalog = JSON.parse(listed.result.content[0].text);
  assert(Array.isArray(catalog.skills) && catalog.skills.length >= 1, 'list_catalog non-empty', catalog);

  const name = catalog.skills[0].name;
  const skillRes = JSON.parse(
    (await rpc('tools/call', { name: 'get_skill', arguments: { name } })).text,
  );
  const skill = JSON.parse(skillRes.result.content[0].text);
  assert(skill.name === name, 'get_skill name', skill);
  assert(typeof skill.title === 'string', 'title');
  assert(typeof skill.version === 'string', 'version');
  assert(typeof skill.skillMd === 'string' && skill.skillMd.length > 20, 'skillMd');
  assert(Array.isArray(skill.required), 'required');

  process.stdout.write(`smoke-mcp: ok skills=${catalog.skills.length} sample=${name}\n`);
} catch (error) {
  process.stderr.write(`${logs}\n`);
  process.stderr.write(`${error instanceof Error ? error.stack : error}\n`);
  process.exitCode = 1;
} finally {
  child.kill('SIGTERM');
  await new Promise((resolve) => {
    const timer = setTimeout(() => {
      child.kill('SIGKILL');
      resolve();
    }, 3000);
    child.on('exit', () => {
      clearTimeout(timer);
      resolve();
    });
  });
}

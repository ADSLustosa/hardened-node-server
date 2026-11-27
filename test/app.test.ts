import assert from 'node:assert/strict';
import { after, before, describe, it } from 'node:test';
import { createApp } from '../src/app.ts';

describe('health response', () => {
  const server = createApp();
  let baseUrl = '';

  before(async () => {
    await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));
    const address = server.address();
    assert.ok(address !== null && typeof address === 'object');
    baseUrl = `http://127.0.0.1:${address.port}`;
  });

  after(async () => {
    server.closeAllConnections();
    await new Promise<void>((resolve, reject) => {
      server.close((err) => (err ? reject(err) : resolve()));
    });
  });

  it('responds 200 with a JSON body', async () => {
    const res = await fetch(`${baseUrl}/`);

    assert.equal(res.status, 200);
    assert.equal(res.headers.get('content-type'), 'application/json; charset=utf-8');
    assert.deepEqual(await res.json(), { status: 'ok' });
  });

  it('does not reveal the technology behind the server', async () => {
    const res = await fetch(`${baseUrl}/`);
    await res.body?.cancel();

    assert.equal(res.headers.get('x-powered-by'), null);
  });
});

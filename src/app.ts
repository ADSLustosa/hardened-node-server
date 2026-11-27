import { Buffer } from 'node:buffer';
import { createServer, type IncomingMessage, type Server, type ServerResponse } from 'node:http';

export function handleRequest(_req: IncomingMessage, res: ServerResponse): void {
  const body = JSON.stringify({ status: 'ok' });

  res.writeHead(200, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
  });
  res.end(body);
}

export function createApp(): Server {
  return createServer(handleRequest);
}

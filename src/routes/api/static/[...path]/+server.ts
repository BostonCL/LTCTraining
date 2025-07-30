import { readFileSync } from 'fs';
import { join } from 'path';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params }) => {
  try {
    const filePath = join(process.cwd(), 'static', params.path);
    console.log('Attempting to serve file:', filePath);
    
    const file = readFileSync(filePath);
    console.log('File read successfully, size:', file.length);

    const ext = params.path.split('.').pop()?.toLowerCase();
    let contentType = 'application/octet-stream';

    if (ext === 'mp3') contentType = 'audio/mpeg';
    else if (ext === 'png') contentType = 'image/png';
    else if (ext === 'jpg' || ext === 'jpeg') contentType = 'image/jpeg';

    console.log('Serving with content-type:', contentType);

    return new Response(file, {
      headers: {
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Cache-Control': 'public, max-age=31536000'
      }
    });
  } catch (error) {
    console.error('Error serving file:', error);
    return new Response('File not found', { status: 404 });
  }
};

export const OPTIONS: RequestHandler = async () => {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  });
}; 
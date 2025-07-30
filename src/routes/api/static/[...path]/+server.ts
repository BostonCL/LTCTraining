import { readFileSync } from 'fs';
import { join } from 'path';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params }) => {
  try {
    const filePath = join(process.cwd(), 'static', params.path);
    const file = readFileSync(filePath);
    
    // Determine content type based on file extension
    const ext = params.path.split('.').pop()?.toLowerCase();
    let contentType = 'application/octet-stream';
    
    if (ext === 'mp3') contentType = 'audio/mpeg';
    else if (ext === 'png') contentType = 'image/png';
    else if (ext === 'jpg' || ext === 'jpeg') contentType = 'image/jpeg';
    
    return new Response(file, {
      headers: {
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'public, max-age=31536000'
      }
    });
  } catch (error) {
    return new Response('File not found', { status: 404 });
  }
}; 
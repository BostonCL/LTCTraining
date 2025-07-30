import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params }) => {
  try {
    const filePath = join(process.cwd(), 'static', params.path);
    
    console.log('Requested file path:', params.path);
    console.log('Full file path:', filePath);
    
    // Check if file exists
    if (!existsSync(filePath)) {
      console.error('File not found:', filePath);
      console.error('This might be due to LFS files not being downloaded during build');
      
      // Return a helpful error response
      return new Response(
        JSON.stringify({
          error: 'File not found',
          message: 'This file is stored in Git LFS and may not be available in the deployment',
          path: params.path,
          suggestion: 'Check if LFS files were properly downloaded during build'
        }), 
        { 
          status: 404,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        }
      );
    }

    const file = readFileSync(filePath);
    console.log('Serving file:', params.path, 'Size:', file.length, 'bytes');

    // Check if file is actually a pointer (LFS issue)
    if (file.length < 1000 && file.toString().includes('version https://git-lfs.github.com/spec/v1')) {
      console.error('File is a Git LFS pointer, not the actual file');
      return new Response(
        JSON.stringify({
          error: 'LFS pointer found',
          message: 'This file is a Git LFS pointer and the actual file was not downloaded',
          path: params.path
        }), 
        { 
          status: 500,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        }
      );
    }

    // Determine content type based on file extension
    const ext = params.path.split('.').pop()?.toLowerCase();
    let contentType = 'application/octet-stream';

    switch (ext) {
      case 'mp3':
        contentType = 'audio/mpeg';
        break;
      case 'wav':
        contentType = 'audio/wav';
        break;
      case 'png':
        contentType = 'image/png';
        break;
      case 'jpg':
      case 'jpeg':
        contentType = 'image/jpeg';
        break;
      case 'gif':
        contentType = 'image/gif';
        break;
      case 'svg':
        contentType = 'image/svg+xml';
        break;
      case 'webp':
        contentType = 'image/webp';
        break;
      default:
        contentType = 'application/octet-stream';
    }

    console.log('Content-Type:', contentType);

    return new Response(file, {
      status: 200,
      headers: {
        'Content-Type': contentType,
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Range',
        'Cache-Control': 'public, max-age=31536000, immutable',
        'Content-Length': file.length.toString()
      }
    });
  } catch (error) {
    console.error('Error serving file:', error);
    return new Response(
      JSON.stringify({
        error: 'Internal server error',
        message: error instanceof Error ? error.message : 'Unknown error'
      }), 
      { 
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
    );
  }
};

export const OPTIONS: RequestHandler = async () => {
  return new Response(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Range'
    }
  });
}; 
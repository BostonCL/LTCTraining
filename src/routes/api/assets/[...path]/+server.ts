import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import type { RequestHandler } from './$types';

// Simple placeholder responses for when LFS files are not available
const createPlaceholderResponse = (contentType: string, filename: string) => {
  if (contentType.startsWith('image/')) {
    // Return a simple SVG placeholder for images
    const svg = `<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="#f0f0f0"/>
      <text x="50%" y="50%" font-family="Arial" font-size="16" fill="#666" text-anchor="middle">
        LFS File Not Available: ${filename}
      </text>
    </svg>`;
    return new Response(svg, {
      status: 200,
      headers: {
        'Content-Type': 'image/svg+xml',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-cache'
      }
    });
  } else if (contentType.startsWith('audio/')) {
    // Return a simple text response for audio files
    return new Response(
      `Audio file not available: ${filename}\nThis file is stored in Git LFS and not available in this deployment.`,
      {
        status: 200,
        headers: {
          'Content-Type': 'text/plain',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'no-cache'
        }
      }
    );
  }
  
  // Default fallback
  return new Response(
    `File not available: ${filename}\nThis file is stored in Git LFS and not available in this deployment.`,
    {
      status: 200,
      headers: {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'no-cache'
      }
    }
  );
};

export const GET: RequestHandler = async ({ params }) => {
  try {
    const filePath = join(process.cwd(), 'static', params.path);
    
    console.log('Requested file path:', params.path);
    console.log('Full file path:', filePath);
    
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
    
    // Check if file exists
    if (!existsSync(filePath)) {
      console.log('File not found, providing placeholder:', filePath);
      return createPlaceholderResponse(contentType, params.path);
    }

    const file = readFileSync(filePath);
    console.log('Serving file:', params.path, 'Size:', file.length, 'bytes');

    // Check if file is actually a pointer (LFS issue)
    if (file.length < 1000 && file.toString().includes('version https://git-lfs.github.com/spec/v1')) {
      console.log('File is a Git LFS pointer, providing placeholder');
      return createPlaceholderResponse(contentType, params.path);
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
    
    // Determine content type for error response
    const ext = params.path.split('.').pop()?.toLowerCase();
    let contentType = 'application/octet-stream';
    if (ext === 'png' || ext === 'jpg' || ext === 'jpeg' || ext === 'gif' || ext === 'svg' || ext === 'webp') {
      contentType = 'image/svg+xml';
    } else if (ext === 'mp3' || ext === 'wav') {
      contentType = 'text/plain';
    }
    
    return createPlaceholderResponse(contentType, params.path);
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
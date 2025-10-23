// Cloudflare R2 CDN Configuration
export const R2_CONFIG = {
  baseUrl: 'https://pub-aca3ec806e844324a6218bb0d8bf7295.r2.dev',
  paths: {
    images: '/images',
    audio: '/audio'
  }
};

// Development mode - serve files locally
const DEV_MODE = false; // Set to false for production to use R2 URLs

// Helper function to get R2 URL for an asset
export function getR2Url(path: string): string {
  // If path already starts with http, return as-is
  if (path.startsWith('http')) {
    return path;
  }
  
  // Remove leading slash if present
  const cleanPath = path.startsWith('/') ? path.slice(1) : path;
  
  // In development mode, serve files from local static directory
  if (DEV_MODE) {
    return `/${cleanPath}`;
  }
  
  return `${R2_CONFIG.baseUrl}/${cleanPath}`;
}

// Helper function for images
export function getImageUrl(imagePath: string): string {
  return getR2Url(imagePath);
}

// Helper function for audio
export function getAudioUrl(audioPath: string): string {
  return getR2Url(audioPath);
}


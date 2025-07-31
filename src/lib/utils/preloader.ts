// Preloader utility for caching audio and image files
class Preloader {
  private audioCache = new Map<string, HTMLAudioElement>();
  private imageCache = new Map<string, HTMLImageElement>();
  private loadingPromises = new Map<string, Promise<void>>();

  // Preload audio files
  async preloadAudio(audioUrls: string[]): Promise<void> {
    const promises = audioUrls.map(url => this.preloadSingleAudio(url));
    await Promise.all(promises);
  }

  private async preloadSingleAudio(url: string): Promise<void> {
    if (this.audioCache.has(url)) return;

    return new Promise((resolve, reject) => {
      const audio = new Audio();
      audio.preload = 'metadata'; // Only load metadata, not full file
      
      audio.onloadedmetadata = () => {
        this.audioCache.set(url, audio);
        resolve();
      };
      
      audio.onerror = () => {
        console.warn(`Failed to preload audio: ${url}`);
        resolve(); // Don't fail the entire preload
      };
      
      audio.src = url;
    });
  }

  // Preload image files
  async preloadImages(imageUrls: string[]): Promise<void> {
    const promises = imageUrls.map(url => this.preloadSingleImage(url));
    await Promise.all(promises);
  }

  private async preloadSingleImage(url: string): Promise<void> {
    if (this.imageCache.has(url)) return;

    return new Promise((resolve, reject) => {
      const img = new Image();
      
      img.onload = () => {
        this.imageCache.set(url, img);
        resolve();
      };
      
      img.onerror = () => {
        console.warn(`Failed to preload image: ${url}`);
        resolve(); // Don't fail the entire preload
      };
      
      img.src = url;
    });
  }

  // Get cached audio
  getCachedAudio(url: string): HTMLAudioElement | null {
    return this.audioCache.get(url) || null;
  }

  // Get cached image
  getCachedImage(url: string): HTMLImageElement | null {
    return this.imageCache.get(url) || null;
  }

  // Clear cache
  clearCache(): void {
    this.audioCache.clear();
    this.imageCache.clear();
    this.loadingPromises.clear();
  }
}

export const preloader = new Preloader(); 
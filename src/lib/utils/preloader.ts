// Enhanced preloader utility for caching audio and image files
class Preloader {
  private audioCache = new Map<string, HTMLAudioElement>();
  private imageCache = new Map<string, HTMLImageElement>();
  private loadingPromises = new Map<string, Promise<void>>();
  private imagePreloadQueue: string[] = [];
  private isPreloading = false;

  // Preload audio files with metadata only
  async preloadAudio(audioUrls: string[]): Promise<void> {
    const promises = audioUrls.map(url => this.preloadSingleAudio(url));
    await Promise.all(promises);
  }

  private async preloadSingleAudio(url: string): Promise<void> {
    if (this.audioCache.has(url)) return;

    return new Promise((resolve) => {
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

  // Aggressive image preloading with priority
  async preloadImages(imageUrls: string[], priority: 'high' | 'normal' = 'normal'): Promise<void> {
    if (priority === 'high') {
      // Load high priority images immediately
      const promises = imageUrls.map(url => this.preloadSingleImage(url, true));
      await Promise.all(promises);
    } else {
      // Queue normal priority images for background loading
      this.imagePreloadQueue.push(...imageUrls);
      this.processImageQueue();
    }
  }

  private async preloadSingleImage(url: string, immediate: boolean = false): Promise<void> {
    if (this.imageCache.has(url)) return;

    return new Promise((resolve) => {
      const img = new Image();
      
      // Set loading priority
      if (immediate) {
        img.fetchPriority = 'high';
      }
      
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

  // Process image queue in background
  private async processImageQueue(): Promise<void> {
    if (this.isPreloading || this.imagePreloadQueue.length === 0) return;
    
    this.isPreloading = true;
    
    while (this.imagePreloadQueue.length > 0) {
      const batch = this.imagePreloadQueue.splice(0, 3); // Process 3 at a time
      const promises = batch.map(url => this.preloadSingleImage(url));
      await Promise.all(promises);
      
      // Small delay to prevent blocking
      await new Promise(resolve => setTimeout(resolve, 50));
    }
    
    this.isPreloading = false;
  }

  // Preload critical images immediately
  async preloadCriticalImages(imageUrls: string[]): Promise<void> {
    return this.preloadImages(imageUrls, 'high');
  }

  // Get cached audio
  getCachedAudio(url: string): HTMLAudioElement | null {
    return this.audioCache.get(url) || null;
  }

  // Get cached image
  getCachedImage(url: string): HTMLImageElement | null {
    return this.imageCache.get(url) || null;
  }

  // Check if image is cached
  isImageCached(url: string): boolean {
    return this.imageCache.has(url);
  }

  // Clear cache
  clearCache(): void {
    this.audioCache.clear();
    this.imageCache.clear();
    this.loadingPromises.clear();
    this.imagePreloadQueue = [];
    this.isPreloading = false;
  }
}

export const preloader = new Preloader(); 
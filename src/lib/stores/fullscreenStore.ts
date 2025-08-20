import { writable, get } from 'svelte/store';
import { browser } from '$app/environment';

// Centralized fullscreen state management
export const fullscreenStore = writable({
  isFullscreen: false,
  currentElement: null as HTMLElement | null
});

// Initialize the store with current fullscreen state
if (browser) {
  // Set initial state
  fullscreenStore.set({
    isFullscreen: !!document.fullscreenElement,
    currentElement: document.fullscreenElement as HTMLElement | null
  });

  // Listen for fullscreen changes globally
  document.addEventListener('fullscreenchange', () => {
    fullscreenStore.set({
      isFullscreen: !!document.fullscreenElement,
      currentElement: document.fullscreenElement as HTMLElement | null
    });
  });
}

// Helper functions for fullscreen management
export function enterFullscreen(element: HTMLElement) {
  if (!browser || !element) return Promise.reject(new Error('No element provided'));
  
  return element.requestFullscreen().then(() => {
    fullscreenStore.set({
      isFullscreen: true,
      currentElement: element
    });
  });
}

export function exitFullscreen() {
  if (!browser) return Promise.reject(new Error('Browser not available'));
  
  return document.exitFullscreen().then(() => {
    fullscreenStore.set({
      isFullscreen: false,
      currentElement: null
    });
  });
}

export function toggleFullscreen(element: HTMLElement) {
  const { isFullscreen } = get(fullscreenStore);
  
  if (isFullscreen) {
    return exitFullscreen();
  } else {
    return enterFullscreen(element);
  }
}

// Get current store value (for use outside of reactive contexts)
export function getFullscreenState() {
  let state: any;
  fullscreenStore.subscribe(s => state = s)();
  return state;
}

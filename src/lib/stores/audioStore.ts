import { writable } from 'svelte/store';

export interface AudioState {
  isPlaying: boolean;
  progress: number;
  duration: number;
  volume: number;
  isMuted: boolean;
  currentTime: number;
  currentIndex: number;
  totalClips: number;
}

export const audioStore = writable<AudioState>({
  isPlaying: false,
  progress: 0,
  duration: 0,
  volume: 1,
  isMuted: false,
  currentTime: 0,
  currentIndex: 0,
  totalClips: 0
});

export const captionEnabled = writable(false);

export const fullscreenEnabled = writable(false);

// Audio control functions
export let audioElement: HTMLAudioElement | null = null;

export function setAudioElement(audio: HTMLAudioElement) {
  audioElement = audio;
}

export function playPause() {
  if (!audioElement) return;
  
  if (audioElement.paused) {
    audioElement.play();
    audioStore.update(state => ({ ...state, isPlaying: true }));
  } else {
    audioElement.pause();
    audioStore.update(state => ({ ...state, isPlaying: false }));
  }
}

export function replay() {
  if (!audioElement) return;
  
  audioElement.currentTime = 0;
  audioElement.play();
  audioStore.update(state => ({ ...state, isPlaying: true, currentTime: 0, progress: 0 }));
}

export function seekTo(percentage: number) {
  if (!audioElement) return;
  
  const newTime = (percentage / 100) * audioElement.duration;
  audioElement.currentTime = newTime;
  audioStore.update(state => ({ 
    ...state, 
    currentTime: newTime, 
    progress: percentage 
  }));
}

export function setVolume(newVolume: number) {
  if (!audioElement) return;
  
  // Clamp volume between 0 and 1
  const clampedVolume = Math.max(0, Math.min(1, newVolume));
  
  audioElement.volume = clampedVolume;
  audioStore.update(state => ({ 
    ...state, 
    volume: clampedVolume, 
    isMuted: clampedVolume === 0 
  }));
}

export function toggleMute() {
  if (!audioElement) return;
  
  audioStore.update(state => {
    const newMuted = !state.isMuted;
    const newVolume = newMuted ? 0 : (state.volume === 0 ? 0.5 : state.volume);
    
    if (audioElement) {
      audioElement.volume = newVolume;
    }
    
    return { 
      ...state, 
      isMuted: newMuted, 
      volume: newVolume 
    };
  });
}

export function updateProgress() {
  if (!audioElement) return;
  
  const progress = (audioElement.currentTime / audioElement.duration) * 100;
  audioStore.update(state => ({ 
    ...state, 
    currentTime: audioElement!.currentTime, 
    progress: progress 
  }));
}

export function setDuration(duration: number) {
  audioStore.update(state => ({ ...state, duration }));
}

export function setCurrentIndex(index: number) {
  audioStore.update(state => ({ ...state, currentIndex: index }));
}

export function setTotalClips(total: number) {
  audioStore.update(state => ({ ...state, totalClips: total }));
}

export function nextClip() {
  if (!audioElement) return;
  
  audioStore.update(state => {
    const nextIndex = Math.min(state.currentIndex + 1, state.totalClips - 1);
    return { ...state, currentIndex: nextIndex };
  });
}

export function previousClip() {
  if (!audioElement) return;
  
  audioStore.update(state => {
    const prevIndex = Math.max(state.currentIndex - 1, 0);
    return { ...state, currentIndex: prevIndex };
  });
}

export function canGoNext(): boolean {
  let canNext = false;
  audioStore.update(state => {
    canNext = state.currentIndex < state.totalClips - 1;
    return state;
  });
  return canNext;
}

export function canGoPrevious(): boolean {
  let canPrev = false;
  audioStore.update(state => {
    canPrev = state.currentIndex > 0;
    return state;
  });
  return canPrev;
} 
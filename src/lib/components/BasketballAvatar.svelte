<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fly, scale } from 'svelte/transition';
  import { audioStore, setAudioElement, setDuration, setCurrentIndex, setTotalClips, updateProgress } from '$lib/stores/audioStore';
  import { browser } from '$app/environment';
  import { preloader } from '$lib/utils/preloader';

  export let scripts: { text: string; audio: string }[] = [];
  export let currentIdx: number = 0;
  export let onComplete: () => void = () => {};
  export let showAvatar: boolean = true;

  let isDone = false;
  let audio: HTMLAudioElement | null = null;
  let isLoading = false;

  // Preload all audio files when component mounts
  onMount(async () => {
    if (browser && scripts.length > 0) {
      const audioUrls = scripts.map(script => script.audio);
      await preloader.preloadAudio(audioUrls);
    }
  });

  function playCurrent() {
    if (!browser) return;
    if (!scripts[currentIdx]) {
      return;
    }

    try {
      isLoading = true;
      
      // Try to get cached audio first
      const cachedAudio = preloader.getCachedAudio(scripts[currentIdx].audio);
      
      if (audio) {
        audio.pause();
        audio.currentTime = 0;
      }

      if (cachedAudio) {
        // Use cached audio
        audio = cachedAudio.cloneNode() as HTMLAudioElement;
      } else {
        // Fallback to creating new audio
        audio = new Audio(scripts[currentIdx].audio);
      }

      audio.onended = handleAudioEnd;
      audio.onloadedmetadata = () => {
        if (audio) {
          setDuration(audio.duration);
          isLoading = false;
        }
      };
      audio.ontimeupdate = () => {
        updateProgress();
      };
      audio.onplay = () => {
        audioStore.update(state => ({ ...state, isPlaying: true }));
        isLoading = false;
      };
      audio.onpause = () => {
        audioStore.update(state => ({ ...state, isPlaying: false }));
      };
      audio.onerror = () => {
        console.error('Audio playback error');
        isLoading = false;
      };
      
      setAudioElement(audio);
      setTotalClips(scripts.length);
      audio.volume = 1;
      
      // Add a small delay to prevent audio conflicts
      setTimeout(() => {
        audio?.play().catch(e => {
          if (e.name === 'AbortError') {
            // Audio play aborted - this is normal when navigating quickly
          } else {
            console.error('Audio play error:', e);
          }
          isLoading = false;
        });
      }, 100);
      
    } catch (e) {
      console.error('Error in playCurrent:', e);
      isLoading = false;
    }
  }

  function handleAudioEnd() {
    audioStore.update(state => ({ ...state, isPlaying: false }));
    if (currentIdx === scripts.length - 1) {
      isDone = true;
      onComplete();
    }
  }

  $: if (browser && scripts.length && typeof currentIdx === 'number') {
    playCurrent();
  }

  onDestroy(() => {
    if (audio) audio.pause();
  });
</script>

{#if showAvatar}
  <div class="flex flex-col items-center justify-center transform translate-x-14 translate-y-15" in:fly={{ y: 40, duration: 400 }} out:fly={{ y: 40, duration: 400 }}>
    <!-- Basketball SVG Avatar -->
    <div class="relative flex flex-col items-center">
      <div class="animate-bounce" transition:scale={{ duration: 300 }}>
        <svg width="80" height="80" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="40" cy="40" r="36" fill="#F59E42" stroke="#E67C1B" stroke-width="6"/>
          <path d="M40 4v72" stroke="#E67C1B" stroke-width="3"/>
          <path d="M4 40h72" stroke="#E67C1B" stroke-width="3"/>
          <path d="M16 16c24 16 24 32 48 48" stroke="#E67C1B" stroke-width="3"/>
          <path d="M64 16c-24 16-24 32-48 48" stroke="#E67C1B" stroke-width="3"/>
        </svg>
        <!-- Eyes -->
        <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 flex gap-3" style="margin-top:10px;">
          <div class="w-3 h-3 bg-black rounded-full"></div>
          <div class="w-3 h-3 bg-black rounded-full"></div>
        </div>
        <!-- Smile -->
        <svg class="absolute left-1/2 top-1/2 -translate-x-1/2" style="margin-top:28px;" width="30" height="10"><path d="M5 5 Q15 15 25 5" stroke="#222" stroke-width="2" fill="none"/></svg>
      </div>
    </div>
  </div>
{/if}

<!-- Loading indicator -->
{#if isLoading}
  <div class="absolute top-4 right-4 bg-blue-500 text-white px-3 py-1 rounded-full text-sm animate-pulse">
    Loading...
  </div>
{/if} 
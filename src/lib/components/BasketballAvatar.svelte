<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fly, scale } from 'svelte/transition';
  import { audioStore, setAudioElement, setDuration, setCurrentIndex, setTotalClips, updateProgress } from '$lib/stores/audioStore';

  // The component now expects the audio file path along with the text
  export let scripts: { text: string; audio: string }[] = [];
  export let onComplete: () => void = () => {};
  export let showAvatar: boolean = true;

  let currentIdx = 0;
  let isDone = false;
  let audio: HTMLAudioElement | null = null;

  function playCurrent() {
    if (!scripts[currentIdx]) return;

    // Stop any previously playing audio
    if (audio) {
      audio.pause();
      audio.currentTime = 0;
    }

    // Create a new Audio object with the static path
    audio = new Audio(scripts[currentIdx].audio);
    
    // Set up audio event listeners
    audio.onended = handleAudioEnd;
    audio.onloadedmetadata = () => {
      if (audio) {
        setDuration(audio.duration);
      }
    };
    audio.ontimeupdate = () => {
      updateProgress();
    };
    audio.onplay = () => {
      audioStore.update(state => ({ ...state, isPlaying: true }));
    };
    audio.onpause = () => {
      audioStore.update(state => ({ ...state, isPlaying: false }));
    };

    // Set the audio element in the store
    setAudioElement(audio);
    setCurrentIndex(currentIdx);
    setTotalClips(scripts.length);
    
    // Set initial volume
    audio.volume = 1;
    
    // Start playing
    audio.play();
  }

  function handleAudioEnd() {
    audioStore.update(state => ({ ...state, isPlaying: false }));
    // Do not auto-advance. Only call onComplete if at the last clip.
    if (currentIdx === scripts.length - 1) {
      isDone = true;
      onComplete();
    }
  }

  // Watch for changes in the current index from the store
  $: storeState = $audioStore;
  $: if (storeState.currentIndex !== currentIdx && storeState.currentIndex >= 0 && storeState.currentIndex < scripts.length) {
    currentIdx = storeState.currentIndex;
    playCurrent();
  }

  onMount(() => {
    playCurrent();
    return () => {
      if (audio) audio.pause();
    };
  });
  
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
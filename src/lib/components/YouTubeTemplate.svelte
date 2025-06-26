<script lang="ts">
import { onMount } from 'svelte';
import BasketballAvatar from '$lib/components/BasketballAvatar.svelte';
import VideoControls from '$lib/components/VideoControls.svelte';
import { captionEnabled, audioStore, nextClip, previousClip, fullscreenEnabled } from '$lib/stores/audioStore';

export let script: { text: string; audio: string }[] = [];
export let title: string = '';
export let description: string = '';

$: ccEnabled = $captionEnabled;
$: audioState = $audioStore;
$: currentCaption = script[audioState.currentIndex]?.text || '';
$: canGoNext = !audioState.isPlaying && audioState.progress >= 99 && audioState.currentIndex < script.length - 1;
$: canGoPrevious = audioState.currentIndex > 0;

let playerArea: HTMLDivElement;
$: isFullscreen = $fullscreenEnabled;

function handleToggleFullscreen() {
  if (!isFullscreen) {
    if (playerArea?.requestFullscreen) {
      playerArea.requestFullscreen();
    }
  } else {
    if (document.fullscreenElement) {
      document.exitFullscreen();
    }
  }
}

onMount(() => {
  const handler = () => {
    fullscreenEnabled.set(!!document.fullscreenElement);
  };
  document.addEventListener('fullscreenchange', handler);
  return () => document.removeEventListener('fullscreenchange', handler);
});
</script>

<div class="w-full max-w-3xl mx-auto px-4">
  <!-- Video Player Area -->
  <div bind:this={playerArea} class="w-full bg-black rounded-lg overflow-hidden shadow-lg mb-6 relative">
    <div class="relative aspect-video bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center w-full">
      <!-- Basketball Avatar in the center -->
      <div class="relative z-10">
        <BasketballAvatar scripts={script} />
      </div>
      <!-- Overlay Navigation Buttons -->
      <button class="absolute left-3 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center bg-black bg-opacity-40 text-white rounded-full shadow hover:bg-opacity-60 transition disabled:opacity-30 disabled:cursor-not-allowed z-20" on:click={previousClip} disabled={!canGoPrevious} aria-label="Previous">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
      </button>
      <button class="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center bg-black bg-opacity-40 text-white rounded-full shadow hover:bg-opacity-60 transition disabled:opacity-30 disabled:cursor-not-allowed z-20" on:click={nextClip} disabled={!canGoNext} aria-label="Next">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
      </button>
      <!-- Play button overlay (optional) -->
      <div class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
        <div class="bg-white bg-opacity-20 rounded-full p-4">
          <svg class="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z"/>
          </svg>
        </div>
      </div>
      <!-- Closed Caption Overlay -->
      {#if ccEnabled}
        <div class="absolute bottom-6 left-1/2 -translate-x-1/2 w-full flex justify-center pointer-events-none z-20">
          <div class="bg-black bg-opacity-60 text-white text-base px-4 py-1 rounded-md max-w-2xl text-center font-medium" style="font-weight: 400;">
            {currentCaption}
          </div>
        </div>
      {/if}
    </div>
    <!-- Video Controls at the bottom -->
    <VideoControls onToggleFullscreen={handleToggleFullscreen} fullscreen={isFullscreen} />
  </div>
  <!-- Video Title -->
  <h1 class="w-full text-2xl font-bold text-gray-900 mb-2">{title}</h1>
  <!-- Video Description -->
  <p class="w-full text-gray-700 mb-4">{description}</p>
</div> 
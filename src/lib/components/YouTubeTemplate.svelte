<script lang="ts">
import { onMount } from 'svelte';
import BasketballAvatar from '$lib/components/BasketballAvatar.svelte';
import VideoControls from '$lib/components/VideoControls.svelte';
import WhiteboardAnimation from '$lib/components/WhiteboardAnimation.svelte';
import { captionEnabled, audioStore, nextClip, previousClip, fullscreenEnabled, setTotalClips } from '$lib/stores/audioStore';

export let script: ({ text: string; audio: string; whiteboardText?: string[]; image?: string })[] = [];
export let title: string = '';
export let image: string | undefined = undefined;
export let showAvatar: boolean = true;
export let isSubmoduleComplete: boolean = false;
export let onNextSubmodule: (() => void) | undefined;
export let completionButtonText: string | undefined = undefined;
export let onCompletionButtonClick: (() => void) | undefined = undefined;

$: ccEnabled = $captionEnabled;
$: audioState = $audioStore;
$: currentIdx = $audioStore.currentIndex;
$: currentScript = script[currentIdx] || script[0];
$: currentCaption = currentScript?.text || '';
$: canGoNext = (
  isSubmoduleComplete ||
  (
    audioState.currentIndex < script.length - 1 &&
    (!audioState.isPlaying && audioState.progress >= 99)
  )
);
$: canGoPrevious = audioState.currentIndex > 0;
$: showCompletionButton = audioState.currentIndex === script.length - 1 && audioState.progress >= 100 && completionButtonText && onCompletionButtonClick;

$: accumulatedWhiteboardText = script
  .slice(0, currentIdx + 1)
  .map(s => s.whiteboardText && s.whiteboardText[0])
  .filter((line): line is string => Boolean(line));

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

function handleNextArrow() {
  if (audioState.currentIndex === script.length - 1 && isSubmoduleComplete && onNextSubmodule) {
    onNextSubmodule();
  } else {
    nextClip();
  }
}

onMount(() => {
  setTotalClips(script.length);
  const handler = () => {
    fullscreenEnabled.set(!!document.fullscreenElement);
  };
  document.addEventListener('fullscreenchange', handler);
  return () => document.removeEventListener('fullscreenchange', handler);
});

$: setTotalClips(script.length);
</script>

<div class="w-full max-w-5xl px-4 mx-auto">
  <!-- Video Player Area -->
  <div bind:this={playerArea} class="w-full bg-black rounded-lg overflow-hidden shadow-lg mb-6 relative">
    <div class="relative aspect-video bg-black w-full overflow-hidden">
      {#if accumulatedWhiteboardText.length > 0}
        <!-- Whiteboard Animation -->
        <div class="absolute inset-0 z-10 bg-white">
          <WhiteboardAnimation 
            textLines={accumulatedWhiteboardText}
            animateIndex={accumulatedWhiteboardText.length - 1}
            drawSpeed={0.03}
          />
        </div>
      {:else if currentScript.image}
        <img 
          src={currentScript.image} 
          alt="Module visual" 
          class="w-full h-full z-0 bg-white object-contain" 
          style="
            object-fit: contain;
            object-position: center center;
            filter: brightness(0.98);
            display: block;
            margin: 0 auto;
            background: white;
          " 
        />
      {:else if image && image !== undefined}
        <img 
          src={image} 
          alt="Module visual" 
          class="w-full h-full z-0 bg-white object-contain" 
          style="
            object-fit: contain;
            object-position: center center;
            filter: brightness(0.98);
            display: block;
            margin: 0 auto;
            background: white;
          " 
        />
      {/if}
      <!-- Basketball Avatar in the center -->
      <BasketballAvatar scripts={script} currentIdx={currentIdx} showAvatar={showAvatar} />
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
    <!-- Navigation Buttons above the duration bar -->
    <div class="w-full flex justify-between items-center mt-0 mb-0 px-0">
      <button class="w-12 h-12 flex items-center justify-center bg-black bg-opacity-40 text-white rounded-full shadow hover:bg-opacity-60 transition disabled:opacity-30 disabled:cursor-not-allowed" on:click={previousClip} disabled={!canGoPrevious} aria-label="Previous">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
      </button>
      {#if showCompletionButton}
        <button 
          on:click={onCompletionButtonClick}
          class="w-32 px-0 py-3 rounded-lg bg-blue-600 bg-opacity-90 text-white font-semibold shadow hover:bg-blue-700 hover:bg-opacity-100 transition flex items-center justify-center text-lg"
        >
          {completionButtonText}
        </button>
      {:else if audioState.currentIndex === script.length - 1 && isSubmoduleComplete && audioState.progress >= 99}
        <button class="w-32 px-0 py-3 rounded-lg bg-blue-600 bg-opacity-80 text-white font-semibold shadow hover:bg-blue-700 hover:bg-opacity-100 transition flex items-center justify-center" on:click={handleNextArrow} aria-label="Next submodule">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
        </button>
      {:else}
        <button class="w-12 h-12 flex items-center justify-center bg-black bg-opacity-40 text-white rounded-full shadow hover:bg-opacity-60 transition disabled:opacity-30 disabled:cursor-not-allowed" on:click={handleNextArrow} disabled={!canGoNext} aria-label="Next">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
        </button>
      {/if}
    </div>
    <VideoControls onToggleFullscreen={handleToggleFullscreen} fullscreen={isFullscreen} />
  </div>
  <!-- Video Title -->
  <h1 class="w-full text-2xl font-bold text-gray-900 mb-2">{title}</h1>
  <!-- Video Description -->
  <p class="w-full text-gray-700 mb-4">{currentScript.text}</p>
</div> 
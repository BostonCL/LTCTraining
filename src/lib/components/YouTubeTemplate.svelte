<script lang="ts">
import { onMount } from 'svelte';
import BasketballAvatar from '$lib/components/BasketballAvatar.svelte';
import VideoControls from '$lib/components/VideoControls.svelte';
import WhiteboardAnimation from '$lib/components/WhiteboardAnimation.svelte';
import { captionEnabled, audioStore, nextClip, previousClip, fullscreenEnabled, setTotalClips, setCurrentIndex, loadProgress, saveProgress } from '$lib/stores/audioStore';
import { preloader } from '$lib/utils/preloader';

  // Props
  export let script: Array<{
    text: string;
    audio: string;
    whiteboardText?: string[];
    image?: string;
  }> = [];
  export let title: string = '';
  export let image: string | undefined = undefined;
  export let showAvatar: boolean = true;
  export let onNextSubmodule: (() => void) | undefined;
  export let completionButtonText: string | undefined = undefined;
  export let onCompletionButtonClick: (() => void) | undefined = undefined;
  export let progressId: string;
  export let nextButtonText: string = "Next";

$: ccEnabled = $captionEnabled;
$: audioState = $audioStore;
let currentIdx = 0;
let imageLoading = false;
let currentImageUrl = '';

onMount(() => {
  setTotalClips(script.length);
  // Restore progress for this module/submodule
  currentIdx = loadProgress(progressId);
  
  // Aggressive preloading for better performance
  const preloadResources = async () => {
    const imageUrls = [];
    if (image) imageUrls.push(image);
    script.forEach(item => {
      if (item.image) imageUrls.push(item.image);
    });
    
    if (imageUrls.length > 0) {
      // Preload critical images immediately
      await preloader.preloadCriticalImages(imageUrls);
    }
  };
  
  preloadResources();
  
  const handler = () => {
    fullscreenEnabled.set(!!document.fullscreenElement);
  };
  document.addEventListener('fullscreenchange', handler);
  
  return () => {
    document.removeEventListener('fullscreenchange', handler);
  };
});

function goToNextSlide() {
  if (currentIdx < script.length - 1) {
    currentIdx += 1;
    saveProgress(progressId, currentIdx);
  }
}

function goToPreviousSlide() {
  if (currentIdx > 0) {
    currentIdx -= 1;
    saveProgress(progressId, currentIdx);
  }
}

$: currentScript = script[currentIdx] || script[0];
$: currentCaption = currentScript?.text || '';
$: canGoNext = (
  currentIdx < script.length - 1 &&
  (!audioState.isPlaying && audioState.progress >= 99)
);
$: canGoPrevious = currentIdx > 0;
$: showCompletionButton = currentIdx === script.length - 1 && audioState.progress >= 100 && completionButtonText && onCompletionButtonClick;
$: showNextButton = currentIdx === script.length - 1 && audioState.progress >= 99;

$: accumulatedWhiteboardText = currentScript.whiteboardText || [];

// Preload next image when current index changes
$: if (currentScript?.image && currentScript.image !== currentImageUrl) {
  currentImageUrl = currentScript.image;
  // Preload the next image immediately
  preloader.preloadCriticalImages([currentScript.image]);
}

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
  if (showNextButton && onNextSubmodule) {
    onNextSubmodule();
  } else {
    goToNextSlide();
  }
}

// Save progress whenever currentIdx changes
$: if (progressId && typeof currentIdx === 'number') {
  saveProgress(progressId, currentIdx);
}

$: if (progressId) {
  const saved = loadProgress(progressId);
  if (typeof saved === 'number' && saved !== currentIdx) {
    currentIdx = saved;
  }
}

function handleImageLoad() {
  imageLoading = false;
}

function handleImageError() {
  imageLoading = false;
  console.error('Failed to load image');
}

function getImageSrc(imageUrl: string): string {
  // Check if image is cached and return optimized version
  if (preloader.isImageCached(imageUrl)) {
    return imageUrl;
  }
  return imageUrl;
}
</script>

<div class="w-full max-w-5xl px-4 mx-auto mt-8">
  <!-- Video Player Area -->
  <div bind:this={playerArea} class="w-full bg-black rounded-lg overflow-hidden shadow-lg mb-6 relative">
    <div class="relative aspect-video bg-black w-full overflow-hidden">
      {#if accumulatedWhiteboardText.length > 0}
        <!-- Whiteboard Animation -->
        <div class="absolute inset-0 z-10 bg-white">
          <WhiteboardAnimation 
            textLines={accumulatedWhiteboardText}
            drawSpeed={0.03}
          />
        </div>
      {:else if currentScript.image}
        <img 
          src={getImageSrc(currentScript.image)} 
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
          loading="eager"
          fetchpriority="high"
          on:load={handleImageLoad}
          on:error={handleImageError}
        />
      {:else if image && image !== undefined}
        <img 
          src={getImageSrc(image)} 
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
          loading="eager"
          fetchpriority="high"
          on:load={handleImageLoad}
          on:error={handleImageError}
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
      <button class="w-12 h-12 flex items-center justify-center bg-black bg-opacity-40 text-white rounded-full shadow hover:bg-opacity-60 transition disabled:opacity-30 disabled:cursor-not-allowed" on:click={goToPreviousSlide} disabled={!canGoPrevious} aria-label="Previous">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
      </button>
      {#if showCompletionButton}
        <button 
          on:click={onCompletionButtonClick}
          class="w-32 px-0 py-3 rounded-lg bg-blue-600 bg-opacity-90 text-white font-semibold shadow hover:bg-blue-700 hover:bg-opacity-100 transition flex items-center justify-center text-lg"
        >
          {completionButtonText}
        </button>
      {:else if showNextButton}
        <button class="w-32 px-4 py-3 rounded-lg bg-blue-600 bg-opacity-80 text-white font-semibold shadow hover:bg-blue-700 hover:bg-opacity-100 transition flex items-center justify-center" on:click={handleNextArrow} aria-label="Next">
          {nextButtonText}
        </button>
      {:else}
        <button class="w-12 h-12 flex items-center justify-center bg-black bg-opacity-40 text-white rounded-full shadow hover:bg-opacity-60 transition disabled:opacity-30 disabled:cursor-not-allowed" on:click={handleNextArrow} disabled={!canGoNext} aria-label="Next">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
        </button>
      {/if}
    </div>
    <VideoControls onToggleFullscreen={handleToggleFullscreen} fullscreen={isFullscreen} currentIdx={currentIdx} onNext={goToNextSlide} onPrevious={goToPreviousSlide} />
  </div>
  <!-- Video Title -->
  <h1 class="w-full text-2xl font-bold text-gray-900 mb-2">{title}</h1>
  <!-- Video Description -->
  <p class="w-full text-gray-700 mb-4">{currentScript.text}</p>
</div> 
<script lang="ts">
  import { audioStore, playPause, replay, seekTo, setVolume, toggleMute, nextClip, previousClip } from '$lib/stores/audioStore';
  import { captionEnabled } from '$lib/stores/audioStore';
  import { fullscreenStore } from '$lib/stores/fullscreenStore';
  import { DEV_FEATURES } from '$lib/config/dev';
  export let onToggleFullscreen: () => void;
  export let fullscreen = false;
  export let currentIdx: number = 0;
  export let onNext: (() => void) | undefined;
  export let onPrevious: (() => void) | undefined;

  let progressBar: HTMLElement;
  let volumeSlider: HTMLInputElement;

  // Use centralized fullscreen state for consistency
  $: fullscreenState = $fullscreenStore.isFullscreen;

  function handleProgressClick(event: MouseEvent) {
    if (!progressBar || !canSeek) return;
    
    const rect = progressBar.getBoundingClientRect();
    const clickX = event.clientX - rect.left;
    const percentage = (clickX / rect.width) * 100;
    seekTo(percentage);
  }

  function handleVolumeChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const newVolume = parseFloat(target.value);
    setVolume(newVolume);
  }

  function formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  // Subscribe to the audio store
  $: audioState = $audioStore;
  $: canGoNext = audioState.currentIndex < audioState.totalClips - 1 && audioState.progress >= 95;
  $: canGoPrevious = audioState.currentIndex > 0;
  $: canSeek = !audioState.isPlaying && audioState.progress >= 99;
  $: ccEnabled = $captionEnabled;
  $: progressCurrent = typeof currentIdx === 'number' && currentIdx > 0 ? currentIdx + 1 : audioState.currentIndex + 1;
  $: progressTotal = audioState.totalClips;

  function toggleCC() {
    captionEnabled.update(v => !v);
  }
</script>

<div class="bg-black bg-opacity-70 text-white p-2 rounded-b-md border-t border-gray-700">
  <!-- Progress Bar -->
  <div class="mb-2">
    <div 
      bind:this={progressBar}
      class="w-full h-1 bg-gray-500 rounded cursor-pointer relative"
      on:click={handleProgressClick}
      on:keydown={(e) => {
        if (!canSeek) return;
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          handleProgressClick(e as any);
        }
      }}
      role="slider"
      tabindex="0"
      aria-label="Video progress"
      aria-valuemin="0"
      aria-valuemax="100"
      aria-valuenow={audioState.progress}
      style="opacity: {canSeek ? 1 : 0.6}; cursor: {canSeek ? 'pointer' : 'not-allowed'};"
    >
      <div 
        class="h-full bg-red-500 rounded transition-all duration-100"
        style="width: {audioState.progress}%"
      ></div>
      <div 
        class="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-red-500 rounded-full border border-white"
        style="left: calc({audioState.progress}% - 6px)"
      ></div>
    </div>
  </div>

  <!-- Controls Row -->
  <div class="flex items-center justify-between text-sm">
    <!-- Left Controls -->
    <div class="flex items-center space-x-2">
      <!-- Play/Pause Button -->
      <button 
        class="text-white hover:text-gray-300 transition-colors p-1"
        on:click={playPause}
        aria-label={audioState.isPlaying ? 'Pause' : 'Play'}
      >
        {#if audioState.isPlaying}
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z"/>
          </svg>
        {:else}
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M8 5v14l11-7z"/>
          </svg>
        {/if}
      </button>

      <!-- Replay Button -->
      <button 
        class="text-white hover:text-gray-300 transition-colors p-1"
        on:click={replay}
        aria-label="Replay"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/>
        </svg>
      </button>

      <!-- Development Navigation Buttons -->
      {#if DEV_FEATURES.showVideoNavigationButtons}
        <!-- Previous Button -->
        <button 
          class="text-white hover:text-gray-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed p-1"
          on:click={onPrevious ? onPrevious : previousClip}
          disabled={!canGoPrevious}
          aria-label="Previous clip"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/>
          </svg>
        </button>

        <!-- Next Button -->
        <button 
          class="text-white hover:text-gray-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed p-1"
          on:click={onNext ? onNext : nextClip}
          disabled={!canGoNext}
          aria-label="Next clip"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/>
          </svg>
        </button>
      {/if}

      <!-- Volume Control -->
      <div class="relative flex items-center group ml-1">
        <button 
          class="text-white hover:text-gray-300 transition-colors p-1"
          on:click={toggleMute}
          aria-label={audioState.isMuted || audioState.volume === 0 ? 'Unmute' : 'Mute'}
        >
          {#if audioState.isMuted || audioState.volume === 0}
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>
            </svg>
          {:else if audioState.volume < 0.5}
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M18.5 12c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM5 9v6h4l5 5V4L9 9H5z"/>
            </svg>
          {:else}
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
            </svg>
          {/if}
        </button>

        <!-- Volume Slider -->
        <div class="ml-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
          <input
            bind:this={volumeSlider}
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={audioState.volume}
            on:input={handleVolumeChange}
            class="w-14 h-1 bg-gray-500 rounded appearance-none cursor-pointer slider"
            aria-label="Volume control"
          />
        </div>

        <!-- Closed Caption Button -->
        <button
          class="ml-2 px-2 py-0.5 rounded border border-gray-400 bg-white text-black text-xs font-semibold focus:outline-none transition-colors duration-150 hover:bg-gray-200"
          aria-label="Closed captions"
          on:click={toggleCC}
          style="line-height: 1.1;"
        >
          CC
        </button>
      </div>
    </div>

    <!-- Right Controls -->
    <div class="flex items-center space-x-2 ml-auto">
      <!-- Time Display -->
      <div class="text-xs text-gray-300">
        {formatTime(audioState.currentTime)} / {formatTime(audioState.duration)}
      </div>

      <!-- Progress Text -->
      <div class="text-xs text-gray-300">
        {progressCurrent} / {progressTotal}
      </div>

      <!-- Fullscreen Button -->
      <button
        class="ml-2 p-1 rounded focus:outline-none hover:bg-gray-700 transition-colors flex items-center justify-center"
        aria-label={fullscreen ? 'Exit fullscreen' : 'Enter fullscreen'}
        on:click={onToggleFullscreen}
        style="width: 2.25rem; height: 2.25rem;"
      >
        {#if fullscreen}
          <!-- Exit Fullscreen Icon (L-corners outward) -->
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4h6M4 4v6M20 4h-6M20 4v6M4 20h6M4 20v-6M20 20h-6M20 20v-6"/>
          </svg>
        {:else}
          <!-- Enter Fullscreen Icon (L-corners inward) -->
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 9L4 4M15 9l5-5M9 15l-5 5M15 15l5 5"/>
          </svg>
        {/if}
      </button>
    </div>
  </div>
</div>

<style>
  .slider::-webkit-slider-thumb {
    appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #ef4444;
    cursor: pointer;
  }

  .slider::-moz-range-thumb {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: #ef4444;
    cursor: pointer;
    border: none;
  }
</style> 
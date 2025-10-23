<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { audioStore, setAudioElement, setDuration, setCurrentIndex, setTotalClips, updateProgress, audioElement } from '$lib/stores/audioStore';
  import { browser } from '$app/environment';
  import { getR2Url } from '$lib/config/r2';
  import { preloader } from '$lib/utils/preloader';

  export let scripts: { text: string; audio: string | string[]; whiteboardText?: string[] | string[][]; image?: string; titleAudio?: string; imageStyle?: string; additionalImage?: string; videoAnimation?: string; }[] = [];
  export let currentIdx: number = 0;
  export let onComplete: () => void = () => {};
  export let showAvatar: boolean = true;

  // Core state
  let audio: HTMLAudioElement | null = null;
  let isLoading = false;
  let avatarVisible = false;
  let isTalking = false;
  
  // Basketball video state
  let basketballVideo: HTMLVideoElement | null = null;
  let currentVideoSrc = getR2Url('/images/module2_sellingtitle_01_animation_no_background.webm');
  
  // Animation states
  let animationState: 'hidden' | 'bouncing-in' | 'playing' | 'bouncing-out' = 'hidden';
  let bounceOffset = 0; // For manual bounce animation
  
  // Avatar configuration
  let avatarMode = 'video'; // 'image' or 'video'

  // Preload all audio files when component mounts
  onMount(async () => {
    if (browser && scripts.length > 0) {
      const audioUrls = scripts.map(script => 
        Array.isArray(script.audio) ? script.audio[0] : script.audio
      );
      await preloader.preloadAudio(audioUrls);
    }
  });

  // Watch audio state and sync with basketball video
  $: isTalking = $audioStore.isPlaying;
  $: currentAudioTime = $audioStore.currentTime;
  $: audioProgress = $audioStore.progress;
  
  // Determine video source based on current script
  $: {
    const currentScript = scripts[currentIdx];
    if (currentScript?.videoAnimation) {
      avatarMode = 'video';
      currentVideoSrc = currentScript.videoAnimation;
    } else {
      avatarMode = 'video';
      currentVideoSrc = getR2Url('/images/module2_sellingtitle_01_animation_no_background.webm');
    }
  }
  
  // Create a unique key for video element to force re-render when source changes
  $: videoKey = currentVideoSrc;
  
  // Sync basketball video with audio controls - only control playback, not visibility
  $: if (basketballVideo && animationState === 'playing' && scripts[currentIdx]?.videoAnimation) {
    if (isTalking) {
      // Audio is playing, ensure video is playing
      if (basketballVideo.paused) {
        basketballVideo.play().catch(e => console.log('Video play error:', e));
      }
    } else {
      // Audio is paused, pause the video (but keep basketball visible)
      if (!basketballVideo.paused) {
        basketballVideo.pause();
      }
    }
  }
  
  // Handle seek functionality - sync video with audio time
  $: if (basketballVideo && animationState === 'playing' && scripts[currentIdx]?.videoAnimation && currentAudioTime !== undefined) {
    // Only sync if there's a significant difference to avoid constant updates
    const timeDiff = Math.abs(basketballVideo.currentTime - currentAudioTime);
    if (timeDiff > 0.1) {
      basketballVideo.currentTime = currentAudioTime;
    }
  }
  
  // Handle restart functionality - reset video when audio restarts
  $: if (basketballVideo && animationState === 'playing' && scripts[currentIdx]?.videoAnimation && audioProgress === 0 && currentAudioTime === 0) {
    basketballVideo.currentTime = 0;
    if (isTalking) {
      basketballVideo.play().catch(e => console.log('Video restart error:', e));
    }
  }

  // Clean bounce animation functions
  function startBounceIn() {
    if (animationState !== 'hidden') return;
    
    animationState = 'bouncing-in';
    avatarVisible = true;
    
    // Only pause audio and video during bounce-in if they're currently playing
    // This prevents the basketball from disappearing when user pauses
    if (audioElement && audioElement.currentTime > 0) {
      audioElement.pause();
      audioStore.update(state => ({ ...state, isPlaying: false }));
    }
    if (basketballVideo && basketballVideo.currentTime > 0) {
      basketballVideo.pause();
    }
    
    console.log('Starting bounce-in animation');
  }

  function completeBounceIn() {
    animationState = 'playing';
    
    // Start audio and video together after bounce-in completes
    setTimeout(() => {
      if (audioElement) {
        audioElement.play().catch(e => console.log('Audio play error:', e));
        audioStore.update(state => ({ ...state, isPlaying: true }));
      }
      if (basketballVideo) {
        // Ensure video starts at the same time as audio
        basketballVideo.currentTime = audioElement?.currentTime || 0;
        basketballVideo.play().catch(e => console.log('Video play error:', e));
      }
      console.log('Audio and video started after bounce-in');
    }, 200);
  }

  function startBounceOut() {
    if (animationState !== 'playing') return;
    
    animationState = 'bouncing-out';
    console.log('Starting bounce-out animation');
    
    // Hide avatar after bounce-out animation completes (1s)
    setTimeout(() => {
      avatarVisible = false;
      animationState = 'hidden';
    }, 1000);
  }

  function handleVideoLoaded() {
    console.log('Basketball video loaded');
  }

  function handleVideoTimeUpdate() {
    // Keep video in sync with audio during playback
    if (basketballVideo && audioElement && animationState === 'playing') {
      const timeDiff = Math.abs(basketballVideo.currentTime - audioElement.currentTime);
      // If video gets out of sync by more than 0.2 seconds, resync it
      if (timeDiff > 0.2) {
        basketballVideo.currentTime = audioElement.currentTime;
      }
    }
  }

  function handleVideoEnded() {
    console.log('Video ended, starting bounce-out');
    startBounceOut();
  }

  function playCurrent() {
    if (!browser) return;
    if (!scripts[currentIdx]) return;

    try {
      isLoading = true;
      
      const currentAudio = scripts[currentIdx].audio;
      const audioUrl = Array.isArray(currentAudio) ? currentAudio[0] : currentAudio;
      
      const cachedAudio = preloader.getCachedAudio(audioUrl);
      
      if (audio) {
        audio.pause();
        audio.currentTime = 0;
      }

      if (cachedAudio) {
        audio = cachedAudio.cloneNode() as HTMLAudioElement;
      } else {
        audio = new Audio(audioUrl);
      }

      audio.onended = handleAudioEnd;
      audio.onloadedmetadata = () => {
        if (audio) {
          setDuration(audio.duration);
          isLoading = false;
        }
      };
      audio.ontimeupdate = () => updateProgress();
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
      
    } catch (e) {
      console.error('Error in playCurrent:', e);
      isLoading = false;
    }
  }

  function handleAudioEnd() {
    audioStore.update(state => ({ ...state, isPlaying: false }));
    if (currentIdx === scripts.length - 1) {
      onComplete();
    }
  }

  // Start bounce-in animation when slide with video animation loads
  $: if (scripts[currentIdx]?.videoAnimation && animationState === 'hidden') {
    setTimeout(() => {
      startBounceIn();
      // Complete bounce-in after animation duration (2s for optimized timing)
      setTimeout(() => {
        completeBounceIn();
      }, 2000);
    }, 100);
  }

  // Ensure basketball stays visible once it's in playing state
  $: if (animationState === 'playing' && scripts[currentIdx]?.videoAnimation) {
    avatarVisible = true;
  }

  // Play current audio when slide changes
  $: if (browser && scripts.length && typeof currentIdx === 'number') {
    playCurrent();
  }

  onDestroy(() => {
    if (audio) audio.pause();
  });
</script>

{#if showAvatar && avatarVisible}
  <div 
    class="absolute left-8 md:left-12 bottom-12 md:bottom-16 z-30 flex flex-col items-center"
    class:bounce-in-from-left={animationState === 'bouncing-in'}
    class:bounce-out-to-right={animationState === 'bouncing-out'}
  >
    <!-- Basketball Avatar -->
    <div class="relative flex flex-col items-center">
      <div class="relative">
        <!-- Basketball Avatar Container -->
        <div class="relative w-80 h-80 md:w-96 md:h-96">
          <!-- Video Mode with Circular Mask -->
          <div class="w-full h-full rounded-full overflow-hidden basketball-circular-mask">
            {#key videoKey}
              <video
                bind:this={basketballVideo}
                class="w-full h-full object-contain basketball-video"
                muted
                playsinline
                on:loadeddata={handleVideoLoaded}
                on:timeupdate={handleVideoTimeUpdate}
                on:ended={handleVideoEnded}
              >
                {#if currentVideoSrc.endsWith('.webm')}
                  <source src={currentVideoSrc} type="video/webm">
                {:else if currentVideoSrc.endsWith('.mov')}
                  <source src={currentVideoSrc} type="video/quicktime">
                {:else if currentVideoSrc.endsWith('.mp4')}
                  <source src={currentVideoSrc} type="video/mp4">
                {:else}
                  <source src={currentVideoSrc} type="video/webm">
                {/if}
                <!-- Fallback to image if video not supported -->
                <img 
                  src={getR2Url('/images/Ballsack.png')}
                  alt="Basketball Avatar"
                  class="w-full h-full object-contain"
                />
              </video>
            {/key}
          </div>
        </div>
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

<style>
  /* Clean bounce-in animation from left - optimized timing */
  .bounce-in-from-left {
    animation: bounceInFromLeft 2s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
  }
  
  /* Clean bounce-out animation to right - minimal bouncing */
  .bounce-out-to-right {
    animation: bounceOutToRight 1s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
  }
  
  /* Basketball Avatar Styles */
  .basketball-video {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    background: transparent;
    mix-blend-mode: normal;
  }
  
  .basketball-circular-mask {
    border-radius: 50%;
    overflow: hidden;
  }
  
  
  @keyframes bounceInFromLeft {
    /* Initial drop from left - high bounce */
    0% { 
      opacity: 0; 
      transform: translateX(-400px) translateY(-150px) scale(0.5) rotate(-120deg); 
    }
    /* First impact - major deformation */
    15% { 
      opacity: 0.9; 
      transform: translateX(-250px) translateY(0px) scaleX(1.3) scaleY(0.7) rotate(-100deg); 
    }
    /* First bounce peak - 85% of original height */
    30% { 
      opacity: 1; 
      transform: translateX(-120px) translateY(-130px) scale(0.7) rotate(-80deg); 
    }
    /* Second impact - less deformation */
    45% { 
      opacity: 1; 
      transform: translateX(-30px) translateY(0px) scaleX(1.2) scaleY(0.8) rotate(-60deg); 
    }
    /* Second bounce peak - 72% of first bounce */
    60% { 
      opacity: 1; 
      transform: translateX(-5px) translateY(-110px) scale(0.85) rotate(-40deg); 
    }
    /* Third impact - minimal deformation */
    75% { 
      opacity: 1; 
      transform: translateX(5px) translateY(0px) scaleX(1.1) scaleY(0.9) rotate(-20deg); 
    }
    /* Third bounce peak - 61% of second bounce */
    90% { 
      opacity: 1; 
      transform: translateX(8px) translateY(-90px) scale(0.95) rotate(-10deg); 
    }
    /* Final settle - no more bouncing */
    100% { 
      opacity: 1; 
      transform: translateX(10px) translateY(0px) scale(1) rotate(0deg); 
    }
  }
  
  @keyframes bounceOutToRight {
    0% { 
      opacity: 1; 
      transform: translateX(0) translateY(0) scale(1) rotate(0deg); 
    }
    /* Quick first bounce */
    30% { 
      opacity: 1; 
      transform: translateX(120px) translateY(-30px) scaleX(1.2) scaleY(0.8) rotate(45deg); 
    }
    /* Single bounce exit */
    60% { 
      opacity: 1; 
      transform: translateX(300px) translateY(-10px) scale(0.8) rotate(90deg); 
    }
    /* Clean exit */
    100% { 
      opacity: 0; 
      transform: translateX(600px) translateY(0px) scale(0.4) rotate(120deg); 
    }
  }
</style>
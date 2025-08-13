<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fly, scale, slide } from 'svelte/transition';
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
  let avatarVisible = false;
  let isTalking = false;
  let mouthOpen = false;
  let eyeBlink = false;
  let eyebrowRaise = false;
  let bounceHeight = 0;
  let mouthInterval: ReturnType<typeof setInterval> | null = null;

  // Preload all audio files when component mounts
  onMount(async () => {
    if (browser && scripts.length > 0) {
      const audioUrls = scripts.map(script => script.audio);
      await preloader.preloadAudio(audioUrls);
    }
    
    // Show avatar after a short delay
    setTimeout(() => {
      avatarVisible = true;
      startBounceAnimation();
      startFaceAnimations();
    }, 500);
  });

  // Watch audio state for talking animation
  $: isTalking = $audioStore.isPlaying;
  
  // Handle mouth animation
  $: if (isTalking && browser) {
    if (mouthInterval) clearInterval(mouthInterval);
    mouthInterval = setInterval(() => {
      mouthOpen = !mouthOpen;
    }, 150); // Talking animation
  } else {
    if (mouthInterval) {
      clearInterval(mouthInterval);
      mouthInterval = null;
    }
    mouthOpen = false;
  }

  function startBounceAnimation() {
    if (!browser) return;
    
    let time = 0;
    const animate = () => {
      time += 0.016; // 60fps
      
      // Smooth bouncing motion
      const bounce = Math.sin(time * 1.2) * Math.exp(-time * 0.4) * 8;
      bounceHeight = Math.max(0, bounce);
      
      requestAnimationFrame(animate);
    };
    
    animate();
  }

  function startFaceAnimations() {
    if (!browser) return;
    
    // Eye blinking
    setInterval(() => {
      eyeBlink = true;
      setTimeout(() => {
        eyeBlink = false;
      }, 150);
    }, 4000);
    
    // Eyebrow raising when talking
    $: if (isTalking) {
      eyebrowRaise = true;
      setTimeout(() => {
        eyebrowRaise = false;
      }, 200);
    }
  }

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
    if (mouthInterval) clearInterval(mouthInterval);
  });
</script>

{#if showAvatar && avatarVisible}
  <div 
    class="absolute left-8 md:left-12 bottom-12 md:bottom-16 z-30 flex flex-col items-center avatar-slide-in"
  >
    <!-- Enhanced Basketball with Better Face -->
    <div class="relative flex flex-col items-center">
      <div 
        class="relative"
        style="transform: translateY({-bounceHeight}px);"
        transition:scale={{ duration: 300 }}
      >
        <!-- Enhanced Shadow -->
        <div 
          class="absolute bg-black opacity-25 rounded-full blur-md"
          style="
            bottom: {-bounceHeight * 0.5 - 10}px;
            left: 50%;
            transform: translateX(-50%);
            width: 90px;
            height: 20px;
          "
        ></div>
        
        <!-- Enhanced Basketball with Better Face -->
        <div class="relative w-24 h-24 md:w-28 md:h-28">
          <!-- Basketball base with gradient -->
          <div class="absolute inset-0 rounded-full bg-gradient-to-br from-orange-400 via-orange-500 to-orange-600 shadow-xl"></div>
          
          <!-- Basketball lines -->
          <svg class="absolute inset-0 w-full h-full" viewBox="0 0 100 100" fill="none">
            <path d="M50 5v90" stroke="#8B4513" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M5 50h90" stroke="#8B4513" stroke-width="2.5" stroke-linecap="round"/>
            <circle cx="50" cy="50" r="35" stroke="#8B4513" stroke-width="1.5" fill="none"/>
          </svg>
          
          <!-- Enhanced Animated Face -->
          <div class="absolute inset-0 flex items-center justify-center">
            <!-- Eyebrows -->
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 flex gap-7" style="margin-top:-15px;">
              <div class="w-5 h-1.5 bg-black rounded-full transition-transform duration-200" 
                   style="transform: translateY({eyebrowRaise ? '-3px' : '0px'});"></div>
              <div class="w-5 h-1.5 bg-black rounded-full transition-transform duration-200" 
                   style="transform: translateY({eyebrowRaise ? '-3px' : '0px'});"></div>
            </div>
            
            <!-- Enhanced Eyes -->
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 flex gap-5" style="margin-top:-3px;">
              <div class="relative">
                <div class="w-5 h-5 md:w-6 md:h-6 bg-black rounded-full relative">
                  <!-- Eye white -->
                  <div class="absolute inset-1 bg-white rounded-full"></div>
                  <!-- Pupil -->
                  <div class="absolute top-1.5 left-1.5 w-2.5 h-2.5 md:w-3 md:h-3 bg-black rounded-full"></div>
                  <!-- Eye highlight -->
                  <div class="absolute top-1 left-1 w-1.5 h-1.5 bg-white rounded-full"></div>
                  <!-- Eyelid for blinking -->
                  <div 
                    class="absolute inset-0 bg-orange-500 rounded-full transition-transform duration-150"
                    style="transform: scaleY({eyeBlink ? 0.1 : 1});"
                  ></div>
                </div>
              </div>
              
              <div class="relative">
                <div class="w-5 h-5 md:w-6 md:h-6 bg-black rounded-full relative">
                  <!-- Eye white -->
                  <div class="absolute inset-1 bg-white rounded-full"></div>
                  <!-- Pupil -->
                  <div class="absolute top-1.5 left-1.5 w-2.5 h-2.5 md:w-3 md:h-3 bg-black rounded-full"></div>
                  <!-- Eye highlight -->
                  <div class="absolute top-1 left-1 w-1.5 h-1.5 bg-white rounded-full"></div>
                  <!-- Eyelid for blinking -->
                  <div 
                    class="absolute inset-0 bg-orange-500 rounded-full transition-transform duration-150"
                    style="transform: scaleY({eyeBlink ? 0.1 : 1});"
                  ></div>
                </div>
              </div>
            </div>
            
            <!-- Enhanced Animated Mouth -->
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2" style="margin-top:18px;">
              {#if mouthOpen}
                <!-- Open mouth (oval) -->
                <div class="w-6 h-4 md:w-7 md:h-5 bg-black rounded-full mouth-talk animate-pulse"></div>
              {:else}
                <!-- Closed mouth (line) -->
                <div class="w-6 h-1.5 md:w-7 md:h-2 bg-black rounded-full"></div>
              {/if}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Enhanced Speech Bubble -->
      {#if $audioStore.isPlaying}
        <div 
          class="absolute -top-10 md:-top-12 -right-6 md:-right-8 bg-white border-2 border-gray-300 rounded-xl px-4 md:px-5 py-3 md:py-4 shadow-xl speech-pulse"
          in:scale={{ duration: 200 }}
          out:scale={{ duration: 200 }}
        >
          <div class="flex items-center space-x-1.5">
            <div class="w-2.5 h-2.5 md:w-3 md:h-3 bg-blue-500 rounded-full animate-pulse"></div>
            <div class="w-2.5 h-2.5 md:w-3 md:h-3 bg-blue-500 rounded-full animate-pulse" style="animation-delay: 0.2s;"></div>
            <div class="w-2.5 h-2.5 md:w-3 md:h-3 bg-blue-500 rounded-full animate-pulse" style="animation-delay: 0.4s;"></div>
          </div>
          <!-- Speech bubble tail -->
          <div class="absolute -bottom-1.5 left-5 w-3 h-3 bg-white border-r-2 border-b-2 border-gray-300 transform rotate-45"></div>
        </div>
      {/if}
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
  .mouth-talk {
    animation: talk 0.15s ease-in-out infinite alternate;
  }
  
  @keyframes talk {
    0% { transform: scaleY(1); }
    100% { transform: scaleY(1.2); }
  }
  
  .speech-pulse {
    animation: pulse 2s ease-in-out infinite;
  }
  
  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }
  
  .avatar-slide-in {
    animation: slideIn 0.5s ease-out;
  }
  
  @keyframes slideIn {
    from { 
      opacity: 0; 
      transform: translateY(20px) scale(0.8); 
    }
    to { 
      opacity: 1; 
      transform: translateY(0) scale(1); 
    }
  }
</style>

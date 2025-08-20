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
  let headTilt = 0;
  let bounceHeight = 0;
  let mouthInterval: ReturnType<typeof setInterval> | null = null;
  let eyeBlinkInterval: ReturnType<typeof setInterval> | null = null;

  // Reactive declarations for animations
  $: if (isTalking) {
    headTilt = Math.sin(Date.now() * 0.003) * 2;
  } else {
    headTilt = 0;
  }

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
    }, 120); // Fast talking animation
  } else {
    if (mouthInterval) {
      clearInterval(mouthInterval);
      mouthInterval = null;
    }
    mouthOpen = false;
  }

  // Start eye blink interval
  $: if (isTalking) {
    if (eyeBlinkInterval) clearInterval(eyeBlinkInterval);
    eyeBlinkInterval = setInterval(() => {
      eyeBlink = true;
      setTimeout(() => {
        eyeBlink = false;
      }, 150);
    }, 4000);
  } else {
    if (eyeBlinkInterval) {
      clearInterval(eyeBlinkInterval);
      eyeBlinkInterval = null;
    }
  }

  function startBounceAnimation() {
    if (!browser) return;
    
    let time = 0;
    const animate = () => {
      time += 0.016; // 60fps
      
      // Gentle floating motion
      const bounce = Math.sin(time * 0.8) * 3;
      bounceHeight = bounce;
      
      requestAnimationFrame(animate);
    };
    
    animate();
  }

  function startFaceAnimations() {
    if (!browser) return;
    
    // Face animations are now handled by reactive declarations
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
    if (eyeBlinkInterval) clearInterval(eyeBlinkInterval);
  });
</script>

{#if showAvatar && avatarVisible}
  <div 
    class="absolute left-8 md:left-12 bottom-12 md:bottom-16 z-30 flex flex-col items-center avatar-slide-in"
  >
    <!-- Cute Cartoon Character -->
    <div class="relative flex flex-col items-center">
      <div 
        class="relative"
        style="transform: translateY({-bounceHeight}px) rotate({headTilt}deg);"
        transition:scale={{ duration: 300 }}
      >
        <!-- Shadow -->
        <div 
          class="absolute bg-black opacity-20 rounded-full blur-sm"
          style="
            bottom: {-bounceHeight * 0.5 - 15}px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 20px;
          "
        ></div>
        
        <!-- Cute Cartoon Character -->
        <div class="relative w-32 h-32 md:w-36 md:h-36">
          <!-- Head -->
          <div class="absolute inset-0 rounded-full bg-gradient-to-br from-yellow-200 via-yellow-300 to-yellow-400 shadow-xl border-4 border-yellow-500"></div>
          
          <!-- Ears -->
          <div class="absolute -top-2 -left-2 w-8 h-8 bg-yellow-300 rounded-full border-2 border-yellow-500"></div>
          <div class="absolute -top-2 -right-2 w-8 h-8 bg-yellow-300 rounded-full border-2 border-yellow-500"></div>
          
          <!-- Enhanced Animated Face -->
          <div class="absolute inset-0 flex items-center justify-center">
            <!-- Eyebrows -->
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 flex gap-8" style="margin-top:-20px;">
              <div class="w-6 h-2 bg-black rounded-full transition-transform duration-200" 
                   style="transform: translateY({eyebrowRaise ? '-4px' : '0px'});"></div>
              <div class="w-6 h-2 bg-black rounded-full transition-transform duration-200" 
                   style="transform: translateY({eyebrowRaise ? '-4px' : '0px'});"></div>
            </div>
            
            <!-- Eyes -->
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 flex gap-6" style="margin-top:-5px;">
              <div class="relative">
                <div class="w-6 h-6 md:w-7 md:h-7 bg-white rounded-full relative border-2 border-black">
                  <!-- Pupil -->
                  <div class="absolute top-1 left-1 w-4 h-4 md:w-5 md:h-5 bg-black rounded-full"></div>
                  <!-- Eye highlight -->
                  <div class="absolute top-0.5 left-0.5 w-2 h-2 bg-white rounded-full"></div>
                  <!-- Eyelid for blinking -->
                  <div 
                    class="absolute inset-0 bg-yellow-300 rounded-full transition-transform duration-150 border-2 border-black"
                    style="transform: scaleY({eyeBlink ? 0.1 : 1});"
                  ></div>
                </div>
              </div>
              
              <div class="relative">
                <div class="w-6 h-6 md:w-7 md:h-7 bg-white rounded-full relative border-2 border-black">
                  <!-- Pupil -->
                  <div class="absolute top-1 left-1 w-4 h-4 md:w-5 md:h-5 bg-black rounded-full"></div>
                  <!-- Eye highlight -->
                  <div class="absolute top-0.5 left-0.5 w-2 h-2 bg-white rounded-full"></div>
                  <!-- Eyelid for blinking -->
                  <div 
                    class="absolute inset-0 bg-yellow-300 rounded-full transition-transform duration-150 border-2 border-black"
                    style="transform: scaleY({eyeBlink ? 0.1 : 1});"
                  ></div>
                </div>
              </div>
            </div>
            
            <!-- Nose -->
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2" style="margin-top:5px;">
              <div class="w-3 h-2 bg-pink-300 rounded-full border border-pink-400"></div>
            </div>
            
            <!-- Animated Mouth -->
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2" style="margin-top:20px;">
              {#if mouthOpen}
                <!-- Open mouth (oval) -->
                <div class="w-8 h-5 md:w-9 md:h-6 bg-black rounded-full mouth-talk"></div>
              {:else}
                <!-- Closed mouth (line) -->
                <div class="w-8 h-2 md:w-9 md:h-2.5 bg-black rounded-full"></div>
              {/if}
            </div>
            
            <!-- Cheeks -->
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2" style="margin-top:15px; margin-left:-25px;">
              <div class="w-4 h-2 bg-pink-200 rounded-full opacity-60"></div>
            </div>
            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2" style="margin-top:15px; margin-left:25px;">
              <div class="w-4 h-2 bg-pink-200 rounded-full opacity-60"></div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Enhanced Speech Bubble -->
      {#if $audioStore.isPlaying}
        <div 
          class="absolute -top-12 md:-top-14 -right-8 md:-right-10 bg-white border-2 border-gray-300 rounded-xl px-4 md:px-5 py-3 md:py-4 shadow-xl speech-pulse"
          in:scale={{ duration: 200 }}
          out:scale={{ duration: 200 }}
        >
          <div class="flex items-center space-x-1.5">
            <div class="w-3 h-3 md:w-3.5 md:h-3.5 bg-blue-500 rounded-full animate-pulse"></div>
            <div class="w-3 h-3 md:w-3.5 md:h-3.5 bg-blue-500 rounded-full animate-pulse" style="animation-delay: 0.2s;"></div>
            <div class="w-3 h-3 md:w-3.5 md:h-3.5 bg-blue-500 rounded-full animate-pulse" style="animation-delay: 0.4s;"></div>
          </div>
          <!-- Speech bubble tail -->
          <div class="absolute -bottom-2 left-6 w-4 h-4 bg-white border-r-2 border-b-2 border-gray-300 transform rotate-45"></div>
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
    animation: talk 0.12s ease-in-out infinite alternate;
  }
  
  @keyframes talk {
    0% { transform: scaleY(1); }
    100% { transform: scaleY(1.3); }
  }
  
  .speech-pulse {
    animation: pulse 2s ease-in-out infinite;
  }
  
  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }
  
  .avatar-slide-in {
    animation: slideIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
  }
  
  @keyframes slideIn {
    from { 
      opacity: 0; 
      transform: translateY(30px) scale(0.8); 
    }
    to { 
      opacity: 1; 
      transform: translateY(0) scale(1); 
    }
  }
</style>

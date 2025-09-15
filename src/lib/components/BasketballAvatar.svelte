<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fly, scale, slide } from 'svelte/transition';
  import { audioStore, setAudioElement, setDuration, setCurrentIndex, setTotalClips, updateProgress } from '$lib/stores/audioStore';
  import { browser } from '$app/environment';
  import { preloader } from '$lib/utils/preloader';

  export let scripts: { text: string; audio: string | string[]; whiteboardText?: string[] | string[][]; image?: string; titleAudio?: string; imageStyle?: string; additionalImage?: string; }[] = [];
  export let currentIdx: number = 0;
  export let onComplete: () => void = () => {};
  export let showAvatar: boolean = true;

  let isDone = false;
  let audio: HTMLAudioElement | null = null;
  let isLoading = false;
  let avatarVisible = false;
  let isTalking = false;
  let bounceHeight = 0;
  let isExiting = false;
  let hasEntered = false;

  // Reactive declarations for animations

  // Preload all audio files when component mounts
  onMount(async () => {
    if (browser && scripts.length > 0) {
      const audioUrls = scripts.map(script => 
        Array.isArray(script.audio) ? script.audio[0] : script.audio
      );
      await preloader.preloadAudio(audioUrls);
    }
    
    // Show avatar after a short delay
    setTimeout(() => {
      avatarVisible = true;
      startBounceAnimation();
    }, 500);
  });

  // Watch audio state for talking animation and entrance/exit
  $: isTalking = $audioStore.isPlaying;
  
  // Handle entrance animation when audio starts
  $: if (isTalking && !hasEntered) {
    hasEntered = true;
    avatarVisible = true;
    startBounceAnimation();
  }
  
  // Handle exit animation when audio ends
  $: if (!isTalking && hasEntered && !isExiting) {
    isExiting = true;
    setTimeout(() => {
      avatarVisible = false;
    }, 1000); // Give time for exit animation
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


  function playCurrent() {
    if (!browser) return;
    if (!scripts[currentIdx]) {
      return;
    }

    try {
      isLoading = true;
      
      // Handle both string and array audio types
      const currentAudio = scripts[currentIdx].audio;
      const audioUrl = Array.isArray(currentAudio) ? currentAudio[0] : currentAudio;
      
      // Try to get cached audio first
      const cachedAudio = preloader.getCachedAudio(audioUrl);
      
      if (audio) {
        audio.pause();
        audio.currentTime = 0;
      }

      if (cachedAudio) {
        // Use cached audio
        audio = cachedAudio.cloneNode() as HTMLAudioElement;
      } else {
        // Fallback to creating new audio
        audio = new Audio(audioUrl);
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
  
  function resetAvatarState() {
    hasEntered = false;
    isExiting = false;
    avatarVisible = false;
  }

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
    class:bounce-in={hasEntered && !isExiting}
    class:bounce-out={isExiting}
  >
    <!-- Custom Basketball Image -->
    <div class="relative flex flex-col items-center">
      <div 
        class="relative"
        style="transform: translateY({-bounceHeight}px);"
        transition:scale={{ duration: 300 }}
      >
        
        <!-- Basketball with custom video -->
        <div class="relative w-80 h-80 md:w-96 md:h-96">
          <!-- Basketball video background -->
          <video 
            src="/images/basketball_avatar_larger_crop.mp4" 
            class="absolute inset-0 w-full h-full object-cover rounded-full"
            autoplay
            loop
            muted
            playsinline
          ></video>
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
  .bounce-in {
    animation: bounceInFromLeft 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
  }
  
  .bounce-out {
    animation: bounceOutToRight 4s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
  }
  
  @keyframes bounceInFromLeft {
    0% { 
      opacity: 0; 
      transform: translateX(-300px) translateY(0px) scale(0.6); 
    }
    15% { 
      opacity: 0.8; 
      transform: translateX(-200px) translateY(-80px) scale(0.7); 
    }
    30% { 
      opacity: 0.9; 
      transform: translateX(-100px) translateY(0px) scale(0.8); 
    }
    45% { 
      opacity: 1; 
      transform: translateX(-50px) translateY(-60px) scale(0.9); 
    }
    60% { 
      opacity: 1; 
      transform: translateX(-20px) translateY(0px) scale(0.95); 
    }
    75% { 
      opacity: 1; 
      transform: translateX(-5px) translateY(-30px) scale(1.0); 
    }
    90% { 
      opacity: 1; 
      transform: translateX(0px) translateY(0px) scale(1.0); 
    }
    100% { 
      opacity: 1; 
      transform: translateX(0) translateY(0) scale(1); 
    }
  }
  
  @keyframes bounceOutToRight {
    0% { 
      opacity: 1; 
      transform: translateX(0) translateY(0) scale(1) rotate(0deg); 
    }
    4% { 
      opacity: 1; 
      transform: translateX(80px) translateY(-40px) scale(1.15) rotate(12deg); 
    }
    8% { 
      opacity: 1; 
      transform: translateX(160px) translateY(0px) scale(0.9) rotate(24deg); 
    }
    12% { 
      opacity: 1; 
      transform: translateX(250px) translateY(-35px) scale(1.1) rotate(36deg); 
    }
    16% { 
      opacity: 1; 
      transform: translateX(340px) translateY(5px) scale(0.85) rotate(48deg); 
    }
    20% { 
      opacity: 1; 
      transform: translateX(430px) translateY(-30px) scale(1.05) rotate(60deg); 
    }
    24% { 
      opacity: 1; 
      transform: translateX(520px) translateY(8px) scale(0.8) rotate(72deg); 
    }
    28% { 
      opacity: 1; 
      transform: translateX(610px) translateY(-25px) scale(0.95) rotate(84deg); 
    }
    32% { 
      opacity: 1; 
      transform: translateX(700px) translateY(10px) scale(0.75) rotate(96deg); 
    }
    36% { 
      opacity: 1; 
      transform: translateX(790px) translateY(-20px) scale(0.9) rotate(108deg); 
    }
    40% { 
      opacity: 1; 
      transform: translateX(880px) translateY(12px) scale(0.7) rotate(120deg); 
    }
    44% { 
      opacity: 1; 
      transform: translateX(970px) translateY(-15px) scale(0.85) rotate(132deg); 
    }
    48% { 
      opacity: 1; 
      transform: translateX(1060px) translateY(8px) scale(0.65) rotate(144deg); 
    }
    52% { 
      opacity: 1; 
      transform: translateX(1150px) translateY(-10px) scale(0.8) rotate(156deg); 
    }
    56% { 
      opacity: 1; 
      transform: translateX(1240px) translateY(5px) scale(0.6) rotate(168deg); 
    }
    60% { 
      opacity: 1; 
      transform: translateX(1330px) translateY(-8px) scale(0.75) rotate(180deg); 
    }
    64% { 
      opacity: 1; 
      transform: translateX(1420px) translateY(3px) scale(0.55) rotate(192deg); 
    }
    68% { 
      opacity: 1; 
      transform: translateX(1510px) translateY(-5px) scale(0.7) rotate(204deg); 
    }
    72% { 
      opacity: 1; 
      transform: translateX(1600px) translateY(2px) scale(0.5) rotate(216deg); 
    }
    76% { 
      opacity: 0.9; 
      transform: translateX(1690px) translateY(-3px) scale(0.6) rotate(228deg); 
    }
    80% { 
      opacity: 0.8; 
      transform: translateX(1780px) translateY(1px) scale(0.45) rotate(240deg); 
    }
    84% { 
      opacity: 0.6; 
      transform: translateX(1870px) translateY(-2px) scale(0.5) rotate(252deg); 
    }
    88% { 
      opacity: 0.4; 
      transform: translateX(1960px) translateY(0px) scale(0.35) rotate(264deg); 
    }
    92% { 
      opacity: 0.2; 
      transform: translateX(2050px) translateY(0px) scale(0.3) rotate(276deg); 
    }
    96% { 
      opacity: 0.1; 
      transform: translateX(2140px) translateY(0px) scale(0.25) rotate(288deg); 
    }
    100% { 
      opacity: 0; 
      transform: translateX(2230px) translateY(0px) scale(0.2) rotate(300deg); 
    }
  }
</style>
<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fly, scale, slide } from 'svelte/transition';
  import { audioStore, setAudioElement, setDuration, setCurrentIndex, setTotalClips, updateProgress, audioElement } from '$lib/stores/audioStore';
  import { browser } from '$app/environment';
  import { getR2Url } from '$lib/config/r2';
  import { preloader } from '$lib/utils/preloader';

  export let scripts: { text: string; audio: string | string[]; whiteboardText?: string[] | string[][]; image?: string; titleAudio?: string; imageStyle?: string; additionalImage?: string; videoAnimation?: string; }[] = [];
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
  
  // Avatar configuration - easy to switch between image and video
  let avatarMode = 'video'; // 'image' or 'video' - default to video for basketball animation
  let basketballVideo: HTMLVideoElement | null = null;
  let videoLoaded = false;
  let videoPlaying = false;
  let videoCurrentTime = 0;
  let videoDuration = 0;
  let currentVideoSrc = getR2Url('/images/module2_sellingtitle_01_animation_no_background.webm'); // Default basketball animation with no background
  
  // Animation states
  let currentState = 'idle'; // 'idle', 'talking', 'excited', 'sleepy'
  let lastAudioTime = 0;
  let speechIntensity = 0;

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
  
  // Sync video playback with audio controls for ALL slides with basketball videos
  $: if (scripts[currentIdx]?.videoAnimation && basketballVideo && bounceInComplete) {
    if ($audioStore.isPlaying) {
      // Audio is playing, ensure video is playing
      if (basketballVideo.paused) {
        basketballVideo.play().catch(e => console.log('Video play error:', e));
      }
    } else {
      // Audio is paused, pause the video
      if (!basketballVideo.paused) {
        basketballVideo.pause();
      }
    }
  }
  
  // Detect replay: when audio currentTime becomes 0 and progress is also 0
  $: if (scripts[currentIdx]?.videoAnimation && basketballVideo && bounceInComplete && $audioStore.currentTime === 0 && $audioStore.progress === 0 && $audioStore.isPlaying) {
    // Reset video to beginning and play
    basketballVideo.currentTime = 0;
    basketballVideo.play().catch(e => console.log('Video replay error:', e));
  }
  
  // Determine avatar mode and video source based on current script
  $: {
    const currentScript = scripts[currentIdx];
    console.log('Current script:', currentScript);
    console.log('currentIdx:', currentIdx);
    console.log('videoAnimation property:', currentScript?.videoAnimation);
    
    if (currentScript?.videoAnimation) {
      // Use specific video animation for this slide
      avatarMode = 'video';
      currentVideoSrc = currentScript.videoAnimation;
      console.log('✅ Setting video source to:', currentVideoSrc);
    } else {
      // Default to basketball video animation for all slides
      avatarMode = 'video';
      currentVideoSrc = getR2Url('/images/module2_sellingtitle_01_animation_no_background.webm');
      console.log('⚠️ No videoAnimation found, using default video source:', currentVideoSrc);
    }
  }
  
  // Reload video when source changes
  $: if (basketballVideo && currentVideoSrc) {
    basketballVideo.load();
    console.log('Reloading basketball video:', currentVideoSrc);
  }
  
  // Create a unique key for video element to force re-render when source changes
  $: videoKey = currentVideoSrc;
  
  // Handle entrance animation when audio starts
  $: if (isTalking && !hasEntered) {
    hasEntered = true;
    avatarVisible = true;
    
    // For selling title slide, start bounce animation immediately
    // For other slides, start bounce animation normally
    startBounceAnimation();
  }

  // Special timing for selling title slide and unit prioritization slide
  $: isSellingTitleSlide = scripts[currentIdx]?.videoAnimation?.includes('ballSackv2_yellow_unit_latest.mov') || 
                           scripts[currentIdx]?.videoAnimation?.includes('ballsackm2s3_unit_prioritization.mov') ||
                           scripts[currentIdx]?.videoAnimation?.includes('ballsackm2s2_yellow_unit.mov') ||
                           scripts[currentIdx]?.videoAnimation?.includes('ballsackm2s4_green_purple_units.mov') ||
                           scripts[currentIdx]?.videoAnimation?.includes('ballsackm2_intro.mov') ||
                           scripts[currentIdx]?.videoAnimation?.includes('ballsackm2_intro.webm') ||
                           scripts[currentIdx]?.videoAnimation?.includes('ballSackIntroS1.mov') ||
                           scripts[currentIdx]?.videoAnimation?.includes('ballSackIntroS12.mov');
  let bounceInComplete = false;
  let videoPlayed = false;
  let bounceOutStarted = false;
  let bounceOutStartTime = 0;
  let audioStarted = false;
  
  // Handle exit animation when audio ends (but not for selling title slide)
  $: if (!isTalking && hasEntered && !isExiting && !isSellingTitleSlide) {
    isExiting = true;
    setTimeout(() => {
      avatarVisible = false;
    }, 1000); // Give time for exit animation
  }

  function startBounceAnimation() {
    if (!browser) return;
    
    console.log('Starting bounce animation, isSellingTitleSlide:', isSellingTitleSlide);
    
    // Reset state for new animation
    bounceInComplete = false;
    videoPlayed = false;
    bounceOutStarted = false;
    audioStarted = false;
    
    // For selling title slide, start off-screen and pause audio initially
    if (isSellingTitleSlide) {
      console.log('Selling title slide - starting off-screen, pausing audio');
      bounceHeight = -50; // Start off-screen above
      if (audioElement) {
        audioElement.pause();
        audioStore.update(state => ({ ...state, isPlaying: false }));
      }
    } else {
      console.log('Normal slide - starting in position');
      bounceHeight = 0; // Start in position for other slides
    }
    
    let time = 0;
    const animate = () => {
      time += 0.016; // 60fps
      
      if (isSellingTitleSlide) {
        // Special timing for selling title slide
        if (time < 1.5) {
          // Bounce in animation - start off screen and bounce into position
          if (time < 0.1) console.log('Phase 1: Bounce in animation starting');
          const progress = time / 1.5;
          const bounce = Math.sin(time * 3) * 20 * (1 - progress);
          const drop = -50 * (1 - progress);
          bounceHeight = bounce + drop;
        } else if (time < 1.5 + 0.5) {
          // Settle into position
          if (time < 1.6) console.log('Phase 2: Settling into position');
          bounceHeight = 0;
          
          // Mark bounce in as complete and start audio/video together
          if (!bounceInComplete) {
            bounceInComplete = true;
            // Pause video initially
            if (basketballVideo) {
              basketballVideo.pause();
            }
            
            // Start both audio and video together after bounce in is complete
            setTimeout(() => {
              if (isSellingTitleSlide && !audioStarted && !videoPlayed) {
                // Start audio
                if (audioElement) {
                  audioElement.play().catch((e: any) => console.log('Audio play error:', e));
                  audioStore.update(state => ({ ...state, isPlaying: true }));
                  audioStarted = true;
                }
                
                // Start video
                if (basketballVideo) {
                  basketballVideo.play().catch(e => console.log('Video play error:', e));
                  videoPlayed = true;

                  // Video will end naturally and trigger bounce out via handleVideoEnded
                  // Audio will also end naturally, but we don't need to wait for both
                  console.log('Video and audio started, will bounce out when video ends');
                }
              }
            }, 500); // Small delay after bounce in completes
          }
        } else if (bounceOutStarted) {
          // Bounce out animation - handled by CSS animation, just keep ball in position
          if (bounceOutStartTime < 0.1) console.log('Phase 4: Bounce out animation starting (CSS)');
          bounceHeight = 0; // Keep ball in position during CSS bounce out
        } else {
          // Waiting period - keep ball in position (bounceHeight = 0)
          bounceHeight = 0;
        }
      } else {
        // Normal gentle floating motion for other slides
        const bounce = Math.sin(time * 0.8) * 3;
        bounceHeight = bounce;
      }
      
      // Update avatar state based on audio
      updateAvatarState();
      
      requestAnimationFrame(animate);
    };
    
    animate();
  }

  function startBounceOut() {
    if (bounceOutStarted) return;
    bounceOutStarted = true;
    bounceOutStartTime = 0; // Reset bounce out timer
    
    // The bounce out animation is now handled in the main animate loop
    // No need for separate animation function
  }

  function updateAvatarState() {
    const currentAudioTime = $audioStore.currentTime;
    const isCurrentlyPlaying = $audioStore.isPlaying;
    
    // Calculate speech intensity
    const audioTimeDelta = Math.abs(currentAudioTime - lastAudioTime);
    if (audioTimeDelta > 0.05) {
      speechIntensity = Math.min(speechIntensity + 0.3, 1.0);
    } else {
      speechIntensity = Math.max(speechIntensity - 0.05, 0);
    }
    lastAudioTime = currentAudioTime;
    
    // Determine avatar state based on audio
    let newState = 'idle';
    if (isCurrentlyPlaying && speechIntensity > 0.7) {
      newState = 'excited';
    } else if (isCurrentlyPlaying && speechIntensity > 0.3) {
      newState = 'talking';
    } else if (isCurrentlyPlaying && speechIntensity < 0.2) {
      newState = 'sleepy';
    }
    
    // Update state if changed
    if (newState !== currentState) {
      currentState = newState;
      updateAvatarPlayback();
    }
  }

  function updateAvatarPlayback() {
    if (avatarMode === 'video' && basketballVideo) {
      // Skip special handling for selling title slide - it's handled in bounce animation
      if (isSellingTitleSlide) {
        return;
      }
      
      // Video mode - control video playback for other slides
      if (isTalking) {
        if (basketballVideo.paused) {
          basketballVideo.play().catch(e => console.log('Video play error:', e));
        }
      } else {
        // When not talking, loop the idle animation
        basketballVideo.currentTime = 0;
        basketballVideo.play().catch(e => console.log('Video play error:', e));
      }
    }
    // Image mode - no special handling needed, just state tracking
  }

  function handleVideoLoaded() {
    videoLoaded = true;
    videoDuration = basketballVideo?.duration || 0;
    console.log('Basketball video loaded, duration:', videoDuration);
  }

  function handleVideoTimeUpdate() {
    if (basketballVideo) {
      videoCurrentTime = basketballVideo.currentTime;
    }
  }

  function handleVideoEnded() {
    console.log('Video ended, checking if should start bounce out');
    if (isSellingTitleSlide && !bounceOutStarted) {
      console.log('Selling title slide video ended, starting bounce out');
      // Use the existing bounce out animation instead of custom bounce
      isExiting = true;
      bounceOutStarted = true;
      
      // Hide avatar after CSS bounce out animation completes (4 seconds)
      setTimeout(() => {
        console.log('CSS bounce out animation complete, hiding avatar');
        avatarVisible = false;
      }, 4000);
    }
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

  // Reset avatar visibility when navigating to a slide with videoAnimation
  $: if (scripts[currentIdx]?.videoAnimation && !avatarVisible) {
    avatarVisible = true;
    hasEntered = false;
    isExiting = false;
    setTimeout(() => {
      startBounceAnimation();
    }, 100);
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
    <!-- Basketball Avatar -->
    <div class="relative flex flex-col items-center">
      <div 
        class="relative"
        style="transform: translateY({-bounceHeight}px);"
        transition:scale={{ duration: 300 }}
      >
        <!-- Basketball Avatar Container -->
        <div class="relative w-80 h-80 md:w-96 md:h-96">
          <!-- Video Mode (Default) with Circular Mask -->
          <div class="w-full h-full rounded-full overflow-hidden basketball-circular-mask">
            {#key videoKey}
              <video
                bind:this={basketballVideo}
                class="w-full h-full object-contain basketball-video"
                data-state={currentState}
                muted
                playsinline
                on:loadeddata={handleVideoLoaded}
                on:timeupdate={handleVideoTimeUpdate}
                on:ended={handleVideoEnded}
              >
                {#if currentVideoSrc.endsWith('.mov')}
                  <source src={currentVideoSrc} type="video/quicktime">
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
  .bounce-in {
    animation: bounceInFromLeft 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
  }
  
  .bounce-out {
    animation: bounceOutToRight 4s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
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
  
  /* State-based animations for video */
  .basketball-video[data-state="excited"] {
    animation: excitedPulse 2s ease-in-out infinite;
  }
  
  .basketball-video[data-state="talking"] {
    animation: talkingNod 3s ease-in-out infinite;
  }
  
  .basketball-video[data-state="sleepy"] {
    animation: sleepySway 4s ease-in-out infinite;
  }
  
  @keyframes excitedPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }
  
  @keyframes talkingNod {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-2px); }
  }
  
  @keyframes sleepySway {
    0%, 100% { transform: rotate(0deg); }
    25% { transform: rotate(1deg); }
    75% { transform: rotate(-1deg); }
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
<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { fly, scale, slide } from 'svelte/transition';
  import { audioStore, setAudioElement, setDuration, setCurrentIndex, setTotalClips, updateProgress } from '$lib/stores/audioStore';
  import { browser } from '$app/environment';
  import { preloader } from '$lib/utils/preloader';
  import { avatarOptions, type AvatarOption, animationPresets } from '$lib/config/avatarOptions';
  import * as THREE from 'three';

  export let scripts: { text: string; audio: string }[] = [];
  export let currentIdx: number = 0;
  export let onComplete: () => void = () => {};
  export let showAvatar: boolean = true;
  export let selectedAvatar: AvatarOption = avatarOptions[0];

  let isDone = false;
  let audio: HTMLAudioElement | null = null;
  let isLoading = false;
  let avatarVisible = false;
  let isTalking = false;
  let container: HTMLDivElement;
  let rendererInitialized = false;
  
  // Three.js variables
  let scene: THREE.Scene;
  let camera: THREE.PerspectiveCamera;
  let renderer: THREE.WebGLRenderer;
  let avatar: any;
  let mixer: THREE.AnimationMixer;
  let clock = new THREE.Clock();

  // Animation state
  let mouthOpen = false;
  let eyebrowRaise = false;
  let eyeBlink = false;
  let headNod = false;

  // Preload all audio files when component mounts
  onMount(async () => {
    if (browser && scripts.length > 0) {
      const audioUrls = scripts.map(script => script.audio);
      await preloader.preloadAudio(audioUrls);
    }
    
    // Show avatar after a short delay
    setTimeout(() => {
      avatarVisible = true;
      initThreeJS();
    }, 500);
  });

  // Watch audio state for talking animation
  $: isTalking = $audioStore.isPlaying;
  
  // Handle talking animation
  $: if (isTalking && avatar) {
    startTalkingAnimation();
  } else if (avatar) {
    stopTalkingAnimation();
  }

  async function initThreeJS() {
    if (!browser || !container) return;

    try {
      // Scene setup
      scene = new THREE.Scene();
      scene.background = new THREE.Color(0x00000000); // Transparent

      // Camera setup
      camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
      );
      camera.position.set(0, 0, 2);

      // Renderer setup
      renderer = new THREE.WebGLRenderer({ 
        alpha: true, 
        antialias: true 
      });
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setPixelRatio(window.devicePixelRatio);
      container.appendChild(renderer.domElement);

      // Lighting
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
      scene.add(ambientLight);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
      directionalLight.position.set(0, 10, 5);
      scene.add(directionalLight);

      rendererInitialized = true;

      // Create a simple avatar immediately
      createSimpleAvatar();
      
      // Start animation loop
      animate();
    } catch (error) {
      console.error('Error initializing Three.js:', error);
      // Fallback to CSS-based avatar
      createCSSAvatar();
    }
  }

  function createSimpleAvatar() {
    if (!scene) return;

    // Create a simple colored sphere as avatar
    const geometry = new THREE.SphereGeometry(0.8, 32, 32);
    const material = new THREE.MeshLambertMaterial({ 
      color: 0xff8c00, // Orange basketball color
      transparent: true,
      opacity: 0.9
    });
    
    avatar = new THREE.Mesh(geometry, material);
    avatar.position.set(0, 0, 0);
    scene.add(avatar);

    // Add basketball texture lines
    const lineGeometry = new THREE.SphereGeometry(0.81, 32, 32);
    const lineMaterial = new THREE.MeshBasicMaterial({
      color: 0x8B4513, // Brown lines
      wireframe: true,
      transparent: true,
      opacity: 0.3
    });
    
    const lines = new THREE.Mesh(lineGeometry, lineMaterial);
    scene.add(lines);

    startIdleAnimations();
  }

  function createCSSAvatar() {
    // Fallback to CSS-based avatar if Three.js fails
    console.log('Using CSS fallback avatar');
  }

  async function loadAvatar() {
    if (!browser || !rendererInitialized) return;

    try {
      switch (selectedAvatar.type) {
        case 'ready-player-me':
          await loadReadyPlayerMeAvatar();
          break;
        case 'live2d':
          await loadLive2DAvatar();
          break;
        case 'custom':
          createCustomAvatar();
          break;
        default:
          createCustomAvatar();
      }
    } catch (error) {
      console.error('Error loading avatar:', error);
      createCustomAvatar();
    }
  }

  async function loadReadyPlayerMeAvatar() {
    if (!scene) return;
    
    try {
      const { GLTFLoader } = await import('three/examples/jsm/loaders/GLTFLoader.js');
      const loader = new GLTFLoader();
      
      // Use a working demo URL or create a simple avatar
      const avatarUrl = 'https://threejs.org/examples/models/gltf/RobotExpressive/RobotExpressive.glb';
      
      loader.load(avatarUrl, (gltf: any) => {
        avatar = gltf.scene;
        avatar.scale.set(0.5, 0.5, 0.5);
        avatar.position.set(0, 0, 0);
        scene.add(avatar);

        // Setup animation mixer
        mixer = new THREE.AnimationMixer(avatar);
        
        // Add idle animation
        if (gltf.animations.length > 0) {
          const idleAction = mixer.clipAction(gltf.animations[0]);
          idleAction.play();
        }

        // Start idle animations
        startIdleAnimations();
      }, undefined, (error) => {
        console.error('Error loading 3D avatar:', error);
        createSimpleAvatar();
      });
    } catch (error) {
      console.error('Error loading Ready Player Me avatar:', error);
      createSimpleAvatar();
    }
  }

  async function loadLive2DAvatar() {
    // For Live2D, we'd need to implement Live2D Cubism SDK
    // This is a placeholder for now
    console.log('Live2D avatar loading not implemented yet');
    createSimpleAvatar();
  }

  function createCustomAvatar() {
    createSimpleAvatar();
  }

  function startIdleAnimations() {
    if (!browser) return;
    
    // Eye blinking
    setInterval(() => {
      eyeBlink = true;
      setTimeout(() => {
        eyeBlink = false;
      }, 150);
    }, 4000);
    
    // Subtle breathing animation
    setInterval(() => {
      if (avatar && !isTalking) {
        const scale = 1 + Math.sin(Date.now() * 0.001) * 0.02;
        avatar.scale.set(scale, scale, scale);
      }
    }, 16);
  }

  function startTalkingAnimation() {
    if (!avatar) return;
    
    // Enhanced talking animation
    const talkInterval = setInterval(() => {
      mouthOpen = !mouthOpen;
      eyebrowRaise = !eyebrowRaise;
      
      // Head nod
      if (Math.random() > 0.7) {
        headNod = true;
        setTimeout(() => {
          headNod = false;
        }, 200);
      }
    }, 200);

    // Scale animation
    avatar.scale.set(1.05, 1.05, 1.05);
    
    return () => clearInterval(talkInterval);
  }

  function stopTalkingAnimation() {
    if (!avatar) return;
    
    mouthOpen = false;
    eyebrowRaise = false;
    headNod = false;
    avatar.scale.set(1, 1, 1);
  }

  function animate() {
    if (!browser) return;
    
    requestAnimationFrame(animate);
    
    if (mixer) {
      mixer.update(clock.getDelta());
    }
    
    if (renderer && scene && camera) {
      renderer.render(scene, camera);
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
    if (renderer) {
      renderer.dispose();
    }
  });
</script>

{#if showAvatar && avatarVisible}
  <div 
    class="absolute left-8 md:left-12 bottom-12 md:bottom-16 z-30 flex flex-col items-center avatar-slide-in"
  >
    <!-- 3D Avatar Container -->
    <div 
      bind:this={container}
      class="relative w-32 h-32 md:w-40 md:h-40"
      style="transform: translateY({isTalking ? -5 : 0}px) rotateY({headNod ? 5 : 0}deg);"
      transition:scale={{ duration: 300 }}
    >
      <!-- Three.js canvas will be inserted here -->
    </div>
    
    <!-- Speech Bubble -->
    {#if $audioStore.isPlaying}
      <div 
        class="absolute -top-8 md:-top-10 -right-4 md:-right-6 bg-white border-2 border-gray-300 rounded-lg px-3 md:px-4 py-2 md:py-3 shadow-lg speech-pulse"
        in:scale={{ duration: 200 }}
        out:scale={{ duration: 200 }}
      >
        <div class="flex items-center space-x-1">
          <div class="w-2 h-2 md:w-2.5 md:h-2.5 bg-blue-500 rounded-full animate-pulse"></div>
          <div class="w-2 h-2 md:w-2.5 md:h-2.5 bg-blue-500 rounded-full animate-pulse" style="animation-delay: 0.2s;"></div>
          <div class="w-2 h-2 md:w-2.5 md:h-2.5 bg-blue-500 rounded-full animate-pulse" style="animation-delay: 0.4s;"></div>
        </div>
        <!-- Speech bubble tail -->
        <div class="absolute -bottom-1 left-4 w-2 h-2 bg-white border-r-2 border-b-2 border-gray-300 transform rotate-45"></div>
      </div>
    {/if}
  </div>
{/if}

<!-- Loading indicator -->
{#if isLoading}
  <div class="absolute top-4 right-4 bg-blue-500 text-white px-3 py-1 rounded-full text-sm animate-pulse">
    Loading...
  </div>
{/if}

<script lang="ts">
  import { onMount, onDestroy, afterUpdate } from 'svelte';
  import { audioStore } from '$lib/stores/audioStore';

  export let textLines: string[] = [];
  export let drawSpeed: number = 0.05; // Speed of text drawing (seconds per character)
  export let animateIndex: number = -1; // Index of the line to animate (default: last line)

  let canvas: HTMLCanvasElement;
  let ctx: CanvasRenderingContext2D;
  let animationFrame: number;
  let currentLineIndex = 0;
  let currentCharIndex = 0;
  let animationStartTime = 0;
  let isAnimating = false;

  // Whiteboard styling
  const backgroundColor = '#ffffff';
  const textColor = '#2c3e50';
  const fontSize = 24;
  const lineHeight = 60; // Increased from 35 to 60 for more space
  const padding = 40;
  const fontFamily = 'Comic Sans MS, cursive, sans-serif';

  function initCanvas() {
    if (!canvas) return;
    
    // Get the parent video container size instead of canvas container
    const videoContainer = canvas.closest('.aspect-video');
    const playerArea = canvas.closest('.bg-black');
    
    if (videoContainer) {
      const rect = videoContainer.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = rect.height;
    } else if (playerArea) {
      const rect = playerArea.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = rect.height;
    } else {
      // Fallback to canvas container
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width;
      canvas.height = rect.height;
    }
    
    ctx = canvas.getContext('2d')!;
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Add subtle grid pattern for whiteboard effect
    ctx.strokeStyle = '#f0f0f0';
    ctx.lineWidth = 1;
    for (let i = 0; i < canvas.width; i += 20) {
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i, canvas.height);
      ctx.stroke();
    }
    for (let i = 0; i < canvas.height; i += 20) {
      ctx.beginPath();
      ctx.moveTo(0, i);
      ctx.lineTo(canvas.width, i);
      ctx.stroke();
    }
    
    ctx.font = `${fontSize}px ${fontFamily}`;
    ctx.fillStyle = textColor;
    ctx.textBaseline = 'top';
    ctx.lineWidth = 3;
  }

  function animate(currentTime: number) {
    if (!ctx || !isAnimating) return;

    // Clear canvas and redraw grid
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Redraw grid pattern
    ctx.strokeStyle = '#f0f0f0';
    ctx.lineWidth = 1;
    for (let i = 0; i < canvas.width; i += 20) {
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i, canvas.height);
      ctx.stroke();
    }
    for (let i = 0; i < canvas.height; i += 20) {
      ctx.beginPath();
      ctx.moveTo(0, i);
      ctx.lineTo(canvas.width, i);
      ctx.stroke();
    }
    
    ctx.fillStyle = textColor;

    // Determine which line to animate
    const animIdx = animateIndex === -1 ? textLines.length - 1 : animateIndex;

    // Instantly draw all lines before the one being animated
    for (let i = 0; i < animIdx; i++) {
      const y = padding + (i * lineHeight);
      if(textLines[i]) ctx.fillText(textLines[i], padding, y);
    }

    // Animate just the target line
    if (animIdx >= 0 && animIdx < textLines.length) {
      const y = padding + (animIdx * lineHeight);
      const elapsedTime = (currentTime - animationStartTime) / 1000;
      const line = textLines[animIdx];
      if (line) {
        let charCount = Math.floor(elapsedTime / drawSpeed);
        if (charCount > line.length) charCount = line.length;
        
        ctx.fillText(line.substring(0, charCount), padding, y);
        
        if (charCount < line.length) {
          animationFrame = requestAnimationFrame(animate);
        } else {
          isAnimating = false;
        }
      } else {
        isAnimating = false;
      }
    } else {
      isAnimating = false;
    }
  }

  function startAnimation() {
    if (isAnimating) return;
    
    isAnimating = true;
    animationStartTime = performance.now();
    animationFrame = requestAnimationFrame(animate);
  }

  function stopAnimation() {
    isAnimating = false;
    if (animationFrame) {
      cancelAnimationFrame(animationFrame);
    }
  }

  function resetAnimation() {
    stopAnimation();
    currentLineIndex = 0;
    currentCharIndex = 0;
    initCanvas();
  }

  let prevTextLines: string[] = [];
  let animationStarted = false;

  // When the slide changes (textLines is updated), reset the animation state
  $: if (JSON.stringify(textLines) !== JSON.stringify(prevTextLines)) {
    prevTextLines = [...textLines];
    animationStarted = false;
    resetAnimation();
  }

  // Start animation as soon as audio starts, but only once per slide
  $: if ($audioStore.isPlaying && !animationStarted && textLines && textLines.length > 0) {
    animationStarted = true;
    startAnimation();
  }

  onMount(() => {
    // Delay to ensure container is properly sized
    setTimeout(() => {
      initCanvas();
    }, 300);
    
    // Handle window resize
    const handleResize = () => {
      initCanvas();
    };
    
    window.addEventListener('resize', handleResize);
    
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  });

  onDestroy(() => {
    stopAnimation();
  });
</script>

<div class="whiteboard-container">
  <canvas
    bind:this={canvas}
    class="whiteboard-canvas w-full h-full"
  ></canvas>
</div>

<style>
  .whiteboard-container {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    /* border removed for production */
  }

  .whiteboard-canvas {
    border: 3px solid #2c3e50;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    background-color: #ffffff;
    width: 100%;
    height: 100%;
  }
</style> 
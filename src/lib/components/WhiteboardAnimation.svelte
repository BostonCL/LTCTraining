<script lang="ts">
  import { onMount, onDestroy, afterUpdate } from 'svelte';
  import { audioStore } from '$lib/stores/audioStore';

  export let textLines: string[] = [];
  export let drawSpeed: number = 0.05; // Speed of text drawing (seconds per character)

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
  const fontSize = 32; // Increased from 24 to 32
  const lineHeight = 60; // Keep as is for now
  const padding = 40;
  const fontFamily = 'Comic Sans MS, cursive, sans-serif';

  // Helper: Word wrap a single string into multiple lines
  function wrapText(ctx: CanvasRenderingContext2D, text: string, maxWidth: number): string[] {
    const words = text.split(' ');
    let lines: string[] = [];
    let currentLine = '';
    for (let i = 0; i < words.length; i++) {
      const testLine = currentLine ? currentLine + ' ' + words[i] : words[i];
      const metrics = ctx.measureText(testLine);
      if (metrics.width > maxWidth && currentLine) {
        lines.push(currentLine);
        currentLine = words[i];
      } else {
        currentLine = testLine;
      }
    }
    if (currentLine) lines.push(currentLine);
    return lines;
  }

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
    ctx.font = `${fontSize}px ${fontFamily}`;
    ctx.textBaseline = 'top';

    // Draw all lines except the last instantly
    let y = padding;
    for (let i = 0; i < textLines.length - 1; i++) {
      if (textLines[i]) {
        const wrapped = wrapText(ctx, textLines[i], canvas.width - 2 * padding);
        for (let w = 0; w < wrapped.length; w++) {
          const line = wrapped[w];
          const x = i === 0 && w === 0 ? (canvas.width - ctx.measureText(line).width) / 2 : padding;
          ctx.fillText(line, x, y);
          y += lineHeight;
        }
      }
    }

    // Animate only the last line
    if (textLines.length > 0) {
      const lastIdx = textLines.length - 1;
      const lineToAnimate = textLines[lastIdx];
      const wrapped = wrapText(ctx, lineToAnimate, canvas.width - 2 * padding);
      const elapsedTime = (currentTime - animationStartTime) / 1000;
      const totalCharsInLine = wrapped.join('').length;
      let charCount = Math.floor(elapsedTime / drawSpeed);
      if (charCount > totalCharsInLine) charCount = totalCharsInLine;
      let charsDrawnInLine = 0;
      for (let w = 0; w < wrapped.length; w++) {
        const lineText = wrapped[w];
        const charsToDrawNow = charCount - charsDrawnInLine;
        if (charsToDrawNow > 0) {
          const sub = lineText.substring(0, charsToDrawNow);
          const x = lastIdx === 0 && w === 0 ? (canvas.width - ctx.measureText(lineText).width) / 2 : padding;
          ctx.fillText(sub, x, y);
        }
        y += lineHeight;
        charsDrawnInLine += lineText.length;
      }
      if (charCount >= totalCharsInLine) {
        isAnimating = false;
      } else {
        animationFrame = requestAnimationFrame(animate);
      }
    }
  }

  function startAnimation() {
    if (isAnimating) return;
    isAnimating = true;
    if (currentLineIndex === 0) {
       animationStartTime = performance.now();
    }
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
    resetAnimation();
    animationStarted = false;
    initCanvas(); // Ensure canvas is ready
    function tryStart() {
      if (ctx) {
        startAnimation();
        animationStarted = true;
      } else {
        setTimeout(tryStart, 50);
      }
    }
    tryStart();
  }

  // Start animation as soon as audio starts, but only once per slide
  $: if ($audioStore.isPlaying && !animationStarted && textLines && textLines.length > 0) {
    animationStarted = true;
    startAnimation();
  }

  onMount(() => {
    initCanvas();
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
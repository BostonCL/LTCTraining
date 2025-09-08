<script lang="ts">
  import { onMount, onDestroy, afterUpdate, createEventDispatcher } from 'svelte';
  import { audioStore, audioElement } from '$lib/stores/audioStore';

  const dispatch = createEventDispatcher();

  export let textLines: string[] | string[][] = [];
  export let drawSpeed: number = 0.05; // Speed of text drawing (seconds per character)
  export let audioText: string = ''; // The text that corresponds to the audio being played
  export let titleAudio: string = ''; // Audio file for the title
  export let startWithAudio: boolean = false; // Special case: start animation when audio starts
  export let showAllAtOnce: boolean = false; // Special case: show all content at once
  export let audioSegments: string[] = []; // Array of audio files to play sequentially

  let canvas: HTMLCanvasElement;
  let ctx: CanvasRenderingContext2D;
  let animationFrame: number;
  let currentLineIndex = 0;
  let currentCharIndex = 0;
  let animationStartTime = 0;
  let isAnimating = false;
  
  // Multi-segment audio handling
  let currentAudioSegment = 0;
  let currentWhiteboardStage = 0;
  let audioElements: HTMLAudioElement[] = [];
  let isPlayingSegments = false;

  // Whiteboard styling
  const backgroundColor = '#ffffff';
  const textColor = '#2c3e50';
  const fontSize = 32; // Increased from 24 to 32
  const lineHeight = 60; // Keep as is for now
  const padding = 40;
  const fontFamily = 'Comic Sans MS, cursive, sans-serif';

  // Helper: Parse text formatting markers
  function parseTextFormatting(text: string): { text: string; isBold: boolean; isUnderlined: boolean } {
    let isBold = false;
    let isUnderlined = false;
    let cleanText = text;
    
    // Check for bold and underline markers
    if (text.includes('**') && text.includes('__')) {
      // Both bold and underlined
      cleanText = text.replace(/\*\*(.*?)\*\*/g, '$1').replace(/__(.*?)__/g, '$1');
      isBold = true;
      isUnderlined = true;
    } else if (text.includes('**')) {
      // Just bold
      cleanText = text.replace(/\*\*(.*?)\*\*/g, '$1');
      isBold = true;
    } else if (text.includes('__')) {
      // Just underlined
      cleanText = text.replace(/__(.*?)__/g, '$1');
      isUnderlined = true;
    }
    
    return { text: cleanText, isBold, isUnderlined };
  }

  // Helper: Check if text is an image URL
  function isImageUrl(text: string): boolean {
    return text.startsWith('![') && text.includes('](') && text.endsWith(')');
  }

  // Helper: Extract image path from markdown image syntax
  function extractImagePath(text: string): string | null {
    const match = text.match(/!\[.*?\]\((.*?)\)/);
    return match ? match[1] : null;
  }

  // Helper: Load and draw image on canvas
  function drawImageOnCanvas(imagePath: string, x: number, y: number, maxWidth: number, maxHeight: number) {
    const img = new Image();
    img.onload = () => {
      if (!ctx || !canvas) return;
      
      // Calculate aspect ratio to maintain proportions
      const aspectRatio = img.width / img.height;
      let drawWidth = maxWidth;
      let drawHeight = maxWidth / aspectRatio;
      
      if (drawHeight > maxHeight) {
        drawHeight = maxHeight;
        drawWidth = maxHeight * aspectRatio;
      }
      
      // Center the image
      const centerX = x + (maxWidth - drawWidth) / 2;
      const centerY = y + (maxHeight - drawHeight) / 2;
      
      ctx.drawImage(img, centerX, centerY, drawWidth, drawHeight);
    };
    img.src = imagePath;
  }

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
    if (!ctx || !canvas || !isAnimating) return;

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

    // Handle multi-stage whiteboard (array of arrays) - skip animation for these
    if (Array.isArray(textLines) && Array.isArray(textLines[0])) {
      return; // Multi-stage slides are handled by showWhiteboardStage
    }
    
    // Handle single-stage whiteboard (array of strings)
    const singleStageTextLines = textLines as string[];
    
    // Check if this is a list slide (shows all terms at once)
    // vs progressive slide (adds one term at a time)
    // For progressive slides, audio text should match only the last line
    const lastLine = singleStageTextLines[singleStageTextLines.length - 1];
    // Check if this is a bullet point slide without title audio (like "For example" slide)
    const isBulletSlideWithoutTitleAudio = singleStageTextLines.length > 1 && 
                                          singleStageTextLines[0].startsWith('**__') && 
                                          singleStageTextLines[0].endsWith('__**') &&
                                          singleStageTextLines[1].startsWith('•') &&
                                          !titleAudio;
    
    const isProgressiveSlide = singleStageTextLines.length > 1 && 
                              lastLine.startsWith('•') && 
                              audioText && 
                              audioText.trim() !== '' &&
                              audioTextMatchesWhiteboard() &&
                              !isBulletSlideWithoutTitleAudio;
    
    const isListSlide = singleStageTextLines.length > 1 && singleStageTextLines[1].startsWith('•') && !isProgressiveSlide;
    
    // Check if this is a regular slide that should animate all lines from the beginning
    // (like AdvertiserConflicts slides that have a title followed by regular sentences)
    const isRegularSlide = singleStageTextLines.length > 1 && 
                          singleStageTextLines[0].startsWith('**__') && 
                          singleStageTextLines[0].endsWith('__**') &&
                          !singleStageTextLines[1].startsWith('•');
    
    // Draw all lines except the last instantly (for progressive slides only)
    let y = padding;
    if (!isListSlide && !isRegularSlide && !isBulletSlideWithoutTitleAudio) {
      for (let i = 0; i < singleStageTextLines.length - 1; i++) {
        if (singleStageTextLines[i]) {
          const formatting = parseTextFormatting(singleStageTextLines[i]);
          const wrapped = wrapText(ctx, formatting.text, canvas.width - 2 * padding);
          for (let w = 0; w < wrapped.length; w++) {
            const line = wrapped[w];
            // Special layout for Stand Alone Rule slide 2
            let x = padding;
            if (singleStageTextLines[i] === 'Not Allowed:') {
              // Position "Not Allowed:" on the left side
              x = padding;
            } else if (singleStageTextLines[i] === 'Allowed:') {
              // Position "Allowed:" on the left side (under the first image)
              x = padding;
            } else if (i === 0 && w === 0) {
              // Center the title (first line, first word wrap)
              x = (canvas.width - ctx.measureText(line).width) / 2;
            } else {
              // Regular left alignment for other text
              x = padding;
            }
            
            // Apply formatting
            if (formatting.isBold) {
              ctx.font = `bold ${fontSize}px ${fontFamily}`;
            } else {
              ctx.font = `${fontSize}px ${fontFamily}`;
            }
            
            ctx.fillText(line, x, y);
            
            // Draw underline if needed
            if (formatting.isUnderlined) {
              const metrics = ctx.measureText(line);
              ctx.strokeStyle = textColor;
              ctx.lineWidth = 3;
              ctx.lineCap = 'round';
              ctx.beginPath();
              ctx.moveTo(x, y + fontSize + 4);
              ctx.lineTo(x + metrics.width, y + fontSize + 4);
              ctx.stroke();
            }
            
            y += lineHeight;
          }
        }
      }
    }

    // Animate based on slide type
    if (singleStageTextLines.length > 0) {
      if (isListSlide || isRegularSlide || isBulletSlideWithoutTitleAudio) {
        // For list slides, animate all lines together
        const elapsedTime = (currentTime - animationStartTime) / 1000;
        const totalChars = singleStageTextLines.map(line => {
          const formatting = parseTextFormatting(line);
          const wrapped = wrapText(ctx, formatting.text, canvas.width - 2 * padding);
          return wrapped.join('').length;
        }).reduce((sum, length) => sum + length, 0);
        
        let charCount = Math.floor(elapsedTime / drawSpeed);
        if (charCount > totalChars) charCount = totalChars;
        
        let charsDrawn = 0;
        for (let i = 0; i < singleStageTextLines.length; i++) {
          const line = singleStageTextLines[i];
          const formatting = parseTextFormatting(line);
          const wrapped = wrapText(ctx, formatting.text, canvas.width - 2 * padding);
          
          for (let w = 0; w < wrapped.length; w++) {
            const lineText = wrapped[w];
            const charsToDrawNow = charCount - charsDrawn;
            if (charsToDrawNow > 0) {
              const sub = lineText.substring(0, charsToDrawNow);
              const x = i === 0 && w === 0 ? (canvas.width - ctx.measureText(lineText).width) / 2 : padding;
              
              // Apply formatting
              if (formatting.isBold) {
                ctx.font = `bold ${fontSize}px ${fontFamily}`;
              } else {
                ctx.font = `${fontSize}px ${fontFamily}`;
              }
              
              ctx.fillText(sub, x, y);
              
              // Draw underline if needed
              if (formatting.isUnderlined) {
                const metrics = ctx.measureText(sub);
                ctx.strokeStyle = textColor;
                ctx.lineWidth = 3;
                ctx.lineCap = 'round';
                ctx.beginPath();
                ctx.moveTo(x, y + fontSize + 4);
                ctx.lineTo(x + metrics.width, y + fontSize + 4);
                ctx.stroke();
              }
            }
            y += lineHeight;
            charsDrawn += lineText.length;
          }
        }
        
        if (charCount >= totalChars) {
          isAnimating = false;
          dispatch('animationComplete');
        } else {
          animationFrame = requestAnimationFrame(animate);
        }
      } else {
        // For progressive slides, animate only the last line
        const lastIdx = singleStageTextLines.length - 1;
        const lineToAnimate = singleStageTextLines[lastIdx];
        const formatting = parseTextFormatting(lineToAnimate);
        const wrapped = wrapText(ctx, formatting.text, canvas.width - 2 * padding);
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
            
            // Apply formatting
            if (formatting.isBold) {
              ctx.font = `bold ${fontSize}px ${fontFamily}`;
            } else {
              ctx.font = `${fontSize}px ${fontFamily}`;
            }
            
            ctx.fillText(sub, x, y);
            
            // Draw underline if needed
            if (formatting.isUnderlined) {
              const metrics = ctx.measureText(sub);
              ctx.strokeStyle = textColor;
              ctx.lineWidth = 3;
              ctx.lineCap = 'round';
              ctx.beginPath();
              ctx.moveTo(x, y + fontSize + 4);
              ctx.lineTo(x + metrics.width, y + fontSize + 4);
              ctx.stroke();
            }
          }
          y += lineHeight;
          charsDrawnInLine += lineText.length;
        }
        if (charCount >= totalCharsInLine) {
          isAnimating = false;
          dispatch('animationComplete');
        } else {
          animationFrame = requestAnimationFrame(animate);
        }
      }
    }
  }

  function startAnimation() {
    if (isAnimating) return;
    isAnimating = true;
    if (currentLineIndex === 0) {
       animationStartTime = performance.now();
    }
    
    if (showAllAtOnce) {
      // Show all content immediately
      showAllContent();
      isAnimating = false;
      dispatch('animationComplete');
    } else {
      animationFrame = requestAnimationFrame(animate);
    }
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

  // Multi-segment audio functions
  function playAudioSegments() {
    if (audioSegments.length === 0) return;
    
    isPlayingSegments = true;
    currentAudioSegment = 0;
    currentWhiteboardStage = 0;
    
    // Show initial whiteboard content
    if (Array.isArray(textLines) && Array.isArray(textLines[0])) {
      showWhiteboardStage(0);
    }
    
    playNextAudioSegment();
  }

  function playNextAudioSegment() {
    if (currentAudioSegment >= audioSegments.length) {
      isPlayingSegments = false;
      dispatch('animationComplete');
      return;
    }

    const audioElement = new Audio(audioSegments[currentAudioSegment]);
    audioElements.push(audioElement);
    
    audioElement.addEventListener('ended', () => {
      currentAudioSegment++;
      currentWhiteboardStage++;
      
      // Update whiteboard content for next stage
      if (Array.isArray(textLines) && Array.isArray(textLines[0]) && currentWhiteboardStage < textLines.length) {
        showWhiteboardStage(currentWhiteboardStage);
      }
      
      // Play next segment
      setTimeout(() => {
        playNextAudioSegment();
      }, 500); // Small delay between segments
    });
    
    audioElement.play().catch((error) => {
      console.error('Failed to play audio segment:', error);
      // Continue to next segment even if this one fails
      currentAudioSegment++;
      currentWhiteboardStage++;
      playNextAudioSegment();
    });
  }

  function showWhiteboardStage(stage: number) {
    if (!ctx || !canvas || !Array.isArray(textLines) || !Array.isArray(textLines[0])) return;
    
    if (stage >= textLines.length) return;
    
    const stageTextLines = textLines[stage];
    
    // Ensure stageTextLines is an array of strings
    if (Array.isArray(stageTextLines)) {
      // Start animation for this stage
      animateWhiteboardStage(stageTextLines);
    }
  }

  function animateWhiteboardStage(stageTextLines: string[]) {
    if (!ctx || !canvas) return;
    
    // Clear any existing animation
    if (animationFrame) {
      cancelAnimationFrame(animationFrame);
    }
    
    // Set up animation variables
    let currentLineIndex = 0;
    let currentCharIndex = 0;
    let animationStartTime = performance.now();
    let isAnimating = true;
    
    function animateStage(currentTime: number) {
      if (!ctx || !canvas || !isAnimating) return;
      
      // Clear canvas and draw background
      ctx.fillStyle = backgroundColor;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Draw grid pattern
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
      
      // Set up text rendering
      ctx.fillStyle = textColor;
      ctx.font = `${fontSize}px ${fontFamily}`;
      ctx.textBaseline = 'top';
      
      const elapsedTime = (currentTime - animationStartTime) / 1000;
      const totalChars = stageTextLines.map(line => {
        const formatting = parseTextFormatting(line);
        const wrapped = wrapText(ctx, formatting.text, canvas.width - 2 * padding);
        return wrapped.join('').length;
      }).reduce((sum, length) => sum + length, 0);
      
      let charCount = Math.floor(elapsedTime / drawSpeed);
      if (charCount > totalChars) charCount = totalChars;
      
      let charsDrawn = 0;
      let y = padding;
      
      for (let i = 0; i < stageTextLines.length; i++) {
        const line = stageTextLines[i];
        const formatting = parseTextFormatting(line);
        const wrapped = wrapText(ctx, formatting.text, canvas.width - 2 * padding);
        
        for (let w = 0; w < wrapped.length; w++) {
          const lineText = wrapped[w];
          const charsToDrawNow = charCount - charsDrawn;
          
          if (charsToDrawNow > 0) {
            const sub = lineText.substring(0, charsToDrawNow);
            const x = i === 0 && w === 0 ? (canvas.width - ctx.measureText(lineText).width) / 2 : padding;
            
            // Apply formatting
            if (formatting.isBold) {
              ctx.font = `bold ${fontSize}px ${fontFamily}`;
            } else {
              ctx.font = `${fontSize}px ${fontFamily}`;
            }
            
            ctx.fillText(sub, x, y);
            
            // Draw underline if needed
            if (formatting.isUnderlined) {
              const metrics = ctx.measureText(sub);
              ctx.strokeStyle = textColor;
              ctx.lineWidth = 3;
              ctx.lineCap = 'round';
              ctx.beginPath();
              ctx.moveTo(x, y + fontSize + 4);
              ctx.lineTo(x + metrics.width, y + fontSize + 4);
              ctx.stroke();
            }
          }
          
          y += lineHeight;
          charsDrawn += lineText.length;
        }
      }
      
      if (charCount >= totalChars) {
        isAnimating = false;
        // Animation complete for this stage
      } else {
        animationFrame = requestAnimationFrame(animateStage);
      }
    }
    
    // Start the animation
    animationFrame = requestAnimationFrame(animateStage);
  }

  let prevTextLines: string[] | string[][] = [];
  let animationStarted = false;

  // When the slide changes (textLines is updated), reset the animation state
  $: if (JSON.stringify(textLines) !== JSON.stringify(prevTextLines)) {
    prevTextLines = Array.isArray(textLines) ? [...textLines] as string[] | string[][] : [];
    resetAnimation();
    animationStarted = false;
    initCanvas(); // Ensure canvas is ready
    // Don't auto-start animation - wait for timing rules
  }

  // Determine if audio text matches whiteboard text
  function audioTextMatchesWhiteboard(): boolean {
    if (!textLines || textLines.length === 0) return false;
    
    // If audio text is empty, treat it as matching (show animation immediately)
    if (!audioText || audioText.trim() === '') return true;
    
    // Clean the audio text (remove common punctuation and normalize)
    const cleanAudioText = audioText
      .replace(/[.,!?;:]/g, '')
      .replace(/\s+/g, ' ')
      .trim()
      .toLowerCase();
    
    console.log('Audio text:', audioText);
    console.log('Clean audio text:', cleanAudioText);
    
    // Handle multi-stage whiteboard (array of arrays)
    if (Array.isArray(textLines) && Array.isArray(textLines[0])) {
      // For multi-stage slides, we don't need to match audio text
      // The segments will be handled by the multi-segment audio system
      return false;
    }
    
    // Handle single-stage whiteboard (array of strings)
    const singleStageTextLines = textLines as string[];
    
    // If there's a title audio, compare main audio text against whiteboard text excluding the first line (title)
    if (titleAudio && singleStageTextLines.length > 1) {
      const contentLines = singleStageTextLines.slice(1); // Skip the first line (title)
      const cleanWhiteboardText = contentLines.map(line => {
        const formatting = parseTextFormatting(line);
        return formatting.text;
      }).join(' ');
      
      const cleanWhiteboardLower = cleanWhiteboardText
        .replace(/[.,!?;:]/g, '')
        .replace(/\s+/g, ' ')
        .trim()
        .toLowerCase();
      
      // For title audio slides, strip the title from the original audio text before cleaning
      let audioTextForComparison = audioText;
      if (singleStageTextLines[0]) {
        const titleText = singleStageTextLines[0].replace(/[.,!?;:•]/g, '').trim();
        
        // Try multiple patterns: "Title: Content", "Title Content", or just "Title"
        const patterns = [
          titleText + ':',
          titleText + ' ',
          titleText
        ];
        
        for (const pattern of patterns) {
          if (audioTextForComparison.toLowerCase().startsWith(pattern.toLowerCase())) {
            audioTextForComparison = audioTextForComparison.substring(pattern.length).trim();
            break;
          }
        }
        
        // If no pattern matched, try to find and remove the title word from the beginning
        if (audioTextForComparison === audioText) {
          const words = audioTextForComparison.toLowerCase().split(' ');
          if (words[0] === titleText.toLowerCase()) {
            audioTextForComparison = audioTextForComparison.substring(titleText.length).trim();
          }
        }
      }
      
      // Clean the stripped audio text
      const cleanAudioTextForComparison = audioTextForComparison
        .replace(/[.,!?;:•]/g, '')
        .replace(/\s+/g, ' ')
        .trim()
        .toLowerCase();
      
      // Make comparison flexible - check if all whiteboard words are present in audio words
      const audioWords = cleanAudioTextForComparison.split(' ').filter(word => word.length > 0);
      const whiteboardWords = cleanWhiteboardLower.split(' ').filter(word => word.length > 0);
      
      // Return true if all whiteboard words are present in audio (allowing for extra words in audio)
      return whiteboardWords.every(word => audioWords.includes(word));
    }
    
    // Check if this is a regular slide (like AdvertiserConflicts) without title audio
    const isRegularSlide = singleStageTextLines.length > 1 && 
                          singleStageTextLines[0].startsWith('**__') && 
                          singleStageTextLines[0].endsWith('__**') &&
                          !singleStageTextLines[1].startsWith('•') &&
                          !titleAudio;
    
    // Check if this is a bullet point slide without title audio (like "For example" slide)
    const isBulletSlideWithoutTitleAudio = singleStageTextLines.length > 1 && 
                                          singleStageTextLines[0].startsWith('**__') && 
                                          singleStageTextLines[0].endsWith('__**') &&
                                          singleStageTextLines[1].startsWith('•') &&
                                          !titleAudio;
    
    // For regular slides or bullet slides without title audio, always return true to start animation immediately
    if (isRegularSlide || isBulletSlideWithoutTitleAudio) {
      console.log('Slide without title audio - starting animation immediately');
      return true;
    }
    
    // For progressive slides, compare audio with the last line only
    if (singleStageTextLines.length > 1) {
      const lastLine = singleStageTextLines[singleStageTextLines.length - 1];
      const formatting = parseTextFormatting(lastLine);
      const cleanLastLine = formatting.text
        .replace(/[.,!?;:•]/g, '') // Also remove bullet points
        .replace(/\s+/g, ' ')
        .trim()
        .toLowerCase();
      
      console.log('Last line:', lastLine);
      console.log('Clean last line:', cleanLastLine);
      console.log('Match:', cleanAudioText === cleanLastLine);
      
      return cleanAudioText === cleanLastLine;
    }
    
    // For single line slides, compare with entire whiteboard text
    const cleanWhiteboardText = singleStageTextLines.map(line => {
      const formatting = parseTextFormatting(line);
      return formatting.text;
    }).join(' ');
    
    const cleanWhiteboardLower = cleanWhiteboardText
      .replace(/[.,!?;:]/g, '')
      .replace(/\s+/g, ' ')
      .trim()
      .toLowerCase();
    
    console.log('Whiteboard text:', singleStageTextLines);
    console.log('Clean whiteboard text:', cleanWhiteboardLower);
    console.log('Match:', cleanAudioText === cleanWhiteboardLower);
    
    return cleanAudioText === cleanWhiteboardLower;
  }



  // Handle title audio if provided
  let titleAudioFinished = false;
  let mainAudioStarted = false;
  let animationTriggered = false;
  




  // Reset state when audio changes
  $: if ($audioStore.currentIndex !== undefined) {
    animationStarted = false;
    animationTriggered = false;
    titleAudioFinished = false;
    mainAudioStarted = false;
  }

  // Track when we've started processing this slide
  let slideProcessed = false;
  let currentSlideId = '';

  // Create a unique slide ID based on textLines content
  $: slideId = textLines.join('|') + '|' + titleAudio;

  // Reset when slide content changes
  $: if (slideId !== currentSlideId) {
    currentSlideId = slideId;
    slideProcessed = false;
    animationTriggered = false;
  }

  // Play title audio when animation starts, then follow timing rules
  $: if ($audioStore.isPlaying && !slideProcessed && textLines && textLines.length > 0) {
    slideProcessed = true;
    animationTriggered = true;
    animationStarted = true;
    
    // Check if this is a multi-segment audio slide
    if (audioSegments.length > 0) {
      console.log('Multi-segment audio detected, starting segment playback');
      // Pause the main audio to let segments play
      if (audioElement) {
        audioElement.pause();
        console.log('Paused main audio for segment playback');
      }
      playAudioSegments();
    } else if (titleAudio) {
      // Pause the main audio to let title audio play first
      if (audioElement) {
        audioElement.pause();
        console.log('Paused main audio for title audio');
      }
      // Play title audio first
      console.log('Title audio detected, playing title first');
      playTitleAudio();
    } else if (startWithAudio) {
      // Special case: start animation immediately when audio starts
      console.log('startWithAudio enabled - starting animation immediately with audio');
      startAnimation();
    } else {
      // No title audio, follow original timing rules
      const shouldStartImmediately = audioTextMatchesWhiteboard();
      
      if (shouldStartImmediately) {
        console.log('No title audio - audio matches whiteboard text - playing together');
        startAnimation();
      } else {
        console.log('No title audio - audio does not match whiteboard text - playing audio first, then animation');
        // Wait for audio to finish before starting animation
        const checkAudioProgress = () => {
          if ($audioStore.progress >= 99) {
            console.log('Audio finished, starting animation');
            startAnimation();
          } else {
            setTimeout(checkAudioProgress, 100);
          }
        };
        checkAudioProgress();
      }
    }
  }

  function playTitleAudio() {
    if (titleAudio) {
      console.log('Playing title audio:', titleAudio);
      const titleAudioElement = new Audio(titleAudio);
      
      // Show the title immediately when title audio starts
      console.log('Showing title immediately for title audio');
      showTitleOnly();
      
      // Listen for title audio completion
      titleAudioElement.addEventListener('ended', () => {
        console.log('Title audio finished, checking timing rules');
        checkTimingRules();
      });
      
      // Try to play the title audio
      titleAudioElement.play().catch((error) => {
        console.error('Failed to play title audio:', error);
        // If autoplay is blocked, just proceed with timing rules
        checkTimingRules();
      });
    }
  }

  function showTitleOnly() {
    if (!ctx || !canvas) return;
    
    // Clear canvas and draw background
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid pattern
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
    
    // Show only the title (first line) immediately
    if (textLines.length > 0) {
      ctx.fillStyle = textColor;
      ctx.font = `${fontSize}px ${fontFamily}`;
      ctx.textBaseline = 'top';
      
      // Handle both single-stage and multi-stage textLines
      let titleLine: string;
      if (Array.isArray(textLines) && Array.isArray(textLines[0])) {
        // Multi-stage: get first line from first stage
        titleLine = (textLines[0] as string[])[0];
      } else {
        // Single-stage: get first line
        titleLine = (textLines as string[])[0];
      }
      
      const formatting = parseTextFormatting(titleLine);
      const wrapped = wrapText(ctx, formatting.text, canvas.width - 2 * padding);
      
      let y = padding;
      for (let w = 0; w < wrapped.length; w++) {
        const line = wrapped[w];
        const x = (canvas.width - ctx.measureText(line).width) / 2;
        
        // Apply formatting
        if (formatting.isBold) {
          ctx.font = `bold ${fontSize}px ${fontFamily}`;
        } else {
          ctx.font = `${fontSize}px ${fontFamily}`;
        }
        
        ctx.fillText(line, x, y);
        
        // Draw underline if needed
        if (formatting.isUnderlined) {
          const metrics = ctx.measureText(line);
          ctx.strokeStyle = textColor;
          ctx.lineWidth = 3;
          ctx.lineCap = 'round';
          ctx.beginPath();
          ctx.moveTo(x, y + fontSize + 4);
          ctx.lineTo(x + metrics.width, y + fontSize + 4);
          ctx.stroke();
        }
        
        y += lineHeight;
      }
    }
  }

  function showAllPreviousContent() {
    if (!ctx || !canvas) return;
    
    // Clear canvas and draw background
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid pattern
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
    
    // Handle multi-stage whiteboard (array of arrays) - skip this function
    if (Array.isArray(textLines) && Array.isArray(textLines[0])) {
      return;
    }
    
    // Handle single-stage whiteboard (array of strings)
    const singleStageTextLines = textLines as string[];
    
    // Show all lines except the last one immediately
    if (singleStageTextLines.length > 1) {
      ctx.fillStyle = textColor;
      ctx.font = `${fontSize}px ${fontFamily}`;
      ctx.textBaseline = 'top';
      
      let y = padding;
      for (let i = 0; i < singleStageTextLines.length - 1; i++) {
        const line = singleStageTextLines[i];
        const formatting = parseTextFormatting(line);
        const wrapped = wrapText(ctx, formatting.text, canvas.width - 2 * padding);
        
        for (let w = 0; w < wrapped.length; w++) {
          const wrappedLine = wrapped[w];
          const x = i === 0 && w === 0 ? (canvas.width - ctx.measureText(wrappedLine).width) / 2 : padding;
          
          // Apply formatting
          if (formatting.isBold) {
            ctx.font = `bold ${fontSize}px ${fontFamily}`;
          } else {
            ctx.font = `${fontSize}px ${fontFamily}`;
          }
          
          ctx.fillText(wrappedLine, x, y);
          
          // Draw underline if needed
          if (formatting.isUnderlined) {
            const metrics = ctx.measureText(wrappedLine);
            ctx.strokeStyle = textColor;
            ctx.lineWidth = 3;
            ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.moveTo(x, y + fontSize + 4);
            ctx.lineTo(x + metrics.width, y + fontSize + 4);
            ctx.stroke();
          }
          
          y += lineHeight;
        }
      }
    }
  }

  function showAllContent() {
    if (!ctx || !canvas) return;
    
    // Clear canvas and draw background
    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw grid pattern
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
    
    // Handle multi-stage whiteboard (array of arrays) - skip this function
    if (Array.isArray(textLines) && Array.isArray(textLines[0])) {
      return;
    }
    
    // Handle single-stage whiteboard (array of strings)
    const singleStageTextLines = textLines as string[];
    
    // Show all content immediately
    ctx.fillStyle = textColor;
    ctx.font = `${fontSize}px ${fontFamily}`;
    ctx.textBaseline = 'top';
    
    let y = padding;
    for (let i = 0; i < singleStageTextLines.length; i++) {
      if (singleStageTextLines[i]) {
        // Check if this line is an image
        if (isImageUrl(singleStageTextLines[i])) {
          const imagePath = extractImagePath(singleStageTextLines[i]);
          if (imagePath) {
            // Draw image below the previous text
            const imageHeight = 200; // Increased height for higher quality images
            drawImageOnCanvas(imagePath, padding, y, canvas.width - 2 * padding, imageHeight);
            y += imageHeight + 20; // Add space after image
          }
        } else {
          // Regular text line
          const formatting = parseTextFormatting(singleStageTextLines[i]);
          const wrapped = wrapText(ctx, formatting.text, canvas.width - 2 * padding);
          for (let w = 0; w < wrapped.length; w++) {
            const line = wrapped[w];
            
            // Special layout for Stand Alone Rule slide 2
            let x = padding;
            if (singleStageTextLines[i] === 'Not Allowed:') {
              // Position "Not Allowed:" on the left side
              x = padding;
            } else if (singleStageTextLines[i] === 'Allowed:') {
              // Position "Allowed:" on the left side (under the first image)
              x = padding;
            } else if (i === 0 && w === 0) {
              // Center the title (first line, first word wrap)
              x = (canvas.width - ctx.measureText(line).width) / 2;
            } else {
              // Regular left alignment for other text
              x = padding;
            }
            
            // Apply formatting
            if (formatting.isBold) {
              ctx.font = `bold ${fontSize}px ${fontFamily}`;
            } else {
              ctx.font = `${fontSize}px ${fontFamily}`;
            }
            
            ctx.fillText(line, x, y);
            
            // Draw underline if needed
            if (formatting.isUnderlined) {
              const metrics = ctx.measureText(line);
              ctx.strokeStyle = textColor;
              ctx.lineWidth = 3;
              ctx.lineCap = 'round';
              ctx.beginPath();
              ctx.moveTo(x, y + fontSize + 4);
              ctx.lineTo(x + metrics.width, y + fontSize + 4);
              ctx.stroke();
            }
            
            y += lineHeight;
          }
        }
      }
    }
  }

  function checkTimingRules() {
    console.log('Checking timing rules...');
    
    // Resume the main audio after title audio finishes
    if (audioElement) {
      audioElement.play();
      console.log('Resumed main audio after title audio');
    }
    
    const shouldStartImmediately = audioTextMatchesWhiteboard();
    
    if (shouldStartImmediately) {
      console.log('Audio matches whiteboard text - playing together');
      // Start animation for the remaining content (skip first line since it's already shown)
      startAnimationForRemainingContent();
    } else {
      console.log('Audio does not match whiteboard text - playing audio first, then animation');
      // Wait for audio to finish before starting animation
      const checkAudioProgress = () => {
        if ($audioStore.progress >= 99) {
          console.log('Audio finished, starting animation');
          startAnimationForRemainingContent();
        } else {
          setTimeout(checkAudioProgress, 100);
        }
      };
      checkAudioProgress();
    }
  }

  function startAnimationForRemainingContent() {
    if (!ctx || !canvas) return;
    
    // Handle multi-stage whiteboard (array of arrays) - skip this function
    if (Array.isArray(textLines) && Array.isArray(textLines[0])) {
      return;
    }
    
    // Handle single-stage whiteboard (array of strings)
    const singleStageTextLines = textLines as string[];
    
    // For progressive slides, show all previous content immediately
    if (singleStageTextLines.length > 1) {
      // Check if this is a list slide (shows all terms at once)
      // vs progressive slide (adds one term at a time)
      // For progressive slides, audio text should match only the last line
      const lastLine = singleStageTextLines[singleStageTextLines.length - 1];
      const isProgressiveSlide = singleStageTextLines.length > 1 && 
                                lastLine.startsWith('•') && 
                                audioText && 
                                audioText.trim() !== '' &&
                                audioTextMatchesWhiteboard();
      
      const isListSlide = singleStageTextLines.length > 1 && singleStageTextLines[1].startsWith('•') && !isProgressiveSlide;
      
      if (isListSlide) {
        // For list slides, animate all lines together
        currentLineIndex = 0;
        currentCharIndex = 0;
        animationStartTime = performance.now();
        startAnimation();
      } else {
        // For progressive slides, show all lines except the last one immediately
        showAllPreviousContent();
        // Start animation from the last line only
        currentLineIndex = singleStageTextLines.length - 1;
        currentCharIndex = 0;
        animationStartTime = performance.now();
        startAnimation();
      }
    } else {
      // For single line slides, start from beginning
      currentLineIndex = 0;
      currentCharIndex = 0;
      animationStartTime = performance.now();
      startAnimation();
    }
  }

  // Handle main audio progress for non-title-audio slides
  $: if ($audioStore.isPlaying && !titleAudio && animationStarted && !isAnimating) {
    const shouldStartImmediately = audioTextMatchesWhiteboard() || showAllAtOnce;
    
    if (shouldStartImmediately) {
      startAnimation();
    } else {
      if ($audioStore.progress >= 99) {
        startAnimation();
      }
    }
  }

  // Start animation immediately when audio starts for showAllAtOnce slides
  $: if ($audioStore.isPlaying && showAllAtOnce && !isAnimating) {
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
<script lang="ts">
  import { onMount } from 'svelte';
  
  let audioLoaded = false;
  let imageLoaded = false;
  let audioError = '';
  let imageError = '';
  
  onMount(() => {
    // Test audio loading
    const audio = new Audio('/audio/introduction/intro_01.mp3');
    audio.onloadstart = () => console.log('Audio loading started');
    audio.oncanplay = () => {
      console.log('Audio can play');
      audioLoaded = true;
    };
    audio.onerror = (e) => {
      console.error('Audio error:', e);
      audioError = 'Failed to load audio';
    };
    
    // Test image loading
    const img = new Image();
    img.onload = () => {
      console.log('Image loaded');
      imageLoaded = true;
    };
    img.onerror = () => {
      console.error('Image failed to load');
      imageError = 'Failed to load image';
    };
    img.src = '/images/introduction/basketballBackground.png';
  });
</script>

<div class="p-8">
  <h1 class="text-2xl font-bold mb-4">Asset Loading Test</h1>
  
  <div class="space-y-4">
    <div>
      <h2 class="text-lg font-semibold">Audio Test</h2>
      <p>Status: {audioLoaded ? '✅ Loaded' : audioError ? '❌ ' + audioError : '⏳ Loading...'}</p>
      <audio controls src="/audio/introduction/intro_01.mp3" class="mt-2"></audio>
    </div>
    
    <div>
      <h2 class="text-lg font-semibold">Image Test</h2>
      <p>Status: {imageLoaded ? '✅ Loaded' : imageError ? '❌ ' + imageError : '⏳ Loading...'}</p>
      <img src="/images/introduction/basketballBackground.png" alt="Test image" class="mt-2 max-w-xs" />
    </div>
    
    <div>
      <h2 class="text-lg font-semibold">Direct Links</h2>
      <ul class="list-disc pl-4">
        <li><a href="/audio/introduction/intro_01.mp3" target="_blank" class="text-blue-600 hover:underline">Audio File</a></li>
        <li><a href="/images/introduction/basketballBackground.png" target="_blank" class="text-blue-600 hover:underline">Image File</a></li>
      </ul>
    </div>
  </div>
</div> 
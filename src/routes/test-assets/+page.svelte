<script lang="ts">
  import { onMount } from 'svelte';
  
  let audioLoaded = false;
  let imageLoaded = false;
  let audioError = '';
  let imageError = '';
  let debugInfo = '';
  
  onMount(() => {
    // Test direct paths
    const audio = new Audio('/audio/introduction/intro_01.mp3');
    audio.onloadstart = () => {
      console.log('Audio loading started');
      debugInfo += 'Audio loading started\n';
    };
    audio.oncanplay = () => {
      console.log('Audio can play');
      debugInfo += 'Audio can play\n';
      audioLoaded = true;
    };
    audio.onerror = (e) => {
      console.error('Audio error:', e);
      debugInfo += `Audio error: ${e}\n`;
      audioError = 'Failed to load audio';
    };
    
    // Test image loading
    const img = new Image();
    img.onload = () => {
      console.log('Image loaded');
      debugInfo += 'Image loaded\n';
      imageLoaded = true;
    };
    img.onerror = () => {
      console.error('Image failed to load');
      debugInfo += 'Image failed to load\n';
      imageError = 'Failed to load image';
    };
    img.src = '/images/introduction/basketballBackground.png';
    
    // Test API route
    const apiAudio = new Audio('/api/static/audio/introduction/intro_01.mp3');
    apiAudio.onloadstart = () => {
      debugInfo += 'API Audio loading started\n';
    };
    apiAudio.oncanplay = () => {
      debugInfo += 'API Audio can play\n';
    };
    apiAudio.onerror = (e) => {
      debugInfo += `API Audio error: ${e}\n`;
    };
    
    // Test direct fetch
    fetch('/audio/introduction/intro_01.mp3')
      .then(response => {
        console.log('Audio fetch response:', response.status);
        debugInfo += `Audio fetch: ${response.status}\n`;
        return response.headers.get('content-type');
      })
      .then(contentType => {
        debugInfo += `Audio content-type: ${contentType}\n`;
      })
      .catch(error => {
        console.error('Audio fetch error:', error);
        debugInfo += `Audio fetch error: ${error}\n`;
      });
      
    fetch('/images/introduction/basketballBackground.png')
      .then(response => {
        console.log('Image fetch response:', response.status);
        debugInfo += `Image fetch: ${response.status}\n`;
        return response.headers.get('content-type');
      })
      .then(contentType => {
        debugInfo += `Image content-type: ${contentType}\n`;
      })
      .catch(error => {
        console.error('Image fetch error:', error);
        debugInfo += `Image fetch error: ${error}\n`;
      });
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
      <h2 class="text-lg font-semibold">API Route Test</h2>
      <audio controls src="/api/static/audio/introduction/intro_01.mp3" class="mt-2"></audio>
      <img src="/api/static/images/introduction/basketballBackground.png" alt="API Test image" class="mt-2 max-w-xs" />
    </div>
    
    <div>
      <h2 class="text-lg font-semibold">Direct Links</h2>
      <ul class="list-disc pl-4">
        <li><a href="/audio/introduction/intro_01.mp3" target="_blank" class="text-blue-600 hover:underline">Audio File</a></li>
        <li><a href="/images/introduction/basketballBackground.png" target="_blank" class="text-blue-600 hover:underline">Image File</a></li>
        <li><a href="/api/static/audio/introduction/intro_01.mp3" target="_blank" class="text-blue-600 hover:underline">API Audio File</a></li>
        <li><a href="/api/static/images/introduction/basketballBackground.png" target="_blank" class="text-blue-600 hover:underline">API Image File</a></li>
      </ul>
    </div>
    
    <div>
      <h2 class="text-lg font-semibold">Debug Info</h2>
      <pre class="bg-gray-100 p-4 rounded text-sm overflow-auto max-h-40">{debugInfo}</pre>
    </div>
  </div>
</div> 
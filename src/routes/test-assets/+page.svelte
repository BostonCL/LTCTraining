<script lang="ts">
	import { onMount } from 'svelte';
	let audioLoaded = false;
	let imageLoaded = false;
	let audioError = '';
	let imageError = '';
	let debugInfo = '';

	onMount(() => {
		// Test API routes only (since direct paths aren't working)
		const apiAudio = new Audio('/api/static/audio/introduction/intro_01.mp3');
		apiAudio.onloadstart = () => { debugInfo += 'API Audio loading started\n'; };
		apiAudio.oncanplay = () => { debugInfo += 'API Audio can play\n'; audioLoaded = true; };
		apiAudio.onerror = (e) => { 
			debugInfo += `API Audio error: ${e}\n`; 
			audioError = 'Failed to load audio';
			console.error('Audio error details:', e);
		};

		const apiImg = new Image();
		apiImg.onload = () => { debugInfo += 'API Image loaded\n'; imageLoaded = true; };
		apiImg.onerror = () => { 
			debugInfo += 'API Image failed to load\n'; 
			imageError = 'Failed to load image';
		};
		apiImg.src = '/api/static/images/introduction/basketballBackground.png';

		// Test API routes with fetch to get detailed info
		fetch('/api/static/audio/introduction/intro_01.mp3')
			.then(response => { 
				debugInfo += `API Audio fetch: ${response.status}\n`; 
				debugInfo += `API Audio headers: ${JSON.stringify(Object.fromEntries(response.headers.entries()))}\n`;
				return response.headers.get('content-type'); 
			})
			.then(contentType => { debugInfo += `API Audio content-type: ${contentType}\n`; })
			.catch(error => { debugInfo += `API Audio fetch error: ${error}\n`; });

		fetch('/api/static/images/introduction/basketballBackground.png')
			.then(response => { 
				debugInfo += `API Image fetch: ${response.status}\n`; 
				debugInfo += `API Image headers: ${JSON.stringify(Object.fromEntries(response.headers.entries()))}\n`;
				return response.headers.get('content-type'); 
			})
			.then(contentType => { debugInfo += `API Image content-type: ${contentType}\n`; })
			.catch(error => { debugInfo += `API Image fetch error: ${error}\n`; });
	});
</script>

<div class="container mx-auto p-8">
	<h1 class="text-3xl font-bold mb-8">Asset Loading Test</h1>

	<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
		<div class="bg-white p-6 rounded-lg shadow-md">
			<h2 class="text-lg font-semibold">Audio Test</h2>
			<p>Status: {audioLoaded ? '✅ Loaded' : audioError ? '❌ ' + audioError : '⏳ Loading...'}</p>
			<audio controls src="/api/static/audio/introduction/intro_01.mp3" class="mt-2"></audio>
		</div>

		<div class="bg-white p-6 rounded-lg shadow-md">
			<h2 class="text-lg font-semibold">Image Test</h2>
			<p>Status: {imageLoaded ? '✅ Loaded' : imageError ? '❌ ' + imageError : '⏳ Loading...'}</p>
			<img src="/api/static/images/introduction/basketballBackground.png" alt="API Test image" class="mt-2 max-w-xs" />
		</div>
	</div>

	<div class="mt-8 bg-white p-6 rounded-lg shadow-md">
		<h2 class="text-lg font-semibold">Debug Info</h2>
		<pre class="bg-gray-100 p-4 rounded mt-2 text-sm overflow-auto max-h-96">{debugInfo}</pre>
	</div>
</div> 
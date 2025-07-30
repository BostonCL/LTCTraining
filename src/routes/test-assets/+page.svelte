<script lang="ts">
	import { onMount } from 'svelte';
	let audioLoaded = false;
	let imageLoaded = false;
	let audioError = '';
	let imageError = '';
	let debugInfo = '';

	onMount(() => {
		// Test direct static paths
		const audio = new Audio('/audio/introduction/intro_01.mp3');
		audio.onloadstart = () => { debugInfo += 'Audio loading started\n'; };
		audio.oncanplay = () => { debugInfo += 'Audio can play\n'; audioLoaded = true; };
		audio.onerror = (e) => { 
			debugInfo += `Audio error: ${e}\n`; 
			audioError = 'Failed to load audio';
			console.error('Audio error details:', e);
		};

		const img = new Image();
		img.onload = () => { debugInfo += 'Image loaded\n'; imageLoaded = true; };
		img.onerror = () => { 
			debugInfo += 'Image failed to load\n'; 
			imageError = 'Failed to load image';
		};
		img.src = '/images/introduction/basketballBackground.png';

		// Test with fetch to get detailed info
		fetch('/audio/introduction/intro_01.mp3')
			.then(response => { 
				debugInfo += `Audio fetch: ${response.status}\n`; 
				debugInfo += `Audio headers: ${JSON.stringify(Object.fromEntries(response.headers.entries()))}\n`;
				return response.headers.get('content-type'); 
			})
			.then(contentType => { debugInfo += `Audio content-type: ${contentType}\n`; })
			.catch(error => { debugInfo += `Audio fetch error: ${error}\n`; });

		fetch('/images/introduction/basketballBackground.png')
			.then(response => { 
				debugInfo += `Image fetch: ${response.status}\n`; 
				debugInfo += `Image headers: ${JSON.stringify(Object.fromEntries(response.headers.entries()))}\n`;
				return response.headers.get('content-type'); 
			})
			.then(contentType => { debugInfo += `Image content-type: ${contentType}\n`; })
			.catch(error => { debugInfo += `Image fetch error: ${error}\n`; });

		// Test API route as backup
		fetch('/api/assets/audio/introduction/intro_01.mp3')
			.then(response => { 
				debugInfo += `API Audio fetch: ${response.status}\n`; 
				debugInfo += `API Audio headers: ${JSON.stringify(Object.fromEntries(response.headers.entries()))}\n`;
				return response.headers.get('content-type'); 
			})
			.then(contentType => { debugInfo += `API Audio content-type: ${contentType}\n`; })
			.catch(error => { debugInfo += `API Audio fetch error: ${error}\n`; });

		fetch('/api/assets/images/introduction/basketballBackground.png')
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
			<h2 class="text-lg font-semibold">Audio Test (Direct)</h2>
			<p>Status: {audioLoaded ? '✅ Loaded' : audioError ? '❌ ' + audioError : '⏳ Loading...'}</p>
			<audio controls src="/audio/introduction/intro_01.mp3" class="mt-2"></audio>
		</div>

		<div class="bg-white p-6 rounded-lg shadow-md">
			<h2 class="text-lg font-semibold">Image Test (Direct)</h2>
			<p>Status: {imageLoaded ? '✅ Loaded' : imageError ? '❌ ' + imageError : '⏳ Loading...'}</p>
			<img src="/images/introduction/basketballBackground.png" alt="Test image" class="mt-2 max-w-xs" />
		</div>
	</div>

	<div class="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8">
		<div class="bg-white p-6 rounded-lg shadow-md">
			<h2 class="text-lg font-semibold">Audio Test (API Route)</h2>
			<audio controls src="/api/assets/audio/introduction/intro_01.mp3" class="mt-2"></audio>
		</div>

		<div class="bg-white p-6 rounded-lg shadow-md">
			<h2 class="text-lg font-semibold">Image Test (API Route)</h2>
			<img src="/api/assets/images/introduction/basketballBackground.png" alt="API Test image" class="mt-2 max-w-xs" />
		</div>
	</div>

	<div class="mt-8 bg-white p-6 rounded-lg shadow-md">
		<h2 class="text-lg font-semibold">Debug Info</h2>
		<pre class="bg-gray-100 p-4 rounded mt-2 text-sm overflow-auto max-h-96">{debugInfo}</pre>
	</div>

	<div class="mt-4 bg-white p-6 rounded-lg shadow-md">
		<h2 class="text-lg font-semibold">Direct Links (for testing)</h2>
		<ul class="list-disc pl-4 space-y-2">
			<li><a href="/audio/introduction/intro_01.mp3" target="_blank" class="text-blue-600 hover:underline">Direct Audio File</a></li>
			<li><a href="/images/introduction/basketballBackground.png" target="_blank" class="text-blue-600 hover:underline">Direct Image File</a></li>
			<li><a href="/api/assets/audio/introduction/intro_01.mp3" target="_blank" class="text-blue-600 hover:underline">API Audio File</a></li>
			<li><a href="/api/assets/images/introduction/basketballBackground.png" target="_blank" class="text-blue-600 hover:underline">API Image File</a></li>
		</ul>
	</div>
</div> 
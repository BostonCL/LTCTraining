<script lang="ts">
	import { onMount } from 'svelte';

	let apiImg: HTMLImageElement;
	let directImg: HTMLImageElement;
	let apiStatus = 'Testing...';
	let directStatus = 'Testing...';
	let apiSize = '';
	let directSize = '';

	onMount(async () => {
		// Test API route
		try {
			const response = await fetch('/api/assets/images/introduction/basketballBackground.png');
			if (response.ok) {
				const blob = await response.blob();
				apiSize = `${(blob.size / 1024 / 1024).toFixed(2)} MB`;
				apiStatus = `✅ API route working (${response.status})`;
			} else {
				apiStatus = `❌ API route failed (${response.status})`;
			}
		} catch (error) {
			apiStatus = `❌ API route error: ${error}`;
		}

		// Test direct static path
		try {
			const response = await fetch('/static/images/introduction/basketballBackground.png');
			if (response.ok) {
				const blob = await response.blob();
				directSize = `${(blob.size / 1024 / 1024).toFixed(2)} MB`;
				directStatus = `✅ Direct static path working (${response.status})`;
			} else {
				directStatus = `❌ Direct static path failed (${response.status})`;
			}
		} catch (error) {
			directStatus = `❌ Direct static path error: ${error}`;
		}
	});
</script>

<svelte:head>
	<title>Test Assets</title>
</svelte:head>

<div class="container mx-auto p-8">
	<h1 class="text-3xl font-bold mb-8">Static Asset Test</h1>

	<div class="mb-6 bg-green-100 p-4 rounded-lg">
		<h2 class="text-lg font-semibold mb-2">Performance Optimization</h2>
		<p class="text-sm">
			<strong>✅ Direct Static Serving:</strong> Files are now served directly from the static directory 
			for maximum performance. No more API route overhead!
		</p>
	</div>

	<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
		<!-- API Route Test -->
		<div class="bg-white p-6 rounded-lg shadow-lg">
			<h2 class="text-xl font-semibold mb-4">API Route Test (Slower)</h2>
			<p class="mb-4"><strong>Status:</strong> {apiStatus}</p>
			<p class="mb-4"><strong>File Size:</strong> {apiSize}</p>
			<img 
				bind:this={apiImg}
				src="/api/assets/images/introduction/basketballBackground.png" 
				alt="Basketball background test" 
				class="mt-2 max-w-xs border"
				on:error={() => apiStatus = '❌ Image failed to load'}
				on:load={() => apiStatus = '✅ Image loaded successfully'}
			/>
		</div>

		<!-- Direct Static Path Test -->
		<div class="bg-white p-6 rounded-lg shadow-lg">
			<h2 class="text-xl font-semibold mb-4">Direct Static Path Test (Faster)</h2>
			<p class="mb-4"><strong>Status:</strong> {directStatus}</p>
			<p class="mb-4"><strong>File Size:</strong> {directSize}</p>
			<img 
				bind:this={directImg}
				src="/static/images/introduction/basketballBackground.png" 
				alt="Basketball background test" 
				class="mt-2 max-w-xs border"
				on:error={() => directStatus = '❌ Image failed to load'}
				on:load={() => directStatus = '✅ Image loaded successfully'}
			/>
		</div>
	</div>

	<div class="mt-8 bg-gray-100 p-6 rounded-lg">
		<h3 class="text-lg font-semibold mb-4">Debug Information</h3>
		<ul class="space-y-2">
			<li><strong>Current URL:</strong> {typeof window !== 'undefined' ? window.location.href : 'Server-side'}</li>
			<li><strong>Environment:</strong> {typeof window !== 'undefined' ? 'Client' : 'Server'}</li>
			<li><a href="/api/assets/images/introduction/basketballBackground.png" target="_blank" class="text-blue-600 hover:underline">API Image File (Slower)</a></li>
			<li><a href="/static/images/introduction/basketballBackground.png" target="_blank" class="text-blue-600 hover:underline">Direct Static File (Faster)</a></li>
		</ul>
	</div>

	<div class="mt-8 bg-yellow-100 p-6 rounded-lg">
		<h3 class="text-lg font-semibold mb-4">Performance Comparison</h3>
		<ul class="space-y-2">
			<li>✅ Direct static paths should load much faster</li>
			<li>✅ No API route overhead</li>
			<li>✅ Better caching with CDN</li>
			<li>✅ Reduced server load</li>
		</ul>
	</div>

	<div class="mt-8 bg-blue-100 p-6 rounded-lg">
		<h3 class="text-lg font-semibold mb-4">What Changed</h3>
		<p class="text-sm">
			<strong>Performance Optimization:</strong> Removed API route rewrites and now serving static files directly. 
			This eliminates the server-side processing overhead and allows Vercel's CDN to cache files more effectively.
		</p>
	</div>
</div> 
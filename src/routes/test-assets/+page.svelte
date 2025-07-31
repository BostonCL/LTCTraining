<script lang="ts">
	import { onMount } from 'svelte';

	let apiImg: HTMLImageElement;
	let directImg: HTMLImageElement;
	let apiStatus = 'Testing...';
	let directStatus = 'Testing...';
	let apiSize = '';
	let directSize = '';

	onMount(async () => {
		// Test API route (via rewrite)
		try {
			const response = await fetch('/images/introduction/basketballBackground.png');
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

		// Test direct API path
		try {
			const response = await fetch('/api/assets/images/introduction/basketballBackground.png');
			if (response.ok) {
				const blob = await response.blob();
				directSize = `${(blob.size / 1024 / 1024).toFixed(2)} MB`;
				directStatus = `✅ Direct API path working (${response.status})`;
			} else {
				directStatus = `❌ Direct API path failed (${response.status})`;
			}
		} catch (error) {
			directStatus = `❌ Direct API path error: ${error}`;
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
			<strong>✅ Optimized API Routes:</strong> Enhanced caching, compression, and reduced logging 
			for better performance while maintaining compatibility.
		</p>
	</div>

	<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
		<!-- Rewrite Path Test -->
		<div class="bg-white p-6 rounded-lg shadow-lg">
			<h2 class="text-xl font-semibold mb-4">Rewrite Path Test (/images/)</h2>
			<p class="mb-4"><strong>Status:</strong> {apiStatus}</p>
			<p class="mb-4"><strong>File Size:</strong> {apiSize}</p>
			<img 
				bind:this={apiImg}
				src="/images/introduction/basketballBackground.png" 
				alt="Basketball background test" 
				class="mt-2 max-w-xs border"
				on:error={() => apiStatus = '❌ Image failed to load'}
				on:load={() => apiStatus = '✅ Image loaded successfully'}
			/>
		</div>

		<!-- Direct API Path Test -->
		<div class="bg-white p-6 rounded-lg shadow-lg">
			<h2 class="text-xl font-semibold mb-4">Direct API Path Test</h2>
			<p class="mb-4"><strong>Status:</strong> {directStatus}</p>
			<p class="mb-4"><strong>File Size:</strong> {directSize}</p>
			<img 
				bind:this={directImg}
				src="/api/assets/images/introduction/basketballBackground.png" 
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
			<li><a href="/images/introduction/basketballBackground.png" target="_blank" class="text-blue-600 hover:underline">Rewrite Path (Recommended)</a></li>
			<li><a href="/api/assets/images/introduction/basketballBackground.png" target="_blank" class="text-blue-600 hover:underline">Direct API Path</a></li>
		</ul>
	</div>

	<div class="mt-8 bg-yellow-100 p-6 rounded-lg">
		<h3 class="text-lg font-semibold mb-4">Performance Improvements</h3>
		<ul class="space-y-2">
			<li>✅ Enhanced caching headers for better browser caching</li>
			<li>✅ Added ETag support for conditional requests</li>
			<li>✅ Accept-Ranges header for partial content requests</li>
			<li>✅ Reduced logging overhead for faster response times</li>
		</ul>
	</div>

	<div class="mt-8 bg-blue-100 p-6 rounded-lg">
		<h3 class="text-lg font-semibold mb-4">What Changed</h3>
		<p class="text-sm">
			<strong>Performance Optimization:</strong> Kept the working rewrite system but optimized the API route 
			with better caching, compression headers, and reduced processing overhead for faster loading times.
		</p>
	</div>
</div> 
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

		// Test direct path
		try {
			const response = await fetch('/images/introduction/basketballBackground.png');
			if (response.ok) {
				const blob = await response.blob();
				directSize = `${(blob.size / 1024 / 1024).toFixed(2)} MB`;
				directStatus = `✅ Direct path working (${response.status})`;
			} else {
				directStatus = `❌ Direct path failed (${response.status})`;
			}
		} catch (error) {
			directStatus = `❌ Direct path error: ${error}`;
		}
	});
</script>

<svelte:head>
	<title>Test Assets</title>
</svelte:head>

<div class="container mx-auto p-8">
	<h1 class="text-3xl font-bold mb-8">Static Asset Test</h1>

	<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
		<!-- API Route Test -->
		<div class="bg-white p-6 rounded-lg shadow-lg">
			<h2 class="text-xl font-semibold mb-4">API Route Test</h2>
			<p class="mb-4"><strong>Status:</strong> {apiStatus}</p>
			<p class="mb-4"><strong>File Size:</strong> {apiSize}</p>
			<img 
				bind:this={apiImg}
				src="/api/assets/images/introduction/basketballBackground.png" 
				alt="Basketball background test" 
				class="mt-2 max-w-xs"
				on:error={() => apiStatus = '❌ Image failed to load'}
				on:load={() => apiStatus = '✅ Image loaded successfully'}
			/>
		</div>

		<!-- Direct Path Test -->
		<div class="bg-white p-6 rounded-lg shadow-lg">
			<h2 class="text-xl font-semibold mb-4">Direct Path Test</h2>
			<p class="mb-4"><strong>Status:</strong> {directStatus}</p>
			<p class="mb-4"><strong>File Size:</strong> {directSize}</p>
			<img 
				bind:this={directImg}
				src="/images/introduction/basketballBackground.png" 
				alt="Basketball background test" 
				class="mt-2 max-w-xs"
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
			<li><a href="/api/assets/images/introduction/basketballBackground.png" target="_blank" class="text-blue-600 hover:underline">API Image File</a></li>
			<li><a href="/images/introduction/basketballBackground.png" target="_blank" class="text-blue-600 hover:underline">Direct Image File</a></li>
		</ul>
	</div>

	<div class="mt-8 bg-yellow-100 p-6 rounded-lg">
		<h3 class="text-lg font-semibold mb-4">Expected Results</h3>
		<ul class="space-y-2">
			<li>✅ Both API route and direct path should work</li>
			<li>✅ File size should be around 2.1 MB</li>
			<li>✅ Images should display correctly</li>
			<li>✅ Content-Type should be image/png</li>
		</ul>
	</div>
</div> 
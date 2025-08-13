<script lang="ts">
  import CuteCartoonAvatar from '$lib/components/CuteCartoonAvatar.svelte';
  import { avatarOptions } from '$lib/config/avatarOptions';

  // Test script
  const testScript = [
    {
      text: "Hello! This is a test of the enhanced 3D avatar. I'm talking to demonstrate the improved animations.",
      audio: "/audio/introduction/intro_01.mp3"
    },
    {
      text: "The avatar should now have much better facial animations and lip-sync capabilities.",
      audio: "/audio/introduction/intro_02.mp3"
    }
  ];

  let currentIdx = 0;
  let selectedAvatar = avatarOptions[0]; // Professional Host

  function onComplete() {
    console.log('Avatar test completed');
  }
</script>

<div class="min-h-screen bg-gray-100 p-8">
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Enhanced Avatar Test</h1>
    
    <div class="bg-white rounded-lg shadow-lg p-6 mb-8">
      <h2 class="text-xl font-semibold mb-4">Cute Cartoon Avatar</h2>
      <div class="p-4 border border-blue-200 rounded-lg bg-blue-50">
        <h3 class="font-semibold text-gray-900">Cute Cartoon Character</h3>
        <p class="text-sm text-gray-600 mt-1">A friendly cartoon character with realistic talking animations and cute facial expressions.</p>
        <div class="flex flex-wrap gap-1 mt-2">
          <span class="px-2 py-1 bg-blue-100 text-xs rounded-full text-blue-600">Talking Animation</span>
          <span class="px-2 py-1 bg-blue-100 text-xs rounded-full text-blue-600">Eye Blinking</span>
          <span class="px-2 py-1 bg-blue-100 text-xs rounded-full text-blue-600">Head Movement</span>
          <span class="px-2 py-1 bg-blue-100 text-xs rounded-full text-blue-600">Cute Design</span>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-lg p-6">
      <h2 class="text-xl font-semibold mb-4">Avatar Preview</h2>
      <div class="relative h-96 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg overflow-hidden">
        <!-- Test area for avatar -->
        <div class="absolute inset-0 flex items-center justify-center">
          <CuteCartoonAvatar 
            scripts={testScript}
            {currentIdx}
            {onComplete}
            showAvatar={true}
          />
        </div>
        
        <!-- Controls -->
        <div class="absolute bottom-4 left-4 right-4">
          <div class="flex gap-2">
            <button 
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
              on:click={() => currentIdx = 0}
            >
              Reset
            </button>
            <button 
              class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
              on:click={() => currentIdx = currentIdx === 0 ? 1 : 0}
            >
              Toggle Script
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-8 bg-white rounded-lg shadow-lg p-6">
      <h2 class="text-xl font-semibold mb-4">Current Script</h2>
      <div class="space-y-4">
        {#each testScript as script, index}
          <div class="p-4 border rounded-lg {currentIdx === index ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}">
            <div class="flex items-center gap-2 mb-2">
              <span class="text-sm font-medium text-gray-500">Script {index + 1}</span>
              {#if currentIdx === index}
                <span class="px-2 py-1 bg-blue-500 text-white text-xs rounded-full">Playing</span>
              {/if}
            </div>
            <p class="text-gray-700">{script.text}</p>
          </div>
        {/each}
      </div>
    </div>
  </div>
</div>

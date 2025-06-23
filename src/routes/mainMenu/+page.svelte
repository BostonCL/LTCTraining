<script lang="ts">
  import { onMount } from 'svelte';
  import { getAuth, signOut, type Auth } from 'firebase/auth';
  import { writable } from 'svelte/store';
  // Placeholder modules
  const modules = [
    {
      title: 'What is live coverage?',
      content: `<div class="space-y-6">
        <div>
          <span class='inline-block bg-blue-100 text-blue-800 font-semibold px-3 py-1 rounded-full mb-2'>Ball Speaks</span>
          <p class='text-gray-800'>"Covering live traffic means you will be monitoring commercial inventory while ensuring airing criteria and guidelines are met. In short, watching different sporting events and making sure the commercials air properly."</p>
        </div>
        <div>
          <span class='inline-block bg-gray-200 text-gray-700 font-semibold px-3 py-1 rounded-full mb-2'>Voice Over</span>
          <p class='text-gray-700'>White board:</p>
          <ul class='list-disc ml-6 text-gray-700'>
            <li>Managing and airing all inventory (commercials) during live games. <span class='italic text-blue-700'>[White board text: airing commercials]</span></li>
            <li>Communicating with the network (through the phone and email) with the producers and Master control. (MC = Master control, the people that send the commercial to air, we communicate with them the most) <span class='italic text-blue-700'>[White board text: Communicating through the phone and email]</span></li>
            <li>Writing down airing times <span class='italic text-blue-700'>[White board text: Writing down airing times]</span></li>
          </ul>
        </div>
        <div>
          <span class='inline-block bg-blue-100 text-blue-800 font-semibold px-3 py-1 rounded-full mb-2'>Ball Speaks</span>
          <ul class='list-disc ml-6 text-gray-800'>
            <li>Proper management of inventory is crucial for the financial success of CBS Sports Network.</li>
            <li>Network operates on a 24-hour clock from 6 AM to 6 AM so our goal is to time out the commercials and organize them in that 24-hour period!</li>
            <li>The role may appear intimidating at first but don't worry it will become comprehensible after this training course.</li>
            <li>Keep in mind there will be practice questions throughout the course and there will be a test you must get 70% or higher on.</li>
            <li>Participants must take notes and prepare questions for a follow-up Zoom call.</li>
          </ul>
          <p class='mt-2 text-sm text-gray-500 italic'>This will be presented as an AI voiceover with a basketball avatar.</p>
        </div>
      </div>`
    },
    {
      title: 'Module 1: Live Coverage Sheet',
      content: `<div class="space-y-6">
        <p class="text-gray-800">This is what a live coverage sheet looks like.</p>
        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4 text-center text-gray-500 italic mb-4">
          [Insert image or example of a live coverage sheet here]
        </div>
        <p class="text-gray-800">I know it looks intimidating now but we are going to dive into the details together.</p>
        <p class="text-gray-800">This sheet is separated by columns that we will break down in the following content.</p>
        <p class="text-blue-700 font-semibold">Take a moment and pause the video here so that you can take it all in.</p>
      </div>`
    },
    {
      title: 'Module 2: Tools & Technology',
      content: 'Learn about the tools and technology used in live traffic reporting.'
    },
    {
      title: 'Module 3: Best Practices',
      content: 'Discover best practices for effective and accurate coverage.'
    }
  ];

  let auth: Auth | undefined;
  onMount(() => {
    auth = getAuth();
  });

  async function handleLogout() {
    try {
      if (auth) {
        await signOut(auth);
      }
      window.location.href = '/';
    } catch (e) {
      alert('Logout failed. Please try again.');
    }
  }

  // Sidebar state
  let sidebarOpen = true;
  const currentModule = writable(0);

  function goToModule(idx: number) {
    currentModule.set(idx);
  }
  function nextModule(idx: number) {
    if (idx < modules.length - 1) currentModule.set(idx + 1);
  }
  function prevModule(idx: number) {
    if (idx > 0) currentModule.set(idx - 1);
  }
</script>

<!-- Progress Bar -->
<div class="w-full bg-gray-200 h-2">
  <div class="bg-blue-600 h-2 transition-all" style="width: {($currentModule + 1) / modules.length * 100}%"></div>
</div>

<!-- Header -->
<header class="w-full flex items-center justify-between py-4 px-8 bg-white shadow-sm border-b">
  <span class="text-2xl font-bold text-gray-900 tracking-tight">Live Traffic Coverage Training</span>
  <button on:click={handleLogout} class="text-gray-500 hover:text-gray-700 text-base font-medium rounded px-4 py-2 border border-gray-200 bg-gray-50">Logout</button>
</header>

<div class="flex min-h-[80vh] relative">
  <!-- Sidebar Table of Contents -->
  {#if sidebarOpen}
    <aside class="bg-white border-r w-64 transition-all duration-200 ease-in-out z-20">
      <div class="flex items-center justify-between px-4 py-3 border-b">
        <span class="font-semibold text-gray-700">Table of Contents</span>
        <button on:click={() => (sidebarOpen = false)} class="text-gray-400 hover:text-gray-700 text-lg font-bold">×</button>
      </div>
      <nav class="flex flex-col divide-y divide-gray-100">
        {#each modules as module, idx}
          <button
            class="text-left px-4 py-3 hover:bg-blue-50 focus:bg-blue-100 transition font-medium text-gray-700 flex items-center gap-2 {($currentModule === idx) ? 'bg-blue-100 text-blue-700' : ''}"
            on:click={() => goToModule(idx)}
          >
            <span class="w-2 h-2 rounded-full {($currentModule === idx) ? 'bg-blue-600' : 'bg-gray-300'}"></span>
            {module.title}
          </button>
        {/each}
      </nav>
    </aside>
  {:else}
    <!-- Floating menu button -->
    <button on:click={() => (sidebarOpen = true)} class="fixed top-24 left-4 z-30 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg p-3 focus:outline-none">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
  {/if}

  <!-- Main Content -->
  <main class="flex-1 flex flex-col items-center justify-center p-8">
    {#each modules as module, idx}
      {#if $currentModule === idx}
        <div class="w-full max-w-2xl mx-auto">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">{module.title}</h2>
          <div class="text-gray-700 text-lg mb-8">{@html module.content}</div>
          <div class="flex justify-between mt-8">
            <button
              class="px-5 py-2 rounded bg-gray-200 text-gray-700 font-medium hover:bg-gray-300 disabled:opacity-50"
              on:click={() => prevModule(idx)}
              disabled={idx === 0}
            >
              Back
            </button>
            <button
              class="px-5 py-2 rounded bg-blue-600 text-white font-medium hover:bg-blue-700 disabled:opacity-50"
              on:click={() => nextModule(idx)}
              disabled={idx === modules.length - 1}
            >
              Next
            </button>
          </div>
        </div>
      {/if}
    {/each}
  </main>
</div> 
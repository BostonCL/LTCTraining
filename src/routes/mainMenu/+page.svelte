<script lang="ts">
  import { onMount } from 'svelte';
  import { getAuth, signOut, type Auth } from 'firebase/auth';
  import { writable, derived } from 'svelte/store';
  // Modules with submodules for Module 1
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
      submodules: [
        {
          title: 'Real Time',
          content: `Real Time is the scheduled start time for a show or game. For example, if a game is scheduled to begin at 8AM, you write down 8:00:00 next to Real Time, regardless of when it actually begins.`
        },
        {
          title: 'Start Time',
          content: `Start Time is when the event actually begins. For example, if the game is delayed and starts at 8:03:30 AM, you write that down next to Start Time.`
        },
        {
          title: 'Hit Time',
          content: `Hit Time is a mock schedule used for planning. These aren't the real times commercials air, just estimated placeholders.`
        },
        {
          title: 'Event Type',
          content: `Event Type tells you what kind of content it is (like a commercial, promo, local ad, or DR). You can also find this info elsewhere if needed.`
        },
        {
          title: 'Length',
          content: `Length is how long the commercial actually is. How long is each break?`
        },
        {
          title: 'Title',
          content: `Title gives details about the specific commercial.`
        },
        {
          title: 'Advertiser',
          content: `Advertiser is who the ad is from.`
        },
        {
          title: 'House Number',
          content: `House Number is a unique ID for the commercial. This is how Master Control identifies which ad you're talking about. Since one advertiser (like Geico) can have several different ads, the house number is key for clarity.`
        },
        {
          title: 'Ordered As',
          content: `Ordered As shows or games the commercial was sold to air with.`
        },
        {
          title: 'Spot End Time',
          content: `Spot End Time is the latest time that specific ad can air.`
        }
      ],
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

  // Sidebar and navigation state
  let sidebarOpen = true;
  const mainIdx = writable(0); // index in modules
  const subIdx = writable(0); // index in submodules (if any)
  let submodulesOpen = true; // controls collapse/expand of Module 1 submodules

  // Derived store for current module/submodule
  const current = derived([mainIdx, subIdx], ([$mainIdx, $subIdx]) => {
    const mod = modules[$mainIdx];
    if (mod.submodules) {
      return { ...mod.submodules[$subIdx], isSub: true, main: mod, mainIdx: $mainIdx, subIdx: $subIdx, subCount: mod.submodules.length };
    }
    return { ...mod, isSub: false, mainIdx: $mainIdx };
  });

  function goToModule(idx: number) {
    mainIdx.set(idx);
    subIdx.set(0);
  }
  function goToSubModule(idx: number) {
    subIdx.set(idx);
  }
  function next() {
    let $mainIdx: number = 0, $subIdx: number = 0;
    mainIdx.subscribe(v => $mainIdx = v)();
    subIdx.subscribe(v => $subIdx = v)();
    const mod = modules[$mainIdx];
    if (mod.submodules && $subIdx < mod.submodules.length - 1) {
      subIdx.set($subIdx + 1);
    } else if ($mainIdx < modules.length - 1) {
      mainIdx.set($mainIdx + 1);
      subIdx.set(0);
    }
  }
  function prev() {
    let $mainIdx: number = 0, $subIdx: number = 0;
    mainIdx.subscribe(v => $mainIdx = v)();
    subIdx.subscribe(v => $subIdx = v)();
    const mod = modules[$mainIdx];
    if (mod.submodules && $subIdx > 0) {
      subIdx.set($subIdx - 1);
    } else if ($mainIdx > 0) {
      mainIdx.set($mainIdx - 1);
      const prevMod = modules[$mainIdx - 1];
      subIdx.set(prevMod.submodules ? prevMod.submodules.length - 1 : 0);
    }
  }
</script>

<!-- Progress Bar -->
<div class="w-full bg-gray-200 h-2">
  <div class="bg-blue-600 h-2 transition-all" style="width: {($mainIdx + 1) / modules.length * 100}%"></div>
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
        {#each modules as mod, idx}
          <div>
            <button
              class="text-left px-4 py-3 hover:bg-blue-50 focus:bg-blue-100 transition font-medium text-gray-700 flex items-center gap-2 w-full {($mainIdx === idx) ? 'bg-blue-100 text-blue-700' : ''}"
              on:click={() => goToModule(idx)}
              style="position: relative;"
            >
              <span class="w-2 h-2 rounded-full {($mainIdx === idx) ? 'bg-blue-600' : 'bg-gray-300'}"></span>
              {mod.title}
              {#if mod.submodules}
                <span class="ml-auto flex items-center justify-center w-7 h-7 rounded-full transition bg-gray-100 hover:bg-blue-200">
                  <button type="button" class="w-full h-full flex items-center justify-center text-lg text-blue-700 focus:outline-none" on:click|stopPropagation={() => submodulesOpen = !submodulesOpen} aria-label="Toggle submodules">
                    <svg class="w-5 h-5 transition-transform duration-200" style="transform: rotate({submodulesOpen && $mainIdx === idx ? 90 : 0}deg);" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
                  </button>
                </span>
              {/if}
            </button>
            {#if mod.submodules && $mainIdx === idx && submodulesOpen}
              <div class="ml-6 flex flex-col bg-blue-50/50 rounded-b-lg pb-2 pt-1">
                {#each mod.submodules as sub, sidx}
                  <button
                    class="text-left px-3 py-2 text-sm hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 rounded {($subIdx === sidx) ? 'bg-blue-200 text-blue-800 font-semibold' : ''}"
                    on:click={() => goToSubModule(sidx)}
                  >
                    <span class="w-2 h-2 rounded-full {($subIdx === sidx) ? 'bg-blue-600' : 'bg-gray-300'}"></span>
                    {sub.title}
                  </button>
                {/each}
              </div>
            {/if}
          </div>
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
    {#if $current.isSub}
      <div class="w-full max-w-2xl mx-auto">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">{$current.title}</h2>
        <div class="text-gray-700 text-lg mb-8">{$current.content}</div>
        <div class="flex justify-between mt-8">
          <button
            class="px-5 py-2 rounded bg-gray-200 text-gray-700 font-medium hover:bg-gray-300 disabled:opacity-50"
            on:click={prev}
            disabled={$mainIdx === 0 && $subIdx === 0}
          >
            Back
          </button>
          <button
            class="px-5 py-2 rounded bg-blue-600 text-white font-medium hover:bg-blue-700 disabled:opacity-50"
            on:click={next}
            disabled={($mainIdx === modules.length - 1) && (!$current.isSub || ('subIdx' in $current && 'subCount' in $current && $current.subIdx === $current.subCount - 1))}
          >
            Next
          </button>
        </div>
      </div>
    {:else}
      <div class="w-full max-w-2xl mx-auto">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">{$current.title}</h2>
        <div class="text-gray-700 text-lg mb-8">{@html $current.content}</div>
        <div class="flex justify-between mt-8">
          <button
            class="px-5 py-2 rounded bg-gray-200 text-gray-700 font-medium hover:bg-gray-300 disabled:opacity-50"
            on:click={prev}
            disabled={$mainIdx === 0}
          >
            Back
          </button>
          <button
            class="px-5 py-2 rounded bg-blue-600 text-white font-medium hover:bg-blue-700 disabled:opacity-50"
            on:click={next}
            disabled={$mainIdx === modules.length - 1 && !$current.isSub}
          >
            Next
          </button>
        </div>
      </div>
    {/if}
  </main>
</div> 
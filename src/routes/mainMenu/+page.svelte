<script lang="ts">
  import { onMount } from 'svelte';
  import { getAuth, signOut, type Auth } from 'firebase/auth';
  import { writable, derived } from 'svelte/store';
  import Introduction from './introduction/Introduction.svelte';
  import Module1Intro from './module-1/Module1Intro.svelte';
  import HitTime from './module-1/HitTime.svelte';
  import EventType from './module-1/EventType.svelte';
  import Length from './module-1/Length.svelte';
  import Title from './module-1/Title.svelte';
  import Advertiser from './module-1/Advertiser.svelte';
  import HouseNumber from './module-1/HouseNumber.svelte';
  import OrderedAs from './module-1/OrderedAs.svelte';
  import SpotEndTime from './module-1/SpotEndTime.svelte';
  import StartTimeRealTime from './module-1/StartTimeRealTime.svelte';
  import StartTimeRealTimeQuiz from './module-1/StartTimeRealTimeQuiz.svelte';
  import ProgramLine from './module-1/ProgramLine.svelte';
  import LengthQuiz from './module-1/LengthQuiz.svelte';
  import HouseNumberQuiz from './module-1/HouseNumberQuiz.svelte';
  import Module3 from './Module3.svelte';
  // Modules with submodules for Module 1
  const modules = [
    {
      title: 'Module 1: Live Coverage Sheet',
      submodules: [
        {
          title: 'Start Time & Real Time',
          content: `Start Time & Real Time are two key timing fields. Real Time is the scheduled start time for a show or game (what was planned), while Start Time is when the event actually begins (what actually happened). For example, if a game is scheduled for 8AM but starts at 8:03:30 AM due to a delay, you write 8:00:00 in Real Time and 8:03:30 in Start Time.`
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
      title: 'Module 3: Marking down commercial times and Moving Units',
      content: `<div class="space-y-6">
        <h2 class="text-xl font-bold text-gray-800">Before we begin this module, here are a few rules when moving units that you need to understand:</h2>
        <ul class="list-disc pl-6 text-gray-700">
          <li>Rule 1: [Add your rule here]</li>
          <li>Rule 2: [Add your rule here]</li>
          <li>Rule 3: [Add your rule here]</li>
        </ul>
        <p class="text-blue-700 font-semibold">Let’s get started with Module 3!</p>
      </div>`
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
  let mainSection = 'introduction'; // 'introduction', 'module1', 'module1sub', 'quiz', or 'other'
  let module1SubIdx = 0;
  let submodulesOpen = true;
  
  // Track completion of submodules
  let completedSubmodules = new Set<number>();
  
  // Mark submodule as completed
  function markSubmoduleCompleted(idx: number) {
    console.log('Marking submodule as completed:', idx);
    completedSubmodules.add(idx);
    console.log('Completed submodules:', Array.from(completedSubmodules));
    // Force reactivity update
    completedSubmodules = completedSubmodules;
  }
  

  
  // Check if Start Time & Real Time is completed (index 1)
  $: startTimeRealTimeCompleted = completedSubmodules.has(1);
  // Check if Length is completed (index 4)
  $: lengthCompleted = completedSubmodules.has(4);
  // Check if House Number is completed (index 7)
  $: houseNumberCompleted = completedSubmodules.has(7);
  
  // Check if any submodule is completed
  $: isSubmoduleCompleted = (idx: number) => completedSubmodules.has(idx);
  
  // Check if Module 1 is fully completed (all 10 submodules)
  $: module1Completed = completedSubmodules.size === 10;

  // Define the content map for easier rendering
  const module1Submodules = [
    { title: 'Program Line', component: ProgramLine },
    { title: 'Start Time & Real Time', component: StartTimeRealTime },
    { title: 'Hit Time', component: HitTime },
    { title: 'Event Type', component: EventType },
    { title: 'Length', component: Length },
    { title: 'Title', component: Title },
    { title: 'Advertiser', component: Advertiser },
    { title: 'House Number', component: HouseNumber },
    { title: 'Ordered As', component: OrderedAs },
    { title: 'Spot End Time', component: SpotEndTime }
  ];

  function goToIntroduction() {
    mainSection = 'introduction';
  }
  function goToModule1Intro() {
    mainSection = 'module1';
  }
  function goToModule1Sub(idx: number) {
    mainSection = 'module1sub';
    module1SubIdx = idx;
  }
  function goToQuiz() {
    mainSection = 'quiz';
  }
  
  function goToNextSubmodule() {
    // Navigate to the next submodule after quiz completion
    goToModule1Sub(2); // Hit Time is index 2
  }
  function next() {
    if (mainSection === 'introduction') {
      goToModule1Intro();
    } else if (mainSection === 'module1') {
      goToModule1Sub(0);
    } else if (mainSection === 'module1sub') {
      if (module1SubIdx < module1Submodules.length - 1) {
        goToModule1Sub(module1SubIdx + 1);
      } else {
        // TODO: go to next module
      }
    } else if (mainSection === 'quiz') {
      // After quiz, go back to main menu or next module
      goToModule1Intro();
    }
  }
  function prev() {
    if (mainSection === 'quiz') {
      goToModule1Sub(0); // Go back to first submodule
    } else if (mainSection === 'module1sub') {
      if (module1SubIdx > 0) {
        goToModule1Sub(module1SubIdx - 1);
      } else {
        goToModule1Intro();
      }
    } else if (mainSection === 'module1') {
      goToIntroduction();
    }
  }
</script>

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
        <button on:click={goToIntroduction} class="text-left px-4 py-3 hover:bg-blue-50 focus:bg-blue-100 transition font-medium text-gray-700 flex items-center gap-2 w-full {mainSection === 'introduction' ? 'bg-blue-100 text-blue-700' : ''}">
          <span class="w-2 h-2 rounded-full {mainSection === 'introduction' ? 'bg-blue-600' : 'bg-gray-300'}"></span>
          Introduction
        </button>
        <div class="flex items-center">
          <button on:click={goToModule1Intro} class="flex-1 text-left px-4 py-3 hover:bg-blue-50 focus:bg-blue-100 transition font-medium text-gray-700 flex items-center gap-2 {mainSection === 'module1' ? 'bg-blue-100 text-blue-700' : ''}">
            <span class="w-2 h-2 rounded-full {mainSection === 'module1' ? 'bg-blue-600' : 'bg-gray-300'}"></span>
            Module 1: Live Coverage Sheet
            {#if module1Completed}
              <svg class="w-4 h-4 text-green-600 ml-auto" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            {/if}
          </button>
          <button
            type="button"
            class="ml-2 flex items-center justify-center w-7 h-7 rounded-full transition bg-gray-100 hover:bg-blue-200"
            on:click={() => submodulesOpen = !submodulesOpen}
            aria-label="Toggle submodules"
          >
            <svg class="w-5 h-5 transition-transform duration-200" style="transform: rotate({submodulesOpen ? 90 : 0}deg);" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
          </button>
        </div>
        {#if submodulesOpen}
          <div class="ml-6 flex flex-col bg-blue-50/50 rounded-b-lg pb-2 pt-1">
            {#each module1Submodules as sub, idx (sub.title)}
              <button on:click={() => goToModule1Sub(idx)} class="text-left px-3 py-2 text-sm hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 rounded {mainSection === 'module1sub' && module1SubIdx === idx ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">
                <span class="w-2 h-2 rounded-full {mainSection === 'module1sub' && module1SubIdx === idx ? 'bg-blue-600' : 'bg-gray-300'}"></span>
                {sub.title}
                {#if completedSubmodules.has(idx)}
                  <svg class="w-4 h-4 text-green-600 ml-auto" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                {/if}
              </button>
              <!-- Show quiz link under Start Time & Real Time -->
              {#if sub.title === 'Start Time & Real Time'}
                <button 
                  on:click={goToQuiz} 
                  class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded ml-4 {mainSection === 'quiz' ? 'bg-green-200 text-green-800 font-semibold' : startTimeRealTimeCompleted ? 'hover:bg-green-100 focus:bg-green-200 text-green-700' : 'text-gray-400 cursor-not-allowed'}"
                  disabled={!startTimeRealTimeCompleted}
                >
                  <span class="w-2 h-2 rounded-full {mainSection === 'quiz' ? 'bg-green-600' : startTimeRealTimeCompleted ? 'bg-green-300' : 'bg-gray-300'}"></span>
                  📝 Quiz {startTimeRealTimeCompleted ? '' : '(Complete module first)'}
                </button>
              {/if}
              <!-- Show quiz link under Length -->
              {#if sub.title === 'Length'}
                <button 
                  on:click={() => { mainSection = 'lengthQuiz'; }} 
                  class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded ml-4 {mainSection === 'lengthQuiz' ? 'bg-green-200 text-green-800 font-semibold' : lengthCompleted ? 'hover:bg-green-100 focus:bg-green-200 text-green-700' : 'text-gray-400 cursor-not-allowed'}"
                  disabled={!lengthCompleted}
                >
                  <span class="w-2 h-2 rounded-full {mainSection === 'lengthQuiz' ? 'bg-green-600' : lengthCompleted ? 'bg-green-300' : 'bg-gray-300'}"></span>
                  📝 Quiz {lengthCompleted ? '' : '(Complete module first)'}
                </button>
              {/if}
              <!-- Show quiz link under House Number -->
              {#if sub.title === 'House Number'}
                <button 
                  on:click={() => { mainSection = 'houseNumberQuiz'; }} 
                  class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded ml-4 {mainSection === 'houseNumberQuiz' ? 'bg-green-200 text-green-800 font-semibold' : houseNumberCompleted ? 'hover:bg-green-100 focus:bg-green-200 text-green-700' : 'text-gray-400 cursor-not-allowed'}"
                  disabled={!houseNumberCompleted}
                >
                  <span class="w-2 h-2 rounded-full {mainSection === 'houseNumberQuiz' ? 'bg-green-600' : houseNumberCompleted ? 'bg-green-300' : 'bg-gray-300'}"></span>
                  📝 Quiz {houseNumberCompleted ? '' : '(Complete module first)'}
                </button>
              {/if}
            {/each}
          </div>
        {/if}
        {#each modules.slice(1) as module, modIdx}
          <button on:click={() => { mainSection = `module${modIdx+2}`; }} class="text-left px-4 py-3 hover:bg-blue-50 focus:bg-blue-100 transition font-medium text-gray-700 flex items-center gap-2 w-full {mainSection === `module${modIdx+2}` ? 'bg-blue-100 text-blue-700' : ''}">
            <span class="w-2 h-2 rounded-full {mainSection === `module${modIdx+2}` ? 'bg-blue-600' : 'bg-gray-300'}"></span>
            {module.title}
          </button>
        {/each}
      </nav>
    </aside>
  {:else}
    <!-- Floating menu button -->
    <button on:click={() => (sidebarOpen = true)} class="fixed top-24 left-4 z-30 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg p-3 focus:outline-none" aria-label="Open sidebar menu">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
  {/if}

  <!-- Main Content -->
  <main class="flex-1 flex flex-col items-center justify-center p-8">
    {#if mainSection === 'introduction'}
      <Introduction />
    {:else if mainSection === 'module1'}
      <Module1Intro on:navigateToNextSubmodule={() => goToModule1Sub(0)} />
    {:else if mainSection === 'module1sub'}
      {#if module1Submodules[module1SubIdx]}
        <svelte:component 
          this={module1Submodules[module1SubIdx].component} 
          isCompleted={completedSubmodules.has(module1SubIdx)}
          on:navigateToQuiz={goToQuiz}
          on:moduleCompleted={(event) => {
            console.log('Received moduleCompleted event:', event.detail);
            markSubmoduleCompleted(event.detail.submoduleIndex);
          }}
          on:navigateToNextSubmodule={() => {
            markSubmoduleCompleted(module1SubIdx);
            if (module1SubIdx < module1Submodules.length - 1) {
              goToModule1Sub(module1SubIdx + 1);
            }
          }}
        />
      {/if}
    {:else if mainSection === 'quiz'}
      <StartTimeRealTimeQuiz on:navigateToNextSubmodule={goToNextSubmodule} />
    {:else if mainSection === 'lengthQuiz'}
      <LengthQuiz on:navigateToNextSubmodule={() => goToModule1Sub(5)} />
    {:else if mainSection === 'houseNumberQuiz'}
      <HouseNumberQuiz on:navigateToNextSubmodule={() => goToModule1Sub(8)} />
    {:else if mainSection === 'module3'}
      <Module3 />
    {/if}

  </main>
</div> 
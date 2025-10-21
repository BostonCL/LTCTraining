<script lang="ts">
  import { onMount } from 'svelte';
  import { signOut, type Auth } from 'firebase/auth';
  import { auth } from '$lib/firebase';
  import { writable, derived } from 'svelte/store';
  import { DEV_FEATURES } from '$lib/config/dev';
  import Introduction from './introduction/Introduction.svelte';
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
  import { getR2Url } from '$lib/config/r2';
  import HouseNumberQuiz from './module-1/HouseNumberQuiz.svelte';
  import EndTime from './module-1/EndTime.svelte';
  import Floaters from './module-1/Floaters.svelte';
  import KeyTab from './module-1/KeyTab.svelte';
  import Module3 from './Module3.svelte';
  import QuizTemplate from '$lib/components/QuizTemplate.svelte';
  import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
  import { audioStore, setCurrentIndex } from '$lib/stores/audioStore';
  import { progressStore } from '$lib/stores/progressStore';
  import Module1Intro from './module-1/+page.svelte';
  import SellingTitle from './module-2/SellingTitle.svelte';
  import TheYellowUnit from './module-2/TheYellowUnit.svelte';
  import UnitPrioritizationDetails from './module-2/UnitPrioritizationDetails.svelte';
  import GreenPurpleUnits from './module-2/GreenPurpleUnits.svelte';
  import Module3Intro from './module-3/Module3Intro.svelte';
  import CommercialTimes from './module-3/CommercialTimes.svelte';
  import BrandSEP from './module-3/BrandSEP.svelte';
  import AdvertiserConflicts from './module-3/AdvertiserConflicts.svelte';
  import StandAloneRule from './module-3/StandAloneRule.svelte';
  import UnitCutPractice from './module-3/UnitCutPractice.svelte';
  import MCEmailPractice from './module-3/MCEmailPractice.svelte';
  import TimeOutPractice from './module-3/TimeOutPractice.svelte';
  import Swaps from './module-3/Swaps.svelte';
  import MasterControlEmail from './module-3/MasterControlEmail.svelte';
  import LocalSwaps from './module-3/LocalSwaps.svelte';
  import FinalExam from './module-3/FinalExam.svelte';
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
      title: 'Module 2: Understanding Units',
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
        <p class="text-blue-700 font-semibold">Let's get started with Module 3!</p>
      </div>`
    }
  ];



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
  let mainSection: string = 'introduction'; // Can be any valid section identifier including all module sections
  let module1SubIdx = 0;
  let submodulesOpen = true;
  
  // Add a submodulesOpen3 state for Module 3
  let submodulesOpen3 = true;
  
  // Add collapsible states for each module
  let module1Collapsed = false;
  let module2Collapsed = false;
  let module3Collapsed = false;
  
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
  
  // Check if Module 1 is fully completed (all 13 submodules)
  $: module1Completed = completedSubmodules.size === 13;
  


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
    { title: 'Spot End Time', component: SpotEndTime },
    { title: 'End Time', component: EndTime },
    { title: 'Floaters', component: Floaters },
    { title: 'Key Tab', component: KeyTab }
  ];

  // Navigation map - defines the flow between modules and submodules
  const navigationMap: Record<string, any> = {
    'introduction': { next: 'module1' },
    'module1': { next: 'module1sub', subIndex: 0 },
    'module1sub': {
      0: { next: 'module1sub', subIndex: 1 }, // Program Line -> Start Time & Real Time
      1: { next: 'quiz' }, // Start Time & Real Time -> Quiz
      2: { next: 'module1sub', subIndex: 3 }, // Hit Time -> Event Type
      3: { next: 'module1sub', subIndex: 4 }, // Event Type -> Length
      4: { next: 'lengthQuiz' }, // Length -> Length Quiz
      5: { next: 'module1sub', subIndex: 6 }, // Title -> Advertiser
      6: { next: 'module1sub', subIndex: 7 }, // Advertiser -> House Number
      7: { next: 'houseNumberQuiz' }, // House Number -> House Number Quiz
      8: { next: 'module1sub', subIndex: 9 }, // Ordered As -> Spot End Time
      9: { next: 'module1sub', subIndex: 10 }, // Spot End Time -> End Time
      10: { next: 'module1sub', subIndex: 11 }, // End Time -> Floaters
      11: { next: 'module1sub', subIndex: 12 }, // Floaters -> Key Tab
      12: { next: 'module1test' } // Key Tab -> Module 1 Test
    },
    'quiz': { next: 'module1sub', subIndex: 2 }, // Start Time & Real Time Quiz -> Hit Time
    'lengthQuiz': { next: 'module1sub', subIndex: 5 }, // Length Quiz -> Title
    'houseNumberQuiz': { next: 'module1sub', subIndex: 8 }, // House Number Quiz -> Ordered As
    'module1test': { next: 'module2' }, // Module 1 Test -> Module 2
    'module2': { next: 'module2_sellingtitle' },
    'module2_sellingtitle': { next: 'module2_yellowunit' },
    'module2_yellowunit': { next: 'module2_unitprioritizationdetails' },
    'module2_unitprioritizationdetails': { next: 'module2_greenpurpleunits' },
    'module2_greenpurpleunits': { next: 'module2test' },
    'module2test': { next: 'module3' },
    'module3': { next: 'module3_brandsep' },
    'module3_brandsep': { next: 'module3_advertiserconflicts' },
    'module3_advertiserconflicts': { next: 'module3_standalonerule' },
    'module3_standalonerule': { next: 'module3_commercialtimes' },
    'module3_commercialtimes': { next: 'module3_swaps' },
    'module3_swaps': { next: 'module3_mastercontrolemail' },
    'module3_mastercontrolemail': { next: 'module3_localswaps' },
    'module3_localswaps': { next: 'module3_excelsheet' },
    'module3_excelsheet': { next: 'module3_unitcutpractice' },
    'module3_unitcutpractice': { next: 'module3_mcemailpractice' },
    'module3_mcemailpractice': { next: 'module3_timeoutpractice' },
    'module3_timeoutpractice': { next: 'finalexam' } // Continue to final exam when complete
  };

  // Function to get the next destination based on current location
  function getNextDestination(currentSection: string, currentSubIndex?: number) {
    if (currentSection === 'module1sub' && typeof currentSubIndex === 'number') {
      return navigationMap.module1sub[currentSubIndex];
    }
    return navigationMap[currentSection];
  }

  // Function to get appropriate next button text based on current location
  function getNextButtonText(currentSection: string, currentSubIndex?: number): string {
    const nextDest = getNextDestination(currentSection, currentSubIndex);
    if (!nextDest) return "Next";
    
    // Check if next destination is a test
    if (nextDest.next === 'module1test' || nextDest.next === 'module2test') {
      return "Take Test";
    }
    
    // Check if next destination is the final exam
    if (nextDest.next === 'finalexam') {
      return "Take Final Exam";
    }
    
    // Check if next destination is the final module completion
    if (nextDest.next === 'introduction') {
      return "Complete Training";
    }
    
    // Check if next destination is a new module
    if (nextDest.next === 'module2' || nextDest.next === 'module3') {
      return "Next Module";
    }
    
    return "Next";
  }

  import { fullscreenStore, getFullscreenState } from '$lib/stores/fullscreenStore';

  // Function to log fullscreen state for debugging
  function logFullscreenState(context: string) {
    const fullscreenState = getFullscreenState();
    const playerArea = document.querySelector('[data-player-area]');
    console.log(`[${context}] Fullscreen: ${fullscreenState.isFullscreen}, Player area found: ${!!playerArea}`);
  }
  
  // Helper function to check if navigation is allowed
  function canNavigateTo(section: string, subIndex?: number): boolean {
    let progressKey: string;
    const debugEnabled = true; // Set to true to see detailed unlock logic
    
    // Map section/subIndex to progress key
    if (section === 'introduction') {
      return true; // Introduction is always accessible
    } else if (section === 'module1') {
      progressKey = 'module1_intro';
    } else if (section === 'module1sub') {
      const submoduleKeys = [
        'module1_programline',
        'module1_starttimerealtime',
        'module1_hittime',
        'module1_eventtype',
        'module1_length',
        'module1_title',
        'module1_advertiser',
        'module1_housenumber',
        'module1_orderedas',
        'module1_spotendtime',
        'module1_endtime',
        'module1_floaters',
        'module1_keytab'
      ];
      progressKey = submoduleKeys[subIndex ?? 0];
    } else if (section === 'quiz') {
      progressKey = 'module1_starttimerealtime_quiz';
    } else if (section === 'lengthQuiz') {
      progressKey = 'module1_length_quiz';
    } else if (section === 'houseNumberQuiz') {
      progressKey = 'module1_housenumber_quiz';
    } else if (section === 'module1test') {
      progressKey = 'module1_test';
    } else if (section === 'module2') {
      progressKey = 'module2_intro';
    } else if (section === 'module2_sellingtitle') {
      progressKey = 'module2_sellingtitle';
    } else if (section === 'module2_yellowunit') {
      progressKey = 'module2_yellowunit';
    } else if (section === 'module2_unitprioritizationdetails') {
      progressKey = 'module2_unitprioritizationdetails';
    } else if (section === 'module2_greenpurpleunits') {
      progressKey = 'module2_greenpurpleunits';
    } else if (section === 'module2test') {
      progressKey = 'module2_test';
    } else if (section === 'module3') {
      progressKey = 'module3_intro';
    } else if (section === 'module3_brandsep') {
      progressKey = 'module3_brandsep';
    } else if (section === 'module3_advertiserconflicts') {
      progressKey = 'module3_advertiserconflicts';
    } else if (section === 'module3_standalonerule') {
      progressKey = 'module3_standalonerule';
    } else if (section === 'module3_commercialtimes') {
      progressKey = 'module3_commercialtimes';
    } else if (section === 'module3_swaps') {
      progressKey = 'module3_swaps';
    } else if (section === 'module3_mastercontrolemail') {
      progressKey = 'module3_mastercontrolemail';
    } else if (section === 'module3_localswaps') {
      progressKey = 'module3_localswaps';
    } else if (section === 'module3_excelsheet') {
      progressKey = 'module3_excelsheet';
    } else if (section === 'module3_unitcutpractice') {
      progressKey = 'module3_unitcutpractice';
    } else if (section === 'module3_mcemailpractice') {
      progressKey = 'module3_mcemailpractice';
    } else if (section === 'module3_timeoutpractice') {
      progressKey = 'module3_timeoutpractice';
    } else if (section === 'finalexam') {
      progressKey = 'finalexam';
    } else {
      return true; // Unknown section, allow navigation (for safety)
    }
    
    const isUnlocked = progressStore.isUnlocked(progressKey as any, progressState);
    if (debugEnabled || !isUnlocked) {
      console.log(`🔓 Checking unlock for ${section}${subIndex !== undefined ? `[${subIndex}]` : ''} (key: ${progressKey}):`, isUnlocked, 'progressState:', progressState);
    }
    return isUnlocked;
  }

  // Function to navigate to the next destination
  function navigateToNext(currentSection: string, currentSubIndex?: number) {
    console.log('navigateToNext called with:', currentSection, currentSubIndex);
    const nextDest = getNextDestination(currentSection, currentSubIndex);
    console.log('nextDest:', nextDest);
    
    // Mark current section as completed before navigating
    markCurrentSectionCompleted(currentSection, currentSubIndex);
    
    // Check if we're in fullscreen before navigation
    const fullscreenState = getFullscreenState();
    const wasFullscreen = fullscreenState.isFullscreen;
    logFullscreenState('Before navigation');
    
    if (nextDest) {
      if (nextDest.subIndex !== undefined) {
        // Navigate to a specific submodule
        console.log('Navigating to submodule:', nextDest.next, 'index:', nextDest.subIndex);
        mainSection = nextDest.next;
        if (nextDest.next === 'module1sub') {
          module1SubIdx = nextDest.subIndex;
        }
      } else {
        // Navigate to a main section
        console.log('Navigating to main section:', nextDest.next);
        mainSection = nextDest.next;
      }
      
      // If we were in fullscreen, restore it on the new content
      if (wasFullscreen) {
        console.log('Was in fullscreen, will restore fullscreen on new content');
        // Use a longer delay and try multiple times
        setTimeout(() => {
          const newPlayerArea = document.querySelector('[data-player-area]') as HTMLElement;
          if (newPlayerArea && newPlayerArea.requestFullscreen) {
            console.log('Opening next content in fullscreen');
            newPlayerArea.requestFullscreen().then(() => {
              console.log('Fullscreen restored successfully');
              logFullscreenState('After restoration');
            }).catch(err => {
              console.log('Failed to open next content in fullscreen:', err);
              // Try one more time after a longer delay
              setTimeout(() => {
                if (newPlayerArea && newPlayerArea.requestFullscreen) {
                  newPlayerArea.requestFullscreen().then(() => {
                    logFullscreenState('After second attempt');
                  }).catch(err2 => {
                    console.log('Second attempt also failed:', err2);
                    logFullscreenState('After failed second attempt');
                  });
                }
              }, 1000);
            });
          } else {
            console.log('No player area found for fullscreen restoration');
            logFullscreenState('No player area found');
          }
        }, 800);
      }
    } else {
      console.log('No next destination found for:', currentSection);
    }
  }
  
  // Helper function to mark current section as completed
  function markCurrentSectionCompleted(currentSection: string, currentSubIndex?: number) {
    console.log('Marking section as completed:', currentSection, currentSubIndex);
    if (currentSection === 'module1') {
      progressStore.markCompleted('module1_intro');
    } else if (currentSection === 'module1sub') {
      const submoduleKeys = [
        'module1_programline',
        'module1_starttimerealtime',
        'module1_hittime',
        'module1_eventtype',
        'module1_length',
        'module1_title',
        'module1_advertiser',
        'module1_housenumber',
        'module1_orderedas',
        'module1_spotendtime',
        'module1_endtime',
        'module1_floaters',
        'module1_keytab'
      ];
      if (currentSubIndex !== undefined && submoduleKeys[currentSubIndex]) {
        progressStore.markCompleted(submoduleKeys[currentSubIndex] as any);
      }
    } else if (currentSection === 'quiz') {
      progressStore.markCompleted('module1_starttimerealtime_quiz');
    } else if (currentSection === 'lengthQuiz') {
      progressStore.markCompleted('module1_length_quiz');
    } else if (currentSection === 'houseNumberQuiz') {
      progressStore.markCompleted('module1_housenumber_quiz');
    } else if (currentSection === 'module2') {
      progressStore.markCompleted('module2_intro');
    } else if (currentSection === 'module2_sellingtitle') {
      progressStore.markCompleted('module2_sellingtitle');
    } else if (currentSection === 'module2_yellowunit') {
      progressStore.markCompleted('module2_yellowunit');
    } else if (currentSection === 'module2_unitprioritizationdetails') {
      progressStore.markCompleted('module2_unitprioritizationdetails');
    } else if (currentSection === 'module2_greenpurpleunits') {
      progressStore.markCompleted('module2_greenpurpleunits');
    } else if (currentSection === 'module3') {
      progressStore.markCompleted('module3_intro');
    } else if (currentSection === 'module3_brandsep') {
      progressStore.markCompleted('module3_brandsep');
    } else if (currentSection === 'module3_advertiserconflicts') {
      progressStore.markCompleted('module3_advertiserconflicts');
    } else if (currentSection === 'module3_standalonerule') {
      progressStore.markCompleted('module3_standalonerule');
    } else if (currentSection === 'module3_commercialtimes') {
      progressStore.markCompleted('module3_commercialtimes');
    } else if (currentSection === 'module3_swaps') {
      progressStore.markCompleted('module3_swaps');
    } else if (currentSection === 'module3_mastercontrolemail') {
      progressStore.markCompleted('module3_mastercontrolemail');
    } else if (currentSection === 'module3_localswaps') {
      progressStore.markCompleted('module3_localswaps');
    } else if (currentSection === 'module3_excelsheet') {
      progressStore.markCompleted('module3_excelsheet');
    } else if (currentSection === 'module3_unitcutpractice') {
      progressStore.markCompleted('module3_unitcutpractice');
    } else if (currentSection === 'module3_mcemailpractice') {
      progressStore.markCompleted('module3_mcemailpractice');
    } else if (currentSection === 'module3_timeoutpractice') {
      progressStore.markCompleted('module3_timeoutpractice');
    }
  }

  function goToIntroduction() {
    if (!canNavigateTo('introduction')) {
      alert('This section is locked. Please complete previous sections first.');
      return;
    }
    const fullscreenState = getFullscreenState();
    const wasFullscreen = fullscreenState.isFullscreen;
    mainSection = 'introduction';
    if (wasFullscreen) {
      setTimeout(() => {
        const newPlayerArea = document.querySelector('[data-player-area]') as HTMLElement;
        if (newPlayerArea && newPlayerArea.requestFullscreen) {
          newPlayerArea.requestFullscreen().catch(err => {
            console.log('Failed to open introduction in fullscreen:', err);
          });
        }
      }, 800);
    }
  }

  // Helper function to navigate to final exam (bypasses TypeScript inference issues)
  function goToFinalExam() {
    if (!canNavigateTo('finalexam')) {
      alert('The Final Exam is locked. Please complete all previous modules first.');
      return;
    }
    const fullscreenState = getFullscreenState();
    const wasFullscreen = fullscreenState.isFullscreen;
    mainSection = 'finalexam';
    if (wasFullscreen) {
      setTimeout(() => {
        const newPlayerArea = document.querySelector('[data-player-area]') as HTMLElement;
        if (newPlayerArea && newPlayerArea.requestFullscreen) {
          newPlayerArea.requestFullscreen().catch(err => {
            console.log('Failed to open final exam in fullscreen:', err);
          });
        }
      }, 800);
    }
  }
  function goToModule1Intro() {
    if (!canNavigateTo('module1')) {
      alert('Module 1 is locked. Please complete the Introduction first.');
      return;
    }
    const fullscreenState = getFullscreenState();
    const wasFullscreen = fullscreenState.isFullscreen;
    mainSection = 'module1';
    if (wasFullscreen) {
      setTimeout(() => {
        const newPlayerArea = document.querySelector('[data-player-area]') as HTMLElement;
        if (newPlayerArea && newPlayerArea.requestFullscreen) {
          newPlayerArea.requestFullscreen().catch(err => {
            console.log('Failed to open module1 intro in fullscreen:', err);
          });
        }
      }, 800);
    }
  }
  function goToModule1Sub(idx: number) {
    // Check if this specific submodule is unlocked using the reactive unlock states
    const submoduleKeys: (keyof typeof module1SubUnlockStates)[] = ['programline', 'starttimerealtime', 'hittime', 'eventtype', 'length', 'title', 'advertiser', 'housenumber', 'orderedas', 'spotendtime', 'endtime', 'floaters', 'keytab'];
    const submoduleKey = submoduleKeys[idx];
    if (submoduleKey && !module1SubUnlockStates[submoduleKey]) {
      alert('This section is locked. Please complete previous sections first.');
      console.log(`🔒 Blocked navigation to module1sub[${idx}] (${submoduleKey}): not unlocked`);
      return;
    }
    console.log(`✅ Navigating to module1sub[${idx}] (${submoduleKey}): unlocked`);
    const fullscreenState = getFullscreenState();
    const wasFullscreen = fullscreenState.isFullscreen;
    mainSection = 'module1sub';
    module1SubIdx = idx;
    if (wasFullscreen) {
      setTimeout(() => {
        const newPlayerArea = document.querySelector('[data-player-area]') as HTMLElement;
        if (newPlayerArea && newPlayerArea.requestFullscreen) {
          newPlayerArea.requestFullscreen().catch(err => {
            console.log('Failed to open module1 sub in fullscreen:', err);
          });
        }
      }, 800);
    }
  }
  function goToQuiz() {
    const fullscreenState = getFullscreenState();
    const wasFullscreen = fullscreenState.isFullscreen;
    mainSection = 'quiz';
    if (wasFullscreen) {
      setTimeout(() => {
        const newPlayerArea = document.querySelector('[data-player-area]') as HTMLElement;
        if (newPlayerArea && newPlayerArea.requestFullscreen) {
          newPlayerArea.requestFullscreen().catch(err => {
            console.log('Failed to open quiz in fullscreen:', err);
          });
        }
      }, 800);
    }
  }
  
  function goToNextSubmodule() {
    // Navigate to the next submodule after quiz completion
    goToModule1Sub(2); // Hit Time is index 2
  }
  function next() {
    if (mainSection === 'introduction') {
      goToModule1Intro();
    } else if (mainSection === 'module1') {
      // Mark Module 1 intro as complete before navigating
      progressStore.markCompleted('module1_intro');
      
      // Go to first submodule (Program Line)
      const fullscreenState = getFullscreenState();
      const wasFullscreen = fullscreenState.isFullscreen;
      mainSection = 'module1sub';
      module1SubIdx = 0;
      if (wasFullscreen) {
        setTimeout(() => {
          const newPlayerArea = document.querySelector('[data-player-area]') as HTMLElement;
          if (newPlayerArea && newPlayerArea.requestFullscreen) {
            newPlayerArea.requestFullscreen().catch(err => {
              console.log('Failed to open module1 sub in fullscreen:', err);
            });
          }
        }, 800);
      }
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

  // End of Module 1 Test questions
  const endOfModule1MainQuestions = [
    { id: 1, question: "What is an Advertiser?", options: [
      "A spreadsheet used to track commercials",
      "A program that airs commercials",
      "An individual or organization promoting products, services, or ideas to a target audience",
      "The same as a Commercial Break"
    ], correctAnswer: 2 },
    { id: 2, question: "What is another word for \"Unit\"?", options: [
      "Floater",
      "Program line",
      "Window",
      "Commercial"
    ], correctAnswer: 3 },
    { id: 3, question: "What is a Commercial Break?", options: [
      "The time when the network stops airing commercials",
      "A planned interval when advertisements are aired",
      "A tab in the Live Coverage Sheet",
      "A program segment"
    ], correctAnswer: 1 },
    { id: 4, question: "In Traffic, what does the term \"Window\" mean?", options: [
      "A computer screen",
      "A spreadsheet column",
      "The time period a program or game airs",
      "A type of commercial"
    ], correctAnswer: 2 },
    { id: 5, question: "What is a Live Coverage Sheet used for?", options: [
      "To design commercials",
      "To display a schedule for commercials/units",
      "To record only game scores",
      "To communicate with advertisers"
    ], correctAnswer: 1 },
    { id: 6, question: "What does \"Swaps\" mean in the Traffic Department?", options: [
      "Creating new commercials",
      "Making real-time changes on the Live Coverage Sheet to adjust commercial placements",
      "Changing program titles",
      "Moving a Window"
    ], correctAnswer: 1 },
    { id: 7, question: "If a unit is marked \"Dead,\" what does that mean?", options: [
      "It will air next week",
      "It will air later that day",
      "It will not air at all that day or night",
      "It must air during every break"
    ], correctAnswer: 2 },
    { id: 8, question: "Who is MC in the Traffic Department?", options: [
      "The Marketing Coordinator",
      "Master Control — the people who send commercials to air",
      "Main Commercial Manager",
      "Multi-Channel Operator"
    ], correctAnswer: 1 },
    { id: 9, question: "Why must you communicate with MC?", options: [
      "They sell the commercials",
      "They create the commercials",
      "They ultimately send commercials to air",
      "They monitor ratings"
    ], correctAnswer: 2 },
    { id: 10, question: "What is the Hit Time column used for?", options: [
      "To show final airing time",
      "To estimate when commercials may air for planning",
      "To communicate with advertisers",
      "To mark dead units"
    ], correctAnswer: 1 },
  ];
  const endOfModule1ExtraQuestions = [
    { id: 11, question: "What information does the Length column show?", options: [
      "Program end time",
      "How long each unit is",
      "The advertiser's budget",
      "The House Number"
    ], correctAnswer: 1 },
    { id: 12, question: "What does the Title column show?", options: [
      "The advertiser's email",
      "The show title and segment numbers",
      "The length of the break",
      "The Real Time of the show"
    ], correctAnswer: 1 },
    { id: 13, question: "Why is the House Number important?", options: [
      "It shows how much the ad cost",
      "It's used by MC to identify the specific ad",
      "It gives the brand's phone number",
      "It determines the Window time"
    ], correctAnswer: 1 },
    { id: 14, question: "What does \"Ordered As\" tell you?", options: [
      "The cost of the commercial",
      "The Window a commercial is sold to",
      "The advertiser's name",
      "The float time"
    ], correctAnswer: 1 },
    { id: 15, question: "What does Spot End Time show?", options: [
      "The moment a program starts",
      "The latest possible time a commercial can air",
      "The time a break should start",
      "The House Number"
    ], correctAnswer: 1 },
    { id: 16, question: "What are Floaters?", options: [
      "Units that will never air",
      "Commercials that always run in the same slot",
      "Extra sold units that need to air during the game",
      "The same as a Program line"
    ], correctAnswer: 2 },
    { id: 17, question: "What is the \"Key\" tab on the Live Coverage Sheet mainly used for?", options: [
      "To sell commercials",
      "To watch live games",
      "For reference of contingency information",
      "To communicate with advertisers"
    ], correctAnswer: 2 },
  ];

  let showExtraQuestions = false;
  let quizPassed = false;
  let quizScore = 0;
  let showMainResults = false;
  let showFinalSummary = false;

  function handleQuizCompleted(event: CustomEvent<any>) {
    quizScore = event.detail.score;
    quizPassed = event.detail.passed;
    if (showExtraQuestions) {
      showFinalSummary = true;
    } else {
      showMainResults = true;
    }
  }

  function handleContinueToExtra() {
    showMainResults = false;
    showExtraQuestions = true;
  }

  function handleContinueToModule2() {
    showMainResults = false;
    showExtraQuestions = false;
    showFinalSummary = false;
    progressStore.markCompleted('module1_test');
    mainSection = 'module2';
  }

  const endOfModule2MainQuestions = [
    { id: 1, question: "Which color represents SOLD commercials on the Live Coverage Sheet?", options: ["Green", "Yellow", "Purple", "Blue"], correctAnswer: 1 },
    { id: 2, question: "Which type of unit is tied to a specific show and cannot be placed elsewhere if cut?", options: ["ROS 24 Hour", "Studio Encore", "Show Specific", "DRs"], correctAnswer: 2 },
    { id: 3, question: "What is the primary reason GREEN-coded commercials are cut first?", options: ["They're too long", "They're unapproved", "They're not mandatory to air and don't generate as much revenue", "They're duplicate content"], correctAnswer: 2 },
    { id: 4, question: "Which of the following has a strict time restriction of 7 PM – 12 AM?", options: ["Studio Encore", "ROS Prime", "Sports Spectacular", "PSAs"], correctAnswer: 1 },
    { id: 5, question: "Which unit has the widest airing flexibility?", options: ["ROS 24 Hour", "ROS Prime", "Locals", "DRs"], correctAnswer: 0 },
    { id: 6, question: "Which unit category includes commercials used during reruns and typically holds no monetary value?", options: ["Show Specific", "Studio Encore", "Sports Spectacular", "DRs"], correctAnswer: 1 },
    { id: 7, question: "Which of the following Encore units must NOT be cut despite the usual rule?", options: ["DR Encore", "ROS Encore", "PBR Encore", "Local Encore"], correctAnswer: 2 },
    { id: 8, question: "What color is used to represent Local units on the Live Coverage Sheet?", options: ["Yellow", "Green", "Red", "Purple"], correctAnswer: 3 },
    { id: 9, question: "PSAs are the most important category of units and are never cut.", options: ["True", "False"], correctAnswer: 1 },
    { id: 10, question: "DRs (Direct Response ads) are not required to air but can earn the network extra money.", options: ["True", "False"], correctAnswer: 0 },
  ];
  const endOfModule2ExtraQuestions = [
    { id: 11, question: "Promos do not generate revenue but still rank higher in priority than PSAs.", options: ["True", "False"], correctAnswer: 0 },
    { id: 12, question: "ROS Prime units are as flexible as ROS 24 Hour units.", options: ["True", "False"], correctAnswer: 1 },
    { id: 13, question: "Local units are always 90 seconds long, no exceptions.", options: ["True", "False"], correctAnswer: 0 },
    { id: 14, question: "Sports Spectacular units are mandatory but can run in other Sports Spectacular windows.", options: ["True", "False"], correctAnswer: 0 },
    { id: 15, question: "Green-coded units include PSAs, Promos, and DRs.", options: ["True", "False"], correctAnswer: 0 },
    { id: 16, question: "Studio Encore units are typically the first sold units to be cut.", options: ["True", "False"], correctAnswer: 0 },
  ];
  let showExtraQuestions2 = false;
  let quizPassed2 = false;
  let quizScore2 = 0;
  let showMainResults2 = false;
  let showFinalSummary2 = false;
  function handleQuizCompleted2(event: CustomEvent<any>) {
    quizScore2 = event.detail.score;
    quizPassed2 = event.detail.passed;
    if (showExtraQuestions2) {
      showFinalSummary2 = true;
    } else {
      showMainResults2 = true;
    }
  }
  function handleContinueToExtra2() {
    showMainResults2 = false;
    showExtraQuestions2 = true;
  }
  function handleContinueToModule3() {
    showMainResults2 = false;
    showExtraQuestions2 = false;
    showFinalSummary2 = false;
    progressStore.markCompleted('module2_test');
    mainSection = 'module3';
  }

  $: audioState = $audioStore;
  $: progressState = $progressStore;
  
  // Force reactivity by creating derived values
  $: {
    // Log changes to help with debugging
    if (progressState) {
      console.log('📊 Progress State Updated:', {
        introduction: progressState.introduction,
        module1_intro: progressState.module1_intro,
        module1_programline: progressState.module1_programline,
        module1_starttimerealtime: progressState.module1_starttimerealtime
      });
    }
  }
  
  // Create reactive unlock states for Module 1 submodules
  $: module1SubUnlockStates = {
    programline: progressStore.isUnlocked('module1_programline', progressState),
    starttimerealtime: progressStore.isUnlocked('module1_starttimerealtime', progressState),
    quiz: progressStore.isUnlocked('module1_starttimerealtime_quiz', progressState),
    hittime: progressStore.isUnlocked('module1_hittime', progressState),
    eventtype: progressStore.isUnlocked('module1_eventtype', progressState),
    length: progressStore.isUnlocked('module1_length', progressState),
    lengthQuiz: progressStore.isUnlocked('module1_length_quiz', progressState),
    title: progressStore.isUnlocked('module1_title', progressState),
    advertiser: progressStore.isUnlocked('module1_advertiser', progressState),
    housenumber: progressStore.isUnlocked('module1_housenumber', progressState),
    houseNumberQuiz: progressStore.isUnlocked('module1_housenumber_quiz', progressState),
    orderedas: progressStore.isUnlocked('module1_orderedas', progressState),
    spotendtime: progressStore.isUnlocked('module1_spotendtime', progressState),
    endtime: progressStore.isUnlocked('module1_endtime', progressState),
    floaters: progressStore.isUnlocked('module1_floaters', progressState),
    keytab: progressStore.isUnlocked('module1_keytab', progressState),
    test: progressStore.isUnlocked('module1_test', progressState)
  }
  
  // Log unlock states for debugging
  $: {
    console.log('🔓 Module 1 Unlock States:', module1SubUnlockStates);
  }
  
  // Check if entire modules are completed (all submodules + test)
  $: module1FullyCompleted = progressState.module1_intro && 
    progressState.module1_programline &&
    progressState.module1_starttimerealtime &&
    progressState.module1_starttimerealtime_quiz &&
    progressState.module1_hittime &&
    progressState.module1_eventtype &&
    progressState.module1_length &&
    progressState.module1_length_quiz &&
    progressState.module1_title &&
    progressState.module1_advertiser &&
    progressState.module1_housenumber &&
    progressState.module1_housenumber_quiz &&
    progressState.module1_orderedas &&
    progressState.module1_spotendtime &&
    progressState.module1_endtime &&
    progressState.module1_floaters &&
    progressState.module1_keytab &&
    progressState.module1_test;
  
  $: module2FullyCompleted = progressState.module2_intro &&
    progressState.module2_sellingtitle &&
    progressState.module2_yellowunit &&
    progressState.module2_unitprioritizationdetails &&
    progressState.module2_greenpurpleunits &&
    progressState.module2_test;
  
  $: module3FullyCompleted = progressState.module3_intro &&
    progressState.module3_brandsep &&
    progressState.module3_advertiserconflicts &&
    progressState.module3_standalonerule &&
    progressState.module3_commercialtimes &&
    progressState.module3_swaps &&
    progressState.module3_mastercontrolemail &&
    progressState.module3_localswaps &&
    progressState.module3_excelsheet &&
    progressState.module3_unitcutpractice &&
    progressState.module3_mcemailpractice &&
    progressState.module3_timeoutpractice;
  
  // Module 2 intro logic (place near other script-level logic)
  let isModule2IntroComplete = false;
  function handleModule2Next() {
    mainSection = 'module2test';
  }
  $: isModule2IntroComplete = mainSection === 'module2' && audioState.currentIndex === module2Script.length - 1 && audioState.progress >= 99;
  $: module2AudioComplete = (
    audioState.currentIndex === module2Script.length - 1 &&
    audioState.progress >= 99 &&
    !audioState.isPlaying
  );

  const module2Script = [
    {
      text: "In the Ordered As column you'll see many different types of units. In this module we will go over what they all are. When moving around units this is the first column you will look at.",
      audio: getR2Url('/audio/module-2/module2_intro.mp3'),
      image: getR2Url('/images/introduction/basketballBackground.png'),
      videoAnimation: getR2Url('/images/ballSackm2Intro.mov')
    },
    {
      text: "Here are the different color categories:",
      audio: getR2Url('/audio/module-2/module2_slide2_combined.mp3'),
      titleAudio: getR2Url('/audio/module-2/01-intro/module2_01_part1.mp3'),
      whiteboardText: [
        "**__Color Coordination__**",
        "• YELLOW - Sold commercials (the important stuff)",
        "• PURPLE - Local units", 
        "• GREEN - Cuttable items (Drs, PSAs, Promos)"
      ]
    }
  ];
</script>

<!-- Header -->
<header class="w-full flex items-center justify-between py-4 px-8 bg-white shadow-sm border-b">
  <span class="text-2xl font-bold text-gray-900 tracking-tight">Live Traffic Coverage Training</span>
  <div class="flex gap-2">
    <button on:click={() => {
      console.log('===== PROGRESS DEBUG =====');
      console.log('Progress State:', progressState);
      console.log('Module 1 Unlock States:', module1SubUnlockStates);
      console.log('Introduction completed:', progressState.introduction);
      console.log('Module 1 Intro completed:', progressState.module1_intro);
      console.log('Program Line completed:', progressState.module1_programline);
      console.log('Start Time completed:', progressState.module1_starttimerealtime);
      
      console.log('\n===== UNLOCK CHECK =====');
      console.log('Program Line unlocked?', module1SubUnlockStates.programline);
      console.log('Start Time unlocked?', module1SubUnlockStates.starttimerealtime);
      
      console.log('\n===== LOCALSTORAGE =====');
      const stored = localStorage.getItem('ltc_training_progress');
      if (stored) {
        console.log('Stored progress:', JSON.parse(stored));
      } else {
        console.log('No stored progress found');
      }
      
      let fixed = false;
      
      // Auto-fix: If introduction is complete but module1_intro is not, fix it
      if (progressState.introduction && !progressState.module1_intro) {
        console.log('🔧 AUTO-FIX: Introduction is complete but Module 1 Intro is not marked. Fixing...');
        progressStore.markCompleted('module1_intro');
        fixed = true;
      }
      
      if (fixed) {
        alert('Fixed! Check the console for details. The progress system should now work correctly.');
      } else {
        alert('Check browser console (F12) for detailed progress information');
      }
    }} class="text-xs text-blue-600 hover:text-blue-800 px-3 py-2 border border-blue-200 rounded bg-blue-50 hover:bg-blue-100">
      🔍 Debug & Fix
    </button>
    <button on:click={handleLogout} class="text-gray-500 hover:text-gray-700 text-base font-medium rounded px-4 py-2 border border-gray-200 bg-gray-50">Logout</button>
  </div>
</header>

<div class="flex min-h-[80vh] relative">
  <!-- Sidebar Table of Contents -->
  {#if sidebarOpen}
    <aside class="sidebar bg-white border-r w-64 transition-all duration-200 ease-in-out z-20">
      <div class="flex items-center justify-between px-4 py-3 border-b">
        <span class="font-semibold text-gray-700">Table of Contents</span>
        <button on:click={() => (sidebarOpen = false)} class="text-gray-400 hover:text-gray-700 text-lg font-bold">×</button>
      </div>
      <nav class="flex flex-col divide-y divide-gray-100">
        <button on:click={goToIntroduction} class="text-left px-3 py-2 hover:bg-blue-50 focus:bg-blue-100 transition font-medium text-gray-700 flex items-center gap-2 text-sm w-full {mainSection === 'introduction' ? 'bg-blue-100 text-blue-700' : ''} {!canNavigateTo('introduction') ? 'opacity-50 cursor-not-allowed' : ''}">
          <span class="block w-2 h-2 rounded-full {mainSection === 'introduction' ? 'bg-blue-600' : 'bg-gray-300'}"></span>
          Introduction
          {#if !canNavigateTo('introduction')}
            <span class="ml-auto text-xs">🔒</span>
          {:else if progressState.introduction}
            <span class="ml-auto text-xs">✅</span>
          {/if}
        </button>
        <!-- Module 1 intro -->
        <div class="flex items-center text-left px-3 py-2 hover:bg-blue-50 focus:bg-blue-100 transition font-medium text-gray-700 gap-2 text-sm w-full {mainSection === 'module1' ? 'bg-blue-100 text-blue-700' : ''} {!canNavigateTo('module1') ? 'opacity-50' : ''}">
          <button on:click={goToModule1Intro} class="flex items-center gap-2 flex-1 text-left {!canNavigateTo('module1') ? 'cursor-not-allowed' : ''}">
            <span class="block w-2 h-2 rounded-full {mainSection === 'module1' ? 'bg-blue-600' : 'bg-gray-300'}"></span>
            Module 1: Live Coverage Sheet
            {#if !canNavigateTo('module1')}
              <span class="ml-2 text-xs">🔒</span>
            {:else if module1FullyCompleted}
              <span class="ml-2 text-xs">✅</span>
            {/if}
          </button>
          <button on:click={() => module1Collapsed = !module1Collapsed} class="text-gray-400 hover:text-gray-600 transition-transform {module1Collapsed ? 'rotate-90' : ''}" aria-label="Toggle Module 1 submodules">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
        {#if !module1Collapsed}
          <div class="ml-6 flex flex-col bg-blue-50/50 rounded-b-lg pb-2 pt-1">
            <button on:click={() => goToModule1Sub(0)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 0 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.programline ? 'opacity-50 cursor-not-allowed text-gray-400' : progressState.module1_programline ? 'text-gray-700' : 'text-gray-700'}">
              Program Line
              {#if !module1SubUnlockStates.programline}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_programline}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(1)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 1 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.starttimerealtime ? 'opacity-50 cursor-not-allowed' : ''}">
              Start Time & Real Time
              {#if !module1SubUnlockStates.starttimerealtime}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_starttimerealtime}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (module1SubUnlockStates.quiz) mainSection = 'quiz'; else alert('This quiz is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded ml-4 {mainSection === 'quiz' ? 'bg-green-200 text-green-800 font-semibold' : ''} {!module1SubUnlockStates.quiz ? 'opacity-50 cursor-not-allowed' : ''}">
              📝 Start Time & Real Time Quiz
              {#if !module1SubUnlockStates.quiz}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_starttimerealtime_quiz}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(2)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 2 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.hittime ? 'opacity-50 cursor-not-allowed' : ''}">
              Hit Time
              {#if !module1SubUnlockStates.hittime}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_hittime}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(3)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 3 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.eventtype ? 'opacity-50 cursor-not-allowed' : ''}">
              Event Type
              {#if !module1SubUnlockStates.eventtype}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_eventtype}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(4)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 4 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.length ? 'opacity-50 cursor-not-allowed' : ''}">
              Length
              {#if !module1SubUnlockStates.length}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_length}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (module1SubUnlockStates.lengthQuiz) mainSection = 'lengthQuiz'; else alert('This quiz is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded ml-4 {mainSection === 'lengthQuiz' ? 'bg-green-200 text-green-800 font-semibold' : ''} {!module1SubUnlockStates.lengthQuiz ? 'opacity-50 cursor-not-allowed' : ''}">
              📝 Length Quiz
              {#if !module1SubUnlockStates.lengthQuiz}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_length_quiz}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(5)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 5 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.title ? 'opacity-50 cursor-not-allowed' : ''}">
              Title
              {#if !module1SubUnlockStates.title}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_title}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(6)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 6 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.advertiser ? 'opacity-50 cursor-not-allowed' : ''}">
              Advertiser
              {#if !module1SubUnlockStates.advertiser}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_advertiser}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(7)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 7 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.housenumber ? 'opacity-50 cursor-not-allowed' : ''}">
              House Number
              {#if !module1SubUnlockStates.housenumber}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_housenumber}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (module1SubUnlockStates.houseNumberQuiz) mainSection = 'houseNumberQuiz'; else alert('This quiz is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded ml-4 {mainSection === 'houseNumberQuiz' ? 'bg-green-200 text-green-800 font-semibold' : ''} {!module1SubUnlockStates.houseNumberQuiz ? 'opacity-50 cursor-not-allowed' : ''}">
              📝 House Number Quiz
              {#if !module1SubUnlockStates.houseNumberQuiz}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_housenumber_quiz}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(8)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 8 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.orderedas ? 'opacity-50 cursor-not-allowed' : ''}">
              Ordered As
              {#if !module1SubUnlockStates.orderedas}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_orderedas}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(9)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 9 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.spotendtime ? 'opacity-50 cursor-not-allowed' : ''}">
              Spot End Time
              {#if !module1SubUnlockStates.spotendtime}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_spotendtime}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(10)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 10 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.endtime ? 'opacity-50 cursor-not-allowed' : ''}">
              End Time
              {#if !module1SubUnlockStates.endtime}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_endtime}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(11)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 11 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.floaters ? 'opacity-50 cursor-not-allowed' : ''}">
              Floaters
              {#if !module1SubUnlockStates.floaters}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_floaters}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => goToModule1Sub(12)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 12 ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!module1SubUnlockStates.keytab ? 'opacity-50 cursor-not-allowed' : ''}">
              Key Tab
              {#if !module1SubUnlockStates.keytab}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_keytab}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (module1SubUnlockStates.test) mainSection = 'module1test'; else alert('The Module 1 Test is locked. Please complete all previous sections first.'); }} class="text-left px-3 py-2 hover:bg-purple-100 focus:bg-purple-200 transition font-medium text-purple-700 flex items-center gap-2 text-sm rounded mt-2 {mainSection === 'module1test' ? 'bg-purple-200 text-purple-900 font-semibold' : ''} {!module1SubUnlockStates.test ? 'opacity-50 cursor-not-allowed' : ''}">
              <span class="block w-2 h-2 rounded-full {mainSection === 'module1test' ? 'bg-purple-600' : 'bg-purple-300'}"></span>
              📝 End of Module 1 Test
              {#if !module1SubUnlockStates.test}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module1_test}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
          </div>
        {/if}
        {#each modules.slice(1) as module, modIdx}
          <div class="flex items-center text-left px-3 py-2 hover:bg-blue-50 focus:bg-blue-100 transition font-medium text-gray-700 gap-2 text-sm w-full {mainSection === `module${modIdx+2}` ? 'bg-blue-100 text-blue-700' : ''} {!canNavigateTo(`module${modIdx+2}`) ? 'opacity-50' : ''}">
            <button on:click={() => { if (canNavigateTo(`module${modIdx+2}`)) mainSection = `module${modIdx+2}`; else alert('This module is locked. Please complete previous modules first.'); }} class="flex items-center gap-2 flex-1 text-left {!canNavigateTo(`module${modIdx+2}`) ? 'cursor-not-allowed' : ''}">
              <span class="block w-2 h-2 rounded-full {mainSection === `module${modIdx+2}` ? 'bg-blue-600' : 'bg-gray-300'}"></span>
              {module.title}
              {#if !canNavigateTo(`module${modIdx+2}`)}
                <span class="ml-2 text-xs">🔒</span>
              {:else if modIdx === 0 && module2FullyCompleted}
                <span class="ml-2 text-xs">✅</span>
              {:else if modIdx === 1 && module3FullyCompleted}
                <span class="ml-2 text-xs">✅</span>
              {/if}
            </button>
            {#if modIdx === 0}
              <button on:click={() => module2Collapsed = !module2Collapsed} class="text-gray-400 hover:text-gray-600 transition-transform {module2Collapsed ? 'rotate-90' : ''}" aria-label="Toggle Module 2 submodules">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
                </svg>
              </button>
            {:else if modIdx === 1}
              <button on:click={() => module3Collapsed = !module3Collapsed} class="text-gray-400 hover:text-gray-600 transition-transform {module3Collapsed ? 'rotate-90' : ''}" aria-label="Toggle Module 3 submodules">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
                </svg>
              </button>
            {/if}
          </div>
          {#if modIdx === 0 && !module2Collapsed}
            <div class="ml-6 flex flex-col bg-blue-50/50 rounded-b-lg pb-2 pt-1">
              <button on:click={() => { if (canNavigateTo('module2_sellingtitle')) mainSection = 'module2_sellingtitle'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module2_sellingtitle' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module2_sellingtitle') ? 'opacity-50 cursor-not-allowed' : ''}">
                Selling Title
                {#if !canNavigateTo('module2_sellingtitle')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module2_sellingtitle}<span class="ml-auto text-xs">✅</span>{/if}
              </button>
              <button on:click={() => { if (canNavigateTo('module2_yellowunit')) mainSection = 'module2_yellowunit'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module2_yellowunit' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module2_yellowunit') ? 'opacity-50 cursor-not-allowed' : ''}">
                The Yellow Unit
                {#if !canNavigateTo('module2_yellowunit')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module2_yellowunit}<span class="ml-auto text-xs">✅</span>{/if}
              </button>
              <button on:click={() => { if (canNavigateTo('module2_unitprioritizationdetails')) mainSection = 'module2_unitprioritizationdetails'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module2_unitprioritizationdetails' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module2_unitprioritizationdetails') ? 'opacity-50 cursor-not-allowed' : ''}">
                Unit Prioritization Details
                {#if !canNavigateTo('module2_unitprioritizationdetails')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module2_unitprioritizationdetails}<span class="ml-auto text-xs">✅</span>{/if}
              </button>
              <button on:click={() => { if (canNavigateTo('module2_greenpurpleunits')) mainSection = 'module2_greenpurpleunits'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module2_greenpurpleunits' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module2_greenpurpleunits') ? 'opacity-50 cursor-not-allowed' : ''}">
                Green & Purple Units
                {#if !canNavigateTo('module2_greenpurpleunits')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module2_greenpurpleunits}<span class="ml-auto text-xs">✅</span>{/if}
              </button>
              <button on:click={() => { if (canNavigateTo('module2test')) mainSection = 'module2test'; else alert('The Module 2 Test is locked. Please complete all previous sections first.'); }} class="text-left px-3 py-2 hover:bg-purple-100 focus:bg-purple-200 transition font-medium text-purple-700 flex items-center gap-2 text-sm rounded mt-2 {mainSection === 'module2test' ? 'bg-purple-200 text-purple-900 font-semibold' : ''} {!canNavigateTo('module2test') ? 'opacity-50 cursor-not-allowed' : ''}">
                <span class="block w-2 h-2 rounded-full {mainSection === 'module2test' ? 'bg-purple-600' : 'bg-purple-300'}"></span>
                📝 End of Module 2 Test
                {#if !canNavigateTo('module2test')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module2_test}<span class="ml-auto text-xs">✅</span>{/if}
              </button>
              <!-- Add more submodules here as needed -->
            </div>
          {/if}
        {/each}
        {#if !module3Collapsed}
          <div class="ml-6 flex flex-col bg-blue-50/50 rounded-b-lg pb-2 pt-1">
            <button on:click={() => { if (canNavigateTo('module3_brandsep')) mainSection = 'module3_brandsep'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_brandsep' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module3_brandsep') ? 'opacity-50 cursor-not-allowed' : ''}">
              Brand SEP
              {#if !canNavigateTo('module3_brandsep')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module3_brandsep}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (canNavigateTo('module3_advertiserconflicts')) mainSection = 'module3_advertiserconflicts'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_advertiserconflicts' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module3_advertiserconflicts') ? 'opacity-50 cursor-not-allowed' : ''}">
              Advertiser Conflicts
              {#if !canNavigateTo('module3_advertiserconflicts')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module3_advertiserconflicts}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (canNavigateTo('module3_standalonerule')) mainSection = 'module3_standalonerule'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_standalonerule' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module3_standalonerule') ? 'opacity-50 cursor-not-allowed' : ''}">
              STAND ALONE Rule
              {#if !canNavigateTo('module3_standalonerule')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module3_standalonerule}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (canNavigateTo('module3_commercialtimes')) mainSection = 'module3_commercialtimes'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_commercialtimes' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module3_commercialtimes') ? 'opacity-50 cursor-not-allowed' : ''}">
              Commercial Times
              {#if !canNavigateTo('module3_commercialtimes')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module3_commercialtimes}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (canNavigateTo('module3_swaps')) mainSection = 'module3_swaps'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_swaps' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module3_swaps') ? 'opacity-50 cursor-not-allowed' : ''}">
              Swaps
              {#if !canNavigateTo('module3_swaps')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module3_swaps}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (canNavigateTo('module3_mastercontrolemail')) mainSection = 'module3_mastercontrolemail'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_mastercontrolemail' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module3_mastercontrolemail') ? 'opacity-50 cursor-not-allowed' : ''}">
              Master Control Email
              {#if !canNavigateTo('module3_mastercontrolemail')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module3_mastercontrolemail}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (canNavigateTo('module3_localswaps')) mainSection = 'module3_localswaps'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_localswaps' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module3_localswaps') ? 'opacity-50 cursor-not-allowed' : ''}">
              Local Swaps
              {#if !canNavigateTo('module3_localswaps')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module3_localswaps}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (canNavigateTo('module3_excelsheet')) mainSection = 'module3_excelsheet'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_excelsheet' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module3_excelsheet') ? 'opacity-50 cursor-not-allowed' : ''}">
              Interactive Excel Sheet
              {#if !canNavigateTo('module3_excelsheet')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module3_excelsheet}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (canNavigateTo('module3_unitcutpractice')) mainSection = 'module3_unitcutpractice'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_unitcutpractice' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module3_unitcutpractice') ? 'opacity-50 cursor-not-allowed' : ''}">
              Unit Cut Practice
              {#if !canNavigateTo('module3_unitcutpractice')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module3_unitcutpractice}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (canNavigateTo('module3_mcemailpractice')) mainSection = 'module3_mcemailpractice'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_mcemailpractice' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module3_mcemailpractice') ? 'opacity-50 cursor-not-allowed' : ''}">
              MC Email Practice
              {#if !canNavigateTo('module3_mcemailpractice')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module3_mcemailpractice}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <button on:click={() => { if (canNavigateTo('module3_timeoutpractice')) mainSection = 'module3_timeoutpractice'; else alert('This section is locked. Please complete previous sections first.'); }} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_timeoutpractice' ? 'bg-blue-200 text-blue-800 font-semibold' : ''} {!canNavigateTo('module3_timeoutpractice') ? 'opacity-50 cursor-not-allowed' : ''}">
              Time Out Practice
              {#if !canNavigateTo('module3_timeoutpractice')}<span class="ml-auto text-xs">🔒</span>{:else if progressState.module3_timeoutpractice}<span class="ml-auto text-xs">✅</span>{/if}
            </button>
            <!-- Add more submodules here as needed -->
          </div>
        {/if}
        
        <!-- Final Exam Section -->
        <div class="flex items-center text-left px-3 py-2 hover:bg-green-50 focus:bg-green-100 transition font-medium text-gray-700 gap-2 text-sm w-full {mainSection === 'finalexam' ? 'bg-green-100 text-green-700' : ''} {!canNavigateTo('finalexam') ? 'opacity-50' : ''}">
          <button on:click={goToFinalExam} class="flex items-center gap-2 flex-1 text-left {!canNavigateTo('finalexam') ? 'cursor-not-allowed' : ''}">
            <span class="block w-2 h-2 rounded-full {mainSection === 'finalexam' ? 'bg-green-600' : 'bg-green-300'}"></span>
            📝 Final Exam
            {#if !canNavigateTo('finalexam')}
              <span class="ml-auto text-xs">🔒</span>
            {:else if progressState.finalexam}
              <span class="ml-auto text-xs">✅</span>
            {/if}
          </button>
        </div>
        
        <!-- Developer Mode Section -->
        {#if DEV_FEATURES.developerMode}
          <div class="mt-6 pt-4 border-t border-gray-200">
            <div class="px-3 py-2 text-xs font-semibold text-yellow-700 uppercase tracking-wide">🔧 Developer Mode</div>
            <div class="space-y-1">
              <button on:click={() => mainSection = 'introduction'} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded hover:bg-yellow-100 {mainSection === 'introduction' ? 'bg-yellow-200 text-yellow-800' : 'text-yellow-700'}">
                🏠 Introduction
              </button>
              <button on:click={() => { mainSection = 'module1'; module1SubIdx = 0; }} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded hover:bg-yellow-100 {mainSection === 'module1' ? 'bg-yellow-200 text-yellow-800' : 'text-yellow-700'}">
                📋 Module 1
              </button>
              <button on:click={() => mainSection = 'module2'} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded hover:bg-yellow-100 {mainSection === 'module2' ? 'bg-yellow-200 text-yellow-800' : 'text-yellow-700'}">
                📋 Module 2
              </button>
              <button on:click={() => mainSection = 'module3'} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded hover:bg-yellow-100 {mainSection === 'module3' ? 'bg-yellow-200 text-yellow-800' : 'text-yellow-700'}">
                📋 Module 3
              </button>
              <button on:click={() => mainSection = 'finalexam'} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded hover:bg-yellow-100 {mainSection === 'finalexam' ? 'bg-yellow-200 text-yellow-800' : 'text-yellow-700'}">
                📝 Final Exam
              </button>
              <button on:click={() => { console.log('Current Progress State:', progressState); alert('Check console for progress state'); }} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded hover:bg-red-100 text-red-700">
                🔍 Log Progress State
              </button>
              <button on:click={() => { if (confirm('Reset ALL progress? This cannot be undone.')) { progressStore.reset(); alert('Progress reset! Refresh the page.'); } }} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded hover:bg-red-100 text-red-700">
                🔄 Reset Progress
              </button>
            </div>
          </div>
        {/if}
      </nav>
    </aside>
  {:else}
    <!-- Floating menu button -->
    <button on:click={() => (sidebarOpen = true)} class="floating-menu-button fixed top-20 left-4 z-30 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg p-3 focus:outline-none" aria-label="Open sidebar menu">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
  {/if}

  <!-- Main Content -->
  <main data-fullscreen-container class="flex-1 flex flex-col items-center {!sidebarOpen ? 'sidebar-collapsed' : ''}">
    {#if mainSection === 'introduction'}
      <Introduction on:navigateToNextSubmodule={() => {
        progressStore.markCompleted('introduction');
        const fullscreenState = getFullscreenState();
        mainSection = 'module1';
        module1SubIdx = 0;
        
        // If we were in fullscreen, restore it on the new content
        if (fullscreenState.isFullscreen) {
          setTimeout(() => {
            // Check if fullscreen is already in use
            if (document.fullscreenElement) {
              console.log('Fullscreen is already in use, skipping restoration');
              return;
            }
            
            const newPlayerArea = document.querySelector('[data-player-area]') as HTMLElement;
            if (newPlayerArea && newPlayerArea.requestFullscreen) {
              newPlayerArea.requestFullscreen().catch(err => {
                console.log('Failed to open module1 intro in fullscreen:', err);
              });
            }
          }, 1000);
        }
      }} />
    {:else if mainSection === 'module1'}
      <Module1Intro on:navigateToNextSubmodule={next} progressId="module1_intro" nextButtonText={getNextButtonText('module1')} />
    {:else if mainSection === 'module1sub'}
      {#if module1SubIdx === 0}
        <ProgramLine progressId="module1_programline" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} />
      {:else if module1SubIdx === 1}
        <StartTimeRealTime progressId="module1_starttimerealtime" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} />
      {:else if module1SubIdx === 2}
        <HitTime progressId="module1_hittime" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} />
      {:else if module1SubIdx === 3}
        <EventType progressId="module1_eventtype" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} />
      {:else if module1SubIdx === 4}
        <Length progressId="module1_length" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} on:navigateToQuiz={() => { 
          console.log('Length: navigateToQuiz called'); 
          const fullscreenState = getFullscreenState();
          mainSection = 'lengthQuiz';
          if (fullscreenState.isFullscreen) {
            setTimeout(() => {
              const newPlayerArea = document.querySelector('[data-player-area]') as HTMLElement;
              if (newPlayerArea && newPlayerArea.requestFullscreen) {
                newPlayerArea.requestFullscreen().catch(err => {
                  console.log('Failed to open quiz in fullscreen:', err);
                });
              }
            }, 800);
          }
        }} />
      {:else if module1SubIdx === 5}
        <Title progressId="module1_title" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} />
      {:else if module1SubIdx === 6}
        <Advertiser progressId="module1_advertiser" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} />
      {:else if module1SubIdx === 7}
        <HouseNumber progressId="module1_housenumber" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} on:navigateToQuiz={() => { 
          console.log('HouseNumber: navigateToQuiz called'); 
          const fullscreenState = getFullscreenState();
          mainSection = 'houseNumberQuiz';
          if (fullscreenState.isFullscreen) {
            setTimeout(() => {
              const newPlayerArea = document.querySelector('[data-player-area]') as HTMLElement;
              if (newPlayerArea && newPlayerArea.requestFullscreen) {
                newPlayerArea.requestFullscreen().catch(err => {
                  console.log('Failed to open quiz in fullscreen:', err);
                });
              }
            }, 800);
          }
        }} />
      {:else if module1SubIdx === 8}
        <OrderedAs progressId="module1_orderedas" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} />
      {:else if module1SubIdx === 9}
        <SpotEndTime progressId="module1_spotendtime" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} />
      {:else if module1SubIdx === 10}
        <EndTime progressId="module1_endtime" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} />
      {:else if module1SubIdx === 11}
        <Floaters progressId="module1_floaters" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} />
      {:else if module1SubIdx === 12}
        <KeyTab progressId="module1_keytab" nextButtonText={getNextButtonText('module1sub', module1SubIdx)} on:navigateToNextSubmodule={() => navigateToNext('module1sub', module1SubIdx)} on:moduleCompleted={e => markSubmoduleCompleted(e.detail.submoduleIndex)} />
      {/if}
    {:else if mainSection === 'quiz'}
      <StartTimeRealTimeQuiz on:navigateToNextSubmodule={() => { console.log('Navigating from quiz'); navigateToNext('quiz'); }} />
    {:else if mainSection === 'lengthQuiz'}
      <LengthQuiz on:navigateToNextSubmodule={() => { console.log('Navigating from lengthQuiz'); navigateToNext('lengthQuiz'); }} />
    {:else if mainSection === 'houseNumberQuiz'}
      <HouseNumberQuiz on:navigateToNextSubmodule={() => { console.log('Navigating from houseNumberQuiz'); navigateToNext('houseNumberQuiz'); }} />
    {:else if mainSection === 'module1test'}
      <div class="w-full max-w-2xl mx-auto">
        <h2 class="text-2xl font-bold mb-4">End of Module 1 Test</h2>
        {#if !showMainResults && !showExtraQuestions && !showFinalSummary}
          <QuizTemplate
            questions={endOfModule1MainQuestions}
            title="End of Module 1 Test"
            description="Test your knowledge of Module 1. You must score at least 70% to pass."
            passingScore={70}
            on:quizCompleted={handleQuizCompleted}
          />
        {:else if showMainResults}
          <div class="quiz-summary">
            <h2 class="text-2xl font-bold mb-2">Test Complete!</h2>
            <p class="mb-2">Your score: {quizScore} / 100</p>
            {#if quizPassed}
              <div class="text-green-700 font-bold mb-4">Congratulations! You passed!</div>
              <button class="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 mt-4" on:click={handleContinueToModule2}>Continue to Module 2</button>
            {:else}
              <div class="text-red-700 font-bold mb-4">You did not pass. Try these extra questions to reinforce your learning.</div>
              <button class="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 mt-4" on:click={handleContinueToExtra}>Continue to Extra Questions</button>
            {/if}
          </div>
        {:else if showExtraQuestions && !showFinalSummary}
          <QuizTemplate
            questions={endOfModule1ExtraQuestions}
            title="Extra Questions"
            description="You did not pass the main test. Try these extra questions to reinforce your learning."
            passingScore={100}
            on:quizCompleted={handleQuizCompleted}
          />
        {:else if showFinalSummary}
          <div class="quiz-summary">
            <h2 class="text-2xl font-bold mb-2">Extra Questions Complete!</h2>
            <p class="mb-2">Thank you for completing the extra questions.</p>
            <div class="text-blue-700 font-bold mb-4">Review your answers and revisit the module if needed.</div>
            <button class="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 mt-4" on:click={handleContinueToModule2}>Continue to Module 2</button>
          </div>
        {/if}
      </div>
    {:else if mainSection === 'module2'}
      <YouTubeTemplate
        script={module2Script}
        title="Module 2: Understanding Units"
        image="/images/introduction/basketballBackground.png"

        onNextSubmodule={() => navigateToNext('module2')}
        progressId="module2_intro"
        nextButtonText={getNextButtonText('module2')}
      />
    {:else if mainSection === 'module2test'}
      <div class="w-full max-w-2xl mx-auto">
        <h2 class="text-2xl font-bold mb-4">End of Module 2 Test</h2>
        {#if !showMainResults2 && !showExtraQuestions2 && !showFinalSummary2}
          <QuizTemplate
            questions={endOfModule2MainQuestions}
            title="End of Module 2 Test"
            description="Test your knowledge of Module 2. You must score at least 70% to pass."
            passingScore={70}
            on:quizCompleted={handleQuizCompleted2}
          />
        {:else if showMainResults2}
          <div class="quiz-summary">
            <h2 class="text-2xl font-bold mb-2">Test Complete!</h2>
            <p class="mb-2">Your score: {quizScore2} / 100</p>
            {#if quizPassed2}
              <div class="text-green-700 font-bold mb-4">Congratulations! You passed!</div>
              <button class="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 mt-4" on:click={handleContinueToModule3}>Continue to Module 3</button>
            {:else}
              <div class="text-red-700 font-bold mb-4">You did not pass. Try these extra questions to reinforce your learning.</div>
              <button class="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 mt-4" on:click={handleContinueToExtra2}>Continue to Extra Questions</button>
            {/if}
          </div>
        {:else if showExtraQuestions2 && !showFinalSummary2}
          <QuizTemplate
            questions={endOfModule2ExtraQuestions}
            title="Extra Questions"
            description="You did not pass the main test. Try these extra questions to reinforce your learning."
            passingScore={100}
            on:quizCompleted={handleQuizCompleted2}
          />
        {:else if showFinalSummary2}
          <div class="quiz-summary">
            <h2 class="text-2xl font-bold mb-2">Extra Questions Complete!</h2>
            <p class="mb-2">Thank you for completing the extra questions.</p>
            <div class="text-blue-700 font-bold mb-4">Review your answers and revisit the module if needed.</div>
            <button class="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 mt-4" on:click={handleContinueToModule3}>Continue to Module 3</button>
          </div>
        {/if}
      </div>
    {:else if mainSection === 'module2_sellingtitle'}
      <SellingTitle progressId="module2_sellingtitle" nextButtonText={getNextButtonText('module2_sellingtitle')} on:navigateToNextSubmodule={() => navigateToNext('module2_sellingtitle')} />
    {:else if mainSection === 'module2_yellowunit'}
      <TheYellowUnit progressId="module2_yellowunit" nextButtonText={getNextButtonText('module2_yellowunit')} on:navigateToNextSubmodule={() => navigateToNext('module2_yellowunit')} />
    {:else if mainSection === 'module2_unitprioritizationdetails'}
      <UnitPrioritizationDetails progressId="module2_unitprioritizationdetails" nextButtonText={getNextButtonText('module2_unitprioritizationdetails')} on:navigateToNextSubmodule={() => navigateToNext('module2_unitprioritizationdetails')} />
    {:else if mainSection === 'module2_greenpurpleunits'}
      <GreenPurpleUnits progressId="module2_greenpurpleunits" nextButtonText={getNextButtonText('module2_greenpurpleunits')} on:navigateToNextSubmodule={() => navigateToNext('module2_greenpurpleunits')} />
    {:else if mainSection === 'module3'}
      <Module3Intro progressId="module3_intro" on:navigateToNextSubmodule={() => navigateToNext('module3')} nextButtonText={getNextButtonText('module3')} />
    {:else if mainSection === 'module3_excelsheet'}
      <Module3 on:navigateToNextSubmodule={() => { 
        progressStore.markCompleted('module3_excelsheet');
        mainSection = 'module3_unitcutpractice'; 
      }} />
    {:else if mainSection === 'module3_commercialtimes'}
      <CommercialTimes progressId="module3_commercialtimes" on:navigateToNextSubmodule={() => navigateToNext('module3_commercialtimes')} nextButtonText={getNextButtonText('module3_commercialtimes')} />
    {:else if mainSection === 'module3_brandsep'}
      <BrandSEP progressId="module3_brandsep" on:navigateToNextSubmodule={() => navigateToNext('module3_brandsep')} nextButtonText={getNextButtonText('module3_brandsep')} />
    {:else if mainSection === 'module3_advertiserconflicts'}
      <AdvertiserConflicts progressId="module3_advertiserconflicts" on:navigateToNextSubmodule={() => navigateToNext('module3_advertiserconflicts')} nextButtonText={getNextButtonText('module3_advertiserconflicts')} />
    {:else if mainSection === 'module3_standalonerule'}
      <StandAloneRule on:navigateToNextSubmodule={() => navigateToNext('module3_standalonerule')} nextButtonText={getNextButtonText('module3_standalonerule')} />
    {:else if mainSection === 'module3_unitcutpractice'}
      <UnitCutPractice on:navigateToNextSubmodule={(event) => { 
        progressStore.markCompleted('module3_unitcutpractice');
        mainSection = event.detail || 'module3_mcemailpractice'; 
      }} />
    {:else if mainSection === 'module3_mcemailpractice'}
      <MCEmailPractice on:navigateToNextSubmodule={(event) => { 
        progressStore.markCompleted('module3_mcemailpractice');
        mainSection = event.detail || 'module3_timeoutpractice'; 
      }} />
    {:else if mainSection === 'module3_timeoutpractice'}
      <TimeOutPractice on:navigateToNextSubmodule={() => { 
        progressStore.markCompleted('module3_timeoutpractice');
        goToFinalExam(); 
      }} />
    {:else if mainSection === 'module3_swaps'}
      <Swaps progressId="module3_swaps" on:navigateToNextSubmodule={() => navigateToNext('module3_swaps')} nextButtonText={getNextButtonText('module3_swaps')} />
    {:else if mainSection === 'module3_mastercontrolemail'}
      <MasterControlEmail progressId="module3_mastercontrolemail" on:navigateToNextSubmodule={() => navigateToNext('module3_mastercontrolemail')} nextButtonText={getNextButtonText('module3_mastercontrolemail')} />
    {:else if mainSection === 'module3_localswaps'}
      <LocalSwaps progressId="module3_localswaps" on:navigateToNextSubmodule={() => navigateToNext('module3_localswaps')} nextButtonText={getNextButtonText('module3_localswaps')} />
    {:else if mainSection === 'finalexam'}
      <FinalExam on:navigateToNextSubmodule={() => { 
        progressStore.markCompleted('finalexam');
        alert('Congratulations! You have completed the entire training course!');
      }} nextButtonText="Complete Training" />
    {/if}

  </main>
</div> 
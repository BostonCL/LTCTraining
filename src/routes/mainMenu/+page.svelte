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
  import HouseNumberQuiz from './module-1/HouseNumberQuiz.svelte';
  import EndTime from './module-1/EndTime.svelte';
  import Floaters from './module-1/Floaters.svelte';
  import KeyTab from './module-1/KeyTab.svelte';
  import Module3 from './Module3.svelte';
  import QuizTemplate from '$lib/components/QuizTemplate.svelte';
  import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
  import { audioStore, setCurrentIndex } from '$lib/stores/audioStore';
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
  function getNextButtonText(currentSection: string, currentSubIndex?: number) {
    const nextDest = getNextDestination(currentSection, currentSubIndex);
    if (!nextDest) return "Next";
    
    // Check if next destination is a test
    if (nextDest.next === 'module1test' || nextDest.next === 'module2test') {
      return "Take Test";
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

  // Function to navigate to the next destination
  function navigateToNext(currentSection: string, currentSubIndex?: number) {
    console.log('navigateToNext called with:', currentSection, currentSubIndex);
    const nextDest = getNextDestination(currentSection, currentSubIndex);
    console.log('nextDest:', nextDest);
    
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

  function goToIntroduction() {
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
    mainSection = 'module3';
  }

  $: audioState = $audioStore;
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
      audio: '/audio/module-2/module2_intro.mp3',
      image: '/images/introduction/basketballBackground.png',
      videoAnimation: '/images/ballSackm2Intro.mov'
    },
    {
      text: "Here are the different color categories:",
      audio: '/audio/module-2/module2_slide2_combined.mp3',
      titleAudio: '/audio/module-2/01-intro/module2_01_part1.mp3',
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
  <button on:click={handleLogout} class="text-gray-500 hover:text-gray-700 text-base font-medium rounded px-4 py-2 border border-gray-200 bg-gray-50">Logout</button>
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
        <button on:click={goToIntroduction} class="text-left px-3 py-2 hover:bg-blue-50 focus:bg-blue-100 transition font-medium text-gray-700 flex items-center gap-2 text-sm w-full {mainSection === 'introduction' ? 'bg-blue-100 text-blue-700' : ''}">
          <span class="block w-2 h-2 rounded-full {mainSection === 'introduction' ? 'bg-blue-600' : 'bg-gray-300'}"></span>
          Introduction
        </button>
        <!-- Module 1 intro -->
        <div class="flex items-center text-left px-3 py-2 hover:bg-blue-50 focus:bg-blue-100 transition font-medium text-gray-700 gap-2 text-sm w-full {mainSection === 'module1' ? 'bg-blue-100 text-blue-700' : ''}">
          <button on:click={goToModule1Intro} class="flex items-center gap-2 flex-1 text-left">
            <span class="block w-2 h-2 rounded-full {mainSection === 'module1' ? 'bg-blue-600' : 'bg-gray-300'}"></span>
            Module 1: Live Coverage Sheet
          </button>
          <button on:click={() => module1Collapsed = !module1Collapsed} class="text-gray-400 hover:text-gray-600 transition-transform {module1Collapsed ? 'rotate-90' : ''}" aria-label="Toggle Module 1 submodules">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
        {#if !module1Collapsed}
          <div class="ml-6 flex flex-col bg-blue-50/50 rounded-b-lg pb-2 pt-1">
            <button on:click={() => goToModule1Sub(0)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 0 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Program Line</button>
            <button on:click={() => goToModule1Sub(1)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 1 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Start Time & Real Time</button>
            <button on:click={() => mainSection = 'quiz'} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded ml-4 {mainSection === 'quiz' ? 'bg-green-200 text-green-800 font-semibold' : ''}">📝 Start Time & Real Time Quiz</button>
            <button on:click={() => goToModule1Sub(2)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 2 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Hit Time</button>
            <button on:click={() => goToModule1Sub(3)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 3 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Event Type</button>
            <button on:click={() => goToModule1Sub(4)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 4 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Length</button>
            <button on:click={() => mainSection = 'lengthQuiz'} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded ml-4 {mainSection === 'lengthQuiz' ? 'bg-green-200 text-green-800 font-semibold' : ''}">📝 Length Quiz</button>
            <button on:click={() => goToModule1Sub(5)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 5 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Title</button>
            <button on:click={() => goToModule1Sub(6)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 6 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Advertiser</button>
            <button on:click={() => goToModule1Sub(7)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 7 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">House Number</button>
            <button on:click={() => mainSection = 'houseNumberQuiz'} class="text-left px-3 py-2 text-sm transition font-medium flex items-center gap-2 rounded ml-4 {mainSection === 'houseNumberQuiz' ? 'bg-green-200 text-green-800 font-semibold' : ''}">📝 House Number Quiz</button>
            <button on:click={() => goToModule1Sub(8)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 8 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Ordered As</button>
            <button on:click={() => goToModule1Sub(9)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 9 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Spot End Time</button>
            <button on:click={() => goToModule1Sub(10)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 10 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">End Time</button>
            <button on:click={() => goToModule1Sub(11)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 11 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Floaters</button>
            <button on:click={() => goToModule1Sub(12)} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module1sub' && module1SubIdx === 12 ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Key Tab</button>
            <button on:click={() => mainSection = 'module1test'} class="text-left px-3 py-2 hover:bg-purple-100 focus:bg-purple-200 transition font-medium text-purple-700 flex items-center gap-2 text-sm rounded mt-2 {mainSection === 'module1test' ? 'bg-purple-200 text-purple-900 font-semibold' : ''}">
              <span class="block w-2 h-2 rounded-full {mainSection === 'module1test' ? 'bg-purple-600' : 'bg-purple-300'}"></span>
              📝 End of Module 1 Test
            </button>
          </div>
        {/if}
        {#each modules.slice(1) as module, modIdx}
          <div class="flex items-center text-left px-3 py-2 hover:bg-blue-50 focus:bg-blue-100 transition font-medium text-gray-700 gap-2 text-sm w-full {mainSection === `module${modIdx+2}` ? 'bg-blue-100 text-blue-700' : ''}">
            <button on:click={() => mainSection = `module${modIdx+2}`} class="flex items-center gap-2 flex-1 text-left">
              <span class="block w-2 h-2 rounded-full {mainSection === `module${modIdx+2}` ? 'bg-blue-600' : 'bg-gray-300'}"></span>
              {module.title}
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
              <button on:click={() => mainSection = 'module2_sellingtitle'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module2_sellingtitle' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Selling Title</button>
              <button on:click={() => mainSection = 'module2_yellowunit'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module2_yellowunit' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">The Yellow Unit</button>
              <button on:click={() => mainSection = 'module2_unitprioritizationdetails'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module2_unitprioritizationdetails' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Unit Prioritization Details</button>
              <button on:click={() => mainSection = 'module2_greenpurpleunits'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module2_greenpurpleunits' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Green & Purple Units</button>
              <button on:click={() => mainSection = 'module2test'} class="text-left px-3 py-2 hover:bg-purple-100 focus:bg-purple-200 transition font-medium text-purple-700 flex items-center gap-2 text-sm rounded mt-2 {mainSection === 'module2test' ? 'bg-purple-200 text-purple-900 font-semibold' : ''}">
                <span class="block w-2 h-2 rounded-full {mainSection === 'module2test' ? 'bg-purple-600' : 'bg-purple-300'}"></span>
                📝 End of Module 2 Test
              </button>
              <!-- Add more submodules here as needed -->
            </div>
          {/if}
        {/each}
        {#if !module3Collapsed}
          <div class="ml-6 flex flex-col bg-blue-50/50 rounded-b-lg pb-2 pt-1">
            <button on:click={() => mainSection = 'module3_brandsep'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_brandsep' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Brand SEP</button>
            <button on:click={() => mainSection = 'module3_advertiserconflicts'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_advertiserconflicts' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Advertiser Conflicts</button>
            <button on:click={() => mainSection = 'module3_standalonerule'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_standalonerule' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">STAND ALONE Rule</button>
            <button on:click={() => mainSection = 'module3_commercialtimes'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_commercialtimes' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Commercial Times</button>
            <button on:click={() => mainSection = 'module3_swaps'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_swaps' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Swaps</button>
            <button on:click={() => mainSection = 'module3_mastercontrolemail'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_mastercontrolemail' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Master Control Email</button>
            <button on:click={() => mainSection = 'module3_localswaps'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_localswaps' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Local Swaps</button>
            <button on:click={() => mainSection = 'module3_excelsheet'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_excelsheet' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Interactive Excel Sheet</button>
            <button on:click={() => mainSection = 'module3_unitcutpractice'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_unitcutpractice' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Unit Cut Practice</button>
            <button on:click={() => mainSection = 'module3_mcemailpractice'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_mcemailpractice' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">MC Email Practice</button>
            <button on:click={() => mainSection = 'module3_timeoutpractice'} class="text-left px-3 py-2 hover:bg-blue-100 focus:bg-blue-200 transition font-medium text-gray-600 flex items-center gap-2 text-sm rounded {mainSection === 'module3_timeoutpractice' ? 'bg-blue-200 text-blue-800 font-semibold' : ''}">Time Out Practice</button>
            <!-- Add more submodules here as needed -->
          </div>
        {/if}
        
        <!-- Final Exam Section -->
        <div class="flex items-center text-left px-3 py-2 hover:bg-green-50 focus:bg-green-100 transition font-medium text-gray-700 gap-2 text-sm w-full {mainSection === 'finalexam' ? 'bg-green-100 text-green-700' : ''}">
          <button on:click={() => mainSection = 'finalexam'} class="flex items-center gap-2 flex-1 text-left">
            <span class="block w-2 h-2 rounded-full {mainSection === 'finalexam' ? 'bg-green-600' : 'bg-green-300'}"></span>
            📝 Final Exam
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
      <Module3 on:navigateToNextSubmodule={() => mainSection = 'module3_unitcutpractice'} />
    {:else if mainSection === 'module3_commercialtimes'}
      <CommercialTimes progressId="module3_commercialtimes" on:navigateToNextSubmodule={() => navigateToNext('module3_commercialtimes')} nextButtonText={getNextButtonText('module3_commercialtimes')} />
    {:else if mainSection === 'module3_brandsep'}
      <BrandSEP progressId="module3_brandsep" on:navigateToNextSubmodule={() => navigateToNext('module3_brandsep')} nextButtonText={getNextButtonText('module3_brandsep')} />
    {:else if mainSection === 'module3_advertiserconflicts'}
      <AdvertiserConflicts progressId="module3_advertiserconflicts" on:navigateToNextSubmodule={() => navigateToNext('module3_advertiserconflicts')} nextButtonText={getNextButtonText('module3_advertiserconflicts')} />
    {:else if mainSection === 'module3_standalonerule'}
      <StandAloneRule on:navigateToNextSubmodule={() => navigateToNext('module3_standalonerule')} nextButtonText={getNextButtonText('module3_standalonerule')} />
    {:else if mainSection === 'module3_unitcutpractice'}
      <UnitCutPractice on:navigateToNextSubmodule={(event) => mainSection = event.detail || 'module3_mcemailpractice'} />
    {:else if mainSection === 'module3_mcemailpractice'}
      <MCEmailPractice on:navigateToNextSubmodule={(event) => mainSection = event.detail || 'module3_timeoutpractice'} />
    {:else if mainSection === 'module3_timeoutpractice'}
      <TimeOutPractice on:navigateToNextSubmodule={goToFinalExam} nextButtonText={getNextButtonText('module3_timeoutpractice')} />
    {:else if mainSection === 'module3_swaps'}
      <Swaps progressId="module3_swaps" on:navigateToNextSubmodule={() => navigateToNext('module3_swaps')} nextButtonText={getNextButtonText('module3_swaps')} />
    {:else if mainSection === 'module3_mastercontrolemail'}
      <MasterControlEmail progressId="module3_mastercontrolemail" on:navigateToNextSubmodule={() => navigateToNext('module3_mastercontrolemail')} nextButtonText={getNextButtonText('module3_mastercontrolemail')} />
    {:else if mainSection === 'module3_localswaps'}
      <LocalSwaps progressId="module3_localswaps" on:navigateToNextSubmodule={() => navigateToNext('module3_localswaps')} nextButtonText={getNextButtonText('module3_localswaps')} />
    {:else if mainSection === 'finalexam'}
      <FinalExam on:navigateToNextSubmodule={() => navigateToNext('finalexam')} nextButtonText="Complete Training" />
    {/if}

  </main>
</div> 
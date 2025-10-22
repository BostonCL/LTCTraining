<script lang="ts">
import { audioStore, setCurrentIndex } from '$lib/stores/audioStore';
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { onMount } from 'svelte';
import { getR2Url } from '$lib/config/r2';

const module2Script = [
  {
    text: "In the Ordered As column you'll see many different types of units. In this module we will go over what they all are. When moving around units this is the first column you will look at.",
    audio: getR2Url('/audio/module-2/module2_intro.mp3'),
    image: getR2Url('/images/introduction/basketballBackground.png'),
    videoAnimation: getR2Url('/images/ballSackm2Intro.webm')
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

// Force reactivity by making it a reactive statement
$: reactiveScript = module2Script;

onMount(() => {
  console.log('Module 2 Intro - module2Script:', module2Script);
  console.log('Module 2 Intro - First slide videoAnimation:', module2Script[0]?.videoAnimation);
  setCurrentIndex(0);
});

$: audioState = $audioStore;
$: isComplete = audioState.currentIndex === module2Script.length - 1 && audioState.progress >= 99;

function handleNext() {
  // Navigate to the first Module 2 submodule
  window.location.href = '/mainMenu/module-2/sellingtitle';
}
</script>

<div style="position: relative; min-height: 60vh;">

  
  <YouTubeTemplate
    script={module2Script}
            title="Module 2: Understanding Units"

    onNextSubmodule={handleNext}
    progressId="module2_intro"
  />
</div> 
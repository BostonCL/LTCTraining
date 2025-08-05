<script lang="ts">
import { audioStore, setCurrentIndex } from '$lib/stores/audioStore';
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { onMount } from 'svelte';

const module2Script = [
  {
    text: "In the Ordered As column you'll see many different types of units. In this module we will go over what they all are. When moving around units this is the first column you will look at. The sold commercials are color coordinated:",
    audio: '/audio/module-2/module2_intro_combined.mp3'
  },
  {
    text: "Here are the different color categories:",
    audio: '/audio/module-2/module2_slide2_combined.mp3',
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
<script lang="ts">
import { audioStore, setCurrentIndex } from '$lib/stores/audioStore';
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { onMount } from 'svelte';

const module2Script = [
  {
    text: "In the Ordered As column you'll see many different types of units. In this module we will go over what they all are. When moving around units this is the first column you will look at.",
    audio: '/audio/module-2/module2_intro.mp3'
  },
  {
    text: "The sold commercials are color coordinated:",
    audio: '/audio/module-2/01-intro/module2_01_part1.mp3'
  },
  {
    text: "Sold commercials (the important stuff) are in YELLOW",
    audio: '/audio/module-2/01-intro/module2_01_part2.mp3',
    whiteboardText: [
      "YELLOW are the SOLD commercials."
    ]
  },
  {
    text: "Local units are PURPLE",
    audio: '/audio/module-2/01-intro/module2_01_part3.mp3',
    whiteboardText: [
      "Locals are PURPLE"
    ]
  },
  {
    text: "Anything in GREEN is cuttable and is not mandatory to air, these will be Drs, PSAs and Promos.",
    audio: '/audio/module-2/01-intro/module2_01_part4.mp3',
    whiteboardText: [
      "GREEN is the first to be cut because they are not worth as much."
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
  // Optionally, dispatch an event or navigate away when done
}
</script>

<div style="position: relative; min-height: 60vh;">

  
  <YouTubeTemplate
    script={module2Script}
    title="Module 2: Tools & Technology"
    isSubmoduleComplete={isComplete}
    onNextSubmodule={handleNext}
    progressId="module2_intro"
  />
</div> 
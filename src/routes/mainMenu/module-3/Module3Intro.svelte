<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

const script = [
  {
    text: "Before we begin this module, here are a few rules when moving units that you need to understand:",
    audio: '/audio/module-3/intro/module3_intro_01.mp3',
    image: '/images/introduction/basketballBackground.png'
  }
];

const videoInfo = {
  title: 'Module 3: Introduction'
};

// Track completion
$: audioState = $audioStore;
$: isComplete = audioState.currentIndex === script.length - 1 && audioState.progress >= 99;

function handleNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate
  script={script}
  title={videoInfo.title}

  onNextSubmodule={handleNext}
  progressId={progressId}
  nextButtonText={nextButtonText}
/> 
<script lang="ts">
import { onMount } from 'svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

const module1Script = [
  { text: 'Welcome to Module 1: Live Coverage Sheet.', audio: '/api/assets/audio/module-1/01-intro/module1_intro.mp3' },
  { text: 'This is what a live coverage sheet looks like.', audio: '/api/assets/audio/module-1/01-intro/module1_01.mp3' },
  { text: 'I know it looks intimidating now but we are going to dive into the details together.', audio: '/api/assets/audio/module-1/01-intro/module1_02.mp3' },
  { text: 'This sheet is separated by columns that we will break down in the following content.', audio: '/api/assets/audio/module-1/01-intro/module1_03.mp3' },
  { text: 'Take a moment and pause the video here so that you can take it all in.', audio: '/api/assets/audio/module-1/01-intro/module1_04.mp3' }
];

const videoInfo = {
  title: 'Module 1: Live Coverage Sheet',
  description: 'This module introduces the live coverage sheet, explains its structure, and prepares you for the details in the following lessons.'
};

const dispatch = createEventDispatcher();

export let progressId: string;
export let nextButtonText: string = "Next";

$: audioState = $audioStore;
$: isComplete = audioState.currentIndex === module1Script.length - 1 && audioState.progress >= 99;

function handleNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<div style="position: relative; min-height: 60vh;">
  <YouTubeTemplate
    script={module1Script}
    title={videoInfo.title}
    image="/api/assets/images/module-1/intro/LiveCoverageCleanWide-0.png"
    onNextSubmodule={handleNext}
    progressId={progressId}
    nextButtonText={nextButtonText}
  />
</div> 
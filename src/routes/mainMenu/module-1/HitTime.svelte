<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

const script = [
  { text: "Right next door is the Hit Time column, this will determine a Mock Schedule. We use Mock Schedules for planning placement of Commercials. Hit Times are not the actual times that commercials air, just estimated placeholders. This column is very important when moving Units around because of a rule called 'Brand SEP.' Brand SEP will be discussed further in Module 3.", audio: '/audio/module-1/03-hit-time/module1_hittime_single.mp3?v=3', image: '/images/module-1/hit-time/HitTime.png' }
];

const videoInfo = {
  title: 'Hit Time',
  description: 'Understand what Hit Time means and how it is used for planning commercial breaks.'
};

// Track completion
$: audioState = $audioStore;
let isComplete = false;

// Check if user has reached the end of the module - multiple conditions
$: if (!isComplete && audioState.currentIndex === script.length - 1) {
  // Condition 1: Progress-based completion
  if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 2 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 2 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 2 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} onNextSubmodule={goNext} progressId={progressId} nextButtonText={nextButtonText} /> 
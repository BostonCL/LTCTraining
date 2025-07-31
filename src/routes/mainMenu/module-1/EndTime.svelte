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
    text: "End Time is the end of each show or game, as soon as the final commercial airs — or when the game ends and transitions to the next program — you'll record the exact end time, down to the second, just like when marking down commercials.",
    audio: '/audio/module-1/end-time/module1_endtime_01.mp3',
    image: '/images/module-1/end-time/EndTimeSheet.png'
  }
];

const videoInfo = {
  title: 'End Time',
  description: 'Understand the End Time column and its importance in commercial timing.'
};

// Track completion
$: audioState = $audioStore;
let isComplete = false;

// Check if user has reached the end of the module - multiple conditions
$: if (!isComplete && audioState.currentIndex === script.length - 1) {
  // Condition 1: Progress-based completion
  if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 10 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 10 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 10 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} image="/images/module-1/end-time/EndTimeSheet.png" onNextSubmodule={goNext} progressId={progressId} nextButtonText={nextButtonText} /> 
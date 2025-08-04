<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

const script = [
  { text: "The Length column tells you the duration of time for each Unit. Adding up the commercial lengths determines how long a Commercial Break will be. This is a common question for producers. Sometimes a break needs to be shorter at the last minute so knowing which units to move is very important. Note: the Program line (the grey row) is never included in the length of the break.", audio: '/audio/module-1/04-length/module1_length_combined.mp3?v=' + Date.now(), image: '/images/module-1/length/Lengthsheet.png?v=' + Date.now() }
];

// Clear any cached progress for this module
if (typeof localStorage !== 'undefined') {
  localStorage.removeItem('progress_module1_length');
}

const videoInfo = {
  title: 'Length',
  description: 'Find out how to determine the length of each commercial break.'
};

// Track completion
$: audioState = $audioStore;
let isComplete = false;

// Check if user has reached the end of the module - multiple conditions
$: if (!isComplete && audioState.currentIndex === script.length - 1) {
  // Condition 1: Progress-based completion
  if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 4 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 4 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 4 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}

function goToQuiz() {
  dispatch('navigateToQuiz');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} onNextSubmodule={goNext} completionButtonText="📝 Take Quiz" onCompletionButtonClick={goToQuiz} progressId={progressId} nextButtonText={nextButtonText} /> 
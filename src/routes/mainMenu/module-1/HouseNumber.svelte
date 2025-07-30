<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

const script = [
  { text: "The House Number column contains a unique ID number for each of the commercials. This is how the MC identifies which ad you're referring to.", audio: '/api/assets/audio/module-1/07-house-number/module1_housenumber_01.mp3' },
  { text: "Since one advertiser, like Geico for example, can have several different ads running during the same program, the House Number is key for identifying which specific commercial you are referencing.", audio: '/api/assets/audio/module-1/07-house-number/module1_housenumber_02.mp3' }
];

const videoInfo = {
  title: 'House Number',
  description: 'Learn why House Numbers are important for identifying commercials.'
};

// Track completion
$: audioState = $audioStore;
let isComplete = false;

// Check if user has reached the end of the module - multiple conditions
$: if (!isComplete && audioState.currentIndex === script.length - 1) {
  // Condition 1: Progress-based completion
  if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 7 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 7 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 7 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}

function goToQuiz() {
  dispatch('navigateToQuiz');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} image="/api/assets/images/module-1/house-number/HouseNumberscreen.png" onNextSubmodule={goNext} completionButtonText="📝 Take Quiz" onCompletionButtonClick={goToQuiz} progressId={progressId} nextButtonText={nextButtonText} /> 
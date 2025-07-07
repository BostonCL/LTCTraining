<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

const script = [
  { text: "Hit Time is a mock schedule used for planning. These aren't the real times commercials air, just estimated placeholders.", audio: '/audio/module-1/03-hit-time/module1_hittime_01.mp3' }
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
  if (audioState.progress >= 70) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 2 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 2 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 50) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 2 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} image="/images/module-1/hit-time/HitTimesheet.png" isSubmoduleComplete={isComplete} onNextSubmodule={goNext} /> 
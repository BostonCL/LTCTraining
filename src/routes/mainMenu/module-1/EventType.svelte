<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

const script = [
  { text: 'Event Type tells you what kind of content it is (like a commercial, promo, local ad, or DR). You can also find this info elsewhere if needed.', audio: '/audio/module-1/08-event-type/module1_eventtype_01.mp3' }
];

const videoInfo = {
  title: 'Event Type',
  description: 'Learn about the different event types and how to identify them.'
};

// Track completion
$: audioState = $audioStore;

let isComplete = false;

// Check if user has reached the end of the module - multiple conditions
$: if (!isComplete && audioState.currentIndex === script.length - 1) {
  // Condition 1: Progress-based completion
  if (audioState.progress >= 70) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 3 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 3 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 50) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 3 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} image="/images/module-1/event-type/EventTypesheet.png" isSubmoduleComplete={isComplete} onNextSubmodule={goNext} /> 
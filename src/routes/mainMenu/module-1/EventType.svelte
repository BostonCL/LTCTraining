<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let isCompleted: boolean = false;

const script = [
  { text: "The Event Type column represents the type of any given Unit.", audio: '/audio/module-1/08-event-type/module1_eventtype_01.mp3' },
  { text: "The different types of Units are: Commercial, Promo, Local, DRs (Direct Response), and PSAs (Public Service Announcements).", audio: '/audio/module-1/08-event-type/module1_eventtype_02.mp3' },
  { text: "Unit Prioritization will be discussed further in Module 2.", audio: '/audio/module-1/08-event-type/module1_eventtype_03.mp3' }
];

const videoInfo = {
  title: 'Event Type',
  description: 'Learn about the different event types and how to identify them.'
};

// Track completion
$: audioState = $audioStore;

let isComplete = false;

// Use the passed isCompleted prop or determine from local state
$: finalIsComplete = isCompleted || isComplete;

// Check if user has reached the end of the module - multiple conditions
$: if (!isComplete && audioState.currentIndex === script.length - 1) {
  // Condition 1: Progress-based completion
  if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 3 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 3 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 3 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} image="/images/module-1/event-type/EventTypesheet.png" isSubmoduleComplete={finalIsComplete} onNextSubmodule={goNext} /> 
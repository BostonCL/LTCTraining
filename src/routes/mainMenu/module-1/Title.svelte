<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let isCompleted: boolean = false;

const script = [
  { text: "The Title column displays the show title and details about specific commercials.", audio: '/audio/module-1/06-title/module1_title_01.mp3' },
  { text: "For example, there could be a note saying 'Obligation,' which means 'IT MUST AIR NO MATTER WHAT.' Or maybe there's a note saying 'Not NFL approved,' meaning it may not air with anything that contains NFL content.", audio: '/audio/module-1/06-title/module1_title_02.mp3' },
  { text: "This column is used to find Advertiser Conflicts, which provide additional information about the advertisers. Advertiser Conflicts will be explored in greater depth in Module 3.", audio: '/audio/module-1/06-title/module1_title_03.mp3' }
];

const videoInfo = {
  title: 'Title',
  description: 'Learn what information is included in the Title field for commercials.'
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
    dispatch('moduleCompleted', { submoduleIndex: 5 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 5 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 5 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} image="/images/module-1/title/Titlescreen.png" isSubmoduleComplete={finalIsComplete} onNextSubmodule={goNext} /> 
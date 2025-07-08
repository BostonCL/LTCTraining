<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let isCompleted: boolean = false;

// Placeholder script, audio, and image. Replace with real content later.
const script = [
  { text: 'The Program line is the gray line that appears before and after each commercial break.', audio: '/audio/module-1/program-line/module1_programline_01.mp3' },
  { text: 'The main details to focus on are, show title and segment number. In this case the show title is "That Other Pregame Show" and the segment number is circled in red. The segment number represents which commercial break you\'re about to enter and is always listed directly above that break.', audio: '/audio/module-1/program-line/module1_programline_02.mp3' },
  { text: 'For example, if you\'re making swaps right below the \'SEG 2\' program line, you\'re working in Break 2.', audio: '/audio/module-1/program-line/module1_programline_03.mp3' }
];

const videoInfo = {
  title: 'Program Line',
  description: 'Learn about the Program Line and its importance in the live coverage sheet.'
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
    dispatch('moduleCompleted', { submoduleIndex: 0 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 0 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 0 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}

// Dynamically set the background image based on the current audio index
$: currentImage =
  audioState.currentIndex === 0
    ? '/images/module-1/program-line/ProgramLinescreen.png'
    : '/images/module-1/program-line/Segmentscreen.png';
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} image={currentImage} isSubmoduleComplete={finalIsComplete} onNextSubmodule={goNext} /> 
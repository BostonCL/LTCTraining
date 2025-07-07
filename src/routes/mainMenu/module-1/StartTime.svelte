<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

const script = [
  { text: 'Start Time is the actual time the game or show begins.', audio: '/audio/module-1/02-start-time-real-time/module1_starttimerealtime_03.mp3' },
  { text: 'For Start Time, let\'s say the game is delayed and starts at 8:03:30 AM. You would write 8:03:30 AM down next to Start Time.', audio: '/audio/module-1/02-start-time-real-time/module1_starttimerealtime_05.mp3' }
];

const videoInfo = {
  title: 'Start Time',
  description: 'Start Time is the actual time the game or show begins.'
};

$: audioState = $audioStore;
let isComplete = false;

$: if (!isComplete && audioState.currentIndex === script.length - 1) {
  if (audioState.progress >= 70) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 11 });
  } else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 11 });
  } else if (audioState.progress >= 50) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 11 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} image="/images/module-1/start-time/LCSheetRS.png" isSubmoduleComplete={isComplete} onNextSubmodule={goNext} /> 
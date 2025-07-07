<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

const script = [
  { text: 'Real Time is the scheduled time that the game or show is supposed to begin.', audio: '/audio/module-1/02-start-time-real-time/module1_starttimerealtime_02.mp3' },
  { text: 'For example: If a show or game is scheduled to begin at 8AM, that is the Real Time. So, you write down 8:00:00 next to Real Time regardless of when it actually begins.', audio: '/audio/module-1/02-start-time-real-time/module1_starttimerealtime_04.mp3' }
];

const videoInfo = {
  title: 'Real Time',
  description: 'Real Time is the scheduled time that the game or show is supposed to begin.'
};

$: audioState = $audioStore;
let isComplete = false;

$: if (!isComplete && audioState.currentIndex === script.length - 1) {
  if (audioState.progress >= 70) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 10 });
  } else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 10 });
  } else if (audioState.progress >= 50) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 10 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} image="/images/module-1/real-time/LCSheetRS.png" isSubmoduleComplete={isComplete} onNextSubmodule={goNext} /> 
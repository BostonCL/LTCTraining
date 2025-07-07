<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';
import { onDestroy } from 'svelte';

const dispatch = createEventDispatcher();

const script = [
  { text: 'Spot End Time is the latest time that specific ad can air.', audio: '/audio/module-1/10-spot-end-time/module1_spotendtime_01.mp3' }
];

const videoInfo = {
  title: 'Spot End Time',
  description: 'Understand the importance of Spot End Time for commercial scheduling.'
};

let isComplete = false;
let unsubscribe: (() => void) | undefined;

onDestroy(() => {
  if (unsubscribe) unsubscribe();
});

unsubscribe = audioStore.subscribe(state => {
  // Check if user has reached the end of the module
  if (!isComplete && state.currentIndex === script.length - 1 && state.progress >= 80) {
    isComplete = true;
    // Dispatch event to mark this submodule as completed (index 9)
    dispatch('moduleCompleted', { submoduleIndex: 9 });
  }
});

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} image="/images/module-1/spot-end-time/SpotEndTimescreen.png" isSubmoduleComplete={isComplete} onNextSubmodule={goNext} /> 
<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';
import { onDestroy } from 'svelte';

const dispatch = createEventDispatcher();

const script = [
  { text: 'Ordered As shows or games the commercial was sold to air with.', audio: '/audio/module-1/09-ordered-as/module1_orderedas_01.mp3' }
];

const videoInfo = {
  title: 'Ordered As',
  description: 'See how the Ordered As field links commercials to specific shows or games.'
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
    // Dispatch event to mark this submodule as completed (index 8)
    dispatch('moduleCompleted', { submoduleIndex: 8 });
  }
});

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} image="/images/module-1/ordered-as/OrderedAsscreen.png" isSubmoduleComplete={isComplete} onNextSubmodule={goNext} /> 
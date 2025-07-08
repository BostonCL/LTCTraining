<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';
import { onDestroy } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let isCompleted: boolean = false;

const script = [
  { text: "The majority of Module 2 will be dedicated to the Ordered As column.", audio: '/audio/module-1/09-ordered-as/module1_orderedas_01.mp3' },
  { text: "In short, the Ordered As column displays what Window a commercial is sold to. This helps us understand where we can place our Commercials.", audio: '/audio/module-1/09-ordered-as/module1_orderedas_02.mp3' }
];

const videoInfo = {
  title: 'Ordered As',
  description: 'See how the Ordered As field links commercials to specific shows or games.'
};

let isComplete = false;
let unsubscribe: (() => void) | undefined;

// Use the passed isCompleted prop or determine from local state
$: finalIsComplete = isCompleted || isComplete;

onDestroy(() => {
  if (unsubscribe) unsubscribe();
});

unsubscribe = audioStore.subscribe(state => {
  // Check if user has reached the end of the module
  if (!isComplete && state.currentIndex === script.length - 1 && state.progress >= 99) {
    isComplete = true;
    // Dispatch event to mark this submodule as completed (index 8)
    dispatch('moduleCompleted', { submoduleIndex: 8 });
  }
});

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} image="/images/module-1/ordered-as/OrderedAsscreen.png" isSubmoduleComplete={finalIsComplete} onNextSubmodule={goNext} /> 
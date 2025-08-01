<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';
import { onDestroy } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let isCompleted: boolean = false;
export let progressId: string;
export let nextButtonText: string = "Next";

const script = [
  { text: "The Spot End Time indicates the latest possible time a specific commercial can air.", audio: '/audio/module-1/10-spot-end-time/module1_spotendtime_01.mp3' },
  { text: "This timing is crucial because airing a commercial past its designated end time can result in missed audience targeting, or contractual violations.", audio: '/audio/module-1/10-spot-end-time/module1_spotendtime_02.mp3' }
];

const videoInfo = {
  title: 'Spot End Time',
  description: 'Understand the importance of Spot End Time for commercial scheduling.'
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
    // Dispatch event to mark this submodule as completed (index 9)
    dispatch('moduleCompleted', { submoduleIndex: 9 });
  }
});

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} image="/images/module-1/spot-end-time/SpotEndTimescreen.png" onNextSubmodule={goNext} progressId={progressId} nextButtonText={nextButtonText} /> 
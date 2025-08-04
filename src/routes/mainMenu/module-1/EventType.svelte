<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

const script = [
	{
		text: "Now let's talk about the Event Type column. The event type column is where you will see what type of event is scheduled to air. This is a very important column because this is how we will time out the rest of the show.",
		audio: '/audio/module-1/08-event-type/module1_eventtype_combined.mp3?v=' + Date.now(),
		image: '/images/module-1/event-type/EventTypesheet.png'
	}
];

// Clear any cached progress for this module
if (typeof localStorage !== 'undefined') {
  localStorage.removeItem('progress_module1_eventtype');
}

const videoInfo = {
	title: 'Event Type'
};

// Track completion
$: audioState = $audioStore;
$: isComplete = audioState.currentIndex === script.length - 1 && audioState.progress >= 99;

function handleNext() {
	dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate
	script={script}
	title={videoInfo.title}
	onNextSubmodule={handleNext}
	progressId={progressId}
	nextButtonText={nextButtonText}
/> 
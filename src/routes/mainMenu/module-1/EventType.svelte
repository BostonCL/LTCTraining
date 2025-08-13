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
		text: "The Event Type column represents the type of any given Unit. The different types of Units are: Commercial, Promo, Local, DRs, and PSAs. Unit Prioritization will be discussed further in Module 2.",
		audio: '/audio/module-1/08-event-type/module1_eventtype_01.mp3',
		image: '/images/module-1/event-type/EventTypesheet.jpg'
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
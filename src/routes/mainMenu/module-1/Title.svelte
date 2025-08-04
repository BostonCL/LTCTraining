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
		text: 'The Title column is where you will see the title of the commercial that is scheduled to air.',
		audio: '/audio/module-1/06-title/module1_title_01.mp3',
		image: '/images/module-1/title/Titlescreen.jpg?v=' + Date.now()
	},
	{
		text: 'This is a very important column because this is how we will time out the rest of the show.',
		audio: '/audio/module-1/06-title/module1_title_02.mp3',
		image: '/images/module-1/title/Titlescreen2.jpg'
	}
];

const videoInfo = {
	title: 'Title'
};

// Track completion
$: audioState = $audioStore;

let isComplete = false;

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
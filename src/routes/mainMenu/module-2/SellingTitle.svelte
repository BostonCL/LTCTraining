<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

// Selling Title script (3 slides)
const script = [
  {
    text: 'Here is a quick term that is important during this section',
    audio: '/api/assets/audio/module-2/selling-title/module2_sellingtitle_01.mp3',
    image: '/api/assets/images/introduction/basketballBackground.png'
  },
  {
    text: 'Everything found in the list above is also called Selling Title. The Selling Title is the word or phrase used to identify the category of a specific commercial.',
    audio: '/api/assets/audio/module-2/selling-title/module2_sellingtitle_02.mp3',
    whiteboardText: [
      'The Selling Title is the word or phrase used to identify the category of a specific commercial.'
    ]
  }
];

const videoInfo = {
  title: 'Selling Title'
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
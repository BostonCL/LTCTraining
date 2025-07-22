<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;

// Commercial Times script (placeholder, update as needed)
const script = [
  {
    text: 'One of our main responsibilities is logging commercial times. You’ll need to watch the entire sporting event and track the commercials as they air to make sure they match what’s on your log sheet.',
    audio: '/audio/module-3/commercial-times/module3_commercialtimes_01.mp3',
    image: '/images/introduction/basketballBackground.png'
  },
  {
    text: 'If you spot any issues — like a commercial that didn’t run — you’ll need to make a swap.',
    audio: '/audio/module-3/commercial-times/module3_commercialtimes_02.mp3',
    image: '/images/introduction/basketballBackground.png'
  }
];

const videoInfo = {
  title: 'Commercial Times'
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
  isSubmoduleComplete={isComplete}
  onNextSubmodule={handleNext}
  progressId={progressId}
/> 
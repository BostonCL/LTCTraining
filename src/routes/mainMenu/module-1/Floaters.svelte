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
    text: "Floaters are occasionally seen underneath the end time section— these are extra sold commercial units that need to air during the game. They're especially common during basketball. For example, if a player gets injured and there's a pause in play, you might run a short 30 second floater. If it's a more serious injury, you could run a longer one, by combining Floaters A and B for a full minute.",
    audio: '/api/assets/audio/module-1/floaters/module1_floaters_01.mp3',
    image: '/api/assets/images/module-1/floaters/FloatersSheet.png'
  },
  {
    text: "Sometimes a Floater will be added to the end of an existing break, but you'll need to be mindful of brand conflicts (which we will go into depth about in Module 3). In this example, if MC wants to add Floater A to Break 12 (the final break), it cannot because there already is a Honda unit in that break.",
    audio: '/api/assets/audio/module-1/floaters/module1_floaters_02.mp3',
    image: '/api/assets/images/module-1/floaters/FloatersSheet.png'
  }
];

const videoInfo = {
  title: 'Floaters',
  description: 'Understand what Floaters are and how they work in the live coverage system.'
};

// Track completion
$: audioState = $audioStore;
let isComplete = false;

// Check if user has reached the end of the module - multiple conditions
$: if (!isComplete && audioState.currentIndex === script.length - 1) {
  // Condition 1: Progress-based completion
  if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 11 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 11 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 11 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} image="/api/assets/images/module-1/floaters/FloatersSheet.png" onNextSubmodule={goNext} progressId={progressId} nextButtonText={nextButtonText} /> 
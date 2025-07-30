<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

// STAND ALONE Rule script (placeholder, update as needed)
const script = [
  {
    text: `STAND ALONE Rule: Alcohol Ad Placement\nCommercials for alcohol brands can never air directly before or after commercials for automotive or insurance companies.`,
    audio: '/api/assets/audio/module-3/stand-alone-rule/module3_standalonerule_01.mp3',
    whiteboardText: [
      'STAND ALONE Rule: Alcohol Ad Placement',
      'Commercials for alcohol brands can never air directly before or after commercials for automotive or insurance companies.'
    ],
    image: '/api/assets/images/introduction/basketballBackground.png'
  },
  {
    text: `Not Allowed:\nAllowed:\nIn this example, the Hershey’s unit creates the necessary separation between the insurance and alcohol units.`,
    audio: '/api/assets/audio/module-3/stand-alone-rule/module3_standalonerule_02.mp3',
    whiteboardText: [
      'Not Allowed:',
      'Allowed:',
      'In this example, the Hershey’s unit creates the necessary separation between the insurance and alcohol units.'
    ],
    image: '/api/assets/images/introduction/basketballBackground.png'
  }
];

const videoInfo = {
  title: 'STAND ALONE Rule'
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
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
    text: `Commercials for alcohol brands can never air directly before or after commercials for automotive or insurance companies.`,
    audio: '/audio/module-3/stand-alone-rule/module3_standalonerule_01.mp3',
    whiteboardText: [
      '**__STAND ALONE Rule__**',
      'Commercials for alcohol brands can never air directly before or after commercials for automotive or insurance companies.'
    ],
    titleAudio: '/audio/module-3/stand-alone-rule/module3_standalonerule_01_title.mp3',
    image: '/images/introduction/basketballBackground.png'
  },
  {
    text: `Not Allowed:\nAllowed:\nIn this example, the Hershey's unit creates the necessary separation between the insurance and alcohol units.`,
    audio: '/audio/module-3/stand-alone-rule/module3_standalonerule_02.mp3',
    titleAudio: '/audio/module-3/stand-alone-rule/module3_standalonerule_02_title.mp3',
    image: '/images/module-3/stand-alone-rule/NotAllowed.jpg',
    imageStyle: 'max-width: 45%; margin-right: 2%;',
    additionalImage: '/images/module-3/stand-alone-rule/Allowed.jpg'
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
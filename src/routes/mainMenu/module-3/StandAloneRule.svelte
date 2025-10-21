<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

  import { getR2Url } from '$lib/config/r2';
const dispatch = createEventDispatcher();

// Props
export let nextButtonText: string = "Next";

// STAND ALONE Rule script (placeholder, update as needed)
const script = [
  {
    text: `Commercials for alcohol brands can never air directly before or after commercials for automotive or insurance companies.`,
    audio: getR2Url('/audio/module-3/stand-alone-rule/module3_standalonerule_01.mp3'),
    whiteboardText: [
      '**__STAND ALONE Rule__**',
      'Commercials for alcohol brands can never air directly before or after commercials for automotive or insurance companies.'
    ],
    titleAudio: getR2Url('/audio/module-3/stand-alone-rule/module3_standalonerule_01_title.mp3'),
    image: getR2Url('/images/introduction/basketballBackground.png')
  },
  {
    text: `Not Allowed:\nAllowed:\nIn the allowed example, you can see the Hershey's unit creates the necessary separation between the insurance and alcohol units.`,
    audio: getR2Url('/audio/module-3/stand-alone-rule/module3_standalonerule_02.mp3'),
    whiteboardText: [
      'Not Allowed:',
      '![Not Allowed](/images/module-3/stand-alone-rule/NotAllowedv2.jpg)',
      'Allowed:',
      '![Allowed](/images/module-3/stand-alone-rule/Allowedv2.jpg)',
      'In this example, the Hershey\'s unit creates the necessary separation between the insurance and alcohol units.'
    ]
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
  progressId="standalone_rule"
  nextButtonText={nextButtonText}
/> 
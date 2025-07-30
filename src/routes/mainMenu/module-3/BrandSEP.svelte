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
    text: `The Brand SEP (Separation) rule requires that all 30-second commercials from the same brand be spaced at least 30 minutes apart.\nIn other words, if you run a 30-second Geico commercial, you must wait at least 30 minutes before airing another 30-second Geico commercial.`,
    audio: '/api/assets/audio/module-3/brand-sep/module3_brandsep_01.mp3',
    whiteboardText: [
      'Brand SEP',
      'The Brand SEP (Separation) rule requires that all 30-second commercials from the same brand be spaced at least 30 minutes apart.',
      'In other words, if you run a 30-second Geico commercial, you must wait at least 30 minutes before airing another 30-second Geico commercial.'
    ],
    image: '/api/assets/images/introduction/basketballBackground.png'
  },
  {
    text: `Additional Guidelines:\n• 15-second ads can run between 30-second ads of the same brand.\n• However, 15-second and 30-second ads cannot appear in the same commercial break. Never schedule more than one commercial from the same brand in the same break.`,
    audio: '/api/assets/audio/module-3/brand-sep/module3_brandsep_02.mp3',
    whiteboardText: [
      'Additional Guidelines:',
      '• 15-second ads can run between 30-second ads of the same brand.',
      '• However, 15-second and 30-second ads cannot appear in the same commercial break. Never schedule more than one commercial from the same brand in the same break.'
    ],
    image: '/api/assets/images/introduction/basketballBackground.png'
  },
  {
    text: `Exceptions:\n• You may break the 30 minute rule during live windows.\n• Also, the Brand Sep resets when starting a new game or show.`,
    audio: '/api/assets/audio/module-3/brand-sep/module3_brandsep_03.mp3',
    whiteboardText: [
      'Exceptions:',
      '• You may break the 30 minute rule during live windows.',
      '• Also, the Brand Sep resets when starting a new game or show.'
    ],
    image: '/api/assets/images/introduction/basketballBackground.png'
  }
];

const videoInfo = {
  title: 'Brand SEP'
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
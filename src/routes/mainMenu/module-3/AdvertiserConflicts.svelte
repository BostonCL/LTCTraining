<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

// Advertiser Conflicts script (placeholder, update as needed)
const script = [
  {
    text: `Advertiser Conflicts also known as Brand Conflicts. Advertiser conflict is when competing brands appear in the same break together. Do not place competing brands in the same break. It is critical to never schedule units from competing brands in the same commercial break.`,
    audio: '/audio/module-3/advertiser-conflicts/module3_advertiserconflicts_01.mp3',
    whiteboardText: [
      'Advertiser Conflicts also known as Brand Conflicts',
      'Advertiser conflict is when competing brands appear in the same break together.',
      'Do not place competing brands in the same break.',
      'It is critical to never schedule units from competing brands in the same commercial break.'
    ],
    image: '/images/introduction/basketballBackground.png'
  },
  {
    text: `For example:\n• Geico and USAA should not air together, as they both sell insurance\n• Lowe’s and Home Depot are direct competitors in home improvement and must also be kept separate.`,
    audio: '/audio/module-3/advertiser-conflicts/module3_advertiserconflicts_02.mp3',
    whiteboardText: [
      'For example:',
      '• Geico and USAA should not air together, as they both sell insurance',
      '• Lowe’s and Home Depot are direct competitors in home improvement and must also be kept separate.'
    ],
    image: '/images/introduction/basketballBackground.png'
  },
  {
    text: `If you’re unsure what a specific brand or unit is, research or ask the Traffic Department to confirm.`,
    audio: '/audio/module-3/advertiser-conflicts/module3_advertiserconflicts_03.mp3',
    whiteboardText: [
      'If you’re unsure',
      'If you’re unsure what a specific brand or unit is,',
      'research or ask the Traffic Department to confirm.'
    ],
    image: '/images/introduction/basketballBackground.png'
  },
  {
    text: `Why this matters:\nIf competing brands appear in the same break, the network will not get paid for either commercial, which results in a significant financial loss.`,
    audio: '/audio/module-3/advertiser-conflicts/module3_advertiserconflicts_04.mp3',
    whiteboardText: [
      'Why this matters:',
      'If competing brands appear in the same break,',
      'the network will not get paid for either commercial,',
      'which results in a significant financial loss.'
    ],
    image: '/images/introduction/basketballBackground.png'
  }
];

const videoInfo = {
  title: 'Advertiser Conflicts'
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
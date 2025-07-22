<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;

const script = [
  {
    text: `Before we begin this module, here are a few rules when moving units that you need to understand:`,
    audio: '/audio/module-3/intro/module3_intro_01.mp3',
    image: '/images/introduction/basketballBackground.png'
  },
  {
    text: `The Brand SEP (Separation) rule requires that all 30-second commercials from the same brand be spaced at least 30 minutes apart.\nIn other words, if you run a 30-second Geico commercial, you must wait at least 30 minutes before airing another 30-second Geico commercial.\nAdditional Guidelines:\n15-second ads can run between 30-second ads of the same brand.\nHowever, 15-second and 30-second ads cannot appear in the same commercial break. Never schedule more than one commercial from the same brand in the same break\nExceptions:\nYou may break the 30 minute rule during live windows.\nAlso, the Brand Sep resets when starting a new game or show.`,
    audio: '/audio/module-3/intro/module3_intro_02.mp3',
    whiteboardText: [
      'Brand SEP',
      '30s same brand: 30 min apart',
      '15s can run between 30s',
      'Never 15s & 30s in same break',
      'Never >1 same brand per break',
      'Exceptions: live windows, new show resets'
    ]
  },
  {
    text: `Advertiser Conflicts also known as Brand Conflicts. Advertiser conflict is when competing brands appear in the same break together. Do not place competing brands in the same break.\nIt is critical to never schedule units from competing brands in the same commercial break.\nFor example:\nGeico and USAA should not air together, as they both sell insurance.\nLowe’s and Home Depot are direct competitors in home improvement and must also be kept separate.\nIf you’re unsure what a specific brand or unit is, research or ask the Traffic Department to confirm.\nWhy this matters:\nIf competing brands appear in the same break, the network will not get paid for either commercial, which results in a significant financial loss.`,
    audio: '/audio/module-3/intro/module3_intro_03.mp3',
    whiteboardText: [
      'Advertiser/Brand Conflicts',
      'Never place competing brands in same break',
      'Ex: Geico & USAA, Lowe’s & Home Depot',
      'Ask if unsure!'
    ]
  },
  {
    text: `STAND ALONE Rule: Alcohol Ad Placement. Commercials for alcohol brands can never air directly before or after commercials for automotive or insurance companies.\nNot Allowed:\nAllowed:\nIn this example, the Hershey’s unit creates the necessary separation between the insurance and alcohol units.`,
    audio: '/audio/module-3/intro/module3_intro_04.mp3',
    whiteboardText: [
      'STAND ALONE Rule: Alcohol Ad Placement',
      'Alcohol cannot air before/after auto or insurance',
      'Use other units to separate them'
    ]
  }
];

const videoInfo = {
  title: 'Module 3: Introduction'
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
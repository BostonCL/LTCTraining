<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

// Commercial Times script (placeholder, update as needed)
const script = [
  {
    text: `One of our main responsibilities is logging commercial times. You'll need to watch the entire sporting event and track the commercials as they air to make sure they match what's on your log sheet. If you spot any issues — like a commercial that didn't run — you'll need to make a swap.`,
    audio: '/audio/module-3/commercial-times/module3_commercialtimes_01.mp3',
    whiteboardText: [
      '**__Write down commercial times__**',
      'One of our main responsibilities is logging commercial times.',
      'Track the commercials as they air to make sure they match what\'s on your log sheet.',
      'If you spot any issues — like a commercial that didn\'t run — you\'ll need to make a swap.'
    ],
    titleAudio: '/audio/module-3/commercial-times/module3_commercialtimes_01_title.mp3',
    image: '/images/introduction/basketballBackground.png'
  },
  {
    text: `You’ll also stay on the phone with the producer, and MC, listening for their countdowns. When they reach ‘one,’ you’ll record the exact time the commercial airs. For example, if it airs at 8:05:32, you’ll write down ‘8:05:32,’ as shown on this Live Coverage Sheet.`,
    audio: '/audio/module-3/commercial-times/module3_commercialtimes_02.mp3',
    image: '/images/module-3/commercial-times/CommercialTimes.png'
  },
  {
    text: `Usually, if a commercial is going to be cut, they’ll mention it over the phone line and ask for your input on which one should be dropped.`,
    audio: '/audio/module-3/commercial-times/module3_commercialtimes_03.mp3',
    image: '/images/module-3/commercial-times/CommercialTimes.png'
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

  onNextSubmodule={handleNext}
  progressId={progressId}
  nextButtonText={nextButtonText}
/> 
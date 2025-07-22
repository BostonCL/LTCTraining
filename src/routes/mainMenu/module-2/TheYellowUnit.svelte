<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;

// The Yellow Unit script (updated to a single animation slide)
const script = [
  {
    text: `Let’s start with the basics: The Yellow Unit category. On the next slide, they are listed from most to least important. As you might remember, they are located in the “Ordered As” column on the live coverage sheet.`,
    audio: '/audio/module-2/yellow-unit/module2_yellowunit_01.mp3',
    image: '/images/introduction/basketballBackground.png'
  },
  {
    text: 'This is our Unit Prioritization List, ranked from highest to lowest importance.',
    audio: '/audio/module-2/yellow-unit/module2_yellowunit_02.mp3',
    whiteboardText: ['Unit Prioritization List']
  },
  {
    text: 'Show Specific',
    audio: '/audio/module-2/yellow-unit/module2_yellowunit_03.mp3',
    whiteboardText: ['Unit Prioritization List', '1st) Show Specific']
  },
  {
    text: 'Sports Spectacular',
    audio: '/audio/module-2/yellow-unit/module2_yellowunit_04.mp3',
    whiteboardText: ['Unit Prioritization List', '1st) Show Specific', '2nd) Sports Spectacular']
  },
  {
    text: 'ROS 24 Hour',
    audio: '/audio/module-2/yellow-unit/module2_yellowunit_05.mp3',
    whiteboardText: ['Unit Prioritization List', '1st) Show Specific', '2nd) Sports Spectacular', '3rd) ROS 24 Hour']
  },
  {
    text: 'ROS Prime',
    audio: '/audio/module-2/yellow-unit/module2_yellowunit_06.mp3',
    whiteboardText: ['Unit Prioritization List', '1st) Show Specific', '2nd) Sports Spectacular', '3rd) ROS 24 Hour', '4th) ROS Prime']
  },
  {
    text: 'Studio Encore/ Sports Encore',
    audio: '/audio/module-2/yellow-unit/module2_yellowunit_07.mp3',
    whiteboardText: ['Unit Prioritization List', '1st) Show Specific', '2nd) Sports Spectacular', '3rd) ROS 24 Hour', '4th) ROS Prime', '5th) Studio Encore/ Sports Encore']
  }
];

const videoInfo = {
  title: 'The Yellow Unit'
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
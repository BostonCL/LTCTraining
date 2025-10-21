<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';
import { getR2Url } from '$lib/config/r2';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

// The Yellow Unit script (updated to combine slides 2 & 3)
const script = [
  {
    text: `Let's start with the basics: The Yellow Unit category. On the next slide, they are listed from most to least important. As you might remember, they are located in the "Ordered As" column on the live coverage sheet.`,
    audio: getR2Url('/audio/module-2/yellow-unit/module2_yellowunit_01.mp3'),
    image: getR2Url('/images/introduction/basketballBackground.png'),
    videoAnimation: getR2Url('/images/ballsackm2s2_yellow_unit.mov')
  },
  {
    text: `This is our Unit Prioritization List, ranked from highest to lowest importance. Starting with Show Specific, which is the highest priority.`,
    audio: getR2Url('/audio/module-2/yellow-unit/module2_yellowunit_02_03_combined.mp3'),
    whiteboardText: ['**__Unit Prioritization List__**', '• **Show Specific**']
  },
  {
    text: 'Sports Spectacular',
    audio: getR2Url('/audio/module-2/yellow-unit/module2_yellowunit_04.mp3'),
    whiteboardText: ['**__Unit Prioritization List__**', '• **Show Specific**', '• **Sports Spectacular**']
  },
  {
    text: 'ROS 24 Hour',
    audio: getR2Url('/audio/module-2/yellow-unit/module2_yellowunit_05.mp3'),
    whiteboardText: ['**__Unit Prioritization List__**', '• **Show Specific**', '• **Sports Spectacular**', '• **ROS 24 Hour**']
  },
  {
    text: 'ROS Prime',
    audio: getR2Url('/audio/module-2/yellow-unit/module2_yellowunit_06.mp3'),
    whiteboardText: ['**__Unit Prioritization List__**', '• **Show Specific**', '• **Sports Spectacular**', '• **ROS 24 Hour**', '• **ROS Prime**']
  },
  {
    text: 'Studio Encore/ Sports Encore',
    audio: getR2Url('/audio/module-2/yellow-unit/module2_yellowunit_07.mp3'),
    whiteboardText: ['**__Unit Prioritization List__**', '• **Show Specific**', '• **Sports Spectacular**', '• **ROS 24 Hour**', '• **ROS Prime**', '• **Studio Encore/ Sports Encore**']
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
  onNextSubmodule={handleNext}
  nextButtonText={nextButtonText}
  progressId={progressId}
/> 
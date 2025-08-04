<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

// Unit Prioritization Details script (placeholder, update as needed)
const script = [
  {
    text: `Let's dive into the details regarding each one.`,
    audio: '/audio/module-2/unit-prioritization-details/module2_unitprioritizationdetails_01.mp3',
    image: '/images/introduction/basketballBackground.png'
  },
  {
    text: `“These units are worth the most money. They are mandatory to air. If a unit with this selling title gets CUT we save it. They are typically sold to that specific show/game, so you need to make sure it airs in that show/game with the same units in it. For example, “T.O.P.S.” (“That Other Pregame Show”, which is a talk show) is a show specific unit. “T.O.P.S.” can only be placed within that show. So if a unit gets cut in the last break and we are immediately going to a basketball game, that “T.O.P.S.”  unit CANNOT go anywhere else and is dead.”`,
    audio: '/audio/module-2/unit-prioritization-details/module2_unitprioritizationdetails_02.mp3',
    whiteboardText: ['**__Show Specific__**', 'High-value, mandatory units tied to specific shows/games'],
    titleAudio: '/audio/module-2/unit-prioritization-details/module2_unitprioritizationdetails_02_title.mp3'
  },
  {
    text: `“These units carry the highest dollar value and are mandatory to air. If a unit with this title is cut, it must be saved. Unlike show-specific units, these are flexible and can be placed in any show or game airing later in the night that contains Sports Spectacular units.”`,
    audio: '/audio/module-2/unit-prioritization-details/module2_unitprioritizationdetails_03.mp3',
    whiteboardText: ['**__Sports Spectacular__**', 'High-value, mandatory units with limited placement flexibility'],
    titleAudio: '/audio/module-2/unit-prioritization-details/module2_unitprioritizationdetails_03_title.mp3'
  },
  {
    text: `“ROS 24 Hour units are the most universal units, meaning they can go in any window. They are high-value but the most versatile, able to air throughout the day and night, which makes them easy to move or reassign. However, be aware that their spot end times may restrict where they can be placed.”`,
    audio: '/audio/module-2/unit-prioritization-details/module2_unitprioritizationdetails_04.mp3',
    whiteboardText: ['**__ROS 24 Hour__**', 'High-value, easy to move units, just watch the end times.'],
    titleAudio: '/audio/module-2/unit-prioritization-details/module2_unitprioritizationdetails_04_title.mp3'
  },
  {
    text: `“ROS Prime units are similar to ROS 24-hour units but are restricted to a specific airing window between 7 PM and 12 AM. Due to this limited time frame, they are challenging to reposition, so it’s best to avoid cutting them. However, they remain eligible to run in any window.”`,
    audio: '/audio/module-2/unit-prioritization-details/module2_unitprioritizationdetails_05.mp3',
    whiteboardText: ['**__ROS Prime__**', 'Time restricted: 7 PM to 12 AM'],
    titleAudio: '/audio/module-2/unit-prioritization-details/module2_unitprioritizationdetails_05_title.mp3'
  },
  {
    text: `“These are zero-dollar units typically aired during re-runs of previous shows. Since they don’t generate revenue, they are usually safe to cut. The exception is PBR Encore units, which despite the “encore” label are treated as show-specific and must always be preserved. Remember, show-specific units are never cut.”`,
    audio: '/audio/module-2/unit-prioritization-details/module2_unitprioritizationdetails_06.mp3',
    whiteboardText: ['**__Studio Encore/ Sports Encore__**', 'The first units to cut in sold inventory'],
    titleAudio: '/audio/module-2/unit-prioritization-details/module2_unitprioritizationdetails_06_title.mp3'
  }
];

const videoInfo = {
  title: 'Unit Prioritization Details'
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
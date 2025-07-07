<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

const script = [
  { text: 'This is the start of the Real Time & Start Time section.', audio: '/audio/module-1/02-start-time-real-time/module1_starttimerealtime_00.mp3' },
  { text: 'Here we will discuss Real Time and Start Time:', audio: '/audio/module-1/02-start-time-real-time/module1_starttimerealtime_01.mp3' },
  { text: 'Real Time: Real Time is the scheduled time that the game or show is supposed to begin.', audio: '/audio/module-1/02-start-time-real-time/module1_starttimerealtime_02.mp3' },
  { text: 'Start Time: Start Time is the actual time the game or show begins.', audio: '/audio/module-1/02-start-time-real-time/module1_starttimerealtime_03.mp3' },
  { text: 'For example: If a show or game is scheduled to begin at 8AM, that is the Real Time. So, you write down 8:00:00 next to Real Time regardless of when it actually begins.', audio: '/audio/module-1/02-start-time-real-time/module1_starttimerealtime_04.mp3' },
  { text: 'But for Start Time, let\'s say the game is delayed and starts at 8:03:30 AM. You would write 8:03:30 AM down next to Start Time.', audio: '/audio/module-1/02-start-time-real-time/module1_starttimerealtime_05.mp3' },
  { text: 'This is how the Real Time/ Start Time column would appear in this example:', audio: '/audio/module-1/02-start-time-real-time/module1_starttimerealtime_06.mp3' }
];

const videoInfo = {
  title: 'Start Time & Real Time',
  description: 'Real Time is the scheduled time that the game or show is supposed to begin. Start Time is the actual time the game or show begins. For example: If a show or game is scheduled to begin at 8AM, that is the Real Time. So, you write down 8:00:00 next to Real Time regardless of when it actually begins. But for Start Time, let\'s say the game is delayed and starts at 8:03:30 AM. You would write 8:03:30 AM down next to Start Time.'
};

let currentIndex = 0;
let isModuleComplete = false;

// Subscribe to audio store
$: audioState = $audioStore;
$: currentIndex = audioState.currentIndex;

// Debug logging to see what's happening
$: console.log('Audio state:', {
  currentIndex: audioState.currentIndex,
  progress: audioState.progress,
  isPlaying: audioState.isPlaying,
  scriptLength: script.length,
  isLastClip: audioState.currentIndex === script.length - 1,
  isModuleComplete
});

// Check if user has reached the end of the module - multiple conditions
$: if (!isModuleComplete && audioState.currentIndex === script.length - 1) {
  // Condition 1: Progress-based completion
  if (audioState.progress >= 70) {
    console.log('Module completed via progress! Dispatching event...');
    isModuleComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 0 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    console.log('Module completed via audio end! Dispatching event...');
    isModuleComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 0 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 50) {
    console.log('Module completed via partial progress! Dispatching event...');
    isModuleComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 0 });
  }
}

// Always use the same image for all slides
$: image = '/images/module-1/start-time-real-time/LCSheetRS.png';

function goToQuiz() {
  dispatch('navigateToQuiz');
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}

</script>

<div class="relative">
  <YouTubeTemplate
    script={script}
    title={videoInfo.title}
    description={videoInfo.description}
    image={image}
    showAvatar={false}
    isSubmoduleComplete={isModuleComplete}
    onNextSubmodule={goNext}
  />
</div> 
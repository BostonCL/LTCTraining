<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

const script = [
  { text: 'Advertiser is who the ad is from.', audio: '/audio/module-1/05-advertiser/module1_advertiser_01.mp3' }
];

const videoInfo = {
  title: 'Advertiser',
  description: 'Understand the importance of the Advertiser field in commercial logs.'
};

// Track completion
$: audioState = $audioStore;

let isComplete = false;

// Check if user has reached the end of the module - multiple conditions
$: if (!isComplete && audioState.currentIndex === script.length - 1) {
  // Condition 1: Progress-based completion
  if (audioState.progress >= 70) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 6 });
  }
  // Condition 2: Audio finished playing
  else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 6 });
  }
  // Condition 3: User has been on last clip for a while
  else if (audioState.progress >= 50) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 6 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} image="/images/module-1/advertiser/Advertiserscreen.png" isSubmoduleComplete={isComplete} onNextSubmodule={goNext} /> 
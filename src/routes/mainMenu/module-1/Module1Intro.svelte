<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const module1Script = [
  { text: "Welcome to module 1! Now, let's begin!", audio: '/audio/module-1/01-intro/module1_intro.mp3' },
  { text: "This is an example of a Live Coverage Sheet. Before each shift, you will receive an email containing a Live Coverage Sheet. This spreadsheet tells us when specific Commercials will air. It is separated by columns that we will break down later on in this module.", audio: '/audio/module-1/01-intro/module1_01.mp3' },
  { text: "Pause here for a moment so that you can take it all in...", audio: '/audio/module-1/01-intro/module1_02.mp3' },
  { text: "Thoroughly understanding the Live Coverage Sheet is crucial to ensuring that you can effectively manage Unit placement during live games, where adjustments are often necessary due to Unit cuts. Each column contains critical information that determines whether a Unit can or cannot be assigned to a specific place on the Live Coverage Sheet.", audio: '/audio/module-1/01-intro/module1_03.mp3' },
  { text: "Let's start at the Program line", audio: '/audio/module-1/01-intro/module1_04.mp3' }
];

const videoInfo = {
  title: 'Module 1: Live Coverage Sheet',
  description: 'This module introduces the live coverage sheet, explains its structure, and prepares you for the details in the following lessons.'
};

const dispatch = createEventDispatcher();

let isComplete = false;
$: audioState = $audioStore;

$: if (!isComplete && audioState.currentIndex === module1Script.length - 1) {
  if (audioState.progress >= 70) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: -1 });
  } else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: -1 });
  } else if (audioState.progress >= 50) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: -1 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate
  script={module1Script}
  title={videoInfo.title}
  description={videoInfo.description}
  image="/images/module-1/intro/LiveCoverageCleanWide-0.png"
  showAvatar={false}
/>
{#if isComplete}
  <div class="flex justify-end mt-8">
    <button class="px-6 py-3 rounded-lg bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 transition" on:click={goNext}>
      Next →
    </button>
  </div>
{/if} 
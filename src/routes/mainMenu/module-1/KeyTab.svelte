<script lang="ts">
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';
  import { audioStore, setCurrentIndex } from '$lib/stores/audioStore';
  import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

  const dispatch = createEventDispatcher();

  // Props
  export let progressId: string;
  export let nextButtonText: string = "Next";

  const keyTabScript = [
    {
      text: "In the bottom left-hand corner of this Excel file, you'll see two tabs: 'Key' and 'Coverage.' All that we have discussed so far is found in the Coverage tab. You'll spend most of your time working in the Coverage tab, but occasionally you'll need to refer to the Key tab. Keep in mind that some information on the Key tab is outdated, so focus only on the important information explained here.",
      audio: '/audio/module-1/keytab/keytab_01.mp3',
      image: '/images/module-1/keytab/KeyTab.png'
    },
    {
      text: "Contingency Plan: This plan outlines what to do if a game runs long — for example, which shows might be cut or adjusted.",
      audio: '/audio/module-1/keytab/keytab_02.mp3',
      image: '/images/module-1/keytab/KeyTab2.png'
    },
    {
      text: "Live Coverage Reports: At the end of your shift, you will send out a Live Coverage Report. The list of email recipients is listed below the Live Coverage Reports section.",
      audio: '/audio/module-1/keytab/keytab_03.mp3',
      image: '/images/module-1/keytab/KeyTab3.jpg'
    },
    {
      text: "One more thing to note: at the top of the sheet, you'll see a color code. The important colors to remember are: Yellow (Commercial), Red (CUT), Blue (Moved From). There will be more information about these color codes and their significance in Module 3.",
      audio: '/audio/module-1/keytab/keytab_04.mp3',
      image: '/images/module-1/keytab/KeyTab4.png'
    }
  ];

  // Force reactivity by making it a reactive statement
  $: reactiveScript = keyTabScript;

  onMount(() => {
    setCurrentIndex(0);
  });

  $: audioState = $audioStore;
  $: isComplete = audioState.currentIndex === keyTabScript.length - 1 && audioState.progress >= 99;

  function handleNext() {
    // Dispatch event to navigate to the next submodule
    dispatch('navigateToNextSubmodule');
  }
</script>

<div style="position: relative; min-height: 60vh;">
  <YouTubeTemplate
    script={keyTabScript}
    title="Key Tab"
    onNextSubmodule={handleNext}
    progressId={progressId}
    nextButtonText={nextButtonText}
  />
</div> 
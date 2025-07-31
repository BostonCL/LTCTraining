<script lang="ts">
  import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
  import { audioStore } from '$lib/stores/audioStore';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let progressId: string;
  export let nextButtonText: string = "Next";

  function handleNext() {
    dispatch('navigateToNextSubmodule');
  }

  const script = [
    {
      text: 'Welcome to this section. Where we will learn how to properly swap units within the live coverage sheet.',
      audio: '/audio/module-3/swaps/module3_swaps_01.mp3',
      image: '/images/module-3/Swaps1.png',
    },
    {
      text: 'In this section, we’ll walk through each step you need to follow to make sure your swaps are accurate and compliant.',
      audio: '/audio/module-3/swaps/module3_swaps_02.mp3',
      image: '/images/module-3/Swaps1.png',
    },
    {
      text: 'Let’s begin with an example scenario. Suppose we are approaching the end of a game, and the producer requests a thirty-second cut from Break 11.',
      audio: '/audio/module-3/swaps/module3_swaps_03.mp3',
      image: '/images/module-3/Swaps2.png',
    },
    {
      text: 'We identify that the Jersey Mike’s unit needs to be swapped because This Major League Fishing unit is sold exclusively to the current window and cannot air in any other window for the rest of the day. Since local units can only be moved when the producer specifically requests it, we cannot cut it. This leaves the thirty-second Jersey Mike’s unit as the only option to move.',
      audio: '/audio/module-3/swaps/module3_swaps_04.mp3',
      image: '/images/module-3/Swaps3.png',
    },
    {
      text: 'Now, let’s go through the steps you need to follow.',
      audio: '/audio/module-3/swaps/module3_swaps_05.mp3',
      image: '/images/module-3/Swaps1.png',
    },
    {
      text: 'Step 1 is to check the Ordered As column. Here, you confirm the unit type. In this case, it is a sports spec unit, which means it can be moved to the next show.',
      audio: '/audio/module-3/swaps/module3_swaps_06.mp3',
      image: '/images/module-3/Swaps4.png',
    },
    {
      text: 'Step 2 is to verify the spot end time. The unit has a 1 AM spot end time. Now keep that in mind when moving it.',
      audio: '/audio/module-3/swaps/module3_swaps_07.mp3',
      image: '/images/module-3/Swaps5.png',
    },
    {
      text: 'Step 3 is to check the unit length. This unit is thirty seconds long. Remember to keep brand separation in mind, but also keep in mind that brand separation rules can be broken during a live window.',
      audio: '/audio/module-3/swaps/module3_swaps_08.mp3',
      image: '/images/module-3/Swaps6.png',
    },
    {
      text: 'Step 4 is to identify which break to cut the inventory from. Let\'s look at Break 1 of the 2PM window. Looks like there is 30 seconds of unsold inventory so this is a good option. Note the spot end time. It is valid to move it into the 2 P M window, it is still within its airing period and is sports spec approved.',
      audio: '/audio/module-3/swaps/module3_swaps_09.mp3',
      image: '/images/module-3/Swaps7.png',
    },
    {
      text: 'Step 5 is to check for brand conflicts within that identified break. Since Jersey Mike\'s is a restaurant, you need to make sure there is no other restaurant brand in the new break. If there is no conflict, we can continue.',
      audio: '/audio/module-3/swaps/module3_swaps_10.mp3',
      image: '/images/module-3/Swaps8.png',
    },
    {
      text: 'Step 6 is to mark the unit status. When a unit is not airing in a break, highlight it red. Red means that the commercial did not air in that break. It can mean that the unit was cut or that it was moved to another break. This is why it is so important to include clear notes next to it. We recommend making clear notations as you go, to avoid confusion later.',
      audio: '/audio/module-3/swaps/module3_swaps_11.mp3',
      image: '/images/module-3/Swaps9.png',
    },
    {
      text: 'Step 7 is to notate the move. Write a note that says: Moved to B one of the 2 P. This means the unit is being moved to Break 1 of the 2 PM window.',
      audio: '/audio/module-3/swaps/module3_swaps_12.mp3',
      image: '/images/module-3/Swaps10.png',
    },
    {
      text: 'Step 8 is to make the cut. We found thirty seconds of green (unsold) inventory in Break One. Double-check that there is no brand conflict. Highlight this inventory red and add a note that says CUT next to it.',
      audio: '/audio/module-3/swaps/module3_swaps_13.mp3',
      image: '/images/module-3/Swaps11.png',
    },
    {
      text: 'Step 9 is to move the unit. Insert a new line within Break 1 and copy and paste the Jersey Mike\'s unit into its new position.',
      audio: '/audio/module-3/swaps/module3_swaps_14.mp3',
      image: '/images/module-3/Swaps12.png',
    },
    {
      text: 'Step 10 is to finalize the notation. On the line you inserted, write moved from B 11 of the 12 PM. Highlight the unit light blue. Blue means that it aired in this break. At this point, the Jersey Mike\'s unit is now properly marked on the live coverage sheet.',
      audio: '/audio/module-3/swaps/module3_swaps_15.mp3',
      image: '/images/module-3/Swaps13.png',
    },
    {
      text: 'Before we wrap up, here are a few key reminders. Always use clear, consistent color coding. Red means the unit did not air here or was moved. Blue means it aired here.',
      audio: '/audio/module-3/swaps/module3_swaps_16.mp3',
    },
    {
      text: 'Always double-check for brand conflicts. Document every move you make to avoid mistakes. And keep your notes organized so you can easily track your changes.',
      audio: '/audio/module-3/swaps/module3_swaps_17.mp3',
    },
    {
      text: 'In the next module, we will learn how to document these adjustments in emails.',
      audio: '/audio/module-3/swaps/module3_swaps_18.mp3',
    },
  ];

  function noop() {}
</script>

<YouTubeTemplate
  script={script}
  title="Swaps (Module 3)"
  progressId={progressId}
  onNextSubmodule={handleNext}
  nextButtonText={nextButtonText}
/> 
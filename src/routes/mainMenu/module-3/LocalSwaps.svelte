<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

export let isCompleted: boolean = false;
export let progressId: string;
export let nextButtonText: string = "Next";

const script = [
  {
    text: "In this section, we will learn how to swap local units when a producer requests it. Let's look at an example. Imagine the producer has to cut 2 minutes from the break we're working in. They decide to cut the local unit. Remember — locals are always 1 minute and :30 seconds long. So, they cut the local unit (1 minute and :30 seconds) plus the :30 seconds Jersey Mike's spot. That adds up to exactly 2 minutes cut from the break.",
    audio: '/audio/module-3/local-swaps/module3_localswaps_01.mp3',
    image: '/images/module-3/local-swaps/Local1.png'
  },
  {
    text: "Now, that local unit is gone from its original spot — but you can't just leave it like that. You must find a new place in the schedule to air that local unit.",
    audio: '/audio/module-3/local-swaps/module3_localswaps_02.mp3',
    image: '/images/module-3/local-swaps/Local2.png'
  },
  {
    text: "Key rules to remember: You must always find swaps for locals. You have to find the exact same amount of time (1 minute and :30 seconds) somewhere else in the schedule. Locals can never air in the same break as another local. They can be in back-to-back breaks, but never together in the same break.",
    audio: '/audio/module-3/local-swaps/module3_localswaps_03.mp3',
    image: '/images/module-3/local-swaps/Local2.png'
  },
  {
    text: "Start by looking for cuttable units. I like to check the green inventory — that's usually the easiest to cut. Sometimes I'll go deep into the overnight hours because it's simpler there.",
    audio: '/audio/module-3/local-swaps/module3_localswaps_04.mp3',
    image: '/images/module-3/local-swaps/Local3.jpg'
  },
  {
    text: "Once you find cuttable units: Mark those units as cut (turn them red). This means they won't air in that break anymore. Next, insert a line for the local unit you're moving. Notate everything as you go.",
    audio: '/audio/module-3/local-swaps/module3_localswaps_05.mp3',
    image: '/images/module-3/local-swaps/Local5.png'
  },
  {
    text: "In this example, we're moving the local unit into Break 5 of the 10 PM game. When you email MC, update the title to: 'Here are the swaps to save 2 minutes from Break 11 of the 12 PM game.' Note the new location: 10 PM game Break 5 CUT: 600812 and 609735 IN: 1:30 local, please use a fill list",
    audio: '/audio/module-3/local-swaps/module3_localswaps_06.mp3',
    image: '/images/module-3/local-swaps/Local6.png'
  },
  {
    text: "Why does this matter? On the traffic side, these schedules already have sold commercials in place. If you just swap in a local unit without using the fill list, it can conflict with other units, create wrong end times, and worst of all, the commercials may not air correctly — which means we wouldn't get paid for them. Using the fill list keeps everything clean. The local network still gets the promised time, and if there's leftover time, PSAs will run instead. The fill list is just a bunch of PSAs that won't conflict with anything else in the break.",
    audio: '/audio/module-3/local-swaps/module3_localswaps_07_08_combined.mp3',
    image: '/images/module-3/local-swaps/Local2.png'
  },
  {
    text: "Then, paste the local unit into its new spot. Mark it blue to show it's airing there.",
    audio: '/audio/module-3/local-swaps/module3_localswaps_09.mp3',
    image: '/images/module-3/local-swaps/Local9.png'
  },
  {
    text: "Add a note that says: 'Moved to Break 5 of the 10 PM game.'",
    audio: '/audio/module-3/local-swaps/module3_localswaps_10.mp3',
    image: '/images/module-3/local-swaps/Local10.png'
  },
  {
    text: "Add a note that says: 'Moved from Break 11 of the 12 PM game.' After you insert the local: In your spreadsheet, mark it as \"No fill\".",
    audio: '/audio/module-3/local-swaps/module3_localswaps_10_11_combined.mp3',
    image: '/images/module-3/local-swaps/Local11.png'
  },
  {
    text: "Finally, double-check that everything is correct:\nThe local is marked as moved to Break 5 of the 10 PM game.\nIt's noted as moved from Break 11 of the 12 PM game.\nAll cuts, moves, and fills are noted.\nYour colors are correct: red means cut, blue means airing.\n\nAnd that's how you swap locals!\nDuring the game, if things are running smoothly and commercials are airing as planned, start preparing a backup plan in case the game does go over.",
    audio: '/audio/module-3/local-swaps/module3_localswaps_11_12_combined.mp3',
    image: '/images/module-3/local-swaps/Local10.png'
  }
];

const videoInfo = {
  title: 'Local Swaps',
  description: 'Learn about Local Swaps and their specific requirements in the Traffic Department.'
};

$: audioState = $audioStore;
let isComplete = false;
$: finalIsComplete = isCompleted || isComplete;

$: if (!isComplete && audioState.currentIndex === script.length - 1) {
  if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 0 });
  } else if (!audioState.isPlaying && audioState.progress > 0) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 0 });
  } else if (audioState.progress >= 99) {
    isComplete = true;
    dispatch('moduleCompleted', { submoduleIndex: 0 });
  }
}

function goNext() {
  dispatch('navigateToNextSubmodule');
}
</script>

<YouTubeTemplate 
  script={script} 
  title={videoInfo.title} 
  image="/images/module-3/local-swaps/Swaps13.png" 
 
  onNextSubmodule={goNext} 
  progressId={progressId} 
  nextButtonText={nextButtonText} 
/> 
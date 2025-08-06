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
    text: "In this section, we are going to learn how to properly document commercial swaps and send them to MC, so they can make the same changes on their end.",
    audio: '/audio/module-3/master-control-email/module3_mastercontrol_01.mp3',
    image: '/images/module-3/master-control-email/Swaps13.png'
  },
  {
    text: "First, always start your email by clearly explaining what swap you're making. For example, you could write: 'Here is the swap to save thirty seconds from break 11 of the 12 PM game.' This lets MC know exactly what you're doing.",
    audio: '/audio/module-3/master-control-email/module3_mastercontrol_02.mp3',
    image: '/images/module-3/master-control-email/Email1.png'
  },
  {
    text: "Next, identify where you're moving the spot to. So, you are moving the Jersey Mikes unit to the 2 PM window, just write: '2 PM Game'. Keep it simple and clear.",
    audio: '/audio/module-3/master-control-email/module3_mastercontrol_03.mp3',
    image: '/images/module-3/master-control-email/Email2.png'
  },
  {
    text: "Under that, write the specific break you're moving the spot into. In this case: 'Break 1'. This shows exactly where the commercial will go.",
    audio: '/audio/module-3/master-control-email/module3_mastercontrol_04.mp3',
    image: '/images/module-3/master-control-email/Email3.png'
  },
  {
    text: "Now, you need to show what's being cut to make room for the new spot. Write: 'CUT' and then paste the house numbers of the commercial or commercials you're removing. Always copy and paste the house numbers directly. This really helps eliminate mistakes.",
    audio: '/audio/module-3/master-control-email/module3_mastercontrol_05.mp3',
    image: '/images/module-3/master-control-email/Emailv3.jpg'
  },
  {
    text: "Finally, show what you're adding in. Under 'CUT'- write 'IN' and paste the house number of the spot you are moving into that break. In this case, you are saving a Jersey Mike's commercial, so you will paste that house number right there.",
    audio: '/audio/module-3/master-control-email/module3_mastercontrol_06.mp3',
    image: '/images/module-3/master-control-email/Email5.png'
  },
  {
    text: "So, your final email should look something like this: 'Here is the swap to save :30 seconds from break 11 of the 12 PM game. 2PM Game Break 1 CUT: [House number being cut] IN: [House number of the Jersey Mike's spot]'",
    audio: '/audio/module-3/master-control-email/module3_mastercontrol_07.mp3',
    image: '/images/module-3/master-control-email/Email5.png'
  },
  {
    text: "Before you hit send, always double check your break numbers, your times, and the house numbers. Being clear and accurate helps MC mark everything correctly on their end which keeps our spots running smoothly.",
    audio: '/audio/module-3/master-control-email/module3_mastercontrol_08.mp3',
    image: '/images/module-3/master-control-email/Email5.png'
  }
];

const videoInfo = {
  title: 'Master Control Email',
  description: 'Learn how to properly communicate changes to Master Control via email.'
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
  image="/images/module-3/master-control-email/MasterControlEmailSheet.png" 
 
  onNextSubmodule={goNext} 
  progressId={progressId} 
  nextButtonText={nextButtonText} 
/> 
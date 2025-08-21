<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;
export let nextButtonText: string = "Next";

// Green & Purple Units script (updated to combine slides 2 & 3)
const script = [
  {
    text: `Now let's talk about the other type of units you will see`,
    audio: '/audio/module-2/green-purple-units/module2_greenpurpleunits_01.mp3',
    image: '/images/introduction/basketballBackground.png'
  },
  {
    text: `Here is a list of the purple and green units you will see on the live coverage sheet. These include Locals, DRs, Promos, and PSAs.`,
    audio: '/audio/module-2/green-purple-units/module2_greenpurpleunits_02_03_combined.mp3',
    whiteboardText: ['**__Purple & Green Units__**', '• **Locals**', '• **DRs**', '• **Promos**', '• **PSAs**'],
    titleAudio: '/audio/module-2/green-purple-units/module2_greenpurpleunits_02_title.mp3'
  },
  {
    text: `Locals are designated time slots sold to local stations for airing community-specific content, such as local car dealership commercials. When stations lack their own material, we fill these slots with sold inventory, which is why locals are never cut without producer approval. Each local spot is strictly 90 seconds long (1 minute and 30 seconds), with no exceptions. On the Live Coverage Sheet, locals are marked in purple for easy identification.`,
    audio: '/audio/module-2/green-purple-units/module2_greenpurpleunits_04.mp3',
    whiteboardText: ['**__Locals__**', 'Fixed 90-sec local spots, filled with community content, marked in purple'],
    titleAudio: '/audio/module-2/green-purple-units/module2_greenpurpleunits_04_title.mp3'
  },
  {
    text: `These are spots we are not contractually obligated to air, but we earn extra revenue if we include them. Often Drs, which is short for direct response commercials, are ads designed to prompt immediate viewer action, such as calling a phone number or visiting a website. This makes them valuable opportunities to boost engagement and revenue when airtime allows.`,
    audio: '/audio/module-2/green-purple-units/module2_greenpurpleunits_05.mp3',
    whiteboardText: ['**__DRs (Direct Response)__**', 'DRs generate additional revenue but are one of the first to be removed.'],
    titleAudio: '/audio/module-2/green-purple-units/module2_greenpurpleunits_05_title.mp3'
  },
  {
    text: `These spots do not directly generate revenue, but because they promote our own content and network programming that helps build audience awareness and engagement, they are given higher priority than PSAs.`,
    audio: '/audio/module-2/green-purple-units/module2_greenpurpleunits_06.mp3',
    whiteboardText: ['**__Promos__**', 'Promos boost network awareness'],
    titleAudio: '/audio/module-2/green-purple-units/module2_greenpurpleunits_06_title.mp3'
  },
  {
    text: `Public Service Announcements (PSAs) are non-commercial messages intended to inform or educate the public on important issues, such as health, safety, or community events. While valuable for raising awareness, PSAs are primarily used to fill airtime and do not generate revenue. Because of this, they are considered the lowest priority in our department and are the first content to be cut when time constraints arise.`,
    audio: '/audio/module-2/green-purple-units/module2_greenpurpleunits_07.mp3',
    whiteboardText: ['**__PSAs__**', 'non-revenue fillers, lowest priority, cut first'],
    titleAudio: '/audio/module-2/green-purple-units/module2_greenpurpleunits_07_title.mp3'
  }
];

const videoInfo = {
  title: 'Green & Purple Units'
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
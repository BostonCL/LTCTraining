<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let progressId: string;

// Green & Purple Units script (placeholder, update as needed)
const script = [
  {
    text: `Now let's talk about the other type of units you will see`,
    audio: '/api/assets/audio/module-2/green-purple-units/module2_greenpurpleunits_01.mp3',
    image: '/api/assets/images/introduction/basketballBackground.png'
  },
  {
    text: `Here is a list of the purple and green units you will see on the live coverage sheet`,
    audio: '/api/assets/audio/module-2/green-purple-units/module2_greenpurpleunits_02.mp3',
    whiteboardText: ['Purple & Green Units']
  },
  {
    text: '',
    audio: '/api/assets/audio/module-2/green-purple-units/module2_greenpurpleunits_03.mp3',
    whiteboardText: ['Purple & Green Units', '• Locals', '• DRs', '• Promos', '• PSAs']
  },
  {
    text: `Locals are designated time slots sold to local stations for airing community-specific content, such as local car dealership commercials. When stations lack their own material, we fill these slots with sold inventory, which is why locals are never cut without producer approval. Each local spot is strictly 90 seconds long (1 minute and 30 seconds), with no exceptions. On the Live Coverage Sheet, locals are marked in purple for easy identification.`,
    audio: '/api/assets/audio/module-2/green-purple-units/module2_greenpurpleunits_04.mp3',
    whiteboardText: ['Locals', 'Fixed 90-sec local spots, filled with community content, marked in purple']
  },
  {
    text: `These are spots we are not contractually obligated to air, but we earn extra revenue if we include them. Often Drs, which is short for direct response commercials, are ads designed to prompt immediate viewer action, such as calling a phone number or visiting a website. This makes them valuable opportunities to boost engagement and revenue when airtime allows.`,
    audio: '/api/assets/audio/module-2/green-purple-units/module2_greenpurpleunits_05.mp3',
    whiteboardText: ['DRs (Direct Response)', 'DRs generate additional revenue but are one of the first to be removed.']
  },
  {
    text: `These spots do not directly generate revenue, but because they promote our own content and network programming that helps build audience awareness and engagement, they are given higher priority than PSAs.`,
    audio: '/api/assets/audio/module-2/green-purple-units/module2_greenpurpleunits_06.mp3',
    whiteboardText: ['Promos', 'Promos boost network awareness']
  },
  {
    text: `Public Service Announcements (PSAs) are non-commercial messages intended to inform or educate the public on important issues, such as health, safety, or community events. While valuable for raising awareness, PSAs are primarily used to fill airtime and do not generate revenue. Because of this, they are considered the lowest priority in our department and are the first content to be cut when time constraints arise.`,
    audio: '/api/assets/audio/module-2/green-purple-units/module2_greenpurpleunits_07.mp3',
    whiteboardText: ['PSAs', 'non-revenue fillers, lowest priority, cut first']
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
/> 
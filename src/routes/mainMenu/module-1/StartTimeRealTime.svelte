<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
import { audioStore } from '$lib/stores/audioStore';
import { createEventDispatcher } from 'svelte';
import { onMount } from 'svelte';

  import { getR2Url } from '$lib/config/r2';
const dispatch = createEventDispatcher();

const script = [
	{
		text: 'The first columns we are going to look at are the Start Time and Real Time columns. The start time column is the time the show is scheduled to start and the real time column is for the time the show actually starts.',
		audio: getR2Url('/audio/module-1/02-start-time-real-time/module1_starttimerealtime_01.mp3'),
		image: getR2Url('/images/module-1/start-time-real-time/StartTime.jpg')
	},
	{
		text: 'Since this is a live event, there is a good chance that the show will not start at its scheduled time, it could start early or it could start late. The real time column is where you will write down the time the show actually starts.',
		audio: getR2Url('/audio/module-1/02-start-time-real-time/module1_starttimerealtime_02.mp3'),
		image: getR2Url('/images/module-1/start-time-real-time/RealTime.jpg')
	},
	{
		text: 'This is an important column because this is how we will time out the rest of the show.',
		audio: getR2Url('/audio/module-1/02-start-time-real-time/module1_starttimerealtime_03.mp3'),
		image: getR2Url('/images/module-1/start-time-real-time/StartTime4.jpg')
	},
	{
		text: 'The start time will always be at the top of the page in the second column.',
		audio: getR2Url('/audio/module-1/02-start-time-real-time/module1_starttimerealtime_04.mp3'),
		image: getR2Url('/images/module-1/start-time-real-time/StartTime2.jpg')
	},
	{
		text: 'For Start Time, let\'s say the game is delayed and starts at 8:03:30. You would write 8:03:30 down next to Start Time.',
		audio: getR2Url('/audio/module-1/02-start-time-real-time/module1_starttimerealtime_05.mp3'),
		image: getR2Url('/images/module-1/start-time-real-time/StartTime5.jpg')
	},
	{
		text: 'So, for example, if the show is scheduled to start at 1:00 PM but it actually starts at 1:02 PM, you will write down 1:02 PM in the real time column.',
		audio: getR2Url('/audio/module-1/02-start-time-real-time/module1_starttimerealtime_06.mp3'),
		image: getR2Url('/images/module-1/start-time-real-time/StartTime6.jpg')
	}
];

const videoInfo = {
  title: 'Start Time & Real Time'
};

export let progressId: string;
export let nextButtonText: string = "Next";

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
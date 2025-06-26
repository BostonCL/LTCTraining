<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

const script = [
  { text: 'Real Time is the scheduled start time for a show or game. For example, if a game is scheduled to begin at 8AM, you write down 8:00:00 next to Real Time, regardless of when it actually begins.', audio: '/audio/module1_starttimerealtime_01.mp3' },
  { text: 'Start Time is when the event actually begins. For example, if the game is delayed and starts at 8:03:30 AM, you write that down next to Start Time.', audio: '/audio/module1_starttimerealtime_02.mp3' },
  { text: 'Key Difference: Real Time is what was planned/scheduled. Start Time is what actually happened.', audio: '/audio/module1_starttimerealtime_03.mp3' }
];

const videoInfo = {
  title: 'Start Time & Real Time',
  description: 'Learn the difference between Real Time (scheduled) and Start Time (actual) for live events.'
};
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} /> 
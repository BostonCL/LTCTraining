<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

const script = [
  { text: "Hit Time is a mock schedule used for planning. These aren't the real times commercials air, just estimated placeholders.", audio: '/audio/module1_hittime_01.mp3' }
];

const videoInfo = {
  title: 'Hit Time',
  description: 'Understand what Hit Time means and how it is used for planning commercial breaks.'
};
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} /> 
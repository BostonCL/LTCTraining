<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

const script = [
  { text: 'Spot End Time is the latest time that specific ad can air.', audio: '/audio/module1_spotendtime_01.mp3' }
];

const videoInfo = {
  title: 'Spot End Time',
  description: 'Understand the importance of Spot End Time for commercial scheduling.'
};
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} /> 
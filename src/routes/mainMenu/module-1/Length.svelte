<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

const script = [
  { text: 'Length is how long the commercial actually is. How long is each break?', audio: '/audio/module1_length_01.mp3' }
];

const videoInfo = {
  title: 'Length',
  description: 'Find out how to determine the length of each commercial break.'
};
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} /> 
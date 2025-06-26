<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

const script = [
  { text: 'Ordered As shows or games the commercial was sold to air with.', audio: '/audio/module1_orderedas_01.mp3' }
];

const videoInfo = {
  title: 'Ordered As',
  description: 'See how the Ordered As field links commercials to specific shows or games.'
};
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} /> 
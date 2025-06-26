<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

const script = [
  { text: 'Event Type tells you what kind of content it is (like a commercial, promo, local ad, or DR). You can also find this info elsewhere if needed.', audio: '/audio/module1_eventtype_01.mp3' }
];

const videoInfo = {
  title: 'Event Type',
  description: 'Learn about the different event types and how to identify them.'
};
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} /> 
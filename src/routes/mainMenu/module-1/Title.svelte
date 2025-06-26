<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

const script = [
  { text: 'Title gives details about the specific commercial.', audio: '/audio/module1_title_01.mp3' }
];

const videoInfo = {
  title: 'Title',
  description: 'Learn what information is included in the Title field for commercials.'
};
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} /> 
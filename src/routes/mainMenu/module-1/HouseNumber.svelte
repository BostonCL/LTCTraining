<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

const script = [
  { text: "House Number is a unique ID for the commercial. This is how Master Control identifies which ad you're talking about. Since one advertiser (like Geico) can have several different ads, the house number is key for clarity.", audio: '/audio/module1_housenumber_01.mp3' }
];

const videoInfo = {
  title: 'House Number',
  description: 'Learn why House Numbers are important for identifying commercials.'
};
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} /> 
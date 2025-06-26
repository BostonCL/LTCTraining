<script lang="ts">
import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

const script = [
  { text: 'Advertiser is who the ad is from.', audio: '/audio/module1_advertiser_01.mp3' }
];

const videoInfo = {
  title: 'Advertiser',
  description: 'Understand the importance of the Advertiser field in commercial logs.'
};
</script>

<YouTubeTemplate script={script} title={videoInfo.title} description={videoInfo.description} /> 
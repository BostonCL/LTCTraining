<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { preloader } from '$lib/utils/preloader';

	onMount(() => {
		// Start preloading critical resources immediately
		const preloadCriticalResources = async () => {
			const criticalImages = [
				'/images/introduction/basketballBackground.png',
				'/images/module-1/intro/LiveCoverageCleanWide-0.png',
				'/images/module-1/start-time-real-time/LCSheetRS.png',
				'/images/module-1/length/Lengthsheet.png',
				'/images/module-1/hit-time/HitTimesheet.png',
				'/images/module-1/advertiser/Advertiserscreen.png',
				'/images/module-1/title/Titlescreen.png',
				'/images/module-1/house-number/HouseNumberscreen.png',
				'/images/module-1/event-type/EventTypesheet.png',
				'/images/module-1/ordered-as/OrderedAsscreen.png',
				'/images/module-1/spot-end-time/SpotEndTimescreen.png',
				'/images/module-1/end-time/EndTimeSheet.png',
				'/images/module-1/floaters/FloatersSheet.png',
				'/images/module-1/program-line/ProgramLinescreen.png'
			];

			const criticalAudio = [
				'/audio/introduction/intro_01.mp3',
				'/audio/introduction/intro_02.mp3',
				'/audio/introduction/intro_03.mp3',
				'/audio/introduction/intro_04.mp3',
				'/audio/introduction/intro_05.mp3'
			];

			// Start preloading in parallel
			Promise.all([
				preloader.preloadCriticalImages(criticalImages),
				preloader.preloadAudio(criticalAudio)
			]).catch(error => {
				console.warn('Preloading failed:', error);
			});
		};

		preloadCriticalResources();
	});
</script>

<slot />

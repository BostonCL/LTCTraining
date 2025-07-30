<script lang="ts">
	import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

	const introScript = [
		{ text: 'What is live coverage?', audio: '/api/assets/audio/introduction/intro_01.mp3' },
		{
			text: 'Covering live traffic means you will be monitoring commercial inventory while ensuring airing criteria and guidelines are met. In short, watching different sporting events and making sure the commercials air properly.',
			audio: '/api/assets/audio/introduction/intro_02.mp3'
		},
		{
			text: 'Managing and airing all inventory (commercials) during live games.',
			audio: '/api/assets/audio/introduction/intro_03.mp3'
		},
		{
			text: 'Communicating with the network (through the phone and email) with the producers and Master control. We refer to Master control as MC, they are the people that send the commercial to air, we communicate with them the most.',
			audio: '/api/assets/audio/introduction/intro_04.mp3'
		},
		{ text: 'Writing down airing times.', audio: '/api/assets/audio/introduction/intro_05.mp3' },
		{
			text: 'Proper management of inventory is crucial for the financial success of CBS Sports Network.',
			audio: '/api/assets/audio/introduction/intro_06.mp3'
		},
		{
			text: 'The network operates on a 24-hour clock from 6 AM to 6 AM so our goal is to time out the commercials and organize them in that 24-hour period!',
			audio: '/api/assets/audio/introduction/intro_07.mp3'
		},
		{
			text: "The role may appear intimidating at first but don't worry it will become comprehensible after this training course.",
			audio: '/api/assets/audio/introduction/intro_08.mp3'
		},
		{
			text: 'Keep in mind there will be practice questions throughout the course and there will be a test you must get 70% or higher on.',
			audio: '/api/assets/audio/introduction/intro_09.mp3'
		},
		{
			text: 'Participants must take notes and prepare questions for a follow-up Zoom call.',
			audio: '/api/assets/audio/introduction/intro_10.mp3'
		}
	];

	const videoInfo = {
		title: 'Introduction to Live Traffic Coverage Training',
		description: 'Welcome to the CBS Live Traffic Coverage Training program. This comprehensive introduction covers the fundamentals of live traffic reporting, including what live coverage means, the key responsibilities involved, and what to expect throughout this training course.'
	};

	function dummyNext() {}
</script>

<YouTubeTemplate script={introScript} title={videoInfo.title} image="/api/assets/images/introduction/basketballBackground.png" onNextSubmodule={dummyNext} progressId="introduction_intro" /> 
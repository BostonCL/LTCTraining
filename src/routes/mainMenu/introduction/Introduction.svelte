<script lang="ts">
	import BasketballAvatar from '$lib/components/BasketballAvatar.svelte';
	import VideoControls from '$lib/components/VideoControls.svelte';

	const introScript = [
		{ text: 'What is live coverage?', audio: '/audio/intro_01.mp3' },
		{
			text: 'Covering live traffic means you will be monitoring commercial inventory while ensuring airing criteria and guidelines are met. In short, watching different sporting events and making sure the commercials air properly.',
			audio: '/audio/intro_02.mp3'
		},
		{
			text: 'Managing and airing all inventory (commercials) during live games.',
			audio: '/audio/intro_03.mp3'
		},
		{
			text: 'Communicating with the network (through the phone and email) with the producers and Master control. We refer to Master control as MC, they are the people that send the commercial to air, we communicate with them the most.',
			audio: '/audio/intro_04.mp3'
		},
		{ text: 'Writing down airing times.', audio: '/audio/intro_05.mp3' },
		{
			text: 'Proper management of inventory is crucial for the financial success of CBS Sports Network.',
			audio: '/audio/intro_06.mp3'
		},
		{
			text: 'The network operates on a 24-hour clock from 6 AM to 6 AM so our goal is to time out the commercials and organize them in that 24-hour period!',
			audio: '/audio/intro_07.mp3'
		},
		{
			text: "The role may appear intimidating at first but don't worry it will become comprehensible after this training course.",
			audio: '/audio/intro_08.mp3'
		},
		{
			text: 'Keep in mind there will be practice questions throughout the course and there will be a test you must get 70% or higher on.',
			audio: '/audio/intro_09.mp3'
		},
		{
			text: 'Participants must take notes and prepare questions for a follow-up Zoom call.',
			audio: '/audio/intro_10.mp3'
		}
	];

	const videoInfo = {
		title: 'Introduction to Live Traffic Coverage Training',
		description: 'Welcome to the CBS Live Traffic Coverage Training program. This comprehensive introduction covers the fundamentals of live traffic reporting, including what live coverage means, the key responsibilities involved, and what to expect throughout this training course.',
		views: '1.2K views',
		uploadDate: 'June 2024',
		duration: '3:45',
		author: 'CBS Sports Network',
		tags: ['Live Traffic', 'Training', 'CBS Sports', 'Commercial Management']
	};
</script>

<div class="max-w-4xl mx-auto">
	<!-- Video Player Area -->
	<div class="bg-black rounded-lg overflow-hidden shadow-lg mb-6">
		<div class="relative aspect-video bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center">
			<!-- Basketball Avatar in the center -->
			<div class="relative z-10">
				<BasketballAvatar scripts={introScript} />
			</div>
			
			<!-- Play button overlay (optional) -->
			<div class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
				<div class="bg-white bg-opacity-20 rounded-full p-4">
					<svg class="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 24 24">
						<path d="M8 5v14l11-7z"/>
					</svg>
				</div>
			</div>
		</div>

		<!-- Video Controls at the bottom -->
		<VideoControls />
	</div>

	<!-- Video Information Section -->
	<div class="space-y-4">
		<!-- Title -->
		<h1 class="text-2xl font-bold text-gray-900">{videoInfo.title}</h1>
		
		<!-- Stats and Actions Row -->
		<div class="flex items-center justify-between text-sm text-gray-600 border-b border-gray-200 pb-4">
			<div class="flex items-center space-x-4">
				<span>{videoInfo.views}</span>
				<span>•</span>
				<span>{videoInfo.uploadDate}</span>
			</div>
			<div class="flex items-center space-x-4">
				<button class="flex items-center space-x-1 hover:text-gray-900 transition">
					<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"/>
					</svg>
					<span>Like</span>
				</button>
				<button class="flex items-center space-x-1 hover:text-gray-900 transition">
					<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"/>
					</svg>
					<span>Share</span>
				</button>
			</div>
		</div>

		<!-- Author and Subscribe -->
		<div class="flex items-center justify-between py-4 border-b border-gray-200">
			<div class="flex items-center space-x-3">
				<div class="w-10 h-10 bg-red-600 rounded-full flex items-center justify-center">
					<span class="text-white font-bold text-sm">CBS</span>
				</div>
				<div>
					<div class="font-semibold text-gray-900">{videoInfo.author}</div>
					<div class="text-sm text-gray-600">1.2M subscribers</div>
				</div>
			</div>
			<button class="bg-red-600 text-white px-6 py-2 rounded-full font-semibold hover:bg-red-700 transition">
				Subscribe
			</button>
		</div>

		<!-- Description -->
		<div class="bg-gray-50 rounded-lg p-4">
			<div class="text-sm text-gray-600 mb-2">Description</div>
			<p class="text-gray-900 leading-relaxed">{videoInfo.description}</p>
			
			<!-- Tags -->
			<div class="flex flex-wrap gap-2 mt-4">
				{#each videoInfo.tags as tag}
					<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">#{tag}</span>
				{/each}
			</div>
		</div>
	</div>
</div> 
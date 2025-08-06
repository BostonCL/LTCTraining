<script lang="ts">
	import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';
	import { onMount } from 'svelte';
	import { createEventDispatcher } from 'svelte';
	import { audioStore } from '$lib/stores/audioStore';

	const dispatch = createEventDispatcher();

	let showPlayButton = true;
	let hasStarted = false;

	const introScript = [
		{ 
			text: 'Hello and welcome! Our job in the Traffic Department at CBS Sports Network is to represent Advertisers and ensure that their Commercials make it to air. Covering live traffic means you will be monitoring commercial inventory in real time while ensuring that airing criteria and network guidelines are met. In other words, you will be watching different sporting events and making sure the commercials are shown on television according to a specific set of rules. Don\'t worry! We will learn all about Commercials and the rules for airing them in the course. Before we begin, here are a few basic terms to familiarize yourself with:',
			audio: '/audio/introduction/intro_01_02_combined.mp3',
			image: '/images/introduction/basketballBackground.jpg'
		},
		{ 
			text: 'Advertiser: An individual or organization that promotes products, services, or ideas to a target audience.',
			audio: '/audio/introduction/intro_03.mp3',
			whiteboardText: ['**__Advertiser__**', 'An individual or organization that promotes products, services, or ideas to a target audience.'],
			titleAudio: '/audio/introduction/intro_03_title.mp3'
		},
		{ 
			text: 'Commercial: A short advertisement that promotes a product or service.',
			audio: '/audio/introduction/intro_04.mp3',
			whiteboardText: ['**__Commercial__**', 'A short advertisement that promotes a product or service.'],
			titleAudio: '/audio/introduction/intro_04_title.mp3'
		},
		{ 
			text: 'Unit: Another word for Commercial. These terms are used interchangeably in the Traffic Department.',
			audio: '/audio/introduction/intro_05.mp3',
			whiteboardText: ['**__Unit__**', 'Another word for Commercial. These terms are used interchangeably in the Traffic Department.'],
			titleAudio: '/audio/introduction/intro_05_title.mp3'
		},
		{ 
			text: 'Commercial Breaks: The planned intervals during which advertisements are aired.',
			audio: '/audio/introduction/intro_06.mp3',
			whiteboardText: ['**__Commercial Breaks__**', 'The planned intervals during which advertisements are aired.'],
			titleAudio: '/audio/introduction/intro_06_title.mp3'
		},
		{ 
			text: 'Window: A term used in the Traffic Department for any particular program or game. Window refers specifically to the time period during which the program or game airs, encompassing the duration from its beginning to its end. For example, instead of saying "7 PM Basketball Game," we would say "7 PM Window."',
			audio: '/audio/introduction/intro_07.mp3',
			whiteboardText: ['**__Window__**', 'Refers to the specific scheduled time period during which a program or game airs, from start to finish.'],
			titleAudio: '/audio/introduction/intro_07_title.mp3'
		},
		{ 
			text: 'Live Coverage Sheet: An excel spreadsheet containing all the vital information you will need in order to properly air Commercials/Units.',
			audio: '/audio/introduction/intro_08.mp3',
			whiteboardText: ['**__Live Coverage Sheet__**', 'An excel spreadsheet containing all the vital information you will need in order to properly air Commercials/Units.'],
			titleAudio: '/audio/introduction/intro_08_title.mp3'
		},
		{ 
			text: 'Swaps: The word for making changes on the live coverage sheet. It typically involves saving or updating a commercial unit. This process includes modifying the placement of commercials during live broadcasts to align with the timing or logistics, to ensure accurate tracking and smooth execution of the broadcast. Essentially, swaps are quick adjustments made in real-time to the coverage sheet to manage commercial placements effectively.',
			audio: '/audio/introduction/intro_09.mp3',
			whiteboardText: ['**__Swaps__**', 'Swaps refer to real-time updates you will make to the live coverage sheet to adjust commercial placements during broadcasts.'],
			titleAudio: '/audio/introduction/intro_09_title.mp3'
		},
		{ 
			text: 'Dead: A term used in the Traffic Department to indicate that a Commercial/Unit will not air at all that day or night.',
			audio: '/audio/introduction/intro_10.mp3',
			whiteboardText: ['**__Dead__**', 'Indicates that a Commercial/Unit will not air at all that day or night'],
			titleAudio: '/audio/introduction/intro_10_title.mp3'
		},
		{ 
			text: 'Cut is a term used when a Commercial/Unit has been removed from its original spot. A Cut Commercial/Unit may still air in another show or time slot. Note: While \'Dead\' and \'Cut\' are sometimes used interchangeably, they do not mean exactly the same thing. A dead unit never airs, while a cut unit might.',
			audio: '/audio/introduction/intro_11.mp3',
			whiteboardText: ['**__CUT__**', 'A term used when a Commercial/Unit has been removed from its original spot. A Cut Commercial/Unit may still air in another show or time slot.'],
			titleAudio: '/audio/introduction/intro_11_title.mp3'
		},
		{ 
			text: 'What is live coverage? Live coverage involves three main responsibilities: Managing and airing all Commercials/Units during live games. Communicating with the network producer and Master Control through phone and email. We will refer to Master Control as MC from here on. They are the people that ultimately send the commercials to air. We communicate with them the most. So be nice to them! And marking down airing times. Effectively managing inventory is crucial for the financial and overall success of CBS Sports Network. The network operates on a 24-hour clock from 6 AM to 6 AM, so our goal is to schedule and properly organize the Commercials within that 24-hour period! Beware! There are many factors that contribute to the ever changing schedules of live coverage. A program can go longer than anticipated. As a result, Units can be cut. Our job is to advocate for Commercials/Units and ensure that they air on TV despite these changes. The role may appear intimidating at first, but don\'t worry. This training course will set you up for success in the CBS Traffic Department. Keep in mind there will be practice questions throughout the course, and there will be a test at the end. You must score 70% or higher on the test to proceed.',
			audio: '/audio/introduction/intro_12_13_14_15_16_combined.mp3',
			image: '/images/introduction/basketballBackground.jpg',
			whiteboardText: ['**__What is live coverage?__**', '• Managing and airing all Commercials/Units during live games', '• Communicating with the network producer and Master Control through phone and email', '• Marking down airing times', '• Effectively managing inventory for CBS Sports Network success', '• Operating on a 24-hour clock from 6 AM to 6 AM', '• Advocating for Commercials/Units despite schedule changes', '• Training course prepares you for success', '• Practice questions and test with 70% minimum score'],
			titleAudio: '/audio/introduction/intro_12_title.mp3'
		},
		{ 
			text: 'Participants must take notes and prepare questions for a follow-up appointment with the Traffic Team.',
			audio: '/audio/introduction/intro_13.mp3'
		}
	];

	const videoInfo = {
		title: 'Introduction to Live Traffic Coverage Training',
		description: 'Welcome to the CBS Live Traffic Coverage Training program. This comprehensive introduction covers the fundamentals of live traffic reporting, including what live coverage means, the key responsibilities involved, and what to expect throughout this training course.'
	};

	function handlePlayClick() {
		showPlayButton = false;
		hasStarted = true;
		// Start the audio playback
		audioStore.update(state => ({ ...state, isPlaying: true }));
	}

	onMount(() => {
		// Reset play button state when component mounts
		showPlayButton = true;
		hasStarted = false;
	});
</script>

{#if showPlayButton && !hasStarted}
	<!-- Play Button Overlay -->
	<div class="w-full max-w-5xl px-4 mx-auto mt-8">
		<div class="w-full bg-black rounded-lg overflow-hidden shadow-lg mb-6 relative">
			<div class="relative aspect-video bg-black w-full overflow-hidden">
				<img 
					src="/images/introduction/basketballBackground.jpg" 
					alt="Introduction background" 
					class="w-full h-full z-0 bg-white object-contain opacity-50" 
					style="
						object-fit: contain;
						object-position: center center;
						filter: brightness(0.98);
						display: block;
						margin: 0 auto;
						background: white;
					" 
				/>
				<!-- YouTube-style Play Button -->
				<div class="absolute inset-0 flex items-center justify-center z-20">
					<button 
						on:click={handlePlayClick}
						class="w-24 h-24 bg-red-600 hover:bg-red-700 rounded-full flex items-center justify-center shadow-lg transform hover:scale-110 transition-all duration-200"
						aria-label="Play introduction"
					>
						<svg class="w-12 h-12 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
							<path d="M8 5v14l11-7z"/>
						</svg>
					</button>
				</div>
				<!-- Play Text -->
				<div class="absolute bottom-8 left-1/2 -translate-x-1/2 text-white text-lg font-medium z-20">
					Click to start introduction
				</div>
			</div>
		</div>
		<!-- Video Title -->
		<h1 class="w-full text-2xl font-bold text-gray-900 mb-2">Introduction</h1>
		<!-- Video Description -->
		<p class="w-full text-gray-700 mb-4">Click the play button to begin the introduction to CBS Sports Network Traffic Department training.</p>
	</div>
{:else}
	<YouTubeTemplate 
		script={introScript} 
		title="Introduction" 
		showAvatar={true}
		progressId="introduction"
		nextButtonText="Continue to Module 1"
		onNextSubmodule={() => {
			// Navigate to Module 1 when introduction is complete
			dispatch('navigateToNextSubmodule');
		}}
	/>
{/if} 
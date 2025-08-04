<script lang="ts">
	import YouTubeTemplate from '$lib/components/YouTubeTemplate.svelte';

	const introScript = [
		{ 
			text: 'Hello and welcome! Our job in the Traffic Department at CBS Sports Network is to represent Advertisers and ensure that their Commercials make it to air. Covering live traffic means you will be monitoring commercial inventory in real time while ensuring that airing criteria and network guidelines are met. In other words, you will be watching different sporting events and making sure the commercials are shown on television according to a specific set of rules. Don\'t worry! We will learn all about Commercials and the rules for airing them in the course.',
			audio: '/audio/introduction/intro_01.mp3',
			image: '/images/introduction/basketballBackground.jpg'
		},
		{ 
			text: 'Before we begin, here are a few basic terms to familiarize yourself with:',
			audio: '/audio/introduction/intro_02.mp3'
		},
		{ 
			text: 'Advertiser: An individual or organization that promotes products, services, or ideas to a target audience.',
			audio: '/audio/introduction/intro_03.mp3'
		},
		{ 
			text: 'Commercial: A short advertisement that promotes a product or service.',
			audio: '/audio/introduction/intro_04.mp3'
		},
		{ 
			text: 'Unit: Another word for Commercial. These terms are used interchangeably in the Traffic Department.',
			audio: '/audio/introduction/intro_05.mp3'
		},
		{ 
			text: 'Commercial Breaks: The planned intervals during which advertisements are aired.',
			audio: '/audio/introduction/intro_06.mp3'
		},
		{ 
			text: 'Window: A term used in the Traffic Department for any particular program or game. Window refers specifically to the time period during which the program or game airs, encompassing the duration from its beginning to its end. For example, instead of saying "7 PM Basketball Game," we would say "7 PM Window."',
			audio: '/audio/introduction/intro_07.mp3'
		},
		{ 
			text: 'Live Coverage Sheet: An excel spreadsheet containing all the vital information you will need in order to properly air Commercials/Units.',
			audio: '/audio/introduction/intro_08.mp3'
		},
		{ 
			text: 'Swaps: The word for making changes on the live coverage sheet. It typically involves saving or updating a commercial unit. This process includes modifying the placement of commercials during live broadcasts to align with the timing or logistics, to ensure accurate tracking and smooth execution of the broadcast. Essentially, swaps are quick adjustments made in real-time to the coverage sheet to manage commercial placements effectively.',
			audio: '/audio/introduction/intro_09.mp3'
		},
		{ 
			text: 'Dead: A term used in the Traffic Department to indicate that a Commercial/Unit will not air at all that day or night.',
			audio: '/audio/introduction/intro_10.mp3'
		},
		{ 
			text: 'CUT: A term used when a Commercial/Unit has been removed from its original spot. A CUT Commercial/Unit may still air in another show or time slot. Note: While \'Dead\' and \'Cut\' are sometimes used interchangeably, they do not mean exactly the same thing. A dead unit never airs, while a cut unit might.',
			audio: '/audio/introduction/intro_11.mp3'
		},
		{ 
			text: 'What is live coverage?',
			audio: '/audio/introduction/intro_12.mp3'
		},
		{ 
			text: 'Managing and airing all Commercials/Units during live games.',
			audio: '/audio/introduction/intro_13.mp3'
		},
		{ 
			text: 'Communicating with the network producer and Master Control through phone and email. We will refer to Master Control as MC from here on. They are the people that ultimately send the commercials to air. We communicate with them the most. So be nice to them!',
			audio: '/audio/introduction/intro_14.mp3'
		},
		{ 
			text: 'Marking down airing times.',
			audio: '/audio/introduction/intro_15.mp3'
		},
		{ 
			text: 'Effectively managing inventory is crucial for the financial and overall success of CBS Sports Network. The network operates on a 24-hour clock from 6 AM to 6 AM, so our goal is to schedule and properly organize the Commercials within that 24-hour period!',
			audio: '/audio/introduction/intro_16.mp3',
			image: '/images/introduction/basketballBackground.jpg'
		},
		{ 
			text: 'Beware! There are many factors that contribute to the ever changing schedules of live coverage. A program can go longer than anticipated. As a result, Units can be cut. Our job is to advocate for Commercials/Units and ensure that they air on TV despite these changes.',
			audio: '/audio/introduction/intro_17.mp3'
		},
		{ 
			text: 'The role may appear intimidating at first, but don\'t worry. This training course will set you up for success in the CBS Traffic Department.',
			audio: '/audio/introduction/intro_18.mp3'
		},
		{ 
			text: 'Keep in mind there will be practice questions throughout the course, and there will be a test at the end. You must score 70% or higher on the test to proceed.',
			audio: '/audio/introduction/intro_19.mp3'
		},
		{ 
			text: 'Participants must take notes and prepare questions for a follow-up appointment with the Traffic Team.',
			audio: '/audio/introduction/intro_20.mp3'
		}
	];

	const videoInfo = {
		title: 'Introduction to Live Traffic Coverage Training',
		description: 'Welcome to the CBS Live Traffic Coverage Training program. This comprehensive introduction covers the fundamentals of live traffic reporting, including what live coverage means, the key responsibilities involved, and what to expect throughout this training course.'
	};

	function dummyNext() {}
</script>

<YouTubeTemplate script={introScript} title={videoInfo.title} onNextSubmodule={dummyNext} progressId="introduction_intro" /> 
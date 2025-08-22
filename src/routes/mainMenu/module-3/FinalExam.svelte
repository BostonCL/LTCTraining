<script lang="ts">
import { createEventDispatcher } from 'svelte';
import { onMount } from 'svelte';

const dispatch = createEventDispatcher();

export let nextButtonText: string = "Complete Module";

let currentQuestion = 0;
let userAnswers: string[] = [];
let showResults = false;
let score = 0;
let totalQuestions = 20;

const questions = [
  {
    question: "What is the primary purpose of Live Traffic at CBS Sports Network?",
    options: [
      "To create advertisements",
      "To track game highlights", 
      "To ensure commercials air properly and meet contractual obligations",
      "To design show formats"
    ],
    correctAnswer: "C"
  },
  {
    question: "Which department is referred to as \"MC\"?",
    options: [
      "Media Content",
      "Master Control",
      "Marketing Coordination", 
      "Main Commercial"
    ],
    correctAnswer: "B"
  },
  {
    question: "Why is the 'Live Coverage Sheet' considered a critical tool?",
    options: [
      "It tracks game scores",
      "It contains advertiser invoices",
      "It provides a full record of commercial placements and break structures",
      "It only stores backup commercials"
    ],
    correctAnswer: "C"
  },
  {
    question: "What must you do before moving a commercial to another break?",
    options: [
      "Ask the Advertiser directly",
      "Confirm brand separation, spot end time, and availability in the new break",
      "Email the Programming Director",
      "Delete it from the sheet"
    ],
    correctAnswer: "B"
  },
  {
    question: "If a show is scheduled for 7:00 PM but starts at 7:03:15 PM, what time do you write under \"Start Time\"?",
    options: [
      "7:00 PM",
      "7:03:15 PM",
      "6:45 PM",
      "7:15 PM"
    ],
    correctAnswer: "B"
  },
  {
    question: "What color is used to highlight a commercial that aired in its new break?",
    options: [
      "Yellow",
      "Green", 
      "Red",
      "Blue"
    ],
    correctAnswer: "D"
  },
  {
    question: "What does \"Moved From\" mean when highlighted in red on the Live Coverage Sheet?",
    options: [
      "The commercial was cut",
      "It is still unsold",
      "The unit was moved to a new break and aired there",
      "It failed brand SEP rules"
    ],
    correctAnswer: "C"
  },
  {
    question: "Which document is sent at the end of each shift?",
    options: [
      "Producer Summary",
      "Float Log",
      "Live Coverage Report",
      "Commercial Invoice"
    ],
    correctAnswer: "C"
  },
  {
    question: "Why is Brand Separation (Brand SEP) important?",
    options: [
      "It determines how long a break is",
      "It reduces the number of commercials",
      "It prevents the same brand from airing too close together",
      "It ensures locals get priority"
    ],
    correctAnswer: "C"
  },
  {
    question: "When is it acceptable to break the Brand SEP rule?",
    options: [
      "During reruns only",
      "During live windows",
      "On weekends only",
      "Never"
    ],
    correctAnswer: "B"
  },
  {
    question: "What should be done if you are unsure whether two brands are competitors?",
    options: [
      "Ignore it",
      "Check the Title column",
      "Ask MC",
      "Research or ask the Traffic Team"
    ],
    correctAnswer: "D"
  },
  {
    question: "Which type of unit always requires exactly 1 minute and 30 seconds of break space?",
    options: [
      "ROS Prime",
      "Local",
      "PSA",
      "Sports Spectacular"
    ],
    correctAnswer: "B"
  },
  {
    question: "What must you include in an email to Master Control when sending a swap?",
    options: [
      "Time zone",
      "Cost of the ad",
      "House numbers for both CUT and IN",
      "Advertiser website"
    ],
    correctAnswer: "C"
  },
  {
    question: "What does it mean if a unit is \"Show Specific\"?",
    options: [
      "It must be scheduled by MC",
      "It can air anywhere",
      "It is only allowed in that specific show and must be preserved",
      "It's optional and cuttable"
    ],
    correctAnswer: "C"
  },
  {
    question: "Which rule prevents an alcohol ad from airing near certain other ads?",
    options: [
      "PSA Cut Rule",
      "Prime Restriction Rule",
      "Standalone Rule",
      "Float Rule"
    ],
    correctAnswer: "C"
  },
  {
    question: "What is the purpose of Floaters?",
    options: [
      "To replace program lines",
      "To provide additional, flexible ad time during pauses in live games",
      "To fill up space in promos",
      "To signal the end of a game"
    ],
    correctAnswer: "B"
  },
  {
    question: "What must every moved commercial have in the spreadsheet?",
    options: [
      "Start and End Times in red",
      "A comment from the advertiser",
      "Color coding and a clear note on where it moved",
      "An updated cost"
    ],
    correctAnswer: "C"
  },
  {
    question: "What is a commercial also called in the Traffic Department?",
    options: [
      "Segment",
      "Unit",
      "Game",
      "Com"
    ],
    correctAnswer: "B"
  },
  {
    question: "What does \"CUT\" mean?",
    options: [
      "The unit is edited",
      "The commercial will never air",
      "The unit was removed from its spot but might air later",
      "A type of show"
    ],
    correctAnswer: "B"
  },
  {
    question: "What do you use to track commercials during live shows?",
    options: [
      "Game Sheet",
      "Live Coverage Sheet",
      "Scoreboard",
      "Camera Log"
    ],
    correctAnswer: "B"
  },
  {
    question: "What is a Window?",
    options: [
      "A break between shows",
      "A local ad",
      "A scheduled game or program time",
      "A cut unit"
    ],
    correctAnswer: "C"
  }
];

function selectAnswer(answer: string) {
  userAnswers[currentQuestion] = answer;
}

function nextQuestion() {
  if (currentQuestion < totalQuestions - 1) {
    currentQuestion++;
  } else {
    calculateScore();
    showResults = true;
  }
}

function previousQuestion() {
  if (currentQuestion > 0) {
    currentQuestion--;
  }
}

function calculateScore() {
  score = 0;
  for (let i = 0; i < totalQuestions; i++) {
    if (userAnswers[i] === questions[i].correctAnswer) {
      score++;
    }
  }
}

function getOptionLetter(index: number): string {
  return String.fromCharCode(65 + index); // A, B, C, D
}

function isCorrect(questionIndex: number): boolean {
  return userAnswers[questionIndex] === questions[questionIndex].correctAnswer;
}

function getScorePercentage(): number {
  return Math.round((score / totalQuestions) * 100);
}

function completeModule() {
  dispatch('navigateToNextSubmodule');
}

onMount(() => {
  // Initialize user answers array
  userAnswers = new Array(totalQuestions).fill('');
});
</script>

<div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
  <div class="text-center mb-8">
    <h1 class="text-3xl font-bold text-gray-800 mb-2">Module 3 Final Exam</h1>
    <p class="text-gray-600">Test your knowledge of Live Traffic procedures</p>
  </div>

  {#if !showResults}
    <!-- Question Display -->
    <div class="mb-8">
      <div class="flex justify-between items-center mb-4">
        <span class="text-sm text-gray-500">Question {currentQuestion + 1} of {totalQuestions}</span>
        <span class="text-sm text-gray-500">{getScorePercentage()}% Complete</span>
      </div>
      
      <div class="bg-gray-50 p-6 rounded-lg mb-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">
          {questions[currentQuestion].question}
        </h2>
        
        <div class="space-y-3">
          {#each questions[currentQuestion].options as option, index}
            <label class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-blue-50 transition-colors {userAnswers[currentQuestion] === getOptionLetter(index) ? 'bg-blue-100 border-blue-300' : 'bg-white border-gray-200'}">
              <input 
                type="radio" 
                name="question{currentQuestion}" 
                value={getOptionLetter(index)}
                checked={userAnswers[currentQuestion] === getOptionLetter(index)}
                on:change={() => selectAnswer(getOptionLetter(index))}
                class="mr-3"
              />
              <span class="font-medium text-gray-700">{getOptionLetter(index)}. {option}</span>
            </label>
          {/each}
        </div>
      </div>
      
      <div class="flex justify-between">
        <button 
          on:click={previousQuestion}
          disabled={currentQuestion === 0}
          class="px-6 py-2 bg-gray-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-600 transition-colors"
        >
          Previous
        </button>
        
        <button 
          on:click={nextQuestion}
          disabled={!userAnswers[currentQuestion]}
          class="px-6 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-700 transition-colors"
        >
          {currentQuestion === totalQuestions - 1 ? 'Finish Exam' : 'Next'}
        </button>
      </div>
    </div>
  {:else}
    <!-- Results Display -->
    <div class="text-center mb-8">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">Exam Results</h2>
      <div class="text-4xl font-bold {getScorePercentage() >= 80 ? 'text-green-600' : 'text-red-600'} mb-2">
        {score}/{totalQuestions}
      </div>
      <div class="text-xl text-gray-600 mb-4">
        {getScorePercentage()}% - {getScorePercentage() >= 80 ? 'Passed!' : 'Needs Improvement'}
      </div>
      
      {#if getScorePercentage() >= 80}
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg mb-6">
          <p class="font-semibold">Congratulations! You've successfully completed Module 3.</p>
          <p class="text-sm mt-1">You can now proceed to the next module or review any missed questions below.</p>
        </div>
      {:else}
        <div class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded-lg mb-6">
          <p class="font-semibold">Please review the material and retake the exam.</p>
          <p class="text-sm mt-1">You need 80% or higher to pass. Review the questions below to understand the correct answers.</p>
        </div>
      {/if}
    </div>

    <!-- Question Review -->
    <div class="space-y-6">
      {#each questions as question, index}
        <div class="border rounded-lg p-4 {isCorrect(index) ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}">
          <div class="flex items-start justify-between mb-2">
            <h3 class="font-semibold text-gray-800">Question {index + 1}</h3>
            <span class="text-sm font-medium {isCorrect(index) ? 'text-green-600' : 'text-red-600'}">
              {isCorrect(index) ? '✓ Correct' : '✗ Incorrect'}
            </span>
          </div>
          
          <p class="text-gray-700 mb-3">{question.question}</p>
          
          <div class="space-y-1">
            {#each question.options as option, optionIndex}
              <div class="flex items-center text-sm">
                <span class="w-6 font-medium {userAnswers[index] === getOptionLetter(optionIndex) ? (isCorrect(index) ? 'text-green-600' : 'text-red-600') : (getOptionLetter(optionIndex) === question.correctAnswer ? 'text-green-600' : 'text-gray-500')}">
                  {getOptionLetter(optionIndex)}.
                </span>
                <span class="{userAnswers[index] === getOptionLetter(optionIndex) ? (isCorrect(index) ? 'text-green-600 font-medium' : 'text-red-600 font-medium') : (getOptionLetter(optionIndex) === question.correctAnswer ? 'text-green-600 font-medium' : 'text-gray-600')}">
                  {option}
                </span>
                {#if getOptionLetter(optionIndex) === question.correctAnswer}
                  <span class="ml-2 text-green-600 font-bold">✓</span>
                {/if}
                {#if userAnswers[index] === getOptionLetter(optionIndex) && !isCorrect(index)}
                  <span class="ml-2 text-red-600 font-bold">✗</span>
                {/if}
              </div>
            {/each}
          </div>
        </div>
      {/each}
    </div>

    <div class="mt-8 text-center">
      <button 
        on:click={completeModule}
        class="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
      >
        {nextButtonText}
      </button>
    </div>
  {/if}
</div> 
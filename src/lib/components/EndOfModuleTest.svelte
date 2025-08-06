<script lang="ts">
  import { onMount } from 'svelte';
  
  type Question = {
    text: string;
    options: string[];
    correct: number;
    explanation?: string;
  };

  // 10 main questions
  const mainQuestions: Question[] = [
    { text: "What is an Advertiser?", options: [
      "A spreadsheet used to track commercials",
      "A program that airs commercials",
      "An individual or organization promoting products, services, or ideas to a target audience",
      "The same as a Commercial Break"
    ], correct: 2 },
    { text: "What is another word for “Unit”?", options: [
      "Floater",
      "Program line",
      "Window",
      "Commercial"
    ], correct: 3 },
    { text: "What is a Commercial Break?", options: [
      "The time when the network stops airing commercials",
      "A planned interval when advertisements are aired",
      "A tab in the Live Coverage Sheet",
      "A program segment"
    ], correct: 1 },
    { text: "In Traffic, what does the term “Window” mean?", options: [
      "A computer screen",
      "A spreadsheet column",
      "The time period a program or game airs",
      "A type of commercial"
    ], correct: 2 },
    { text: "What is a Live Coverage Sheet used for?", options: [
      "To design commercials",
      "To display a schedule for commercials/units",
      "To record only game scores",
      "To communicate with advertisers"
    ], correct: 1 },
    { text: "What does “Swaps” mean in the Traffic Department?", options: [
      "Creating new commercials",
      "Making real-time changes on the Live Coverage Sheet to adjust commercial placements",
      "Changing program titles",
      "Moving a Window"
    ], correct: 1 },
    { text: "If a unit is marked “Dead,” what does that mean?", options: [
      "It will air next week",
      "It will air later that day",
      "It will not air at all that day or night",
      "It must air during every break"
    ], correct: 2 },
    { text: "Who is MC in the Traffic Department?", options: [
      "The Marketing Coordinator",
      "Master Control — the people who send commercials to air",
      "Main Commercial Manager",
      "Multi-Channel Operator"
    ], correct: 1 },
    { text: "Why must you communicate with MC?", options: [
      "They sell the commercials",
      "They create the commercials",
      "They ultimately send commercials to air",
      "They monitor ratings"
    ], correct: 2 },
    { text: "What is the Hit Time column used for?", options: [
      "To show final airing time",
      "To estimate when commercials may air for planning",
      "To communicate with advertisers",
      "To mark dead units"
    ], correct: 1 },
  ];

  // 7 extra questions
  const extraQuestions: Question[] = [
    { text: "What information does the Length column show?", options: [
      "Program end time",
      "How long each unit is",
      "The advertiser’s budget",
      "The House Number"
    ], correct: 1 },
    { text: "What does the Title column show?", options: [
      "The advertiser’s email",
      "The show title and segment numbers",
      "The length of the break",
      "The Real Time of the show"
    ], correct: 1 },
    { text: "Why is the House Number important?", options: [
      "It shows how much the ad cost",
      "It’s used by MC to identify the specific ad",
      "It gives the brand’s phone number",
      "It determines the Window time"
    ], correct: 1 },
    { text: "What does “Ordered As” tell you?", options: [
      "The cost of the commercial",
      "The Window a commercial is sold to",
      "The advertiser’s name",
      "The float time"
    ], correct: 1 },
    { text: "What does Spot End Time show?", options: [
      "The moment a program starts",
      "The latest possible time a commercial can air",
      "The time a break should start",
      "The House Number"
    ], correct: 1 },
    { text: "What are Floaters?", options: [
      "Units that will never air",
      "Commercials that always run in the same slot",
      "Extra sold units that need to air during the game",
      "The same as a Program line"
    ], correct: 2 },
    { text: "What is the “Key” tab on the Live Coverage Sheet mainly used for?", options: [
      "To sell commercials",
      "To watch live games",
      "For reference of contingency information",
      "To communicate with advertisers"
    ], correct: 2 },
  ];

  let currentQuestionIndex = 0;
  let userAnswers: number[] = [];
  let showFeedback = false;
  let feedback = "";
  let showExtraQuestions = false;
  let extraQuestionIndex = 0;
  let extraUserAnswers: number[] = [];
  let showSummary = false;
  let score = 0;
  let failThreshold = 7; // must get at least 7/10 correct
  
  // Fullscreen state
  let isFullscreen = false;

  function submitAnswer(selected: number) {
    if (!showExtraQuestions) {
      userAnswers[currentQuestionIndex] = selected;
      showFeedback = true;
      const isCorrect = selected === mainQuestions[currentQuestionIndex].correct;
      feedback = isCorrect ? "✅ Correct!" : "❌ Incorrect.";
      if (mainQuestions[currentQuestionIndex].explanation) {
        feedback += " " + mainQuestions[currentQuestionIndex].explanation;
      }
    } else {
      extraUserAnswers[extraQuestionIndex] = selected;
      showFeedback = true;
      const isCorrect = selected === extraQuestions[extraQuestionIndex].correct;
      feedback = isCorrect ? "✅ Correct!" : "❌ Incorrect.";
      if (extraQuestions[extraQuestionIndex].explanation) {
        feedback += " " + extraQuestions[extraQuestionIndex].explanation;
      }
    }
  }

  function nextQuestion() {
    showFeedback = false;
    feedback = "";
    if (!showExtraQuestions) {
      if (currentQuestionIndex < mainQuestions.length - 1) {
        currentQuestionIndex++;
      } else {
        // Calculate score
        score = userAnswers.filter((ans, i) => ans === mainQuestions[i].correct).length;
        if (score < failThreshold) {
          showExtraQuestions = true;
          extraQuestionIndex = 0;
        } else {
          showSummary = true;
        }
      }
    } else {
      if (extraQuestionIndex < extraQuestions.length - 1) {
        extraQuestionIndex++;
      } else {
        showSummary = true;
      }
    }
  }

  function handleToggleFullscreen() {
    if (!isFullscreen) {
      // Enter fullscreen
      const playerArea = document.querySelector('[data-player-area]') as HTMLElement;
      if (playerArea && playerArea.requestFullscreen) {
        playerArea.requestFullscreen().then(() => {
          isFullscreen = true;
        }).catch(err => {
          console.log('Failed to enter fullscreen:', err);
        });
      }
    } else {
      // Exit fullscreen
      if (document.exitFullscreen) {
        document.exitFullscreen().then(() => {
          isFullscreen = false;
        }).catch(err => {
          console.log('Failed to exit fullscreen:', err);
        });
      }
    }
  }

  // Check fullscreen state on mount and listen for changes
  onMount(() => {
    isFullscreen = !!document.fullscreenElement;
    
    const handleFullscreenChange = () => {
      isFullscreen = !!document.fullscreenElement;
    };
    
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  });
</script>

{#if !showSummary}
  <div class="quiz-container" data-player-area>
    <!-- Fullscreen toggle button -->
    <button
      class="absolute top-4 right-4 z-50 p-2 rounded-lg bg-white/80 hover:bg-white shadow-lg transition-all duration-200 hover:scale-110"
      on:click={handleToggleFullscreen}
      title="Toggle fullscreen"
    >
      {#if isFullscreen}
        <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      {:else}
        <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/>
        </svg>
      {/if}
    </button>
    <div class="quiz-progress">
      {#if !showExtraQuestions}
        Question {currentQuestionIndex + 1} of {mainQuestions.length}
      {:else}
        Extra Question {extraQuestionIndex + 1} of {extraQuestions.length}
      {/if}
    </div>
    <div class="quiz-question">
      {#if !showExtraQuestions}
        {mainQuestions[currentQuestionIndex].text}
      {:else}
        {extraQuestions[extraQuestionIndex].text}
      {/if}
    </div>
    <div class="quiz-options">
      {#if !showExtraQuestions}
        {#each mainQuestions[currentQuestionIndex].options as option, i}
          <button on:click={() => submitAnswer(i)} disabled={showFeedback}>
            {option}
          </button>
        {/each}
      {:else}
        {#each extraQuestions[extraQuestionIndex].options as option, i}
          <button on:click={() => submitAnswer(i)} disabled={showFeedback}>
            {option}
          </button>
        {/each}
      {/if}
    </div>
    {#if showFeedback}
      <div class="quiz-feedback">{feedback}</div>
      <button on:click={nextQuestion}>
        {(!showExtraQuestions && currentQuestionIndex === mainQuestions.length - 1) ||
         (showExtraQuestions && extraQuestionIndex === extraQuestions.length - 1)
          ? 'Finish'
          : 'Next'}
      </button>
    {/if}
  </div>
{:else}
  <div class="quiz-summary" data-player-area>
    <!-- Fullscreen toggle button -->
    <button
      class="absolute top-4 right-4 z-50 p-2 rounded-lg bg-white/80 hover:bg-white shadow-lg transition-all duration-200 hover:scale-110"
      on:click={handleToggleFullscreen}
      title="Toggle fullscreen"
    >
      {#if isFullscreen}
        <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      {:else}
        <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"/>
        </svg>
      {/if}
    </button>
    <h2>Test Complete!</h2>
    <p>Your score: {score} / {mainQuestions.length}</p>
    {#if showExtraQuestions}
      <p>You were given extra questions to help reinforce your learning.</p>
    {/if}
    <!-- Add more summary/retake options here -->
  </div>
{/if}

<style>
.quiz-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.quiz-progress {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: #0074D9;
}
.quiz-question {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
}
.quiz-options button {
  display: block;
  width: 100%;
  margin-bottom: 0.5rem;
  padding: 0.75rem;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #c3c3c3;
  background: #fff;
  cursor: pointer;
  transition: background 0.2s;
}
.quiz-options button:disabled {
  background: #e0e0e0;
  cursor: not-allowed;
}
.quiz-options button:hover:enabled {
  background: #e6f7ff;
}
.quiz-feedback {
  margin: 1rem 0;
  font-size: 1.1rem;
  font-weight: 500;
}
.quiz-summary {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
  text-align: center;
}
</style> 
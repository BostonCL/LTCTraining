<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { onMount } from 'svelte';

  export let questions: {
    id: number;
    question: string;
    options: string[];
    correctAnswer: number;
    explanation?: string;
  }[] = [];
  
  export let title: string = 'Module Quiz';
  export let description: string = 'Test your knowledge with these questions.';
  export let passingScore: number = 70;
  export const showResults: boolean = true;
  export let image: string | undefined = undefined;

  const dispatch = createEventDispatcher();

  let currentQuestionIndex = 0;
  let selectedAnswers: (number | null)[] = [];
  let quizCompleted = false;
  let score = 0;
  let timeStarted: number;
  let timeCompleted: number;

  $: currentQuestion = questions[currentQuestionIndex];
  $: isLastQuestion = currentQuestionIndex === questions.length - 1;
  $: canProceed = selectedAnswers[currentQuestionIndex] !== null && selectedAnswers[currentQuestionIndex] !== undefined;
  $: progress = ((currentQuestionIndex) / questions.length) * 100;

  onMount(() => {
    timeStarted = Date.now();
    selectedAnswers = new Array(questions.length).fill(null);
  });

  function selectAnswer(optionIndex: number) {
    selectedAnswers[currentQuestionIndex] = optionIndex;
    selectedAnswers = [...selectedAnswers];
  }

  function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
      currentQuestionIndex++;
    }
  }

  function previousQuestion() {
    if (currentQuestionIndex > 0) {
      currentQuestionIndex--;
    }
  }

  function completeQuiz() {
    timeCompleted = Date.now();
    const correctAnswers = selectedAnswers.filter((answer, index) => 
      answer === questions[index].correctAnswer
    ).length;
    score = Math.round((correctAnswers / questions.length) * 100);
    quizCompleted = true;
    dispatch('quizCompleted', {
      score,
      passed: score >= passingScore,
      timeSpent: timeCompleted - timeStarted,
      answers: selectedAnswers
    });
  }
</script>

<div class="flex justify-center items-center min-h-[80vh] bg-gradient-to-br from-slate-50 to-blue-100">
  <div class="w-full max-w-2xl rounded-3xl overflow-hidden relative bg-gradient-to-br from-white/90 to-blue-50/80">
    <div class="p-6 sm:p-10">
      <h1 class="text-2xl font-extrabold text-slate-900 mb-1 tracking-tight">{title}</h1>
      <p class="text-slate-500 mb-6">{description}</p>

      {#if !quizCompleted}
        {#if questions.length > 1}
          <div class="flex items-center justify-between mb-4">
            <span class="text-sm text-slate-400 font-semibold tracking-wide flex items-center gap-1">📝 Question {currentQuestionIndex + 1} of {questions.length}</span>
          </div>
        {/if}
        
        {#if image}
          <div class="mb-6 flex justify-center">
            <img src={image} alt="" class="max-w-full max-h-64 object-contain rounded-lg shadow-md" />
          </div>
        {/if}
        
        <div class="text-2xl font-semibold text-slate-900 mb-6 animate-fadein font-display tracking-wide">{currentQuestion.question}</div>
        <div class="border-b border-slate-200 mb-6"></div>
        <div class="grid gap-4 mb-10 animate-fadein">
          {#each currentQuestion.options as option, optionIndex}
            <button
              type="button"
              class="w-full text-left rounded-xl border-2 px-5 py-4 text-base font-semibold focus:outline-none transition-all duration-200 transform
                {selectedAnswers[currentQuestionIndex] === optionIndex
                  ? 'border-blue-600 bg-blue-50 shadow-lg scale-105 text-blue-900 ring-2 ring-blue-200'
                  : 'border-slate-200 bg-white hover:border-blue-400 hover:bg-blue-50 hover:scale-[1.03]'}"
              on:click={() => selectAnswer(optionIndex)}
              aria-pressed={selectedAnswers[currentQuestionIndex] === optionIndex}
            >
              <span class="inline-block align-middle">{option}</span>
              {#if selectedAnswers[currentQuestionIndex] === optionIndex}
                <span class="float-right ml-2 text-blue-600 text-xl align-middle">✔</span>
              {/if}
            </button>
          {/each}
        </div>
        <div class="flex justify-between items-center gap-2 mt-2">
          {#if questions.length > 1}
            <button
              class="px-4 py-2 rounded-lg text-slate-500 bg-slate-100 hover:bg-slate-200 font-medium disabled:opacity-40"
              on:click={previousQuestion}
              disabled={currentQuestionIndex === 0}
            >
              ← Previous
            </button>
          {:else}
            <div></div>
          {/if}
          {#if isLastQuestion}
            <button
              class="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 disabled:opacity-40"
              on:click={completeQuiz}
              disabled={!canProceed}
            >
              Complete Quiz
            </button>
          {:else}
            <button
              class="px-6 py-2 rounded-lg bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 disabled:opacity-40"
              on:click={nextQuestion}
              disabled={!canProceed}
            >
              Next →
            </button>
          {/if}
        </div>
      {:else}
        <div class="relative flex flex-col items-center justify-center py-16">
          <!-- Confetti background (CSS dots) -->
          <div class="absolute inset-0 pointer-events-none z-0">
            <div class="w-full h-full bg-[radial-gradient(circle,_#dbeafe_1.5px,_transparent_1.5px)] bg-[length:32px_32px] opacity-60 animate-fadein"></div>
          </div>
          <div class="relative z-10 flex flex-col items-center">
            {#if score >= passingScore}
              <div class="rounded-full bg-green-100 p-6 mb-4 animate-fadein">
                <svg class="w-16 h-16 text-green-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2l4-4"/></svg>
              </div>
              <div class="text-2xl font-bold text-green-700 mb-2 animate-fadein">Congratulations! You passed!</div>
            {:else}
              <div class="rounded-full bg-red-100 p-6 mb-4 animate-fadein">
                <svg class="w-16 h-16 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
              </div>
              <div class="text-2xl font-bold text-red-700 mb-2 animate-fadein">Try again next time.</div>
            {/if}
            <div class="text-4xl font-extrabold my-4 text-slate-900 animate-fadein">{score}%</div>
            <button
              class="px-8 py-3 rounded-lg bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 mt-6 text-lg animate-fadein"
              on:click={() => dispatch('continue')}
            >
              Continue
            </button>
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  @keyframes fadein {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: none; }
  }
  .animate-fadein {
    animation: fadein 0.5s cubic-bezier(.4,0,.2,1);
  }
  button[aria-pressed="true"] {
    outline: 2px solid #2563eb;
    outline-offset: 2px;
  }
</style> 
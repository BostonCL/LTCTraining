<script lang="ts">
import QuizTemplate from '$lib/components/QuizTemplate.svelte';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

const questions = [
  {
    id: 1,
    question: 'Why is the House Number important?',
    options: [
      "It shows the ad's cost",
      "It tells you when to air the ad",
      "It helps MC know exactly which ad you're referring to."
    ],
    correctAnswer: 2, // c) It helps MC know exactly which ad you're referring to.
    explanation: 'The House Number is a unique identifier that helps Master Control (MC) know exactly which ad you are referring to.'
  }
];

function handleQuizCompleted(event: CustomEvent) {
  const { score, passed, timeSpent, answers } = event.detail;
  dispatch('quizCompleted', { score, passed, timeSpent, answers });
}

function handleContinue() {
  dispatch('navigateToNextSubmodule');
}
</script>

<div class="min-h-screen bg-gray-50 py-8 px-4">
  <QuizTemplate
    questions={questions}
    title="House Number Quiz"
    description="Test your understanding of why the House Number is important."
    passingScore={100}
    on:quizCompleted={handleQuizCompleted}
    on:continue={handleContinue}
  />
</div> 
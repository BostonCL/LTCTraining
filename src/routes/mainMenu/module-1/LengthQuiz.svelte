<script lang="ts">
import QuizTemplate from '$lib/components/QuizTemplate.svelte';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

const questions = [
  {
    id: 1,
    question: 'How long would this commercial break be?',
    image: '', // To be filled in with the screenshot path
    options: [
      '2:30 mins',
      '2:00 mins',
      '1:45 mins',
      '2:15 mins'
    ],
    correctAnswer: 0, // A) 2:30 mins
    explanation: 'The correct answer is 2:30 mins, based on the sum of the lengths in the provided sheet.'
  }
];

function handleQuizCompleted(event: CustomEvent) {
  const { score, passed, timeSpent, answers } = event.detail;
  // Record the quiz result or trigger completion logic here
  dispatch('quizCompleted', { score, passed, timeSpent, answers });
}

function handleContinue() {
  // Dispatch event to navigate to the next submodule
  dispatch('navigateToNextSubmodule');
}
</script>

<div class="min-h-screen bg-gray-50 py-8 px-4">
  <img src="/images/LengthQuiz.png" alt="Length Quiz Screenshot" class="mx-auto mb-6 max-w-full h-auto rounded shadow" />
  <QuizTemplate
    questions={questions}
    title="Length Quiz"
    description="Test your understanding of how to calculate the total length of a commercial break."
    passingScore={100}
    on:quizCompleted={handleQuizCompleted}
    on:continue={handleContinue}
  />
</div> 
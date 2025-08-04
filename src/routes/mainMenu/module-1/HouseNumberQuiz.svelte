<script lang="ts">
  import QuizTemplate from '$lib/components/QuizTemplate.svelte';
  import { createEventDispatcher } from 'svelte';
  import { quizStore } from '$lib/stores/quizStore';

  const dispatch = createEventDispatcher();

  const questions = [
    {
      id: 1,
      question: "What is the purpose of the House Number on the Live Coverage Sheet?",
      options: [
        "To show the cost of the commercial",
        "To identify the specific commercial for Master Control",
        "To indicate the time slot",
        "To show the advertiser's contact information"
      ],
      correctAnswer: 1,
      explanation: "The House Number is a unique identifier that Master Control uses to identify which specific commercial to air, especially when an advertiser has multiple different ads."
    },
    {
      id: 2,
      question: "Why is the House Number important when communicating with Master Control?",
      options: [
        "It shows how much the ad costs",
        "It helps MC identify the exact commercial to air",
        "It indicates the time the ad should air",
        "It shows the advertiser's name"
      ],
      correctAnswer: 1,
      explanation: "Since one advertiser (like Geico) can have several different ads, the house number is key for clarity when communicating with Master Control."
    }
  ];

  function handleQuizCompleted(event: CustomEvent) {
    const { score, passed, timeSpent, answers } = event.detail;
    console.log(`Quiz completed! Score: ${score}%, Passed: ${passed}, Time: ${timeSpent}ms`);
    
    // Record the quiz result
    quizStore.recordResult({
      moduleId: 'house-number',
      score,
      passed,
      timeSpent,
      completedAt: new Date(),
      answers
    });
  }

  function handleContinue() {
    // Dispatch event to navigate to the next submodule
    console.log('HouseNumberQuiz: handleContinue called');
    dispatch('navigateToNextSubmodule');
  }
</script>

<QuizTemplate
  questions={questions}
  title="House Number Quiz"
  description="Test your understanding of the House Number column and its importance."
  passingScore={80}
  on:quizCompleted={handleQuizCompleted}
  on:continue={handleContinue}
/> 
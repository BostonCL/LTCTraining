<script lang="ts">
  import QuizTemplate from '$lib/components/QuizTemplate.svelte';
  import { createEventDispatcher } from 'svelte';
  import { quizStore } from '$lib/stores/quizStore';

  const dispatch = createEventDispatcher();

  const questions = [
    {
      id: 1,
      question: "What does the Length column show on the Live Coverage Sheet?",
      options: [
        "The time the show starts",
        "How long each unit is",
        "The advertiser's name",
        "The house number"
      ],
      correctAnswer: 1,
      explanation: "The Length column shows how long each commercial unit is (e.g., 30 seconds, 60 seconds, etc.)."
    },
    {
      id: 2,
      question: "If a commercial break has three 30-second spots, what is the total length of that break?",
      options: [
        "30 seconds",
        "60 seconds",
        "90 seconds",
        "120 seconds"
      ],
      correctAnswer: 2,
      explanation: "Three 30-second spots would total 90 seconds (30 + 30 + 30 = 90)."
    }
  ];

  function handleQuizCompleted(event: CustomEvent) {
    const { score, passed, timeSpent, answers } = event.detail;
    console.log(`Quiz completed! Score: ${score}%, Passed: ${passed}, Time: ${timeSpent}ms`);
    
    // Record the quiz result
    quizStore.recordResult({
      moduleId: 'length',
      score,
      passed,
      timeSpent,
      completedAt: new Date(),
      answers
    });
  }

  function handleContinue() {
    // Dispatch event to navigate to the next submodule
    dispatch('navigateToNextSubmodule');
  }
</script>

<QuizTemplate
  questions={questions}
  title="Length Quiz"
  description="Test your understanding of the Length column and commercial break timing."
  passingScore={80}
  on:quizCompleted={handleQuizCompleted}
  on:continue={handleContinue}
/> 
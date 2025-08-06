<script lang="ts">
  import QuizTemplate from '$lib/components/QuizTemplate.svelte';
  import { createEventDispatcher } from 'svelte';
  import { quizStore } from '$lib/stores/quizStore';

  const dispatch = createEventDispatcher();

  const questions = [
    {
      id: 1,
      question: "A football game is scheduled to begin at 7:00:00 PM, but due to a delay, it actually begins at 7:06:45 PM. What is the Real Time of the game?",
      options: [
        "7:06:45 PM",
        "7:00:00 PM",
        "7:05:00 PM",
        "6:55:00 PM"
      ],
      correctAnswer: 1,
      explanation: "Real Time is always the scheduled time (7:00:00 PM), regardless of when the game actually starts. Even though the game was delayed and started at 7:06:45 PM, the Real Time remains the originally scheduled time."
    },
    {
      id: 2,
      question: "A football game is scheduled to begin at 7:00:00 PM, but due to a delay, it actually begins at 7:06:45 PM. Using the same example above, what is the Start Time?",
      options: [
        "7:00:00 PM",
        "6:59:59 PM",
        "7:06:45 PM",
        "7:10:00 PM"
      ],
      correctAnswer: 2,
      explanation: "Start Time is the actual time when the event begins. In this case, the game actually started at 7:06:45 PM due to the delay, so that is the Start Time."
    }
  ];

  function handleQuizCompleted(event: CustomEvent) {
    const { score, passed, timeSpent, answers } = event.detail;
    console.log(`Quiz completed! Score: ${score}%, Passed: ${passed}, Time: ${timeSpent}ms`);
    
    // Record the quiz result
    quizStore.recordResult({
      moduleId: 'start-time-real-time',
      score,
      passed,
      timeSpent,
      completedAt: new Date(),
      answers
    });
  }

  function handleContinue() {
    // Dispatch event to navigate to the next submodule
    console.log('StartTimeRealTimeQuiz: handleContinue called');
    dispatch('navigateToNextSubmodule');
  }
</script>

<QuizTemplate
  questions={questions}
  title="Start Time & Real Time Quiz"
  description="Test your understanding of Real Time vs Start Time concepts."
  passingScore={80}
  on:quizCompleted={handleQuizCompleted}
  on:continue={handleContinue}
/> 
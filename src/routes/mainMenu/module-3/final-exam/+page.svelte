<script lang="ts">
import FinalExam from '../FinalExam.svelte';
import { goto } from '$app/navigation';

let progressId = 'module3_finalexam';
let nextButtonText = "Complete Training";

function handleNext() {
  // Navigate to completion or back to main menu
  goto('/mainMenu');
}
</script>

<FinalExam {progressId} {nextButtonText} on:navigateToNextSubmodule={handleNext} /> 
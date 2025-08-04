<script lang="ts">
import TheYellowUnit from '../TheYellowUnit.svelte';
import { goto } from '$app/navigation';

let progressId = 'module2_yellowunit';
let nextButtonText = "Next";

function handleNext() {
  goto('/mainMenu/module-2/unitprioritizationdetails');
}
</script>

<TheYellowUnit {progressId} {nextButtonText} on:navigateToNextSubmodule={handleNext} /> 
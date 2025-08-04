<script lang="ts">
import UnitPrioritizationDetails from '../UnitPrioritizationDetails.svelte';
import { goto } from '$app/navigation';

let progressId = 'module2_unitprioritizationdetails';
let nextButtonText = "Next";

function handleNext() {
  goto('/mainMenu/module-2/greenpurpleunits');
}
</script>

<UnitPrioritizationDetails {progressId} {nextButtonText} on:navigateToNextSubmodule={handleNext} /> 
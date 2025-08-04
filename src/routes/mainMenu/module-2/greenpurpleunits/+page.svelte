<script lang="ts">
import GreenPurpleUnits from '../GreenPurpleUnits.svelte';
import { goto } from '$app/navigation';

let progressId = 'module2_greenpurpleunits';

function handleNext() {
  goto('/mainMenu/module-2/test');
}
</script>

<GreenPurpleUnits {progressId} on:navigateToNextSubmodule={handleNext} /> 
<script lang="ts">
import SellingTitle from '../SellingTitle.svelte';
import { goto } from '$app/navigation';

let progressId = 'module2_sellingtitle';
let nextButtonText = "Next";

function handleNext() {
  goto('/mainMenu/module-2/yellowunit');
}
</script>

<SellingTitle {progressId} {nextButtonText} on:navigateToNextSubmodule={handleNext} /> 
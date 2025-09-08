<script lang="ts">
import { goto } from '$app/navigation';

function downloadTrainingGuide() {
  // Create a link element to trigger the download
  const link = document.createElement('a');
  link.href = '/training-guide.pdf';
  link.download = 'CBS Sports Network Traffic Department Training Guide.pdf';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function goToMainMenu() {
  goto('/mainMenu');
}
</script>

<div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg text-center">
  <div class="mb-8">
    <!-- Success Icon -->
    <div class="mx-auto w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mb-6">
      <svg class="w-12 h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
    </div>
    
    <h1 class="text-4xl font-bold text-gray-800 mb-4">🎉 Congratulations! 🎉</h1>
    <p class="text-xl text-gray-600 mb-6">You have successfully completed the CBS Sports Network Traffic Department Training!</p>
    
    <div class="bg-green-50 border border-green-200 rounded-lg p-6 mb-8">
      <h2 class="text-2xl font-semibold text-green-800 mb-3">Training Complete!</h2>
      <p class="text-green-700 mb-4">
        You've demonstrated mastery of Live Traffic procedures, brand separation rules, 
        commercial management, and all essential skills needed for the Traffic Department.
      </p>
      <p class="text-green-700 font-medium">
        You are now ready to handle live traffic responsibilities with confidence!
      </p>
    </div>
  </div>

  <!-- Download Section -->
  <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
    <h3 class="text-xl font-semibold text-blue-800 mb-3">📚 Download Your Training Guide</h3>
    <p class="text-blue-700 mb-4">
      Download the complete CBS Sports Network Traffic Department Training Guide for future reference.
      This comprehensive guide contains all the procedures, rules, and best practices you've learned.
    </p>
    
    <button 
      on:click={downloadTrainingGuide}
      class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200 flex items-center justify-center mx-auto"
    >
      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
      </svg>
      Download Training Guide (PDF)
    </button>
  </div>



  <!-- Action Buttons -->
  <div class="flex flex-col sm:flex-row gap-4 justify-center">
    <button 
      on:click={goToMainMenu}
      class="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200"
    >
      Return to Main Menu
    </button>
  </div>
</div>

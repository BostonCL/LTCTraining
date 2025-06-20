<script lang="ts">
  import { onMount } from 'svelte';
  import { getAuth, signOut, type Auth } from 'firebase/auth';
  // Placeholder modules
  const modules = [
    {
      title: 'Module 1: Introduction',
      description: 'Get an overview of live traffic coverage and its importance.',
      status: 'Not started'
    },
    {
      title: 'Module 2: Tools & Technology',
      description: 'Learn about the tools and technology used in live traffic reporting.',
      status: 'In progress'
    },
    {
      title: 'Module 3: Best Practices',
      description: 'Discover best practices for effective and accurate coverage.',
      status: 'Completed'
    }
  ];

  let auth: Auth | undefined;
  onMount(() => {
    auth = getAuth();
  });

  async function handleLogout() {
    try {
      if (auth) {
        await signOut(auth);
      }
      window.location.href = '/';
    } catch (e) {
      alert('Logout failed. Please try again.');
    }
  }
</script>

<!-- Header -->
<header class="w-full flex items-center justify-between py-6 px-8 bg-white shadow-sm mb-12">
  <span class="text-2xl font-bold text-gray-900 tracking-tight">Live Traffic Coverage Training</span>
  <div class="flex items-center gap-4">
    <a href="/mainMenuV1" class="text-blue-600 hover:underline text-sm font-medium">Show V1</a>
    <button on:click={handleLogout} class="text-gray-500 hover:text-gray-700 text-base font-medium rounded px-4 py-2 border border-gray-200 bg-gray-50">Logout</button>
  </div>
</header>

<!-- Main Content -->
<main class="w-full max-w-2xl mx-auto px-4">
  <!-- Course Overview -->
  <section class="mb-12">
    <h2 class="text-xl font-semibold text-gray-800 mb-1">Your Training Timeline (V2)</h2>
    <p class="text-gray-500 text-base mb-6">Progress through each module in order. Click to start or continue.</p>
  </section>

  <!-- Timeline Modules List -->
  <section class="relative border-l-2 border-gray-200 pl-8">
    {#each modules as module, i}
      <div class="mb-12 relative group">
        <div class="absolute -left-5 top-1 w-4 h-4 rounded-full border-2 border-gray-300 bg-white group-hover:border-blue-500 transition"></div>
        <div class="flex flex-col md:flex-row md:items-center md:justify-between">
          <div>
            <h3 class="text-lg font-bold text-gray-900 mb-1">{module.title}</h3>
            <p class="text-gray-500 mb-2">{module.description}</p>
            <span class="text-xs px-2 py-1 rounded-full font-medium
              {module.status === 'Completed' ? 'bg-green-100 text-green-700' : ''}
              {module.status === 'In progress' ? 'bg-yellow-100 text-yellow-700' : ''}
              {module.status === 'Not started' ? 'bg-gray-100 text-gray-500' : ''}">
              {module.status}
            </span>
          </div>
          <button class="mt-4 md:mt-0 ml-0 md:ml-6 px-5 py-2 text-sm font-semibold rounded bg-blue-600 text-white hover:bg-blue-700 transition shadow">
            {module.status === 'Completed' ? 'Review' : module.status === 'In progress' ? 'Continue' : 'Start'}
          </button>
        </div>
      </div>
    {/each}
  </section>
</main> 
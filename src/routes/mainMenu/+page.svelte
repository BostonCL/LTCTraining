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
<header class="w-full flex items-center justify-between py-4 px-6 bg-white shadow-sm mb-8">
  <span class="text-xl font-bold text-gray-900 tracking-tight">Live Traffic Coverage Training</span>
  <button on:click={handleLogout} class="text-gray-500 hover:text-gray-700 text-sm font-medium rounded px-3 py-1 border border-gray-200 bg-gray-50">Logout</button>
</header>

<!-- Main Content -->
<main class="w-full max-w-3xl mx-auto px-4">
  <!-- Course Overview -->
  <section class="mb-10 text-center">
    <h2 class="text-2xl font-semibold text-gray-800 mb-2">Welcome to your training dashboard</h2>
    <p class="text-gray-500 text-base md:text-lg">Select a module below to begin or continue your training.</p>
  </section>

  <!-- Modules List -->
  <section class="grid gap-6 md:grid-cols-2">
    {#each modules as module}
      <div class="bg-white rounded-xl shadow p-6 flex flex-col justify-between border border-gray-100">
        <div>
          <h3 class="text-lg font-bold text-gray-900 mb-1">{module.title}</h3>
          <p class="text-gray-500 mb-4">{module.description}</p>
        </div>
        <div class="flex items-center justify-between mt-auto">
          <span class="text-xs px-2 py-1 rounded-full font-medium
            {module.status === 'Completed' ? 'bg-green-100 text-green-700' : ''}
            {module.status === 'In progress' ? 'bg-yellow-100 text-yellow-700' : ''}
            {module.status === 'Not started' ? 'bg-gray-100 text-gray-500' : ''}">
            {module.status}
          </span>
          <button class="ml-2 px-4 py-1.5 text-sm font-semibold rounded bg-gray-900 text-white hover:bg-gray-800 transition">
            {module.status === 'Completed' ? 'Review' : module.status === 'In progress' ? 'Continue' : 'Start'}
          </button>
        </div>
      </div>
    {/each}
  </section>
</main> 
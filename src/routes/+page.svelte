<script lang="ts">
  import { onMount } from 'svelte';
  import { signInWithEmailAndPassword, createUserWithEmailAndPassword, onAuthStateChanged } from 'firebase/auth';
  import { auth } from '$lib/firebase';

  let email = '';
  let password = '';
  let error = '';
  let loading = false;
  let isLogin = true;
  let loginAttempts = 0;
  const maxAttempts = 5;
  let isRateLimited = false;
  let rateLimitTimer: ReturnType<typeof setTimeout>;

  // Check if user is already authenticated
  onMount(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        // User is already signed in, redirect to main menu
        window.location.href = '/mainMenu';
      }
    });
    
    return unsubscribe;
  });

  async function handleSubmit() {
    // Check rate limiting
    if (isRateLimited) {
      error = 'Too many attempts. Please wait before trying again.';
      return;
    }

    if (loginAttempts >= maxAttempts) {
      isRateLimited = true;
      error = 'Too many login attempts. Please wait 5 minutes before trying again.';
      
      // Reset after 5 minutes
      rateLimitTimer = setTimeout(() => {
        isRateLimited = false;
        loginAttempts = 0;
        error = '';
      }, 5 * 60 * 1000);
      
      return;
    }

    loading = true;
    error = '';
    loginAttempts++;
    
    try {
      if (isLogin) {
        await signInWithEmailAndPassword(auth, email, password);
        window.location.href = '/mainMenu';
      } else {
        await createUserWithEmailAndPassword(auth, email, password);
        window.location.href = '/mainMenu';
      }
    } catch (e: any) {
      if (e.code === 'auth/too-many-requests') {
        error = 'Too many requests. Please wait a moment before trying again.';
        isRateLimited = true;
        
        // Reset after 2 minutes for Firebase rate limiting
        setTimeout(() => {
          isRateLimited = false;
        }, 2 * 60 * 1000);
      } else {
        error = e.message;
      }
    } finally {
      loading = false;
    }
  }

  // Cleanup timer on component destroy
  onMount(() => {
    return () => {
      if (rateLimitTimer) {
        clearTimeout(rateLimitTimer);
      }
    };
  });
</script>

<div class="min-h-screen bg-gray-100 flex flex-col items-center justify-center px-4">
  <div class="mb-12 mt-8 md:mt-0 text-center">
    <h1 class="text-3xl md:text-4xl font-semibold text-gray-900 mb-2 tracking-tight">Welcome to</h1>
    <h2 class="text-2xl md:text-3xl font-bold text-gray-800 mb-2">Live Traffic Coverage Training</h2>
    <p class="text-gray-500 text-base md:text-lg">Sign in or create your account to get started.</p>
  </div>
  <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-10 flex flex-col items-center">
    <div class="w-full">
      <h2 class="text-base font-medium text-center mb-4 text-gray-700">{isLogin ? 'Login' : 'Create Account'}</h2>
      <form on:submit|preventDefault={handleSubmit} class="space-y-5">
        <input
          class="block w-full border border-gray-300 focus:border-blue-500 rounded-lg px-4 py-2 outline-none transition bg-gray-50 placeholder-gray-400"
          type="email"
          placeholder="Email"
          bind:value={email}
          required
        />
        <input
          class="block w-full border border-gray-300 focus:border-blue-500 rounded-lg px-4 py-2 outline-none transition bg-gray-50 placeholder-gray-400"
          type="password"
          placeholder="Password"
          bind:value={password}
          required
        />
        <button
          class="w-full bg-gray-900 hover:bg-gray-800 text-white py-2.5 rounded-lg font-semibold shadow transition disabled:opacity-50 text-base"
          type="submit"
          disabled={loading}
        >
          {loading ? (isLogin ? 'Logging in...' : 'Creating account...') : (isLogin ? 'Login' : 'Create Account')}
        </button>
        <button
          type="button"
          class="w-full text-gray-500 hover:text-gray-700 underline text-xs mt-2"
          on:click={() => { isLogin = !isLogin; error = ''; }}
        >
          {isLogin ? 'Need to create an account?' : 'Already have an account? Login'}
        </button>
        {#if error}
          <p class="text-red-600 text-center mt-2 text-sm">{error}</p>
        {/if}
      </form>
    </div>
  </div>
</div>

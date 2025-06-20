<script lang="ts">
  import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword } from 'firebase/auth';
  import { app } from '$lib/firebase';

  let email = '';
  let password = '';
  let error = '';
  let loading = false;
  let isLogin = true;

  const auth = getAuth(app);

  async function handleSubmit() {
    loading = true;
    error = '';
    try {
      if (isLogin) {
        await signInWithEmailAndPassword(auth, email, password);
        window.location.href = '/';
      } else {
        await createUserWithEmailAndPassword(auth, email, password);
        window.location.href = '/';
      }
    } catch (e: any) {
      error = e.message;
    } finally {
      loading = false;
    }
  }
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

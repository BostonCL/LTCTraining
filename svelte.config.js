import adapter from '@sveltejs/adapter-vercel';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
	preprocess: vitePreprocess(),
	kit: { 
		adapter: adapter({
			includeFiles: ['static/**/*']
		}),
		files: {
			assets: 'static'
		}
	}
};

export default config;

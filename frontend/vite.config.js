import path from 'node:path';
import preact from '@preact/preset-vite';
import {defineConfig, loadEnv} from 'vite';

const envDirectory = path.join(import.meta.dirname, '..');
const envPrefix = 'SOCIAL_FE_';

export default defineConfig(({mode}) => {
	const env = loadEnv(mode, envDirectory, envPrefix);

	return {
		server: {
			host: env.SOCIAL_FE_HOST,
			port: Number(env.SOCIAL_FE_PORT),
			strictPort: true,
		},
		plugins: [preact()],
		envDir: envDirectory,
		envPrefix,
	};
});

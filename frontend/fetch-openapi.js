#!/usr/bin/env node
import {spawnSync} from 'node:child_process';
import process from 'node:process';
import {fileURLToPath} from 'node:url';
import {loadEnv} from 'vite';

const envDirectory = fileURLToPath(new URL('..', import.meta.url));
const envPrefix = 'SOCIAL_FE_';

const env = loadEnv(
	process.env.NODE_ENV ?? 'development',
	envDirectory,
	envPrefix,
);

spawnSync(
	'pnpm',
	[
		'exec',
		'openapi-typescript',
		new URL('openapi/openapi.json', env.SOCIAL_FE_BE_URL).href,
		'-o',
		fileURLToPath(new URL('src/services/api.d.ts', import.meta.url)),
	],
	{
		stdio: 'inherit',
	},
);

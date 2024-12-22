#!/usr/bin/env node
import process from 'node:process';
import {fileURLToPath} from 'node:url';
import {loadEnv} from 'vite';
import {createClient} from '@hey-api/openapi-ts';

const envDirectory = fileURLToPath(new URL('..', import.meta.url));
const envPrefix = 'SOCIAL_FE_';

const env = loadEnv(
	process.env.NODE_ENV ?? 'development',
	envDirectory,
	envPrefix,
);

createClient({
	client: '@hey-api/client-fetch',
	input: new URL('openapi/openapi.json', env.SOCIAL_FE_BE_URL).href,
	output: fileURLToPath(new URL('src/api', import.meta.url)),
});

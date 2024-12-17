import createClient from 'openapi-fetch';
import type {paths} from './api.js';

export const apiUrl = new URL(String(import.meta.env.SOCIAL_FE_BE_URL));

export const client = createClient<paths>({
	baseUrl: apiUrl.href,
});

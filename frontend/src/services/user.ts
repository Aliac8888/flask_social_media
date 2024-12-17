import type {components} from './api.js';
import {client} from './backend.js';

export async function createUser(userData: components['schemas']['UserInit']) {
	const {data, response} = await client.POST('/users/', {
		body: userData,
	});

	if (!data) {
		throw new Error('Failed to create a new user', {cause: response});
	}

	return data;
}

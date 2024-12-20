import {apiUrl} from './backend.js';

export type User = {
	name: string;
	email: string;
	// TODO: Add friends property.
};

export async function createUser(userData: User) {
	const response = await fetch(new URL('users/', apiUrl), {
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify(userData),
	});

	return response.json();
}

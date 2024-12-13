import {apiUrl} from './backend.js';

export type Comment = {
	body: string;
	// TODO: Add post and author properties.
};

export async function createComment(commentData: Comment) {
	const response = await fetch(new URL('comments/', apiUrl), {
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify(commentData),
	});

	return response.json();
}

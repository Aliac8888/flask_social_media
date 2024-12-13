import {apiUrl} from './backend.js';

export type Post = {
	body: string;
	date: Date;
	special: boolean;
	// TODO: Add author property.
};

export async function createPost(postData: Post) {
	const response = await fetch(new URL('posts/', apiUrl), {
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify(postData),
	});

	return response.json();
}

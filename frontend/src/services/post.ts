import type {components} from './api.js';
import {apiUrl} from './backend.js';

export type PostPatch = components['schemas']['PostPatch'];
export type PostWithId = components['schemas']['PostWithId'];
export type PostsList = components['schemas']['PostsList'];
export type PostNotFound = components['schemas']['PostNotFound'];
export type PostInit = components['schemas']['PostInit'];
export type PostId = components['schemas']['PostId'];

export async function getPosts() {
	const response = await fetch(new URL('posts/', apiUrl));
	const data = (await response.json()) as PostsList;

	return data.posts.map((post) => ({
		...post,
		date: new Date(post.creation_time), // Convert string to Date object.
	}));
}

export async function createPost(postData: PostInit) {
	const response = await fetch(new URL('posts/', apiUrl), {
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify({
			content: postData.content,
			author: '6761f019eff4f614566204e3',
		}),
	});

	return response.json();
}

export async function updatePost(postId: string, patchData: PostPatch) {
	const response = await fetch(new URL(`posts/${postId}`, apiUrl), {
		method: 'PATCH',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify(patchData),
	});

	return response;
}

import type {components} from './api.js';
import {apiUrl} from './backend.js';

export type CommentPatch = components['schemas']['CommentPatch'];
export type CommentWithId = components['schemas']['CommentWithId'];
export type CommentsList = components['schemas']['CommentsList'];
export type CommentNotFound = components['schemas']['CommentNotFound'];
export type CommentInit = components['schemas']['CommentInit'];
export type CommentId = components['schemas']['CommentId'];

export async function createComment(commentData: CommentInit) {
	const response = await fetch(new URL('comments/', apiUrl), {
		method: 'POST',
		headers: {'Content-Type': 'application/json'},
		body: JSON.stringify(commentData),
	});

	return response.json();
}

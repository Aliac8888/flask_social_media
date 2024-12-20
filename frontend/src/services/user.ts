import type {components} from './api.js';
import {client} from './backend.js';

export type UserExists = components['schemas']['UserExists'];
export type UserWithFriends = components['schemas']['UserWithFriends'];
export type UserPatch = components['schemas']['UserPatch'];
export type UserWithId = components['schemas']['UserWithId'];
export type UsersList = components['schemas']['UsersList'];
export type UserNotFound = components['schemas']['UserNotFound'];
export type UserInit = components['schemas']['UserInit'];
export type UserId = components['schemas']['UserId'];

export async function createUser(userData: UserInit) {
	const {data, response} = await client.POST('/users/', {
		body: userData,
	});

	if (!data) {
		throw new Error('Failed to create a new user', {cause: response});
	}

	return data;
}

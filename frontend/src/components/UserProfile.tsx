import type {UserWithFriends} from '../services/user.js';

export function UserProfile({user}: {user: UserWithFriends}) {
	return (
		<div class="user-profile">
			<div class="user-profile__name">{user.name}</div>
			<div class="user-profile__email">{user.email}</div>
			{/* TODO: Add friends view. */}
		</div>
	);
}

import type {User} from '../api/index.js';

export function UserProfile({user}: {user: User}) {
	return (
		<div class="user-profile">
			<div class="user-profile__name">{user.name}</div>
			<div class="user-profile__email">{user.email}</div>
			{/* TODO: Add friends view. */}
		</div>
	);
}

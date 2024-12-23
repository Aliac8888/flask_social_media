import type {User} from '../api/index.js';

export function UserView({user}: {user: User}) {
	return (
		<div class="user-view">
			<div class="user-view__name">{user.name}</div>
			<div class="user-view__email">{user.email}</div>
		</div>
	);
}

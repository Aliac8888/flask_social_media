import type {User} from '../services/user.js';
import './UserProfile.css';

export function UserProfile({user}: {user: User}) {
	return (
		<div class="user-profile">
			<div class="user-profile__name">{user.name}</div>
			<div class="user-profile__email">{user.email}</div>
			{/* TODO: Add friends view. */}
		</div>
	);
}

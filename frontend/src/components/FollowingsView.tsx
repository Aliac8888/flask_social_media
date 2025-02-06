import {useState} from 'preact/hooks';
import {getUserFollowers, getUserFollowings} from '../api/sdk.gen.js';
import type {User} from '../api/types.gen.js';
import {useAsyncEffect} from '../async-effect.js';
import './FollowingsView.css';
import {UserView} from './UserView.js';

export function FollowingsView({
	user,
	reversed,
}: {
	user: User;
	reversed?: boolean;
}) {
	const [users, setUsers] = useState<User[]>([]);

	useAsyncEffect(async () => {
		setUsers([]);

		let data;

		if (reversed) {
			({data} = await getUserFollowers({
				path: {
					// eslint-disable-next-line @typescript-eslint/naming-convention
					user_id: user.id,
				},
			}));
		} else {
			({data} = await getUserFollowings({
				path: {
					// eslint-disable-next-line @typescript-eslint/naming-convention
					user_id: user.id,
				},
			}));
		}

		if (data) {
			setUsers(data);
		}
	}, [user.id, reversed]);

	return users.length > 0 ? (
		<div class="followings-view">
			{users.map((i) => (
				<div class="followings-view__user">
					<UserView user={i} />
				</div>
			))}
		</div>
	) : null;
}

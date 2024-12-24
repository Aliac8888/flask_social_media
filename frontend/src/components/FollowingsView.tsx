import {useEffect, useState} from 'preact/hooks';
import type {User} from '../api/types.gen.js';
import {userGet, userUserIdFollowingsGet} from '../api/sdk.gen.js';
import {useAsyncEffect} from '../async-effect.js';
import {UserView} from './UserView.js';
import './FollowingsView.css';

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
			({data} = await userGet({
				query: {
					// eslint-disable-next-line @typescript-eslint/naming-convention
					following_id: user.id,
				},
			}));
		} else {
			({data} = await userUserIdFollowingsGet({
				path: {
					// eslint-disable-next-line @typescript-eslint/naming-convention
					user_id: user.id,
				},
			}));
		}

		if (data) {
			setUsers(data.users);
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

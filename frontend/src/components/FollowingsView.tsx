import {useEffect, useState} from 'preact/hooks';
import type {User} from '../api/types.gen.js';
import {userGet, userUserIdFollowingsGet} from '../api/sdk.gen.js';
import {useAsyncEffect} from '../async-effect.js';
import {UserView} from './UserView.js';

export function FollowingsView({user}: {user: User}) {
	const [followings, setFollowings] = useState<User[]>([]);

	useAsyncEffect(async () => {
		const {data} = await userUserIdFollowingsGet({
			path: {
				// eslint-disable-next-line @typescript-eslint/naming-convention
				user_id: user.id,
			},
		});

		if (data) {
			setFollowings(data.users);
		}
	}, [user.id]);

	return followings.length > 0 ? (
		<div>
			<p>Followings</p>
			<div>
				{followings.map((i) => (
					<UserView user={i} />
				))}
			</div>
		</div>
	) : null;
}

import {useEffect, useState} from 'preact/hooks';
import type {User} from '../api/types.gen.js';
import {userGet} from '../api/sdk.gen.js';
import {useAsyncEffect} from '../async-effect.js';
import {UserView} from './UserView.js';

export function FollowersView({user}: {user: User}) {
	const [followers, setFollowers] = useState<User[]>([]);

	useAsyncEffect(async () => {
		const {data} = await userGet({
			query: {
				// eslint-disable-next-line @typescript-eslint/naming-convention
				following_id: user.id,
			},
		});

		if (data) {
			setFollowers(data.users);
		}
	}, [user.id]);

	return followers.length > 0 ? (
		<div>
			<p>Followers</p>
			<div>
				{followers.map((i) => (
					<UserView user={i} />
				))}
			</div>
		</div>
	) : null;
}

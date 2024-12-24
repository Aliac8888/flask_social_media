import {useEffect, useState} from 'preact/hooks';
import {
	userGet,
	userUserIdFollowingsGet,
	userUserIdGet,
	type User,
} from '../api/index.js';
import {useAsyncEffect} from '../async-effect.js';
import {UserView} from './UserView.js';
import {FollowersView} from './FollowersView.js';
import {FollowingsView} from './FollowingsView.js';

export function ProfilePage({userId}: {userId: string | User}) {
	const [user, setUser] = useState<User | undefined>(
		typeof userId === 'object' ? userId : undefined,
	);

	useAsyncEffect(async () => {
		if (typeof userId === 'object') {
			setUser(userId);
			return;
		}

		setUser(undefined);

		const {data} = await userUserIdGet({
			path: {
				// eslint-disable-next-line @typescript-eslint/naming-convention
				user_id: userId,
			},
		});

		if (data) {
			setUser(data);
		}
	}, [userId]);

	const [tab, setTab] = useState<'followers' | 'followings' | undefined>();

	return user ? (
		<div>
			<UserView user={user} />
			<div>
				<div>
					<button
						onClick={() => {
							setTab('followers');
						}}
					>
						Followers
					</button>
					<button
						onClick={() => {
							setTab('followings');
						}}
					>
						Followings
					</button>
				</div>
				{tab === 'followers' ? (
					<FollowersView user={user} />
				) : tab === 'followings' ? (
					<FollowingsView user={user} />
				) : null}
			</div>
		</div>
	) : (
		<div>Loading…</div>
	);
}

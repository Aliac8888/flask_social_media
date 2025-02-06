import {useEffect, useState} from 'preact/hooks';
import {getUserById, type User} from '../api/index.js';
import {useAsyncEffect} from '../async-effect.js';
import {UserView} from './UserView.js';
import {FollowingsView} from './FollowingsView.js';
import './ProfilePage.css';

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

		const {data} = await getUserById({
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
		<div class="profile-page">
			<div class="profile-page__profile">
				<UserView user={user} editable />
			</div>
			<div class="profile-page__tab-container">
				<div class="profile-page__tab-bar">
					<button
						class={`profile-page__tab-button ${tab === 'followers' ? 'profile-page--tab-active' : ''}`}
						onClick={() => {
							setTab('followers');
						}}
					>
						Followers
					</button>
					<button
						class={`profile-page__tab-button ${tab === 'followings' ? 'profile-page--tab-active' : ''}`}
						onClick={() => {
							setTab('followings');
						}}
					>
						Followings
					</button>
				</div>
				{tab === 'followers' ? (
					<FollowingsView user={user} reversed />
				) : tab === 'followings' ? (
					<FollowingsView user={user} />
				) : null}
			</div>
		</div>
	) : (
		<div class="profile-page">
			<p class="profile-page__loader">Loading…</p>
		</div>
	);
}

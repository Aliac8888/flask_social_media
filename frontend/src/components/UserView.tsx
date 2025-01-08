import {useState} from 'preact/hooks';
import {
	userFollowerIdFollowingsFollowingIdDelete,
	userFollowerIdFollowingsFollowingIdPut,
	userUserIdDelete,
	userUserIdPatch,
	type User,
} from '../api/index.js';
import {useUser} from '../user.js';
import styles from './UserView.module.css';

export function UserView({
	user,
	onUpdate,
	editable,
}: {
	user: User;
	onUpdate?: () => void;
	editable?: boolean;
}) {
	const avatar = user.name.charAt(0).toUpperCase();
	const context = useUser();
	const [editing, setEditing] = useState(false);

	return (
		<div className={styles['user-view']}>
			<div className={styles['user-view__avatar']}>{avatar}</div>
			<div className={styles['user-view__name']}>
				{editing ? (
					<textarea
						onInput={(event) => {
							user.name = event.currentTarget.value;
						}}
						value={user.name}
					/>
				) : (
					user.name
				)}
			</div>
			{editable && (
				<div className={styles['user-view__email']}>
					{editing ? (
						<textarea
							onInput={(event) => {
								user.email = event.currentTarget.value;
							}}
							value={user.email}
						/>
					) : (
						user.email
					)}
				</div>
			)}
			{user.id === context.auth?.user.id && editable ? (
				editing ? (
					<div>
						<button
							onClick={async () => {
								await userUserIdPatch({
									// eslint-disable-next-line @typescript-eslint/naming-convention
									path: {user_id: user.id},
									body: {
										email: user.email,
										name: user.name,
									},
								});
								setEditing(false);
							}}
						>
							Done
						</button>
					</div>
				) : (
					<div>
						<button
							onClick={() => {
								setEditing(true);
							}}
						>
							Edit
						</button>
						<button
							onClick={() => {
								context.auth = undefined;
							}}
						>
							Logout
						</button>
						<button
							onClick={async () => {
								await userUserIdDelete({
									path: {
										// eslint-disable-next-line @typescript-eslint/naming-convention
										user_id: user.id,
									},
								});
								context.auth = undefined;
							}}
						>
							Delete
						</button>
					</div>
				)
			) : (
				context.auth &&
				user.id !== context.auth?.user.id && (
					<div>
						<button
							onClick={async () => {
								await userFollowerIdFollowingsFollowingIdPut({
									path: {
										follower_id: context.auth!.user.id,
										following_id: user.id,
									},
								});
							}}
						>
							Follow
						</button>
						<button
							onClick={async () => {
								await userFollowerIdFollowingsFollowingIdDelete({
									path: {
										follower_id: context.auth!.user.id,
										following_id: user.id,
									},
								});
							}}
						>
							Unfollow
						</button>
					</div>
				)
			)}
		</div>
	);
}

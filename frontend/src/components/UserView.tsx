import {useState} from 'preact/hooks';
import {
	deleteUser,
	followUser,
	unfollowUser,
	updateUser,
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
								await updateUser({
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
								await deleteUser({
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
								await followUser({
									path: {
										// eslint-disable-next-line @typescript-eslint/naming-convention
										follower_id: context.auth!.user.id,
										// eslint-disable-next-line @typescript-eslint/naming-convention
										following_id: user.id,
									},
								});
							}}
						>
							Follow
						</button>
						<button
							onClick={async () => {
								await unfollowUser({
									path: {
										// eslint-disable-next-line @typescript-eslint/naming-convention
										follower_id: context.auth!.user.id,
										// eslint-disable-next-line @typescript-eslint/naming-convention
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

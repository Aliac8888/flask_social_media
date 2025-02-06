import {useState} from 'preact/hooks';
import {deletePost, updatePost, type Post, type User} from '../api/index.js';
import {useUser} from '../user.js';
import {UserView} from './UserView.js';
import styles from './PostView.module.css';

export function PostView({
	post,
	onUpdate,
}: {
	post: Post;
	onUpdate?: () => void;
}) {
	const [editing, setEditing] = useState(false);
	const {auth} = useUser();

	return (
		<div
			className={`${styles['post-view']} ${
				post.creation_time === post.modification_time
					? ''
					: styles['post-view--show-modification-time']
			}`}
		>
			<div className={styles['post-view__header']}>
				<UserView user={post.author} />
				<div className={styles['post-view__creation-time']}>
					{new Date(post.creation_time).toLocaleString()}
				</div>
				<div className={styles['post-view__modification-time']}>
					{new Date(post.modification_time).toLocaleString()}
				</div>
			</div>
			<div className={styles['post-view__body']}>
				{editing ? (
					<textarea
						onInput={(event) => {
							post.content = event.currentTarget.value;
						}}
						value={post.content}
					/>
				) : (
					post.content
				)}
			</div>
			{post.author.id === auth?.user.id ? (
				editing ? (
					<div>
						<button
							onClick={async () => {
								await updatePost({
									// eslint-disable-next-line @typescript-eslint/naming-convention
									path: {post_id: post.id},
									body: {content: post.content},
								});

								onUpdate?.();
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
							onClick={async () => {
								await deletePost({
									// eslint-disable-next-line @typescript-eslint/naming-convention
									path: {post_id: post.id},
								});

								onUpdate?.();
							}}
						>
							Delete
						</button>
					</div>
				)
			) : null}
		</div>
	);
}

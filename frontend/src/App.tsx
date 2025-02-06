import {useEffect, useState} from 'preact/hooks';
import {PostView} from './components/PostView.js';
import {
	createPost,
	getAllPosts,
	getPostFeed,
	updatePost,
	type Post,
} from './api/index.js';
import {useAsyncEffect} from './async-effect.js';
import styles from './App.module.css';
import {ProfilePage} from './components/ProfilePage.js';
import {AuthPage} from './components/AuthPage.js';
import {useUser} from './user.js';
import {PostPage} from './components/PostPage.js';

export function App() {
	const [posts, setPosts] = useState<Post[]>([]);
	const [newPostBody, setNewPostBody] = useState<string>('');
	const [local, setLocal] = useState(false);
	const {auth} = useUser();

	// Fetch posts on page load
	useAsyncEffect(async () => {
		const {data} =
			auth && local
				? // eslint-disable-next-line @typescript-eslint/naming-convention
					await getPostFeed({path: {user_id: auth.user.id}})
				: await getAllPosts();

		setPosts(data ?? []);
	}, [auth?.user.id, local]);

	// Handle new post creation
	async function handleCreatePost() {
		if (!newPostBody || !auth) return;

		await createPost({
			body: {author: auth.user.id, content: newPostBody},
		});
		setNewPostBody('');

		const {data} =
			auth && local
				? // eslint-disable-next-line @typescript-eslint/naming-convention
					await getPostFeed({path: {user_id: auth.user.id}})
				: await getAllPosts();
		setPosts(data ?? []);
	}

	// Handle special update (toggle star for a post)
	async function handleUpdatePost(postId: string) {
		await updatePost({
			// eslint-disable-next-line @typescript-eslint/naming-convention
			path: {post_id: postId},
			body: {content: newPostBody},
		});

		const {data} =
			auth && local
				? // eslint-disable-next-line @typescript-eslint/naming-convention
					await getPostFeed({path: {user_id: auth.user.id}})
				: await getAllPosts();
		setPosts(data ?? []);
	}

	return (
		<div className={styles['app-container']}>
			<AuthPage />
			{auth && <ProfilePage userId={auth.user.id} />}

			<button
				onClick={() => {
					setLocal(!local);
				}}
			>
				{local ? 'local' : 'global'}
			</button>
			<h1 className={styles.header}>Posts</h1>

			{/* New Post Form */}
			<div className={styles['create-post']}>
				<h2>Create New Post</h2>
				<textarea
					value={newPostBody}
					onInput={(event) => {
						setNewPostBody(event.currentTarget.value);
					}}
					placeholder="Enter post content"
				/>
				<button onClick={handleCreatePost}>Create Post</button>
			</div>

			{/* List of Posts */}
			<div className={styles['posts-list']}>
				{/* TODO: Paginate the posts. */}
				{posts
					.slice(-100)
					.reverse()
					.map((post) => (
						<div key={post.id} className="post-container">
							<PostPage
								post={post}
								onUpdate={async () => {
									const {data} =
										auth && local
											? // eslint-disable-next-line @typescript-eslint/naming-convention
												await getPostFeed({path: {user_id: auth.user.id}})
											: await getAllPosts();
									setPosts(data ?? []);
								}}
							/>
						</div>
					))}
			</div>
		</div>
	);
}

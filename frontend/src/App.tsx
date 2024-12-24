import {useEffect, useState} from 'preact/hooks';
import {PostView} from './components/PostView.js';
import {postGet, postPost, postPostIdPatch, type Post} from './api/index.js';
import {useAsyncEffect} from './async-effect.js';
import styles from './App.module.css';
import {ProfilePage} from './components/ProfilePage.js';
import {AuthPage} from './components/AuthPage.js';
import {useUser} from './user.js';

export function App() {
	const [posts, setPosts] = useState<Post[]>([]);
	const [newPostBody, setNewPostBody] = useState<string>('');
	const {auth} = useUser();

	// Fetch posts on page load
	useAsyncEffect(async () => {
		const {data} = await postGet();
		setPosts(data?.posts ?? []);
	}, []);

	// Handle new post creation
	async function handleCreatePost() {
		if (!newPostBody || !auth) return;

		await postPost({
			body: {author: auth.user.id, content: newPostBody},
		});
		setNewPostBody('');

		const {data} = await postGet();
		setPosts(data?.posts ?? []);
	}

	// Handle special update (toggle star for a post)
	async function handleUpdatePost(postId: string) {
		await postPostIdPatch({
			// eslint-disable-next-line @typescript-eslint/naming-convention
			path: {post_id: postId},
			body: {content: newPostBody},
		});

		const {data} = await postGet();
		setPosts(data?.posts ?? []);
	}

	return (
		<div className={styles['app-container']}>
			<AuthPage />
			{auth && <ProfilePage userId={auth.user.id} />}
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
				{posts.map((post) => (
					<div key={post.id} className="post-container">
						<PostView
							post={post}
							onUpdate={async () => {
								const {data} = await postGet();
								setPosts(data?.posts ?? []);
							}}
						/>
					</div>
				))}
			</div>
		</div>
	);
}

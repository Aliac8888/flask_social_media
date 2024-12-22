import {useEffect, useState} from 'preact/hooks';
import {PostView} from './components/PostView.js';
import {postGet, postPost, postPostIdPatch, type Post} from './api/index.js';
import {useAsyncEffect} from './async-effect.js';

export function App() {
	const [posts, setPosts] = useState<Post[]>([]);
	const [newPostBody, setNewPostBody] = useState<string>('');

	// Fetch posts on page load
	useAsyncEffect(async () => {
		const {data} = await postGet();
		setPosts(data?.posts ?? []);
	}, []);

	// Handle new post creation
	async function handleCreatePost() {
		if (!newPostBody) return;

		await postPost({body: {author: '', content: newPostBody}});
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
		<div>
			<h1>Posts</h1>
			{/* New Post Form */}
			<div>
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
			<div>
				{posts.map((post) => (
					<div key={post.id} class="post-container">
						<PostView post={post} />
						<button onClick={async () => handleUpdatePost(post.id)}>
							Star Post
						</button>
					</div>
				))}
			</div>
		</div>
	);
}

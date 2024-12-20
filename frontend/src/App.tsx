import {useEffect, useState} from 'preact/hooks';
import {
	getPosts,
	createPost,
	updatePost,
	type PostWithId,
} from './services/post.js';
import {PostView} from './components/PostView.js';

export function App() {
	const [posts, setPosts] = useState<PostWithId[]>([]);
	const [newPostBody, setNewPostBody] = useState<string>('');

	// Fetch posts on page load
	useEffect(() => {
		async function fetchPosts() {
			const postsData = await getPosts();
			setPosts(postsData);
		}

		void fetchPosts();
	}, []);

	// Handle new post creation
	async function handleCreatePost() {
		if (!newPostBody) return;

		await createPost({content: newPostBody, author: ''});
		setNewPostBody('');
		const updatedPosts = await getPosts(); // Refresh the list
		setPosts(updatedPosts);
	}

	// Handle special update (toggle star for a post)
	async function handleUpdatePost(postId: string) {
		await updatePost(postId, {content: newPostBody});
		const updatedPosts = await getPosts(); // Refresh the list
		setPosts(updatedPosts);
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

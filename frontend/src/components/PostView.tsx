import type {Post} from '../api/index.js';

export function PostView({post}: {post: Post}) {
	return (
		<div class="post-view">
			{/* TODO: Add author profile view. */}
			<div class="post-view__body">{post.content}</div>
			{/* TODO: Add comments view. */}
		</div>
	);
}

import type {Post} from '../services/post.js';

export function PostView({post}: {post: Post}) {
	return (
		<div class="post-view">
			{/* TODO: Add author profile view. */}
			<div class="post-view__special">{post.special ? '★' : ''}</div>
			<div class="post-view__date">{post.date.toLocaleString()}</div>
			<div class="post-view__body">{post.body}</div>
			{/* TODO: Add comments view. */}
		</div>
	);
}

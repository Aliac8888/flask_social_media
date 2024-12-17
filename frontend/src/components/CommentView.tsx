import type {Comment} from '../services/comment.js';

export function CommentView({comment}: {comment: Comment}) {
	return (
		<div class="comment-view">
			{/* TODO: Add author profile view. */}
			<div class="comment-view__body">{comment.body}</div>
		</div>
	);
}

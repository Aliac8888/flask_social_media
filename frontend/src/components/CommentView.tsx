import type {CommentWithId} from '../services/comment.js';

export function CommentView({comment}: {comment: CommentWithId}) {
	return (
		<div class="comment-view">
			{/* TODO: Add author profile view. */}
			<div class="comment-view__body">{comment.content}</div>
		</div>
	);
}

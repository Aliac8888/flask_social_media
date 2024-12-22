import {type Comment} from '../api/index.js';

export function CommentView({comment}: {comment: Comment}) {
	return (
		<div class="comment-view">
			{/* TODO: Add author profile view. */}
			<div class="comment-view__body">{comment.content}</div>
		</div>
	);
}

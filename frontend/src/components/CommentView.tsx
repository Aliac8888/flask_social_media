import {type Comment, type User} from '../api/index.js';
import {UserView} from './UserView.js';

export function CommentView({comment}: {comment: Comment}) {
	return (
		<div class="comment-view">
			<div class="comment-view__header">
				<UserView user={comment.author} />
				<div class="post-view__creation-time">
					{new Date(comment.creation_time).toLocaleString()}
				</div>
				<div class="post-view__modification-time">
					{new Date(comment.modification_time).toLocaleString()}
				</div>
			</div>
			<div class="comment-view__body">{comment.content}</div>
		</div>
	);
}

import {useState} from 'preact/hooks';
import {
	commentCommentIdDelete,
	commentCommentIdPatch,
	type Comment,
	type User,
} from '../api/index.js';
import {useUser} from '../user.js';
import {UserView} from './UserView.js';

export function CommentView({
	comment,
	onUpdate,
}: {
	comment: Comment;
	onUpdate?: () => void;
}) {
	const {auth} = useUser();
	const [editing, setEditing] = useState(false);

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
			<div class="comment-view__body">
				{editing ? (
					<textarea
						onInput={(event) => {
							comment.content = event.currentTarget.value;
						}}
						value={comment.content}
					/>
				) : (
					comment.content
				)}
			</div>
			{comment.author.id === auth?.user.id ? (
				editing ? (
					<div>
						<button
							onClick={async () => {
								await commentCommentIdPatch({
									// eslint-disable-next-line @typescript-eslint/naming-convention
									path: {comment_id: comment.id},
									body: {content: comment.content},
								});

								onUpdate?.();
								setEditing(false);
							}}
						>
							Done
						</button>
					</div>
				) : (
					<div>
						<button
							onClick={() => {
								setEditing(true);
							}}
						>
							Edit
						</button>
						<button
							onClick={async () => {
								await commentCommentIdDelete({
									// eslint-disable-next-line @typescript-eslint/naming-convention
									path: {comment_id: comment.id},
								});

								onUpdate?.();
							}}
						>
							Delete
						</button>
					</div>
				)
			) : null}
		</div>
	);
}

import {useState} from 'preact/hooks';
import {
	createComment,
	getCommentsOfPost,
	type Comment,
	type Post,
} from '../api/index.js';
import {useAsyncEffect} from '../async-effect.js';
import {useUser} from '../user.js';
import {PostView} from './PostView.js';
import {CommentView} from './CommentView.js';

export function PostPage({
	post,
	onUpdate,
}: {
	post: Post;
	onUpdate?: () => void;
}) {
	const [comments, setComments] = useState<Comment[]>([]);
	const [showComments, setShowComments] = useState<boolean>(false);
	const {auth} = useUser();

	useAsyncEffect(async () => {
		if (!showComments) return;

		setComments([]);

		// eslint-disable-next-line @typescript-eslint/naming-convention
		const {data} = await getCommentsOfPost({path: {post_id: post.id}});

		if (data) {
			setComments(data);
		}
	}, [showComments]);

	return (
		<div>
			<PostView post={post} onUpdate={onUpdate} />
			<div>
				<button
					onClick={() => {
						setComments([]);
						setShowComments(!showComments);
					}}
				>
					{showComments ? 'Hide Comments' : 'Show Comments'}
				</button>
			</div>
			<div>
				{showComments && auth && (
					<form
						onSubmit={async (event) => {
							event.preventDefault();
							const formData = new FormData(
								event.currentTarget,
								event.submitter,
							);

							await createComment({
								body: {
									author: auth.user.id,
									post: post.id,
									content: String(formData.get('content')),
								},
							});

							const {data} = await getCommentsOfPost({
								// eslint-disable-next-line @typescript-eslint/naming-convention
								path: {post_id: post.id},
							});

							if (data) {
								setComments(data);
							}
						}}
					>
						<h2>Create New Comment</h2>
						<textarea name="content" placeholder="Enter post content" />
						<button>Create Post</button>
					</form>
				)}
				{comments.map((i) => (
					<CommentView
						comment={i}
						onUpdate={async () => {
							const {data} = await getCommentsOfPost({
								// eslint-disable-next-line @typescript-eslint/naming-convention
								path: {post_id: post.id},
							});

							if (data) {
								setComments(data);
							}
						}}
					/>
				))}
			</div>
		</div>
	);
}

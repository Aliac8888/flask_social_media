import type {Post, User} from '../api/index.js';
import {UserView} from './UserView.js';

export function PostView({post}: {post: Post}) {
	return (
		<div
			class={`post-view ${post.creation_time === post.modification_time ? '' : 'post-view--show-modification-time'}`}
		>
			<div class="post-view__header">
				<UserView user={post.author} />
				<div class="post-view__creation-time">
					{new Date(post.creation_time).toLocaleString()}
				</div>
				<div class="post-view__modification-time">
					{new Date(post.modification_time).toLocaleString()}
				</div>
			</div>
			<div class="post-view__body">{post.content}</div>
		</div>
	);
}

import type {Post, User} from '../api/index.js';
import {UserView} from './UserView.js';
import styles from './PostView.module.css';

export function PostView({post}: {post: Post}) {
		return (
    <div
      className={`${styles['post-view']} ${
        post.creation_time === post.modification_time
          ? ''
          : styles['post-view--show-modification-time']
      }`}
    >
      <div className={styles['post-view__header']}>
        <UserView user={post.author} />
        <div className={styles['post-view__creation-time']}>
          {new Date(post.creation_time).toLocaleString()}
        </div>
        <div className={styles['post-view__modification-time']}>
          {new Date(post.modification_time).toLocaleString()}
        </div>
      </div>
      <div className={styles['post-view__body']}>{post.content}</div>
    </div>
  );
}

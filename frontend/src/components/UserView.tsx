import type {User} from '../api/index.js';
import styles from './UserView.module.css';

export function UserView({user}: {user: User}) {
	const avatar = user.name.charAt(0).toUpperCase();

  return (
    <div className={styles['user-view']}>
      <div className={styles['user-view__avatar']}>{avatar}</div>
      <div className={styles['user-view__name']}>{user.name}</div>
    </div>
  );
}

import {useState} from 'preact/hooks';
import {useUser} from '../user.js';
import type {AuthResponse} from '../api/types.gen.js';
import {LoginForm} from './LoginForm.js';
import {SignupForm} from './SignupForm.js';

export function AuthPage({
	initialAction,
	onAuthenticated,
}: {
	initialAction?: 'login' | 'signup';
	onAuthenticated?: (action: 'login' | 'signup', auth: AuthResponse) => void;
}) {
	const [action, setAction] = useState<'login' | 'signup' | undefined>(
		initialAction,
	);

	const user = useUser();

	return action === 'login' ? (
		<LoginForm
			onLoggedIn={(auth) => {
				user.auth = auth;
				onAuthenticated?.('login', auth);
			}}
		/>
	) : action === 'signup' ? (
		<SignupForm
			onSignedUp={(auth) => {
				user.auth = auth;
				onAuthenticated?.('signup', auth);
			}}
		/>
	) : (
		<div>
			<button
				onClick={() => {
					setAction('login');
				}}
			>
				Login
			</button>
			<button
				onClick={() => {
					setAction('signup');
				}}
			>
				Signup
			</button>
		</div>
	);
}

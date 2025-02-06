import {useState} from 'preact/hooks';
import {useUser} from '../user.js';
import type {AuthnResponse} from '../api/types.gen.js';
import {LoginForm} from './LoginForm.js';
import {SignupForm} from './SignupForm.js';
import './AuthPage.css';

export function AuthPage({
	initialAction,
	onAuthenticated,
}: {
	initialAction?: 'login' | 'signup';
	onAuthenticated?: (action: 'login' | 'signup', auth: AuthnResponse) => void;
}) {
	const [action, setAction] = useState<'login' | 'signup' | undefined>(
		initialAction,
	);

	const user = useUser();

	return action === 'login' ? (
		<div class="auth-page">
			<button
				class="auth-page__back"
				onClick={() => {
					setAction(undefined);
				}}
			>
				Back
			</button>
			<LoginForm
				onLoggedIn={(auth) => {
					user.auth = auth;
					onAuthenticated?.('login', auth);
				}}
			/>
		</div>
	) : action === 'signup' ? (
		<div class="auth-page">
			<button
				class="auth-page__back"
				onClick={() => {
					setAction(undefined);
				}}
			>
				Back
			</button>
			<SignupForm
				onSignedUp={(auth) => {
					user.auth = auth;
					onAuthenticated?.('signup', auth);
				}}
			/>
		</div>
	) : (
		<div class="auth-page">
			<div class="auth-page__bar">
				<button
					class="auth-page__button"
					onClick={() => {
						setAction('login');
					}}
				>
					Login
				</button>
				<button
					class="auth-page__button"
					onClick={() => {
						setAction('signup');
					}}
				>
					Signup
				</button>
			</div>
		</div>
	);
}

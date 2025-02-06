import {login} from '../api/sdk.gen.js';
import type {AuthnResponse} from '../api/types.gen.js';
import {FormInput} from './FormInput.js';
import './LoginForm.css';

export function LoginForm({
	onLoggedIn,
}: {
	onLoggedIn?: (auth: AuthnResponse) => void;
}) {
	return (
		<form
			class="login-form"
			onSubmit={async (event) => {
				event.preventDefault();
				const formData = new FormData(event.currentTarget, event.submitter);

				const {data} = await login({
					body: {
						email: String(formData.get('email')),
						password: String(formData.get('password')),
					},
				});

				if (data) {
					onLoggedIn?.(data);
				}
			}}
		>
			<FormInput type="email" name="email" label="Email" required />
			<FormInput type="password" name="password" label="Password" required />
			<div class="login-form__controls">
				<button type="reset">Clear</button>
				<button>Login</button>
			</div>
		</form>
	);
}

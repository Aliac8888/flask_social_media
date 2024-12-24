import {userLoginPost} from '../api/sdk.gen.js';
import type {AuthResponse} from '../api/types.gen.js';
import {FormInput} from './FormInput.js';

export function LoginForm({
	onLoggedIn,
}: {
	onLoggedIn?: (auth: AuthResponse) => void;
}) {
	return (
		<form
			onSubmit={async (event) => {
				event.preventDefault();
				const formData = new FormData(event.currentTarget, event.submitter);

				const {data} = await userLoginPost({
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
			<div>
				<button type="reset">Clear</button>
				<button>Create</button>
			</div>
		</form>
	);
}

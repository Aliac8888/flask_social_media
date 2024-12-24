import {userPost} from '../api/sdk.gen.js';
import type {AuthResponse} from '../api/types.gen.js';
import {FormInput} from './FormInput.js';
import './SignupForm.css';

export const SignupForm = ({
	onSignedUp,
}: {
	onSignedUp?: (auth: AuthResponse) => void;
}) => {
	return (
		<form
			class="signup-form"
			onSubmit={async (event) => {
				event.preventDefault();
				const formData = new FormData(event.currentTarget, event.submitter);

				const {data} = await userPost({
					body: {
						name: String(formData.get('username')),
						email: String(formData.get('email')),
						password: String(formData.get('password')),
					},
				});

				if (data) {
					onSignedUp?.(data);
				}
			}}
		>
			<FormInput name="username" label="Username" required />
			<FormInput type="email" name="email" label="Email" required />
			<FormInput type="password" name="password" label="Password" required />
			<div class="signup-form__controls">
				<button type="reset">Clear</button>
				<button>Create</button>
			</div>
		</form>
	);
};

import {createUser} from '../services/user.js';
import {FormInput} from './FormInput.js';

export const CreateUserForm = ({
	onCreated,
}: {
	onCreated?: (id: string) => void;
}) => {
	return (
		<form
			onSubmit={async (event) => {
				event.preventDefault();

				const formData = new FormData(event.currentTarget, event.submitter);

				await createUser({
					name: String(formData.get('username')),
					email: String(formData.get('email')),
				});
			}}
		>
			<FormInput name="username" label="Username" required />
			<FormInput type="email" name="email" label="Email" required />
			<div>
				<button type="reset">Clear</button>
				<button>Create</button>
			</div>
		</form>
	);
};

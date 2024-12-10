import {useState} from 'preact/hooks';
import {createUser, type User} from './services/user.js';

export function App() {
	const [users, setUsers] = useState([]);

	const addUser = async () => {
		const newUser: User = {name: 'Saeed :3', email: 'saeedsaeed@example.com'};
		const response = await createUser(newUser);
		console.log(response);
	};

	return (
		<div>
			<button onClick={addUser}>Add User</button>
		</div>
	);
}

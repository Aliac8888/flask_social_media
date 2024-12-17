import {useState} from 'preact/hooks';
import {createUser, type User} from './services/user.js';
import {CreateUserForm} from './components/CreateUserForm.js';

export function App() {
	return <CreateUserForm />;
}

import {createContext} from 'preact';
import {useContext, useState} from 'preact/hooks';

const userContext = createContext<{id: string | undefined} | undefined>(
	undefined,
);

export function useUser() {
	const value = useContext(userContext);

	if (value === undefined) {
		throw new Error('Not in a user provider');
	}

	return value.id;
}

export function UserProvider() {
	const [id, setId] = useState<string | undefined>();

	return (
		<userContext.Provider
			value={{
				get id() {
					return id;
				},
				set id(newUser) {
					setId(newUser);
				},
			}}
		></userContext.Provider>
	);
}

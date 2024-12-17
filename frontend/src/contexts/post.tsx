import {createContext} from 'preact';
import {useContext, useState} from 'preact/hooks';

const postContext = createContext<{id: string | undefined} | undefined>(
	undefined,
);

export function usePost() {
	const value = useContext(postContext);

	if (value === undefined) {
		throw new Error('Not in a user provider');
	}

	return value.id;
}

export function UserProvider() {
	const [id, setId] = useState<string | undefined>();

	return (
		<postContext.Provider
			value={{
				get id() {
					return id;
				},
				set id(newId) {
					setId(newId);
				},
			}}
		></postContext.Provider>
	);
}

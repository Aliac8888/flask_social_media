import {createContext, type ComponentChildren} from 'preact';
import {useContext, useEffect, useState} from 'preact/hooks';
import {client, type AuthResponse} from './api/index.js';

const userContext = createContext<{auth: AuthResponse | undefined} | undefined>(
	undefined,
);

export function useUser() {
	const auth = useContext(userContext);

	if (!auth) {
		throw new Error('Outside of user provider');
	}

	return auth;
}

export function UserProvider({children}: {children: ComponentChildren}) {
	const [auth, setAuth] = useState<AuthResponse | undefined>(undefined);

	useEffect(() => {
		const callback: Parameters<
			(typeof client)['interceptors']['request']['use']
		>[0] = (request, options) => {
			if (auth) {
				request.headers.set('Authorization', `Bearer ${auth.jwt}`);
			}

			return request;
		};

		client.interceptors.request.use(callback);

		return () => {
			client.interceptors.request.eject(callback);
		};
	}, [auth]);

	return (
		<userContext.Provider
			value={{
				get auth() {
					return auth;
				},
				set auth(newAuth) {
					setAuth(newAuth);
				},
			}}
		>
			{children}
		</userContext.Provider>
	);
}

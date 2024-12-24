import {render} from 'preact';
import {App} from './App.js';
import {client} from './api/index.js';
import {UserProvider} from './user.js';

client.setConfig({
	baseUrl: String(import.meta.env.SOCIAL_FE_BE_URL),
});

render(
	<UserProvider>
		<App />
	</UserProvider>,
	document.body,
);

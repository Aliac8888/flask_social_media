import {render} from 'preact';
import {App} from './App.js';
import {client} from './api/index.js';

client.setConfig({
	baseUrl: String(import.meta.env.SOCIAL_FE_BE_URL),
});

render(<App />, document.body);

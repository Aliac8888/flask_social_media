import {useId} from 'preact/hooks';
import type {JSX} from 'preact/jsx-runtime';
import './FormInput.css';

export const FormInput = (
	p: JSX.IntrinsicElements['input'] & {label: string},
) => {
	const id = p.id ?? useId();

	return (
		<div class="form-input">
			<label for={id}>{p.label}</label>
			<input type="text" {...p} id={id} />
		</div>
	);
};

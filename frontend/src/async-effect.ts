import {useEffect, type Inputs} from 'preact/hooks';

type CleanUp = () => void | Promise<void>;

export function useAsyncEffect(
	effectFunction: (
		callback: (cleanup: CleanUp) => void,
	) => void | Promise<void>,
	deps?: Inputs,
) {
	useEffect(() => {
		let cleanup: CleanUp | boolean = false;

		void effectFunction((cleanup_) => {
			if (cleanup === true) {
				void cleanup_();
			} else {
				cleanup = cleanup_;
			}
		});

		return async () => {
			if (typeof cleanup === 'function') {
				await cleanup();
			}

			cleanup = true;
		};
	}, deps);
}

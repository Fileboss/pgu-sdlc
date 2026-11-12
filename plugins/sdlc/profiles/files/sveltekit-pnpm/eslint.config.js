// sdlc eslint v1 (sveltekit): the shared TypeScript base plus Svelte.
// Add this project's own rules in the last block only.
import prettier from 'eslint-config-prettier';
import { existsSync } from 'node:fs';
import path from 'node:path';
import js from '@eslint/js';
import svelte from 'eslint-plugin-svelte';
import { defineConfig, includeIgnoreFile } from 'eslint/config';
import globals from 'globals';
import ts from 'typescript-eslint';

const gitignorePath = path.resolve(import.meta.dirname, '.gitignore');

export default defineConfig(
	existsSync(gitignorePath) ? includeIgnoreFile(gitignorePath) : {},
	js.configs.recommended,
	ts.configs.recommended,
	svelte.configs.recommended,
	prettier,
	svelte.configs.prettier,
	{
		languageOptions: { globals: { ...globals.browser, ...globals.node } },
		rules: {
			// typescript-eslint advises against no-undef on TypeScript projects: tsc checks it.
			'no-undef': 'off'
		}
	},
	{
		files: ['**/*.svelte', '**/*.svelte.ts', '**/*.svelte.js'],
		languageOptions: {
			parserOptions: {
				projectService: true,
				extraFileExtensions: ['.svelte'],
				parser: ts.parser
			}
		}
	},
	{
		rules: {
			'svelte/button-has-type': 'error'
		}
	},
	{
		// This project's own rules.
		rules: {}
	}
);

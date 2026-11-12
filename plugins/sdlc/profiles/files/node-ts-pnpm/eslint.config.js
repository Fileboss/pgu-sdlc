// sdlc eslint v1 (node-ts): the shared base of every TypeScript project.
// Add this project's own rules in the last block only.
import prettier from 'eslint-config-prettier';
import { existsSync } from 'node:fs';
import path from 'node:path';
import js from '@eslint/js';
import { defineConfig, includeIgnoreFile } from 'eslint/config';
import globals from 'globals';
import ts from 'typescript-eslint';

const gitignorePath = path.resolve(import.meta.dirname, '.gitignore');

export default defineConfig(
	existsSync(gitignorePath) ? includeIgnoreFile(gitignorePath) : {},
	{ ignores: ['dist/', 'build/', 'coverage/'] },
	js.configs.recommended,
	ts.configs.recommended,
	prettier,
	{
		languageOptions: { globals: { ...globals.node } },
		rules: {
			// typescript-eslint advises against no-undef on TypeScript projects: tsc checks it.
			'no-undef': 'off'
		}
	},
	{
		// This project's own rules.
		rules: {}
	}
);

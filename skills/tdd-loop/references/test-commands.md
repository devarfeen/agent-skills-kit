# Focused-test commands by ecosystem

How to run ONE test (the loop's inner command), then the widened scope. Find
the runner from the manifest and lockfile, not from a folder's name; when
unsure, read how CI runs tests (`.github/workflows/`, `Makefile`, composer/npm
scripts) — that is the project's own answer.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## JS / TS

- **Vitest:** `pnpm vitest run path/to/file.test.ts` · one test: add `-t "name"` · widen: `pnpm vitest run src/module/`
- **Jest:** `pnpm jest path/to/file.test.ts -t "name"` · widen: `pnpm jest src/module/`
- **Node test runner:** `node --test path/to/file.test.js`
- **Playwright:** `pnpm playwright test path/spec.ts -g "name"` — E2E; prefer a unit seam for the loop and keep E2E for widen/verify.

Use the project's installed package manager. For an installed binary, use
`pnpm exec vitest run path/to/file.test.ts`, `npm exec --no -- vitest run path/to/file.test.ts`,
or `yarn run vitest run path/to/file.test.ts`. `npm run <script> -- <args>`
requires that script in `package.json`; it is not a substitute for running a
binary. Check that the runner is installed first; do not download a missing
runner to guess the test command.

Package-manager syntax checked 2026-09-09 against [pnpm exec](https://pnpm.io/cli/exec),
[npm exec](https://docs.npmjs.com/cli/v11/commands/npm-exec/),
and [yarn run](https://yarnpkg.com/cli/run).

## PHP

- **Pest:** `./vendor/bin/pest path/to/SomeTest.php --filter=name`
- **PHPUnit:** `./vendor/bin/phpunit --filter=testName path/to/SomeTest.php`
- **Laravel:** `php artisan test --filter=Name` · widen: `php artisan test tests/Feature/Module/`

## Python

- **pytest:** `pytest path/to/test_file.py::test_name -x` · widen: `pytest tests/module/ -x`
- **Django:** `python manage.py test app.tests.TestClass.test_name`

## Go

- `go test ./pkg/module/ -run 'TestName$' -count=1` · widen: `go test ./pkg/...` (`-count=1` defeats the test cache so red is really red)

## React Native

- Usually Jest (as above) with `@testing-library/react-native` for component seams; device/E2E suites are verify-phase, not loop-phase.

## Watch mode

Prefer single non-watch runs inside the loop — deterministic exit codes beat
watch UIs for agents. Watch mode is for a human driving.

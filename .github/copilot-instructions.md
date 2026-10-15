# oblt-actions

This repository contains GitHub composite actions. Top-level directories are action namespaces; each action declares its interface in `action.yml` and documents usage in its README.

Keep this file focused on cross-repository guidance and below 4,000 characters. Review policies and path-specific guidance live in `.github/instructions/*.instructions.md`; follow the instruction files matched to the changed paths.

## Development

- Keep changes focused, maintainable, and compatible with existing action contracts.
- Run pre-commit hooks before committing.
- When action behavior changes, add or update its end-to-end test workflow under `.github/workflows/test-<action>.yml`; exercise composite actions with `uses: ./<action-path>`.
- When action inputs, outputs, or usage change, update its README and examples.
- Keep each action focused on one responsibility. If a namespace contains multiple actions, give each its own directory and `action.yml`.
- Prefer editing existing files; create only files needed for the task.
- Keep these instructions accurate as repository standards change.

## Pull requests

- Create a feature branch from `main`; open pull requests against `main` with a clear description and an appropriate changelog label (for example, `changelog:breaking`, `changelog:feature`, `changelog:fix`, `changelog:docs`, `changelog:dependencies`, or `changelog:ci`).
- Ensure checks pass before merging; squash-merge pull requests and delete the feature branch afterward.
- Document and communicate breaking changes, use the `changelog:breaking` label, and update the description of [issue #126](https://github.com/elastic/oblt-actions/issues/126).

## Security

Assist with defensive security work only. Validate untrusted inputs, use least-privilege access, and never expose or commit secrets.

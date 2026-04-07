# Farmaciola Home Assistant Integration

Farmaciola is a Home Assistant custom integration for medicine-related automation workflows.

## Requirements

- Python 3.11+
- `pip`
- `git`

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements_test.txt -r requirements_dev.txt
```

## Install local git hooks

This project uses `pre-commit` for:

- `pre-commit`: formatting and lint checks
- `pre-push`: full test suite
- `commit-msg`: Conventional Commit validation

Install hooks:

```bash
pre-commit install
pre-commit install --hook-type pre-push
pre-commit install --hook-type commit-msg
```

## Common commands

```bash
pre-commit run --all-files
pytest
cz check --message "feat: add new medication parser"
cz changelog
```

## Cursor IDE integration

This repository includes VS Code/Cursor workspace settings in `.vscode/`:

- `tasks.json` with one-click tasks:
  - `Farmaciola: Install Dev Dependencies`
  - `Farmaciola: Lint (pre-commit all files)`
  - `Farmaciola: Test (pytest)`
  - `Farmaciola: CI Check (lint + test)`
- `settings.json` for local `.venv` interpreter and pytest discovery
- `extensions.json` recommendations for Python, Pylance, and Ruff

Run tasks from `Terminal -> Run Task...` in Cursor.

## Conventional Commits

Use [Conventional Commits](https://www.conventionalcommits.org/) for all commits.

Examples:

- `feat: add medicine stock alert sensor`
- `fix: handle empty CIMA response`
- `docs: clarify setup instructions`
- `chore: update test dependencies`

## Release process

Releases are automated on pushes to `main`:

1. CI validates linting and tests.
2. Release workflow runs Commitizen bump logic.
3. The workflow updates:
   - `CHANGELOG.md`
   - `custom_components/farmaciola/manifest.json` version
4. A tag like `vX.Y.Z` is created and pushed.
5. A GitHub Release is published from generated changelog content.

## Contributing and community

- Contribution guide: `CONTRIBUTING.md`
- Code of Conduct: `CODE_OF_CONDUCT.md`

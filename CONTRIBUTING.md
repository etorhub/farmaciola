# Contributing to Farmaciola

Thanks for helping improve this Home Assistant integration.

## Workflow

1. Create a branch from `main`.
2. Make your changes with tests.
3. Run local checks.
4. Use a Conventional Commit message.
5. Open a pull request.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements_test.txt -r requirements_dev.txt
```

Install hooks once:

```bash
pre-commit install
pre-commit install --hook-type pre-push
pre-commit install --hook-type commit-msg
```

## Required checks

Before pushing, run:

```bash
pre-commit run --all-files
pytest
```

## Commit message format

This repository enforces Conventional Commits.

Valid examples:

- `feat: add support for medicine reminders`
- `fix: avoid crash when notify service is missing`
- `docs: update release instructions`
- `test: improve integration constants coverage`

Invalid examples:

- `updated stuff`
- `fix bug`

You can manually validate a message with:

```bash
cz check --message "feat: add support for medicine reminders"
```

## Pull requests

- Keep PRs focused and small.
- Include tests for behavior changes.
- Explain user-facing impact.
- Ensure CI passes.

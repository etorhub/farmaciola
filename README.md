# Farmaciola Home Assistant Integration

Farmaciola is a Home Assistant custom integration for medicine-related automation workflows.

## Home Assistant installation

Install this repository under `config/custom_components/farmaciola/` (for example via [HACS](https://hacs.xyz/) or a manual copy), then **restart Home Assistant**.

Add the integration from **Settings → Devices & services → Add integration** and search for **Farmaciola**. HACS does not block config-flow integrations; they behave like any other custom component.

### Verify the files on your host

If something does not match what you expect (for example after an update), open `config/custom_components/farmaciola/manifest.json` on the **same machine** Home Assistant runs on and confirm:

- `"config_flow": true` is present (required for adding the integration from the UI).
- `"version"` matches the release or branch you intended to install.

### Troubleshooting: “This integration cannot be added from the UI”

1. Confirm `manifest.json` on the host includes `"config_flow": true` and the expected `version` (see above). If you use HACS from a tagged release, ensure that release contains this field; your local git checkout may be newer than what HACS installed.
2. Perform a **full restart** of Home Assistant (not only “Reload” of YAML).
3. Check **Settings → System → Logs** and search for `farmaciola`. On startup you should see messages such as `Farmaciola integration module ready (version …)`. Import or dependency errors appear here if the integration failed to load.
4. Ensure there is only **one** copy of `custom_components/farmaciola` (no duplicate or stale folder).
5. From HACS, try **Redownload** or reinstall the integration, then restart again.

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

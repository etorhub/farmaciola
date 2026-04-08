# Farmaciola — CLAUDE.md

## What this is

A Home Assistant custom integration that acts as a smart medicine cabinet. It provides expiry tracking, CIMA (Spanish AEMPS registry) medicine lookup, and a dedicated Lovelace panel with a companion custom card.

## Structure

```
custom_components/farmaciola/   # HA integration (Python)
  __init__.py                   # Entry point — setup, panel registration, HTTP routes
  api.py                        # aiohttp views (REST endpoints called by the frontend)
  cima.py                       # CIMA API client (external medicine registry)
  scheduler.py                  # Hourly expiry-check task
  storage.py                    # Persistent storage via HA Store
  const.py                      # Domain constants
  www/
    panel.js                    # Lovelace panel (vanilla JS custom element)
    card.js                     # Lovelace custom card
tests/                          # pytest, async tests mirroring the module structure
```

## Key conventions

- Python ≥ 3.11, async/await throughout — follow existing HA async patterns.
- Commit messages must follow [Conventional Commits](https://www.conventionalcommits.org/).
- `ruff` handles linting and formatting — do not fight it.

## Pre-commit hooks (enforced automatically, do not bypass)

- **commit-msg**: `commitizen` validates the commit message format.
- **pre-push**: `pytest -q` must pass before pushing.

Run `pre-commit install --hook-type commit-msg --hook-type pre-push` once in a fresh clone.

## Running tests

```bash
source venv/bin/activate
pytest
```

## Finding things

- Medicine data model: `storage.py`
- Notification / expiry logic: `scheduler.py`
- External CIMA API contract: `cima.py` + `tests/test_cima.py`
- Frontend ↔ backend API contract: `api.py` (routes) and `www/panel.js` (fetch calls)

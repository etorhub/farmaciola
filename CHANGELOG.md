# Changelog

All notable changes to this project are documented in this file.

## v0.7.2 (2026-04-08)

### Fix

- **expiry**: treat medicines as expired only after their month has fully passed

## v0.7.1 (2026-04-08)

### Fix

- strip foto_manual from list endpoint to fix slow panel load

## v0.7.0 (2026-04-08)

### Feat

- add "Sin fecha de caducidad" option to medicines

## v0.6.0 (2026-04-07)

### Feat

- add farmaciola-card Lovelace custom card

## v0.5.1 (2026-04-07)

### Fix

- input selector rerender

## v0.5.0 (2026-04-07)

### Feat

- add dashboard stats bar with expiry filters to panel

## v0.4.5 (2026-04-07)

### Fix

- stop re-rendering form on every keystroke in CIMA search input

### Refactor

- remove LLM/Claude remnants and clean up config flow

## v0.4.4 (2026-04-07)

### Fix

- enhance HTTP registration and error handling in Farmaciola integration

## v0.4.3 (2026-04-07)

### Refactor

- remove Claude API key handling from config flow and related components, update UI and translations for notification service only

## v0.4.2 (2026-04-07)

### Fix

- update CLAUDE_MODEL alias and enhance error logging for LLMClient

## v0.4.1 (2026-04-07)

### Fix

- enhance error handling and validation for LLMClient API key, update translations for error messages

## v0.4.0 (2026-04-07)

### Feat

- improve LLMClient initialization and config flow handling for optional API key

## v0.3.2 (2026-04-07)

### Fix

- fix config flow

## v0.3.1 (2026-04-07)

### Fix

- update documentation URL and format requirements in manifest.json

## v0.3.0 (2026-04-07)

### Feat

- enhance project setup with VS Code integration and improve error handling for AsyncAnthropic
- add FarmaciolaPanel vanilla JS web component
- wire all components in async_setup_entry
- add config flow with Claude API key validation
- add REST API views for medicines and CIMA proxy
- add expiry scheduler with 7-day notification window
- add LLMClient for Claude summary generation
- add CimaClient with search and detail
- add FarmaciolaStorage CRUD layer

### Fix

- preserve created_at on update, add save assertions to tests

## v0.2.0 (2026-04-07)

### Feat

- scaffold farmaciola integration

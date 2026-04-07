# Changelog

All notable changes to this project are documented in this file.

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

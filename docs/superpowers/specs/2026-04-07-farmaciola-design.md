# Farmaciola — Home Assistant Home Pharmacy Integration
**Date:** 2026-04-07
**Status:** Approved

---

## Context

Managing a home pharmacy is error-prone without tooling: medicines expire unnoticed, duplicates accumulate, and finding the right drug in an emergency is slow. Farmaciola is a Home Assistant custom integration that solves this with a searchable catalog of medicines at home, CIMA API-powered identification (no manual data entry), Claude-generated summaries, and proactive expiry notifications. It presents as an independent sidebar panel with a Mushroom-compatible aesthetic.

---

## Architecture

**Two-layer: Python backend + Vanilla JS frontend panel**

```
custom_components/farmaciola/     ← HA custom component (Python)
  __init__.py                     - integration setup & panel registration
  manifest.json                   - HA integration manifest
  config_flow.py                  - setup wizard (Claude API key, notify service)
  const.py                        - constants (DOMAIN, STORAGE_KEY, etc.)
  storage.py                      - medicine catalog CRUD (HA .storage JSON)
  cima.py                         - CIMA REST API client (proxy)
  llm.py                          - Claude API client (summary generation)
  api.py                          - HA HTTP REST endpoint registration
  scheduler.py                    - daily expiry check & HA notification dispatch
  www/
    panel.html                    - single-file SPA (inline CSS + JS)
  translations/
    en.json
    es.json
```

The Python backend exposes REST endpoints on HA's HTTP server (authenticated via HA's standard `Authorization: Bearer <token>` header). The frontend calls these endpoints from the browser. All external API calls (CIMA, Claude) go through the backend — no API keys or external calls from the browser.

---

## Data Model

Stored in HA's built-in `.storage/farmaciola.json` as a keyed dict of medicine entries.

```json
{
  "id": "uuid-v4",
  "source": "cima",
  "nregistro": "80298",
  "nombre": "Ibuprofeno Kern Pharma 600mg",
  "dosis": "600mg",
  "forma_farmaceutica": "Comprimidos recubiertos",
  "laboratorio": "Kern Pharma SL",
  "via_administracion": "Vía oral",
  "foto_url": "https://cima.aemps.es/cima/fotos/thumbnails/...",
  "foto_manual": null,
  "principios_activos": ["Ibuprofeno 600mg"],
  "prescripcion": false,
  "summary": "Anti-inflammatory NSAID used for...",
  "fecha_caducidad": "2025-01-01",
  "notas": "Half used",
  "notified_at": null,
  "created_at": "2024-11-01T10:00:00Z",
  "updated_at": "2024-11-01T10:00:00Z"
}
```

**Key decisions:**
- `source: "cima" | "manual"` — determines which fields are populated and whether a summary is auto-generated
- `summary` — generated once by Claude on first save, cached permanently (no repeated API calls)
- `notified_at` — ISO timestamp; set when 7-day expiry notification is sent, prevents duplicate notifications
- `foto_manual` — base64-encoded image for manual entries only
- `fecha_caducidad` — stored as first day of the given month (YYYY-MM-01), since medicine expiry is month-precision

---

## REST API Endpoints

All endpoints under `/api/farmaciola/`, authenticated with HA long-lived access token.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/farmaciola/medicines` | List all medicines |
| POST | `/api/farmaciola/medicines` | Add medicine (triggers Claude summary) |
| PUT | `/api/farmaciola/medicines/{id}` | Update medicine |
| DELETE | `/api/farmaciola/medicines/{id}` | Delete medicine |
| GET | `/api/farmaciola/cima/search?q=` | Proxy CIMA medicine search (top 10) |
| GET | `/api/farmaciola/cima/medicamento?nregistro=` | Proxy CIMA full medicine detail |

---

## CIMA Integration Flow

1. User types in "Medicine name" field → frontend debounces 300ms → calls `GET /api/farmaciola/cima/search?q={query}`
2. Backend calls `https://cima.aemps.es/cima/rest/medicamentos?nombre={query}&pagina=1`, returns top 10 results
3. Frontend renders dropdown: thumbnail image + medicine name + dosage pill
4. User selects → frontend calls `GET /api/farmaciola/cima/medicamento?nregistro={nregistro}` for full detail
5. Form collapses to: selected medicine preview card + expiry date (MM/YYYY) + optional notes field
6. On "Save" → POST to backend → backend calls Claude API → stores complete entry

**Manual fallback** (toggle at top of form):
- Fields: name, dosage, pharmaceutical form, optional photo upload (stored as base64), expiry date, notes
- No auto-summary. A "Generate summary ✨" button available if user wants Claude to summarize from the name/notes they provided.

---

## LLM Integration (Claude)

**Model:** `claude-haiku-4-5-20251001` (fast, cheap, sufficient for brief summaries)

**Prompt pattern:**
```
You are a medical information assistant. Given the following medicine data, write a 2-3 sentence plain-language summary of what it is used for, its main active ingredient, and any important usage notes. Be concise and factual. Do not give dosage advice.

Medicine: {nombre}
Active ingredients: {principios_activos}
Pharmaceutical form: {forma_farmaceutica}
Administration route: {via_administracion}
Prescription required: {prescripcion}
```

**Config:** Claude API key stored in HA's config entry (encrypted). Configurable via the HA integration setup flow.

---

## Notifications

**Scheduler:** Registered via `async_track_time_interval`, runs daily at 09:00 local time.

**Logic:**
- For each medicine: compute days until `fecha_caducidad`
- If `7 >= days_remaining >= 0` AND `notified_at` is null → fire notifications + set `notified_at = now()`
- If `days_remaining < 0` (already expired) → no notification (user sees red chip in UI)

**Notification channels:**
1. `hass.services.async_call("persistent_notification", "create", {...})` — HA bell icon
2. `hass.services.async_call("notify", "notify", {"message": ..., "title": ...})` — mobile push (configurable service name, default: `notify.notify`)

**Message format:**
> **⚠ Medicine expiring soon**
> *Ibuprofeno Kern Pharma 600mg* expires on 15/01/2025 (in 5 days). Check your medicine cabinet.

---

## Frontend Panel

**Registration:** `hass.components.frontend.async_register_built_in_panel()` with `webcomponent_name`, pointing to `www/panel.html`. Appears as "Farmaciola 💊" in the HA sidebar.

**Styling:** Uses HA CSS custom properties (`--primary-color`, `--card-background-color`, `--secondary-text-color`, etc.) for automatic theme adaptation including Mushroom. Rounded cards (12-16px radius), pill chips, soft shadows — matching Mushroom aesthetics.

**Panel layout:**
- **Header:** "Farmaciola 💊" + search input (filters list live by `nombre` or `summary` text) + "+ Add" button (purple pill)
- **List:** Compact rows — 36px thumbnail | name (bold) + dosage · lab (grey subtitle) | expiry date (right-aligned, colour-coded)
  - Green: > 30 days remaining
  - Amber: 1–30 days remaining
  - Red bold: expired
- **Detail modal:** Full photo, chips (route, dosage, prescription required), Claude summary box (purple left border), data rows, Edit / Delete buttons
- **Add/Edit modal:** CIMA Search ↔ Manual Entry toggle; CIMA path shows autocomplete dropdown; after selection shows medicine preview card + expiry date + notes; Edit pre-fills all fields

**Search:** Client-side filter on the in-memory list (already loaded). Matches `nombre` and `summary` fields case-insensitively.

**Authentication:** Panel reads HA's `window.hassConnection` or uses `fetch` with `Authorization: Bearer ${hass.auth.data.access_token}` for all API calls.

---

## Config Flow (HA Integration Setup)

Steps when user adds "Farmaciola" integration in HA:
1. **Claude API key** — text field, validated by making a test API call
2. **Notify service** — text field, default `notify.notify`, used for mobile push

Settings editable afterwards via HA's integration options flow.

---

## File Structure (complete)

```
custom_components/farmaciola/
  __init__.py
  manifest.json
  config_flow.py
  const.py
  storage.py
  cima.py
  llm.py
  api.py
  scheduler.py
  www/
    panel.html
  translations/
    en.json
    es.json

docs/
  superpowers/
    specs/
      2026-04-07-farmaciola-design.md
```

---

## Verification

End-to-end test checklist:
1. Install integration in HA dev container → config flow completes without error
2. Panel appears in HA sidebar, loads without JS errors
3. Type "ibuprofen" in add form → CIMA autocomplete shows results with thumbnails
4. Select a medicine, set expiry date → save → appears in list
5. Click list row → detail modal opens with Claude summary populated
6. Search "pain" → filters to ibuprofen (summary match)
7. Edit a medicine → expiry date updates, list colour changes
8. Delete a medicine → removed from list
9. Set expiry date to 5 days from now → restart HA → check notification fires at 09:00
10. Manual entry flow → save without CIMA data → entry appears in list without photo

import json
import logging

import aiohttp
from homeassistant.components.frontend import async_register_built_in_panel
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import CimaDetailView, CimaSearchView, MedicineView, MedicinesView
from .cima import CimaClient
from .const import CONF_NOTIFY_SERVICE, DEFAULT_NOTIFY_SERVICE, DOMAIN
from .scheduler import async_setup_scheduler
from .storage import FarmaciolaStorage

_LOGGER = logging.getLogger(__name__)


def _read_integration_version(hass: HomeAssistant) -> str:
    """Best-effort version string from manifest.json for log correlation."""
    try:
        manifest_path = hass.config.path("custom_components/farmaciola/manifest.json")
        with open(manifest_path, encoding="utf-8") as fp:
            return str(json.load(fp).get("version", "unknown"))
    except (OSError, ValueError, json.JSONDecodeError):
        return "unknown"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    ver = _read_integration_version(hass)
    _LOGGER.info(
        "Farmaciola integration module ready (version %s, domain %s). "
        "Add it from Settings → Devices & services if not already configured.",
        ver,
        DOMAIN,
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ver = _read_integration_version(hass)
    _LOGGER.info(
        "Farmaciola starting setup for config entry %s (version %s)",
        entry.entry_id,
        ver,
    )
    storage = await FarmaciolaStorage(hass).async_load()
    session = aiohttp.ClientSession()
    cima = CimaClient(session)
    notify_service = entry.data.get(CONF_NOTIFY_SERVICE, DEFAULT_NOTIFY_SERVICE)

    hass.data[DOMAIN] = {
        "storage": storage,
        "cima": cima,
        "session": session,
    }

    # Register REST API views
    hass.http.register_view(MedicinesView())
    hass.http.register_view(MedicineView())
    hass.http.register_view(CimaSearchView())
    hass.http.register_view(CimaDetailView())

    # Serve panel static files
    hass.http.register_static_path(
        "/farmaciola_static",
        hass.config.path("custom_components/farmaciola/www"),
        cache_headers=False,
    )

    # Register sidebar panel
    async_register_built_in_panel(
        hass,
        component_name="custom",
        sidebar_title="Farmaciola",
        sidebar_icon="mdi:pill",
        frontend_url_path="farmaciola",
        config={
            "_panel_custom": {
                "name": "farmaciola-panel",
                "module_url": "/farmaciola_static/panel.js",
            }
        },
        require_admin=False,
    )

    # Start expiry scheduler
    unsub = await async_setup_scheduler(hass, storage, notify_service)
    hass.data[DOMAIN]["unsub_scheduler"] = unsub

    _LOGGER.info(
        "Farmaciola setup complete for entry %s: REST API, panel, and scheduler active",
        entry.entry_id,
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("Farmaciola unloading config entry %s", entry.entry_id)
    data = hass.data.get(DOMAIN, {})
    if unsub := data.get("unsub_scheduler"):
        unsub()
    if session := data.get("session"):
        await session.close()
    hass.data.pop(DOMAIN, None)
    return True

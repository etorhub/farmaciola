import json
import logging

import aiohttp
from homeassistant.components.frontend import (
    async_register_built_in_panel,
    async_remove_panel,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import CimaDetailView, CimaSearchView, MedicineView, MedicinesView
from .cima import CimaClient
from .const import CONF_NOTIFY_SERVICE, DEFAULT_NOTIFY_SERVICE, DOMAIN
from .scheduler import async_setup_scheduler
from .storage import FarmaciolaStorage

_LOGGER = logging.getLogger(__name__)

# Routes survive integration reload; register once per HA process (see _async_register_http).
_HTTP_REGISTERED_KEY = f"{DOMAIN}_http_registered"


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


async def _async_register_http(hass: HomeAssistant) -> None:
    """Register REST views and static panel assets once per Home Assistant run.

    ``register_static_path`` was removed in Home Assistant 2025.7; use
    ``async_register_static_paths`` when available. Re-registering the same
    routes on reload raises, so we guard with ``_HTTP_REGISTERED_KEY``.
    """
    if hass.data.get(_HTTP_REGISTERED_KEY):
        return

    hass.http.register_view(MedicinesView())
    hass.http.register_view(MedicineView())
    hass.http.register_view(CimaSearchView())
    hass.http.register_view(CimaDetailView())

    www_path = hass.config.path("custom_components/farmaciola/www")
    if hasattr(hass.http, "async_register_static_paths"):
        from homeassistant.components.http import StaticPathConfig

        await hass.http.async_register_static_paths(
            [StaticPathConfig("/farmaciola_static", www_path, False)]
        )
    elif hasattr(hass.http, "register_static_path"):
        hass.http.register_static_path("/farmaciola_static", www_path, False)
    else:
        _LOGGER.error(
            "Farmaciola: Home Assistant has no supported static file API "
            "(async_register_static_paths / register_static_path). "
            "Upgrade Home Assistant or report this to the integration author."
        )
        raise RuntimeError("Unsupported Home Assistant HTTP static path API")

    hass.data[_HTTP_REGISTERED_KEY] = True


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

    await _async_register_http(hass)

    # Sidebar panel (async_remove_panel in unload avoids duplicate on reload)
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
    async_remove_panel(hass, "farmaciola", warn_if_unknown=False)
    return True

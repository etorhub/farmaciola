import aiohttp
from homeassistant.components.frontend import async_register_built_in_panel
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import CimaDetailView, CimaSearchView, MedicineView, MedicinesView
from .cima import CimaClient
from .const import (
    CONF_CLAUDE_API_KEY,
    CONF_NOTIFY_SERVICE,
    DEFAULT_NOTIFY_SERVICE,
    DOMAIN,
)
from .llm import LLMClient
from .scheduler import async_setup_scheduler
from .storage import FarmaciolaStorage


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    storage = await FarmaciolaStorage(hass).async_load()
    session = aiohttp.ClientSession()
    cima = CimaClient(session)
    llm = LLMClient(entry.data[CONF_CLAUDE_API_KEY])
    notify_service = entry.data.get(CONF_NOTIFY_SERVICE, DEFAULT_NOTIFY_SERVICE)

    hass.data[DOMAIN] = {
        "storage": storage,
        "cima": cima,
        "llm": llm,
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

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = hass.data.get(DOMAIN, {})
    if unsub := data.get("unsub_scheduler"):
        unsub()
    if session := data.get("session"):
        await session.close()
    hass.data.pop(DOMAIN, None)
    return True

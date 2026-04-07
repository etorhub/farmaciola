"""Farmaciola Home Assistant integration."""

# Stub implementation - full implementation in Task 8
# Import these at module level to avoid import errors
try:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from .const import DOMAIN

    async def async_setup(hass: HomeAssistant, config: dict) -> bool:
        hass.data.setdefault(DOMAIN, {})
        return True

    async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
        return True

    async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
        hass.data.pop(DOMAIN, None)
        return True
except ImportError:
    # homeassistant not installed (e.g., during testing)
    pass

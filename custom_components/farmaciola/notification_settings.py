"""Persistent notification preferences for Farmaciola (panel-controlled)."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import (
    DEFAULT_NOTIFICATION_SETTINGS,
    STORAGE_NOTIFICATION_SETTINGS_KEY,
    STORAGE_VERSION,
)


def get_available_notify_services(hass: HomeAssistant) -> list[str]:
    """Return sorted notify.* service names registered in Home Assistant."""
    notify_domain = hass.services.async_services().get("notify", {})
    return sorted(f"notify.{name}" for name in notify_domain)


def default_notification_settings() -> dict:
    """Return a copy of the default notification settings."""
    return dict(DEFAULT_NOTIFICATION_SETTINGS)


class NotificationSettingsStore:
    def __init__(self, hass: HomeAssistant) -> None:
        self._store = Store(hass, STORAGE_VERSION, STORAGE_NOTIFICATION_SETTINGS_KEY)
        self._data: dict = default_notification_settings()
        self._loaded = False

    async def async_load(
        self, seed_notify_service: str | None = None
    ) -> NotificationSettingsStore:
        raw = await self._store.async_load()
        if raw:
            self._data = {**default_notification_settings(), **raw}
        elif seed_notify_service:
            self._data = default_notification_settings()
            self._data["notify_service"] = seed_notify_service
            await self._save()
        self._loaded = True
        return self

    def get(self) -> dict:
        return dict(self._data)

    async def async_update(self, updates: dict) -> dict:
        self._data = {**self._data, **updates}
        await self._save()
        return self.get()

    async def _save(self) -> None:
        await self._store.async_save(self._data)

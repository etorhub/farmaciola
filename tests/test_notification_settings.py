from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.farmaciola.const import DEFAULT_NOTIFY_SERVICE
from custom_components.farmaciola.notification_settings import (
    NotificationSettingsStore,
    default_notification_settings,
    get_available_notify_services,
)


@pytest.fixture
def mock_hass():
    hass = MagicMock()
    hass.services.async_services.return_value = {
        "notify": {"notify": {}, "mobile_app_phone": {}}
    }
    return hass


@pytest.fixture
async def settings_store(mock_hass):
    with patch("custom_components.farmaciola.notification_settings.Store") as MockStore:
        mock_store = AsyncMock()
        mock_store.async_load.return_value = None
        MockStore.return_value = mock_store
        store = NotificationSettingsStore(mock_hass)
        await store.async_load()
        yield store, mock_store


async def test_get_available_notify_services_sorted(mock_hass):
    services = get_available_notify_services(mock_hass)
    assert services == ["notify.mobile_app_phone", "notify.notify"]


async def test_async_load_seeds_from_config_entry(mock_hass):
    with patch("custom_components.farmaciola.notification_settings.Store") as MockStore:
        mock_store = AsyncMock()
        mock_store.async_load.return_value = None
        MockStore.return_value = mock_store
        store = NotificationSettingsStore(mock_hass)
        await store.async_load(seed_notify_service="notify.mobile_app_phone")

    assert store.get()["notify_services"] == ["notify.mobile_app_phone"]
    mock_store.async_save.assert_awaited_once()


async def test_async_load_merges_stored_data(mock_hass):
    with patch("custom_components.farmaciola.notification_settings.Store") as MockStore:
        mock_store = AsyncMock()
        mock_store.async_load.return_value = {
            "enabled": False,
            "notify_mobile": False,
        }
        MockStore.return_value = mock_store
        store = NotificationSettingsStore(mock_hass)
        await store.async_load()

    data = store.get()
    assert data["enabled"] is False
    assert data["notify_mobile"] is False
    assert data["notify_persistent"] is True
    assert data["notify_services"] == [DEFAULT_NOTIFY_SERVICE]


async def test_async_load_migrates_legacy_notify_service(mock_hass):
    with patch("custom_components.farmaciola.notification_settings.Store") as MockStore:
        mock_store = AsyncMock()
        mock_store.async_load.return_value = {
            "notify_service": "notify.mobile_app_phone"
        }
        MockStore.return_value = mock_store
        store = NotificationSettingsStore(mock_hass)
        await store.async_load()

    data = store.get()
    assert data["notify_services"] == ["notify.mobile_app_phone"]
    assert "notify_service" not in data


async def test_async_load_migrates_legacy_blank_notify_service(mock_hass):
    with patch("custom_components.farmaciola.notification_settings.Store") as MockStore:
        mock_store = AsyncMock()
        mock_store.async_load.return_value = {"notify_service": ""}
        MockStore.return_value = mock_store
        store = NotificationSettingsStore(mock_hass)
        await store.async_load()

    assert store.get()["notify_services"] == []


async def test_async_load_keeps_existing_notify_services_list(mock_hass):
    with patch("custom_components.farmaciola.notification_settings.Store") as MockStore:
        mock_store = AsyncMock()
        mock_store.async_load.return_value = {
            "notify_services": ["notify.a", "notify.b"]
        }
        MockStore.return_value = mock_store
        store = NotificationSettingsStore(mock_hass)
        await store.async_load()

    data = store.get()
    assert data["notify_services"] == ["notify.a", "notify.b"]
    assert "notify_service" not in data


async def test_async_update_persists(settings_store):
    store, mock_store = settings_store
    mock_store.async_save.reset_mock()
    updated = await store.async_update({"enabled": False})
    assert updated["enabled"] is False
    mock_store.async_save.assert_awaited_once()


def test_default_notification_settings_is_copy():
    a = default_notification_settings()
    b = default_notification_settings()
    a["enabled"] = False
    a["notify_services"].append("notify.extra")
    assert b["enabled"] is True
    assert b["notify_services"] == [DEFAULT_NOTIFY_SERVICE]

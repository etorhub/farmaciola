from datetime import date, timedelta
from unittest.mock import AsyncMock, MagicMock
from custom_components.farmaciola.scheduler import check_expiry_and_notify


def make_medicine(
    days_until_expiry, notified=False, med_id="abc-123", nombre="Test Med"
):
    expiry_date = date.today() + timedelta(days=days_until_expiry)
    expiry = expiry_date.isoformat()
    return {
        "id": med_id,
        "nombre": nombre,
        "fecha_caducidad": expiry,
        "notified_at": "2024-01-01T00:00:00Z" if notified else None,
    }


async def test_notifies_when_7_days_remaining():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [make_medicine(7)]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify.notify")

    assert hass.services.async_call.call_count == 2  # persistent + mobile
    storage.mark_notified.assert_awaited_once_with("abc-123")


async def test_no_notification_when_already_notified():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [make_medicine(7, notified=True)]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify.notify")

    hass.services.async_call.assert_not_called()


async def test_no_notification_when_30_days_remaining():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [make_medicine(30)]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify.notify")

    hass.services.async_call.assert_not_called()


async def test_no_notification_when_no_expiry_date():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [
        {"id": "x", "nombre": "X", "fecha_caducidad": None, "notified_at": None}
    ]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify.notify")

    hass.services.async_call.assert_not_called()


async def test_notifies_when_0_days_remaining():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [make_medicine(0)]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify.notify")

    assert hass.services.async_call.call_count == 2

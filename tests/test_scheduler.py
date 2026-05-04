from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch
from custom_components.farmaciola.scheduler import (
    async_setup_scheduler,
    check_expiry_and_notify,
)


def _month_offset(months: int) -> date:
    """Return the first day of the month that is `months` away from today."""
    today = date.today()
    total_months = today.year * 12 + today.month - 1 + months
    year, month = divmod(total_months, 12)
    return date(year, month + 1, 1)


def make_medicine(expiry_date, notified=False, med_id="abc-123", nombre="Test Med"):
    return {
        "id": med_id,
        "nombre": nombre,
        "fecha_caducidad": expiry_date.isoformat() if expiry_date else None,
        "notified_at": "2024-01-01T00:00:00Z" if notified else None,
    }


async def test_notifies_when_expiry_this_month():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [make_medicine(_month_offset(0))]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify.notify")

    assert hass.services.async_call.call_count == 2  # persistent + mobile
    storage.mark_notified.assert_awaited_once_with("abc-123")


async def test_notifies_when_expiry_past_month():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [make_medicine(_month_offset(-1))]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify.notify")

    assert hass.services.async_call.call_count == 2
    storage.mark_notified.assert_awaited_once_with("abc-123")


async def test_no_notification_when_next_month():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [make_medicine(_month_offset(1))]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify.notify")

    hass.services.async_call.assert_not_called()


async def test_no_notification_when_already_notified():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [make_medicine(_month_offset(0), notified=True)]
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


async def test_no_notification_when_future_month():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [make_medicine(_month_offset(3))]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify.notify")

    hass.services.async_call.assert_not_called()


async def test_no_notification_when_no_caduca():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [
        {
            "id": "x",
            "nombre": "X",
            "no_caduca": True,
            "fecha_caducidad": _month_offset(0).isoformat(),
            "notified_at": None,
        }
    ]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify.notify")

    hass.services.async_call.assert_not_called()


async def test_invalid_date_format_skipped():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [
        {
            "id": "x",
            "nombre": "X",
            "fecha_caducidad": "not-a-date",
            "notified_at": None,
        }
    ]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify.notify")

    hass.services.async_call.assert_not_called()


async def test_notify_service_without_dot():
    hass = MagicMock()
    hass.services.async_call = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = [make_medicine(_month_offset(0))]
    storage.mark_notified = AsyncMock()

    await check_expiry_and_notify(hass, storage, "notify")

    assert hass.services.async_call.call_count == 2


async def test_async_setup_scheduler_returns_unsub():
    hass = MagicMock()
    storage = MagicMock()
    storage.get_all.return_value = []
    mock_unsub = MagicMock()

    with patch(
        "custom_components.farmaciola.scheduler.async_track_time_interval",
        return_value=mock_unsub,
    ) as mock_track:
        unsub = await async_setup_scheduler(hass, storage, "notify.notify")

    assert unsub is mock_unsub
    mock_track.assert_called_once()


async def test_async_setup_scheduler_initial_tick_exception():
    hass = MagicMock()
    storage = MagicMock()
    storage.get_all.side_effect = Exception("storage failure")
    mock_unsub = MagicMock()

    with patch(
        "custom_components.farmaciola.scheduler.async_track_time_interval",
        return_value=mock_unsub,
    ):
        unsub = await async_setup_scheduler(hass, storage, "notify.notify")

    assert unsub is mock_unsub

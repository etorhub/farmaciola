import logging
from datetime import date, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval

_LOGGER = logging.getLogger(__name__)


async def check_expiry_and_notify(
    hass: HomeAssistant, storage, notify_service: str
) -> None:
    today = date.today()
    for medicine in storage.get_all():
        if medicine.get("no_caduca"):
            continue
        if not medicine.get("fecha_caducidad"):
            continue
        if medicine.get("notified_at"):
            continue
        try:
            expiry = date.fromisoformat(medicine["fecha_caducidad"])
        except ValueError:
            continue
        expiry_month_start = date(expiry.year, expiry.month, 1)
        if today >= expiry_month_start:
            nombre = medicine.get("nombre", "Unknown medicine")
            expiry_str = expiry.strftime("%m/%Y")
            message = f"⚠ {nombre} expires {expiry_str}. Check your medicine cabinet."
            hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "Medicine expiring soon",
                    "message": message,
                    "notification_id": f"farmaciola_{medicine['id']}",
                },
            )
            parts = notify_service.split(".", 1)
            domain = parts[0]
            service = parts[1] if len(parts) > 1 else "notify"
            hass.services.async_call(
                domain,
                service,
                {"title": "⚠ Medicine expiring soon", "message": message},
            )
            await storage.mark_notified(medicine["id"])


async def async_setup_scheduler(hass: HomeAssistant, storage, notify_service: str):
    async def _tick(now=None):
        try:
            await check_expiry_and_notify(hass, storage, notify_service)
        except Exception:
            _LOGGER.exception("Farmaciola expiry notification run failed")

    try:
        await _tick()
    except Exception:
        _LOGGER.exception("Farmaciola initial expiry check failed")

    return async_track_time_interval(hass, _tick, timedelta(hours=24))

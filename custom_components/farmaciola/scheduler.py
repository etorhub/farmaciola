from datetime import date, timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval


async def check_expiry_and_notify(
    hass: HomeAssistant, storage, notify_service: str
) -> None:
    today = date.today()
    for medicine in storage.get_all():
        if not medicine.get("fecha_caducidad"):
            continue
        if medicine.get("notified_at"):
            continue
        try:
            expiry = date.fromisoformat(medicine["fecha_caducidad"])
        except ValueError:
            continue
        days_remaining = (expiry - today).days
        if 0 <= days_remaining <= 7:
            nombre = medicine.get("nombre", "Unknown medicine")
            expiry_str = expiry.strftime("%d/%m/%Y")
            message = (
                f"⚠ {nombre} expires on {expiry_str} "
                f"(in {days_remaining} day{'s' if days_remaining != 1 else ''}). "
                "Check your medicine cabinet."
            )
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
        await check_expiry_and_notify(hass, storage, notify_service)

    await _tick()
    return async_track_time_interval(hass, _tick, timedelta(hours=24))

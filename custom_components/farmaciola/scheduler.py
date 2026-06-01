import logging
from datetime import date, timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval

_LOGGER = logging.getLogger(__name__)


def _notify_service_exists(hass: HomeAssistant, notify_service: str) -> bool:
    if not notify_service or "." not in notify_service:
        return False
    domain, service = notify_service.split(".", 1)
    if domain != "notify":
        return False
    return service in hass.services.async_services().get("notify", {})


async def check_expiry_and_notify(hass: HomeAssistant, storage, settings: dict) -> None:
    if not settings.get("enabled"):
        return

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
        if today < expiry_month_start:
            continue

        nombre = medicine.get("nombre", "Unknown medicine")
        expiry_str = expiry.strftime("%m/%Y")
        message = f"⚠ {nombre} expires {expiry_str}. Check your medicine cabinet."
        title = "Medicine expiring soon"
        mobile_title = "⚠ Medicine expiring soon"
        sent = False

        if settings.get("notify_persistent"):
            hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": title,
                    "message": message,
                    "notification_id": f"farmaciola_{medicine['id']}",
                },
            )
            sent = True

        if settings.get("notify_mobile"):
            notify_service = settings.get("notify_service") or ""
            if _notify_service_exists(hass, notify_service):
                domain, service = notify_service.split(".", 1)
                hass.services.async_call(
                    domain,
                    service,
                    {"title": mobile_title, "message": message},
                )
                sent = True
            elif notify_service:
                _LOGGER.warning(
                    "Farmaciola: notify service %s is not available; skipping mobile alert",
                    notify_service,
                )

        if sent:
            await storage.mark_notified(medicine["id"])


async def async_setup_scheduler(hass: HomeAssistant, storage, settings_store):
    async def _tick(now=None):
        try:
            await check_expiry_and_notify(hass, storage, settings_store.get())
        except Exception:
            _LOGGER.exception("Farmaciola expiry notification run failed")

    try:
        await _tick()
    except Exception:
        _LOGGER.exception("Farmaciola initial expiry check failed")

    return async_track_time_interval(hass, _tick, timedelta(hours=24))

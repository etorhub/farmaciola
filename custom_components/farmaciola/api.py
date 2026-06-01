from homeassistant.components.http import HomeAssistantView

from .const import DOMAIN
from .notification_settings import get_available_notify_services


def _validate_notification_settings(hass, body: dict) -> str | None:
    """Return an error message if invalid, else None."""
    enabled = bool(body.get("enabled"))
    notify_persistent = bool(body.get("notify_persistent"))
    notify_mobile = bool(body.get("notify_mobile"))
    notify_service = (body.get("notify_service") or "").strip()

    if enabled and not notify_persistent and not notify_mobile:
        return "At least one delivery channel is required when reminders are enabled"

    if notify_mobile:
        if not notify_service.startswith("notify."):
            return "notify_service must be a notify.* service (e.g. notify.notify)"
        available = get_available_notify_services(hass)
        if notify_service not in available:
            return f"Unknown notify service: {notify_service}"

    return None


def _settings_response(hass, settings_store):
    settings = settings_store.get()
    return {
        **settings,
        "available_notify_services": get_available_notify_services(hass),
    }


class NotificationSettingsView(HomeAssistantView):
    url = "/api/farmaciola/notifications/settings"
    name = "api:farmaciola:notifications:settings"
    requires_auth = True

    async def get(self, request):
        hass = request.app["hass"]
        settings_store = hass.data[DOMAIN]["notification_settings"]
        return self.json(_settings_response(hass, settings_store))

    async def put(self, request):
        hass = request.app["hass"]
        settings_store = hass.data[DOMAIN]["notification_settings"]
        try:
            body = await request.json()
        except Exception:
            return self.json({"error": "Invalid JSON"}, status_code=400)

        updates = {
            "enabled": bool(body.get("enabled")),
            "notify_persistent": bool(body.get("notify_persistent")),
            "notify_mobile": bool(body.get("notify_mobile")),
            "notify_service": (body.get("notify_service") or "").strip(),
        }
        error = _validate_notification_settings(hass, updates)
        if error:
            return self.json({"error": error}, status_code=400)

        await settings_store.async_update(updates)
        return self.json(_settings_response(hass, settings_store))


class MedicinesView(HomeAssistantView):
    url = "/api/farmaciola/medicines"
    name = "api:farmaciola:medicines"
    requires_auth = True

    async def get(self, request):
        storage = request.app["hass"].data[DOMAIN]["storage"]
        return self.json(storage.get_list())

    async def post(self, request):
        storage = request.app["hass"].data[DOMAIN]["storage"]
        try:
            data = await request.json()
        except Exception:
            return self.json({"error": "Invalid JSON"}, status_code=400)

        medicine_id = await storage.add_medicine(data)
        return self.json(storage.get_by_id(medicine_id), status_code=201)


class MedicineView(HomeAssistantView):
    url = "/api/farmaciola/medicines/{medicine_id}"
    name = "api:farmaciola:medicine"
    requires_auth = True

    async def get(self, request, medicine_id):
        storage = request.app["hass"].data[DOMAIN]["storage"]
        med = storage.get_by_id(medicine_id)
        if med is None:
            return self.json({"error": "Not found"}, status_code=404)
        return self.json(med)

    async def put(self, request, medicine_id):
        storage = request.app["hass"].data[DOMAIN]["storage"]
        try:
            data = await request.json()
        except Exception:
            return self.json({"error": "Invalid JSON"}, status_code=400)
        if not await storage.update_medicine(medicine_id, data):
            return self.json({"error": "Not found"}, status_code=404)
        return self.json(storage.get_by_id(medicine_id))

    async def delete(self, request, medicine_id):
        storage = request.app["hass"].data[DOMAIN]["storage"]
        if not await storage.delete_medicine(medicine_id):
            return self.json({"error": "Not found"}, status_code=404)
        return self.json({"ok": True})


class CimaSearchView(HomeAssistantView):
    url = "/api/farmaciola/cima/search"
    name = "api:farmaciola:cima:search"
    requires_auth = True

    async def get(self, request):
        cima = request.app["hass"].data[DOMAIN]["cima"]
        query = request.query.get("q", "").strip()
        if not query:
            return self.json([])
        try:
            results = await cima.search(query)
        except Exception:
            return self.json([], status_code=502)
        return self.json(results)


class CimaDetailView(HomeAssistantView):
    url = "/api/farmaciola/cima/medicamento"
    name = "api:farmaciola:cima:medicamento"
    requires_auth = True

    async def get(self, request):
        cima = request.app["hass"].data[DOMAIN]["cima"]
        nregistro = request.query.get("nregistro", "").strip()
        if not nregistro:
            return self.json({"error": "nregistro required"}, status_code=400)
        try:
            detail = await cima.get_detail(nregistro)
        except Exception:
            return self.json({"error": "CIMA error"}, status_code=502)
        return self.json(detail)

from homeassistant.components.http import HomeAssistantView
from .const import DOMAIN


class MedicinesView(HomeAssistantView):
    url = "/api/farmaciola/medicines"
    name = "api:farmaciola:medicines"
    requires_auth = True

    async def get(self, request):
        storage = request.app["hass"].data[DOMAIN]["storage"]
        return self.json(storage.get_all())

    async def post(self, request):
        hass = request.app["hass"]
        storage = hass.data[DOMAIN]["storage"]
        llm = hass.data[DOMAIN]["llm"]
        try:
            data = await request.json()
        except Exception:
            return self.json({"error": "Invalid JSON"}, status_code=400)

        if data.get("source") == "cima" and not data.get("summary"):
            data["summary"] = await llm.generate_summary(data)

        medicine_id = await storage.add_medicine(data)
        return self.json(storage.get_by_id(medicine_id), status_code=201)


class MedicineView(HomeAssistantView):
    url = "/api/farmaciola/medicines/{medicine_id}"
    name = "api:farmaciola:medicine"
    requires_auth = True

    async def put(self, request, medicine_id):
        hass = request.app["hass"]
        storage = hass.data[DOMAIN]["storage"]
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

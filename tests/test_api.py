from unittest.mock import AsyncMock, MagicMock

from custom_components.farmaciola.api import (
    CimaDetailView,
    CimaSearchView,
    MedicineView,
    MedicinesView,
)
from custom_components.farmaciola.const import DOMAIN


def make_request(storage=None, cima=None, query_params=None):
    request = MagicMock()
    request.app = {"hass": MagicMock()}
    request.app["hass"].data = {DOMAIN: {}}
    if storage is not None:
        request.app["hass"].data[DOMAIN]["storage"] = storage
    if cima is not None:
        request.app["hass"].data[DOMAIN]["cima"] = cima
    request.query = query_params or {}
    return request


# Call view methods as unbound functions with a MagicMock self, because the
# view classes inherit from a mocked HomeAssistantView, which breaks normal
# instance attribute resolution for methods defined in the subclass.


# --- MedicinesView ---


async def test_medicines_get_returns_list():
    storage = MagicMock()
    storage.get_list.return_value = [{"id": "1", "nombre": "Aspirina"}]
    request = make_request(storage=storage)
    self = MagicMock()

    await MedicinesView.get(self, request)

    storage.get_list.assert_called_once()
    self.json.assert_called_once_with([{"id": "1", "nombre": "Aspirina"}])


async def test_medicines_post_valid_json():
    storage = MagicMock()
    storage.add_medicine = AsyncMock(return_value="new-id")
    storage.get_by_id.return_value = {"id": "new-id", "nombre": "Test"}
    request = make_request(storage=storage)
    request.json = AsyncMock(return_value={"nombre": "Test"})
    self = MagicMock()

    await MedicinesView.post(self, request)

    storage.add_medicine.assert_awaited_once_with({"nombre": "Test"})
    self.json.assert_called_once_with(
        {"id": "new-id", "nombre": "Test"}, status_code=201
    )


async def test_medicines_post_invalid_json():
    storage = MagicMock()
    request = make_request(storage=storage)
    request.json = AsyncMock(side_effect=Exception("bad json"))
    self = MagicMock()

    await MedicinesView.post(self, request)

    self.json.assert_called_once_with({"error": "Invalid JSON"}, status_code=400)


# --- MedicineView ---


async def test_medicine_get_found():
    storage = MagicMock()
    storage.get_by_id.return_value = {"id": "abc", "nombre": "Ibuprofeno"}
    request = make_request(storage=storage)
    self = MagicMock()

    await MedicineView.get(self, request, "abc")

    self.json.assert_called_once_with({"id": "abc", "nombre": "Ibuprofeno"})


async def test_medicine_get_not_found():
    storage = MagicMock()
    storage.get_by_id.return_value = None
    request = make_request(storage=storage)
    self = MagicMock()

    await MedicineView.get(self, request, "missing")

    self.json.assert_called_once_with({"error": "Not found"}, status_code=404)


async def test_medicine_put_success():
    storage = MagicMock()
    storage.update_medicine = AsyncMock(return_value=True)
    storage.get_by_id.return_value = {"id": "abc", "nombre": "Updated"}
    request = make_request(storage=storage)
    request.json = AsyncMock(return_value={"nombre": "Updated"})
    self = MagicMock()

    await MedicineView.put(self, request, "abc")

    storage.update_medicine.assert_awaited_once_with("abc", {"nombre": "Updated"})
    self.json.assert_called_once_with({"id": "abc", "nombre": "Updated"})


async def test_medicine_put_not_found():
    storage = MagicMock()
    storage.update_medicine = AsyncMock(return_value=False)
    request = make_request(storage=storage)
    request.json = AsyncMock(return_value={"nombre": "X"})
    self = MagicMock()

    await MedicineView.put(self, request, "missing")

    self.json.assert_called_once_with({"error": "Not found"}, status_code=404)


async def test_medicine_put_invalid_json():
    storage = MagicMock()
    request = make_request(storage=storage)
    request.json = AsyncMock(side_effect=Exception("bad json"))
    self = MagicMock()

    await MedicineView.put(self, request, "abc")

    self.json.assert_called_once_with({"error": "Invalid JSON"}, status_code=400)


async def test_medicine_delete_success():
    storage = MagicMock()
    storage.delete_medicine = AsyncMock(return_value=True)
    request = make_request(storage=storage)
    self = MagicMock()

    await MedicineView.delete(self, request, "abc")

    storage.delete_medicine.assert_awaited_once_with("abc")
    self.json.assert_called_once_with({"ok": True})


async def test_medicine_delete_not_found():
    storage = MagicMock()
    storage.delete_medicine = AsyncMock(return_value=False)
    request = make_request(storage=storage)
    self = MagicMock()

    await MedicineView.delete(self, request, "missing")

    self.json.assert_called_once_with({"error": "Not found"}, status_code=404)


# --- CimaSearchView ---


async def test_cima_search_empty_query_returns_empty_list():
    cima = MagicMock()
    request = make_request(cima=cima, query_params={"q": ""})
    self = MagicMock()

    await CimaSearchView.get(self, request)

    self.json.assert_called_once_with([])
    cima.search.assert_not_called()


async def test_cima_search_no_q_param_returns_empty_list():
    cima = MagicMock()
    request = make_request(cima=cima, query_params={})
    self = MagicMock()

    await CimaSearchView.get(self, request)

    self.json.assert_called_once_with([])


async def test_cima_search_with_query_returns_results():
    cima = MagicMock()
    cima.search = AsyncMock(return_value=[{"nregistro": "123", "nombre": "Med"}])
    request = make_request(cima=cima, query_params={"q": "ibuprofeno"})
    self = MagicMock()

    await CimaSearchView.get(self, request)

    cima.search.assert_awaited_once_with("ibuprofeno")
    self.json.assert_called_once_with([{"nregistro": "123", "nombre": "Med"}])


async def test_cima_search_upstream_error_returns_502():
    cima = MagicMock()
    cima.search = AsyncMock(side_effect=Exception("CIMA down"))
    request = make_request(cima=cima, query_params={"q": "algo"})
    self = MagicMock()

    await CimaSearchView.get(self, request)

    self.json.assert_called_once_with([], status_code=502)


# --- CimaDetailView ---


async def test_cima_detail_missing_nregistro_returns_400():
    cima = MagicMock()
    request = make_request(cima=cima, query_params={})
    self = MagicMock()

    await CimaDetailView.get(self, request)

    self.json.assert_called_once_with({"error": "nregistro required"}, status_code=400)


async def test_cima_detail_returns_detail():
    cima = MagicMock()
    cima.get_detail = AsyncMock(return_value={"nregistro": "80298", "nombre": "Ibu"})
    request = make_request(cima=cima, query_params={"nregistro": "80298"})
    self = MagicMock()

    await CimaDetailView.get(self, request)

    cima.get_detail.assert_awaited_once_with("80298")
    self.json.assert_called_once_with({"nregistro": "80298", "nombre": "Ibu"})


async def test_cima_detail_upstream_error_returns_502():
    cima = MagicMock()
    cima.get_detail = AsyncMock(side_effect=Exception("CIMA down"))
    request = make_request(cima=cima, query_params={"nregistro": "80298"})
    self = MagicMock()

    await CimaDetailView.get(self, request)

    self.json.assert_called_once_with({"error": "CIMA error"}, status_code=502)

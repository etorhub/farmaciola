import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from custom_components.farmaciola.storage import FarmaciolaStorage


@pytest.fixture
def mock_hass():
    return MagicMock()


@pytest.fixture
async def storage(mock_hass):
    with patch("custom_components.farmaciola.storage.Store") as MockStore:
        mock_store = AsyncMock()
        mock_store.async_load.return_value = {}
        MockStore.return_value = mock_store
        s = FarmaciolaStorage(mock_hass)
        await s.async_load()
        yield s


async def test_add_medicine_returns_uuid(storage):
    med_id = await storage.add_medicine(
        {"source": "cima", "nombre": "Ibuprofeno 600mg"}
    )
    assert len(med_id) == 36
    assert "-" in med_id


async def test_add_medicine_stores_data(storage):
    med_id = await storage.add_medicine({"source": "cima", "nombre": "Paracetamol"})
    result = storage.get_by_id(med_id)
    assert result["nombre"] == "Paracetamol"
    assert result["id"] == med_id
    assert result["notified_at"] is None
    assert "created_at" in result


async def test_get_all_returns_list(storage):
    await storage.add_medicine({"nombre": "A"})
    await storage.add_medicine({"nombre": "B"})
    all_meds = storage.get_all()
    assert len(all_meds) == 2


async def test_update_medicine(storage):
    med_id = await storage.add_medicine({"nombre": "Old"})
    success = await storage.update_medicine(med_id, {"nombre": "New"})
    assert success is True
    assert storage.get_by_id(med_id)["nombre"] == "New"


async def test_update_medicine_not_found(storage):
    success = await storage.update_medicine("nonexistent-id", {"nombre": "X"})
    assert success is False


async def test_delete_medicine(storage):
    med_id = await storage.add_medicine({"nombre": "ToDelete"})
    success = await storage.delete_medicine(med_id)
    assert success is True
    assert storage.get_by_id(med_id) is None


async def test_delete_medicine_not_found(storage):
    success = await storage.delete_medicine("nonexistent-id")
    assert success is False


async def test_mark_notified(storage):
    med_id = await storage.add_medicine({"nombre": "Expiring"})
    await storage.mark_notified(med_id)
    assert storage.get_by_id(med_id)["notified_at"] is not None

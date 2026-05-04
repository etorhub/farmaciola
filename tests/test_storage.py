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
        yield s, mock_store


@pytest.fixture
async def storage_only(mock_hass):
    with patch("custom_components.farmaciola.storage.Store") as MockStore:
        mock_store = AsyncMock()
        mock_store.async_load.return_value = {}
        MockStore.return_value = mock_store
        s = FarmaciolaStorage(mock_hass)
        await s.async_load()
        yield s


async def test_add_medicine_returns_uuid(storage):
    s, mock_store = storage
    med_id = await s.add_medicine({"source": "cima", "nombre": "Ibuprofeno 600mg"})
    assert len(med_id) == 36
    assert "-" in med_id
    mock_store.async_save.assert_called()


async def test_add_medicine_stores_data(storage):
    s, mock_store = storage
    med_id = await s.add_medicine({"source": "cima", "nombre": "Paracetamol"})
    result = s.get_by_id(med_id)
    assert result["nombre"] == "Paracetamol"
    assert result["id"] == med_id
    assert result["notified_at"] is None
    assert "created_at" in result
    mock_store.async_save.assert_called()


async def test_get_all_returns_list(storage_only):
    await storage_only.add_medicine({"nombre": "A"})
    await storage_only.add_medicine({"nombre": "B"})
    all_meds = storage_only.get_all()
    assert len(all_meds) == 2


async def test_update_medicine(storage):
    s, mock_store = storage
    med_id = await s.add_medicine({"nombre": "Old"})
    original_created_at = s.get_by_id(med_id)["created_at"]
    mock_store.async_save.reset_mock()
    success = await s.update_medicine(med_id, {"nombre": "New"})
    assert success is True
    assert s.get_by_id(med_id)["nombre"] == "New"
    assert s.get_by_id(med_id)["created_at"] == original_created_at
    mock_store.async_save.assert_called()


async def test_update_medicine_not_found(storage_only):
    success = await storage_only.update_medicine("nonexistent-id", {"nombre": "X"})
    assert success is False


async def test_delete_medicine(storage):
    s, mock_store = storage
    med_id = await s.add_medicine({"nombre": "ToDelete"})
    mock_store.async_save.reset_mock()
    success = await s.delete_medicine(med_id)
    assert success is True
    assert s.get_by_id(med_id) is None
    mock_store.async_save.assert_called()


async def test_delete_medicine_not_found(storage_only):
    success = await storage_only.delete_medicine("nonexistent-id")
    assert success is False


async def test_mark_notified(storage):
    s, mock_store = storage
    med_id = await s.add_medicine({"nombre": "Expiring"})
    mock_store.async_save.reset_mock()
    await s.mark_notified(med_id)
    assert s.get_by_id(med_id)["notified_at"] is not None
    mock_store.async_save.assert_called()


async def test_mark_notified_twice_succeeds(storage):
    s, mock_store = storage
    med_id = await s.add_medicine({"nombre": "Expiring"})
    mock_store.async_save.reset_mock()
    await s.mark_notified(med_id)
    first_notified_at = s.get_by_id(med_id)["notified_at"]
    assert first_notified_at is not None

    await s.mark_notified(med_id)
    second_notified_at = s.get_by_id(med_id)["notified_at"]
    assert second_notified_at is not None
    assert mock_store.async_save.call_count == 2


async def test_get_list_excludes_foto_manual(storage_only):
    await storage_only.add_medicine({"nombre": "A", "foto_manual": "base64data"})
    await storage_only.add_medicine({"nombre": "B"})
    result = storage_only.get_list()
    assert len(result) == 2
    for item in result:
        assert "foto_manual" not in item
        assert "has_foto_manual" in item
    with_foto = next(r for r in result if r["nombre"] == "A")
    without_foto = next(r for r in result if r["nombre"] == "B")
    assert with_foto["has_foto_manual"] is True
    assert without_foto["has_foto_manual"] is False


async def test_mark_notified_nonexistent_is_noop(storage_only):
    await storage_only.mark_notified("nonexistent-id")

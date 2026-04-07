import uuid
from datetime import datetime, timezone
from homeassistant.helpers.storage import Store
from .const import STORAGE_VERSION, STORAGE_KEY


class FarmaciolaStorage:
    def __init__(self, hass):
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self._data: dict[str, dict] = {}

    async def async_load(self) -> "FarmaciolaStorage":
        data = await self._store.async_load()
        self._data = data or {}
        return self

    async def _save(self):
        await self._store.async_save(self._data)

    def get_all(self) -> list[dict]:
        return list(self._data.values())

    def get_by_id(self, medicine_id: str) -> dict | None:
        return self._data.get(medicine_id)

    async def add_medicine(self, data: dict) -> str:
        medicine_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        self._data[medicine_id] = {
            **data,
            "id": medicine_id,
            "notified_at": None,
            "created_at": now,
            "updated_at": now,
        }
        await self._save()
        return medicine_id

    async def update_medicine(self, medicine_id: str, data: dict) -> bool:
        if medicine_id not in self._data:
            return False
        now = datetime.now(timezone.utc).isoformat()
        original_created_at = self._data[medicine_id]["created_at"]
        self._data[medicine_id] = {
            **self._data[medicine_id],
            **data,
            "id": medicine_id,
            "created_at": original_created_at,
            "updated_at": now,
        }
        await self._save()
        return True

    async def delete_medicine(self, medicine_id: str) -> bool:
        if medicine_id not in self._data:
            return False
        del self._data[medicine_id]
        await self._save()
        return True

    async def mark_notified(self, medicine_id: str) -> None:
        if medicine_id in self._data:
            self._data[medicine_id]["notified_at"] = datetime.now(
                timezone.utc
            ).isoformat()
            await self._save()

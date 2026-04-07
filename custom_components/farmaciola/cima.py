import aiohttp
from .const import CIMA_BASE_URL


class CimaClient:
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session

    async def search(self, query: str) -> list[dict]:
        url = f"{CIMA_BASE_URL}/medicamentos"
        async with self._session.get(
            url, params={"nombre": query, "pagina": 1}
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()
        return [self._norm_search(r) for r in data.get("resultados", [])[:10]]

    async def get_detail(self, nregistro: str) -> dict:
        url = f"{CIMA_BASE_URL}/medicamento"
        async with self._session.get(url, params={"nregistro": nregistro}) as resp:
            resp.raise_for_status()
            data = await resp.json()
        return self._norm_detail(data)

    def _first_foto(self, fotos: list) -> str | None:
        return fotos[0]["url"] if fotos else None

    def _norm_search(self, r: dict) -> dict:
        return {
            "nregistro": r.get("nregistro"),
            "nombre": r.get("nombre"),
            "dosis": r.get("dosis"),
            "foto_url": self._first_foto(r.get("fotos", [])),
            "forma_farmaceutica": (r.get("formaFarmaceuticaSimplificada") or {}).get(
                "nombre"
            ),
            "laboratorio": r.get("labtitular"),
        }

    def _norm_detail(self, r: dict) -> dict:
        vias = r.get("viasAdministracion", [])
        principios = r.get("principiosActivos", [])
        return {
            "nregistro": r.get("nregistro"),
            "nombre": r.get("nombre"),
            "dosis": r.get("dosis"),
            "foto_url": self._first_foto(r.get("fotos", [])),
            "forma_farmaceutica": (r.get("formaFarmaceutica") or {}).get("nombre"),
            "laboratorio": r.get("labtitular"),
            "via_administracion": vias[0]["nombre"] if vias else None,
            "principios_activos": [
                f"{p['nombre']} {p.get('cantidad', '')} {p.get('unidad', '')}".strip()
                for p in principios
            ],
            "prescripcion": r.get("receta", False),
            "source": "cima",
        }

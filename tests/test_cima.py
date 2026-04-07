import pytest
from unittest.mock import AsyncMock, MagicMock
from custom_components.farmaciola.cima import CimaClient

MOCK_SEARCH_RESPONSE = {
    "totalFilas": 2,
    "pagina": 1,
    "tamanioPagina": 200,
    "resultados": [
        {
            "nregistro": "80298",
            "nombre": "Ibuprofeno Kern Pharma 600mg EFG",
            "dosis": "600mg",
            "labtitular": "Kern Pharma SL",
            "fotos": [
                {
                    "tipo": "materialas",
                    "url": "https://cima.aemps.es/cima/fotos/thumbnails/materialas/80298/80298_materialas.jpg",
                }
            ],
            "formaFarmaceuticaSimplificada": {"id": 1, "nombre": "Comprimidos"},
        },
        {
            "nregistro": "51347",
            "nombre": "Neobrufen 400mg",
            "dosis": "400mg",
            "labtitular": "Abbott",
            "fotos": [],
            "formaFarmaceuticaSimplificada": {"id": 1, "nombre": "Comprimidos"},
        },
    ],
}

MOCK_DETAIL_RESPONSE = {
    "nregistro": "80298",
    "nombre": "Ibuprofeno Kern Pharma 600mg EFG",
    "dosis": "600mg",
    "labtitular": "Kern Pharma SL",
    "fotos": [
        {
            "tipo": "materialas",
            "url": "https://cima.aemps.es/cima/fotos/thumbnails/materialas/80298/80298_materialas.jpg",
        }
    ],
    "formaFarmaceutica": {"id": 1, "nombre": "Comprimidos recubiertos"},
    "viasAdministracion": [{"id": 1, "nombre": "VÍA ORAL"}],
    "principiosActivos": [{"nombre": "Ibuprofeno", "cantidad": "600", "unidad": "mg"}],
    "receta": False,
}


@pytest.fixture
def mock_session():
    session = MagicMock()
    return session


def make_mock_response(json_data):
    mock_resp = AsyncMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json = AsyncMock(return_value=json_data)
    mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_resp.__aexit__ = AsyncMock(return_value=False)
    return mock_resp


async def test_search_returns_normalized_list(mock_session):
    mock_session.get.return_value = make_mock_response(MOCK_SEARCH_RESPONSE)
    client = CimaClient(mock_session)
    results = await client.search("ibuprofeno")
    assert len(results) == 2
    assert results[0]["nregistro"] == "80298"
    assert results[0]["nombre"] == "Ibuprofeno Kern Pharma 600mg EFG"
    assert (
        results[0]["foto_url"]
        == "https://cima.aemps.es/cima/fotos/thumbnails/materialas/80298/80298_materialas.jpg"
    )
    assert results[1]["foto_url"] is None  # no fotos


async def test_search_limits_to_10(mock_session):
    many_results = [MOCK_SEARCH_RESPONSE["resultados"][0]] * 15
    mock_session.get.return_value = make_mock_response(
        {**MOCK_SEARCH_RESPONSE, "resultados": many_results}
    )
    client = CimaClient(mock_session)
    results = await client.search("ibuprofeno")
    assert len(results) == 10


async def test_get_detail_returns_normalized(mock_session):
    mock_session.get.return_value = make_mock_response(MOCK_DETAIL_RESPONSE)
    client = CimaClient(mock_session)
    detail = await client.get_detail("80298")
    assert detail["nregistro"] == "80298"
    assert detail["via_administracion"] == "VÍA ORAL"
    assert detail["principios_activos"] == ["Ibuprofeno 600 mg"]
    assert detail["prescripcion"] is False
    assert detail["forma_farmaceutica"] == "Comprimidos recubiertos"

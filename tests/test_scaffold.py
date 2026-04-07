from custom_components.farmaciola.const import DOMAIN, CIMA_BASE_URL


def test_constants():
    assert DOMAIN == "farmaciola"
    assert CIMA_BASE_URL == "https://cima.aemps.es/cima/rest"

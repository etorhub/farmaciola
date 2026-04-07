from custom_components.farmaciola.const import DOMAIN, CIMA_BASE_URL, CLAUDE_MODEL

def test_constants():
    assert DOMAIN == "farmaciola"
    assert CIMA_BASE_URL == "https://cima.aemps.es/cima/rest"
    assert CLAUDE_MODEL == "claude-haiku-4-5-20251001"

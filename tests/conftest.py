import sys
import os
from unittest.mock import MagicMock


# ---------------------------------------------------------------------------
# Stub base classes — must be real Python classes so that integration modules
# can inherit from them and define methods on the resulting subclasses.
# ---------------------------------------------------------------------------

class _HomeAssistantView:
    """Minimal stand-in for homeassistant.components.http.HomeAssistantView."""
    def json(self, data, status_code=200):
        return MagicMock()


class _ConfigFlow:
    """Stand-in for homeassistant.config_entries.ConfigFlow."""
    VERSION = 1

    def __init_subclass__(cls, domain=None, **kwargs):
        super().__init_subclass__(**kwargs)

    def async_create_entry(self, **kwargs):
        return MagicMock()

    def async_show_form(self, **kwargs):
        return MagicMock()


class _OptionsFlow:
    """Stand-in for homeassistant.config_entries.OptionsFlow."""
    def async_create_entry(self, **kwargs):
        return MagicMock()

    def async_show_form(self, **kwargs):
        return MagicMock()


# ---------------------------------------------------------------------------
# Build module mocks, wiring in the stub classes where needed.
# ---------------------------------------------------------------------------

_http_mod = MagicMock()
_http_mod.HomeAssistantView = _HomeAssistantView
_http_mod.StaticPathConfig = MagicMock

_config_entries_mod = MagicMock()
_config_entries_mod.ConfigFlow = _ConfigFlow
_config_entries_mod.OptionsFlow = _OptionsFlow

# The homeassistant module must expose config_entries as a real attribute so
# that "from homeassistant import config_entries" resolves to our stub, not
# to an auto-generated MagicMock child.
_ha_mod = MagicMock()
_ha_mod.config_entries = _config_entries_mod

# homeassistant.core.callback is used as a decorator — make it a passthrough
# so decorated functions remain callable coroutines/functions.
_core_mod = MagicMock()
_core_mod.callback = lambda fn: fn

# Mock homeassistant before importing any custom_components
sys.modules["homeassistant"] = _ha_mod
sys.modules["homeassistant.core"] = _core_mod
sys.modules["homeassistant.config_entries"] = _config_entries_mod
sys.modules["homeassistant.components"] = MagicMock()
sys.modules["homeassistant.components.http"] = _http_mod
sys.modules["homeassistant.components.frontend"] = MagicMock()
sys.modules["homeassistant.helpers"] = MagicMock()
sys.modules["homeassistant.helpers.storage"] = MagicMock()
sys.modules["homeassistant.helpers.event"] = MagicMock()

# Make custom_components importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

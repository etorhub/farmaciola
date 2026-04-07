import sys
import os
from unittest.mock import MagicMock

# Mock homeassistant before importing any custom_components
sys.modules["homeassistant"] = MagicMock()
sys.modules["homeassistant.core"] = MagicMock()
sys.modules["homeassistant.config_entries"] = MagicMock()
sys.modules["homeassistant.components"] = MagicMock()
sys.modules["homeassistant.components.http"] = MagicMock()
sys.modules["homeassistant.components.frontend"] = MagicMock()
sys.modules["homeassistant.helpers"] = MagicMock()
sys.modules["homeassistant.helpers.storage"] = MagicMock()
sys.modules["homeassistant.helpers.event"] = MagicMock()

# Make custom_components importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

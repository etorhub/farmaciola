import sys
import os
from unittest.mock import MagicMock

# Mock homeassistant before importing any custom_components
sys.modules["homeassistant"] = MagicMock()
sys.modules["homeassistant.helpers"] = MagicMock()
sys.modules["homeassistant.helpers.storage"] = MagicMock()

# Make custom_components importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

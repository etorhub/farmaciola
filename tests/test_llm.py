from unittest.mock import AsyncMock, MagicMock, patch
from custom_components.farmaciola.llm import LLMClient

SAMPLE_MEDICINE = {
    "nombre": "Ibuprofeno Kern Pharma 600mg",
    "principios_activos": ["Ibuprofeno 600 mg"],
    "forma_farmaceutica": "Comprimidos recubiertos",
    "via_administracion": "VÍA ORAL",
    "prescripcion": False,
}


async def test_generate_summary_returns_string():
    with patch("custom_components.farmaciola.llm.AsyncAnthropic") as MockAnthropic:
        mock_client = AsyncMock()
        MockAnthropic.return_value = mock_client
        mock_message = MagicMock()
        mock_message.content = [
            MagicMock(text="Anti-inflammatory medicine for pain relief.")
        ]
        mock_client.messages.create = AsyncMock(return_value=mock_message)

        client = LLMClient("fake-api-key")
        summary = await client.generate_summary(SAMPLE_MEDICINE)

        assert summary == "Anti-inflammatory medicine for pain relief."
        mock_client.messages.create.assert_called_once()
        call_kwargs = mock_client.messages.create.call_args[1]
        assert "Ibuprofeno Kern Pharma 600mg" in call_kwargs["messages"][0]["content"]


async def test_generate_summary_returns_empty_on_error():
    with patch("custom_components.farmaciola.llm.AsyncAnthropic") as MockAnthropic:
        mock_client = AsyncMock()
        MockAnthropic.return_value = mock_client
        mock_client.messages.create = AsyncMock(side_effect=Exception("API error"))

        client = LLMClient("fake-api-key")
        summary = await client.generate_summary(SAMPLE_MEDICINE)

        assert summary == ""

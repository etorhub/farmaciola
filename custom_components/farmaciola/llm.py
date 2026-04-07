try:
    from anthropic import AsyncAnthropic
except ModuleNotFoundError:

    class AsyncAnthropic:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs):
            raise ModuleNotFoundError(
                "anthropic is not installed. Install project dependencies to use LLM features."
            )


from typing import Optional

from .const import CLAUDE_MODEL

_PROMPT = """You are a medical information assistant. Write a 2-3 sentence plain-language summary of what this medicine is used for, its main active ingredient, and any important usage notes. Be concise and factual. Do not give dosage advice.

Medicine: {nombre}
Active ingredients: {principios_activos}
Pharmaceutical form: {forma_farmaceutica}
Administration route: {via_administracion}
Prescription required: {prescripcion}"""


class LLMClient:
    def __init__(self, api_key: Optional[str]):
        key = (api_key or "").strip()
        self._client = AsyncAnthropic(api_key=key) if key else None

    async def generate_summary(self, medicine: dict) -> str:
        if not self._client:
            return ""
        prompt = _PROMPT.format(
            nombre=medicine.get("nombre", ""),
            principios_activos=", ".join(medicine.get("principios_activos") or []),
            forma_farmaceutica=medicine.get("forma_farmaceutica", ""),
            via_administracion=medicine.get("via_administracion", ""),
            prescripcion="Yes" if medicine.get("prescripcion") else "No",
        )
        try:
            message = await self._client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception:
            return ""

    async def validate_key(self) -> bool:
        if not self._client:
            return False
        try:
            await self._client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=5,
                messages=[{"role": "user", "content": "test"}],
            )
            return True
        except Exception:
            return False

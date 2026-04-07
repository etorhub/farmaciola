import logging
from typing import Optional, Tuple

from .const import CLAUDE_MODEL

_LOGGER = logging.getLogger(__name__)

_ANTHROPIC_AVAILABLE = False
AsyncAnthropic = None  # type: ignore[misc, assignment]
try:
    from anthropic import (
        APIConnectionError,
        APITimeoutError,
        AsyncAnthropic,
        AuthenticationError,
        BadRequestError,
        NotFoundError,
        PermissionDeniedError,
        RateLimitError,
        UnprocessableEntityError,
    )

    _ANTHROPIC_AVAILABLE = True
except ModuleNotFoundError:
    pass


def _log_claude_exception(prefix: str, err: BaseException) -> None:
    """Log SDK errors with response body when present (explains 400/422 messages)."""
    body = getattr(err, "body", None)
    request_id = getattr(err, "request_id", None)
    if body is not None or request_id is not None:
        _LOGGER.warning(
            "%s (%s): %s request_id=%s body=%s",
            prefix,
            type(err).__name__,
            err,
            request_id,
            body,
        )
    else:
        _LOGGER.warning("%s (%s): %s", prefix, type(err).__name__, err)


_PROMPT = """You are a medical information assistant. Write a 2-3 sentence plain-language summary of what this medicine is used for, its main active ingredient, and any important usage notes. Be concise and factual. Do not give dosage advice.

Medicine: {nombre}
Active ingredients: {principios_activos}
Pharmaceutical form: {forma_farmaceutica}
Administration route: {via_administracion}
Prescription required: {prescripcion}"""


def _validation_error_key(exc: BaseException) -> str:
    """Map an Anthropic SDK exception to a config-flow translation key."""
    if isinstance(exc, AuthenticationError):
        return "invalid_api_key"
    if isinstance(exc, PermissionDeniedError):
        return "permission_denied"
    if isinstance(exc, RateLimitError):
        return "rate_limit"
    if isinstance(exc, NotFoundError):
        return "model_not_found"
    if isinstance(exc, (BadRequestError, UnprocessableEntityError)):
        return "bad_request"
    if isinstance(exc, (APIConnectionError, APITimeoutError)):
        return "cannot_connect"
    return "api_error"


class LLMClient:
    def __init__(self, api_key: Optional[str]):
        key = (api_key or "").strip()
        if not key or not _ANTHROPIC_AVAILABLE:
            self._client = None
        else:
            self._client = AsyncAnthropic(api_key=key)

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
        except Exception as err:
            _log_claude_exception("Claude summary request failed", err)
            return ""

    async def validate_key(self) -> Tuple[bool, Optional[str]]:
        """Check API key with a minimal request. Returns (ok, error_key or None)."""
        if not _ANTHROPIC_AVAILABLE:
            _LOGGER.warning(
                "Claude validation cannot run: anthropic package is not installed "
                "(restart Home Assistant after installing the integration)"
            )
            return False, "dependency_missing"
        if not self._client:
            return False, "invalid_api_key"
        try:
            await self._client.messages.create(
                model=CLAUDE_MODEL,
                # Avoid very small max_tokens — some accounts/models return 400.
                max_tokens=64,
                messages=[{"role": "user", "content": "Reply with OK."}],
            )
            return True, None
        except Exception as err:
            key = _validation_error_key(err)
            _log_claude_exception("Claude API key validation failed", err)
            return False, key

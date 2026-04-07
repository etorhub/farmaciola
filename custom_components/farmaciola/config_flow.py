import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import (
    DOMAIN,
    CONF_CLAUDE_API_KEY,
    CONF_NOTIFY_SERVICE,
    DEFAULT_NOTIFY_SERVICE,
)
from .llm import LLMClient


class FarmaciolaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    _api_key: str = ""

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            raw = (user_input.get(CONF_CLAUDE_API_KEY) or "").strip()
            if not raw:
                self._api_key = ""
                return await self.async_step_notify()
            client = LLMClient(raw)
            if await client.validate_key():
                self._api_key = raw
                return await self.async_step_notify()
            errors[CONF_CLAUDE_API_KEY] = "invalid_api_key"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Optional(CONF_CLAUDE_API_KEY, default=""): str}
            ),
            errors=errors,
        )

    async def async_step_notify(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Farmaciola",
                data={
                    CONF_CLAUDE_API_KEY: self._api_key,
                    CONF_NOTIFY_SERVICE: user_input.get(
                        CONF_NOTIFY_SERVICE, DEFAULT_NOTIFY_SERVICE
                    ),
                },
            )
        return self.async_show_form(
            step_id="notify",
            data_schema=vol.Schema(
                {vol.Optional(CONF_NOTIFY_SERVICE, default=DEFAULT_NOTIFY_SERVICE): str}
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return FarmaciolaOptionsFlow(config_entry)


class FarmaciolaOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        if user_input is not None:
            new_key = (user_input.get(CONF_CLAUDE_API_KEY) or "").strip()
            if new_key:
                client = LLMClient(new_key)
                if not await client.validate_key():
                    errors[CONF_CLAUDE_API_KEY] = "invalid_api_key"
            if not errors:
                preserved_opts = dict(self._config_entry.options)
                new_data = {**self._config_entry.data}
                new_data[CONF_CLAUDE_API_KEY] = new_key
                new_data[CONF_NOTIFY_SERVICE] = user_input.get(
                    CONF_NOTIFY_SERVICE,
                    self._config_entry.data.get(
                        CONF_NOTIFY_SERVICE, DEFAULT_NOTIFY_SERVICE
                    ),
                )
                self.hass.config_entries.async_update_entry(
                    self._config_entry, data=new_data
                )
                await self.hass.config_entries.async_reload(self._config_entry.entry_id)
                return self.async_create_entry(title="", data=preserved_opts)

        current_key = self._config_entry.data.get(CONF_CLAUDE_API_KEY) or ""
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_CLAUDE_API_KEY,
                        default=current_key,
                    ): str,
                    vol.Optional(
                        CONF_NOTIFY_SERVICE,
                        default=self._config_entry.data.get(
                            CONF_NOTIFY_SERVICE, DEFAULT_NOTIFY_SERVICE
                        ),
                    ): str,
                }
            ),
            errors=errors,
        )

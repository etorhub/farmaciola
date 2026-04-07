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
            client = LLMClient(user_input[CONF_CLAUDE_API_KEY])
            if await client.validate_key():
                self._api_key = user_input[CONF_CLAUDE_API_KEY]
                return await self.async_step_notify()
            else:
                errors[CONF_CLAUDE_API_KEY] = "invalid_api_key"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_CLAUDE_API_KEY): str}),
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
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_NOTIFY_SERVICE,
                        default=self._config_entry.data.get(
                            CONF_NOTIFY_SERVICE, DEFAULT_NOTIFY_SERVICE
                        ),
                    ): str,
                }
            ),
        )

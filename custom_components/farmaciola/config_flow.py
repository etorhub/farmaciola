import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import (
    DOMAIN,
    CONF_NOTIFY_SERVICE,
    DEFAULT_NOTIFY_SERVICE,
)


class FarmaciolaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Farmaciola",
                data={
                    CONF_NOTIFY_SERVICE: user_input.get(
                        CONF_NOTIFY_SERVICE, DEFAULT_NOTIFY_SERVICE
                    ),
                },
            )

        return self.async_show_form(
            step_id="user",
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
            new_data = {**self._config_entry.data}
            new_data.pop("claude_api_key", None)
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
            preserved_opts = dict(self._config_entry.options)
            return self.async_create_entry(title="", data=preserved_opts)

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

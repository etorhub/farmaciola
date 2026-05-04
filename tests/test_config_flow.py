from unittest.mock import AsyncMock, MagicMock

from custom_components.farmaciola.config_flow import (
    FarmaciolaConfigFlow,
    FarmaciolaOptionsFlow,
)
from custom_components.farmaciola.const import CONF_NOTIFY_SERVICE, DEFAULT_NOTIFY_SERVICE


async def test_user_step_shows_form_when_no_input():
    flow = FarmaciolaConfigFlow()
    flow.async_show_form = MagicMock(return_value="form_result")

    result = await flow.async_step_user(None)

    flow.async_show_form.assert_called_once()
    call_kwargs = flow.async_show_form.call_args
    assert call_kwargs.kwargs["step_id"] == "user"


async def test_user_step_creates_entry_with_input():
    flow = FarmaciolaConfigFlow()
    flow.async_create_entry = MagicMock(return_value="entry_result")

    result = await flow.async_step_user({CONF_NOTIFY_SERVICE: "notify.mobile"})

    flow.async_create_entry.assert_called_once_with(
        title="Farmaciola",
        data={CONF_NOTIFY_SERVICE: "notify.mobile"},
    )


async def test_user_step_uses_default_when_key_missing():
    flow = FarmaciolaConfigFlow()
    flow.async_create_entry = MagicMock(return_value="entry_result")

    result = await flow.async_step_user({})

    flow.async_create_entry.assert_called_once_with(
        title="Farmaciola",
        data={CONF_NOTIFY_SERVICE: DEFAULT_NOTIFY_SERVICE},
    )


def test_get_options_flow_returns_options_flow_instance():
    config_entry = MagicMock()
    options_flow = FarmaciolaConfigFlow.async_get_options_flow(config_entry)

    assert type(options_flow).__name__ == "FarmaciolaOptionsFlow"
    assert options_flow._config_entry is config_entry


async def test_options_flow_init_step_shows_form_when_no_input():
    config_entry = MagicMock()
    config_entry.data = {CONF_NOTIFY_SERVICE: "notify.default"}

    flow = FarmaciolaOptionsFlow(config_entry)
    flow.async_show_form = MagicMock(return_value="form_result")

    result = await flow.async_step_init(None)

    flow.async_show_form.assert_called_once()
    call_kwargs = flow.async_show_form.call_args
    assert call_kwargs.kwargs["step_id"] == "init"


async def test_options_flow_init_step_updates_entry_with_input():
    config_entry = MagicMock()
    config_entry.data = {CONF_NOTIFY_SERVICE: "notify.old"}
    config_entry.options = {}

    flow = FarmaciolaOptionsFlow(config_entry)
    flow.hass = MagicMock()
    flow.hass.config_entries.async_reload = AsyncMock()
    flow.async_create_entry = MagicMock(return_value="entry_result")

    result = await flow.async_step_init({CONF_NOTIFY_SERVICE: "notify.new"})

    flow.hass.config_entries.async_update_entry.assert_called_once()
    flow.hass.config_entries.async_reload.assert_awaited_once_with(
        config_entry.entry_id
    )
    flow.async_create_entry.assert_called_once_with(title="", data={})


async def test_options_flow_init_step_uses_default_when_key_missing():
    config_entry = MagicMock()
    config_entry.data = {CONF_NOTIFY_SERVICE: "notify.current"}
    config_entry.options = {}

    flow = FarmaciolaOptionsFlow(config_entry)
    flow.hass = MagicMock()
    flow.hass.config_entries.async_reload = AsyncMock()
    flow.async_create_entry = MagicMock(return_value="entry_result")

    await flow.async_step_init({})

    update_call = flow.hass.config_entries.async_update_entry.call_args
    updated_data = update_call.kwargs["data"]
    assert updated_data[CONF_NOTIFY_SERVICE] == "notify.current"

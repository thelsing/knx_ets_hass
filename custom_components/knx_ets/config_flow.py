"""Adds config flow for Blueprint."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import selector

from .const import DOMAIN, LOGGER


class KnxEtsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for KnxEts."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title="Default",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    # vol.Required(
                    #     CONF_USERNAME,
                    #     default=(user_input or {}).get(CONF_USERNAME, vol.UNDEFINED),
                    # ): selector.TextSelector(
                    #     selector.TextSelectorConfig(
                    #         type=selector.TextSelectorType.TEXT,
                    #     ),
                    # ),
                    # vol.Required(CONF_PASSWORD): selector.TextSelector(
                    #     selector.TextSelectorConfig(
                    #         type=selector.TextSelectorType.PASSWORD,
                    #     ),
                    # ),
                },
            ),
            errors=_errors,
        )

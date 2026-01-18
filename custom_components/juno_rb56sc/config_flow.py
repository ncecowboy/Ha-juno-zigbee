"""Config flow for Juno RB56SC Zigbee Light integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import zha
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import device_registry as dr

from .const import CONF_DEVICE, DOMAIN, MANUFACTURER

_LOGGER = logging.getLogger(__name__)


class JunoRB56SCConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Juno RB56SC Zigbee Light."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._device_id: str | None = None
        self._devices: dict[str, str] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            self._device_id = user_input[CONF_DEVICE]
            
            # Create a unique ID based on the device
            await self.async_set_unique_id(self._device_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=self._devices.get(self._device_id, "Juno RB56SC Light"),
                data={CONF_DEVICE: self._device_id},
            )

        # Get available Juno RB56SC devices
        self._devices = await self._get_juno_devices(self.hass)

        if not self._devices:
            return self.async_abort(reason="no_devices_found")

        data_schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE): vol.In(self._devices),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def _get_juno_devices(self, hass: HomeAssistant) -> dict[str, str]:
        """Get list of Juno devices from device registry."""
        device_registry = dr.async_get(hass)
        devices = {}

        for device in device_registry.devices.values():
            # Check if device is a Juno device (any model)
            if device.manufacturer and MANUFACTURER.lower() in device.manufacturer.lower():
                devices[device.id] = (
                    f"{device.name or device.model} ({device.manufacturer})"
                )

        return devices

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> JunoRB56SCOptionsFlow:
        """Get the options flow for this handler."""
        return JunoRB56SCOptionsFlow(config_entry)


class JunoRB56SCOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Juno RB56SC Zigbee Light."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )

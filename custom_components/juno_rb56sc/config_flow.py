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
import homeassistant.helpers.config_validation as cv

from .const import CONF_DEVICE, DOMAIN, MANUFACTURER

_LOGGER = logging.getLogger(__name__)


class JunoRB56SCConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Juno RB56SC Zigbee Light."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._devices: dict[str, str] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            selected_device_ids = user_input[CONF_DEVICE]
            
            if not selected_device_ids:
                errors["base"] = "no_devices_selected"
            else:
                # Get all devices for display names
                all_devices = await self._get_all_juno_devices(self.hass)
                
                # Get currently configured device IDs
                configured_devices = {
                    entry.unique_id
                    for entry in self.hass.config_entries.async_entries(DOMAIN)
                    if entry.unique_id
                }
                
                # Filter out already configured devices
                new_device_ids = [
                    device_id for device_id in selected_device_ids
                    if device_id not in configured_devices
                ]
                
                if not new_device_ids:
                    return self.async_abort(reason="already_configured")
                
                # Create entries for all devices
                # We create the first one through the normal flow
                first_device_id = new_device_ids[0]
                await self.async_set_unique_id(first_device_id)
                self._abort_if_unique_id_configured()
                
                # For additional devices (if any), initiate separate flows
                if len(new_device_ids) > 1:
                    for device_id in new_device_ids[1:]:
                        # Start a new config flow for each additional device
                        self.hass.async_create_task(
                            self.hass.config_entries.flow.async_init(
                                DOMAIN,
                                context={"source": "import"},
                                data={CONF_DEVICE: device_id, "device_id": device_id, "device_name": all_devices.get(device_id, "Juno Light")},
                            )
                        )
                
                # Return entry for the first device
                return self.async_create_entry(
                    title=all_devices.get(first_device_id, "Juno Light"),
                    data={CONF_DEVICE: first_device_id},
                )

        # Get available Juno devices (excluding already configured ones)
        self._devices = await self._get_juno_devices(self.hass)

        if not self._devices:
            return self.async_abort(reason="no_devices_found")

        data_schema = vol.Schema(
            {
                vol.Required(CONF_DEVICE): cv.multi_select(self._devices),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_import(
        self, import_data: dict[str, Any]
    ) -> FlowResult:
        """Handle import from configuration.yaml or programmatic setup."""
        device_id = import_data.get("device_id")
        device_name = import_data.get("device_name", "Juno Light")
        
        if not device_id:
            return self.async_abort(reason="no_device_id")
        
        # Set unique ID and check if already configured
        await self.async_set_unique_id(device_id)
        self._abort_if_unique_id_configured()
        
        # Create the entry
        return self.async_create_entry(
            title=device_name,
            data={CONF_DEVICE: device_id},
        )

    async def _get_juno_devices(self, hass: HomeAssistant) -> dict[str, str]:
        """Get list of Juno devices from device registry, excluding already configured ones."""
        device_registry = dr.async_get(hass)
        devices = {}

        # Get all currently configured device IDs for this integration
        configured_devices = {
            entry.unique_id
            for entry in self.hass.config_entries.async_entries(DOMAIN)
            if entry.unique_id
        }

        for device in device_registry.devices.values():
            # Check if device is a Juno device (any model)
            if device.manufacturer and MANUFACTURER.lower() in device.manufacturer.lower():
                # Skip if already configured
                if device.id in configured_devices:
                    continue
                    
                # Use device name if available, otherwise fall back to model
                device_name = device.name_by_user or device.name or device.model or "Unknown"
                devices[device.id] = device_name

        return devices

    async def _get_all_juno_devices(self, hass: HomeAssistant) -> dict[str, str]:
        """Get list of all Juno devices from device registry (including configured ones)."""
        device_registry = dr.async_get(hass)
        devices = {}

        for device in device_registry.devices.values():
            # Check if device is a Juno device (any model)
            if device.manufacturer and MANUFACTURER.lower() in device.manufacturer.lower():
                # Use device name if available, otherwise fall back to model
                device_name = device.name_by_user or device.name or device.model or "Unknown"
                devices[device.id] = device_name

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

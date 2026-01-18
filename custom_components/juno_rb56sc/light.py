"""Light platform for Juno RB56SC Zigbee Light integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CONF_DEVICE, DOMAIN, MANUFACTURER, MODEL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Juno RB56SC light from a config entry."""
    device_id = config_entry.data[CONF_DEVICE]
    
    device_registry = dr.async_get(hass)
    entity_registry = er.async_get(hass)
    
    device = device_registry.async_get(device_id)
    
    if not device:
        _LOGGER.error("Device %s not found in registry", device_id)
        return

    # Find existing ZHA light entity for this device
    entities = er.async_entries_for_device(entity_registry, device_id)
    light_entity_id = None
    
    for entity in entities:
        if entity.domain == "light" and entity.platform == "zha":
            light_entity_id = entity.entity_id
            break
    
    if light_entity_id:
        _LOGGER.debug("Found ZHA light entity: %s", light_entity_id)
        async_add_entities([JunoRB56SCLight(hass, device, light_entity_id, config_entry)])
    else:
        _LOGGER.warning("No ZHA light entity found for device %s", device_id)


class JunoRB56SCLight(LightEntity):
    """Representation of a Juno RB56SC Zigbee Light."""

    _attr_has_entity_name = True
    _attr_name = "Light"
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}

    def __init__(
        self,
        hass: HomeAssistant,
        device: dr.DeviceEntry,
        zha_light_entity_id: str,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the Juno RB56SC light."""
        self.hass = hass
        self._device = device
        self._zha_light_entity_id = zha_light_entity_id
        self._attr_unique_id = f"{device.id}_juno_light"
        self._attr_device_info = {
            "identifiers": device.identifiers,
            "name": device.name,
            "manufacturer": device.manufacturer or MANUFACTURER,
            "model": device.model or MODEL,
            "sw_version": device.sw_version,
        }
        self._attr_is_on = False
        self._attr_brightness = 255

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        # Sync initial state from ZHA entity
        await self._sync_from_zha()

    async def _sync_from_zha(self) -> None:
        """Sync state from the underlying ZHA light entity."""
        zha_state = self.hass.states.get(self._zha_light_entity_id)
        if zha_state:
            self._attr_is_on = zha_state.state == "on"
            self._attr_brightness = zha_state.attributes.get(ATTR_BRIGHTNESS, 255)
            _LOGGER.debug(
                "Synced state from ZHA: is_on=%s, brightness=%s",
                self._attr_is_on,
                self._attr_brightness,
            )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        service_data = {"entity_id": self._zha_light_entity_id}
        
        if ATTR_BRIGHTNESS in kwargs:
            service_data[ATTR_BRIGHTNESS] = kwargs[ATTR_BRIGHTNESS]
            self._attr_brightness = kwargs[ATTR_BRIGHTNESS]
        
        await self.hass.services.async_call(
            "light",
            "turn_on",
            service_data,
            blocking=True,
        )
        
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        await self.hass.services.async_call(
            "light",
            "turn_off",
            {"entity_id": self._zha_light_entity_id},
            blocking=True,
        )
        
        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Update the entity state."""
        await self._sync_from_zha()

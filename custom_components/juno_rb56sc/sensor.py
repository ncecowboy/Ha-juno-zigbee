"""Sensor platform for Juno RB56SC Zigbee Light integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ATTR_FIRMWARE_VERSION,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    CONF_DEVICE,
    DOMAIN,
    MANUFACTURER,
    MODEL,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Juno RB56SC sensors from a config entry."""
    device_id = config_entry.data[CONF_DEVICE]
    
    device_registry = dr.async_get(hass)
    device = device_registry.async_get(device_id)
    
    if not device:
        _LOGGER.error("Device %s not found in registry", device_id)
        return

    sensors = [
        JunoFirmwareSensor(device, config_entry),
        JunoManufacturerSensor(device, config_entry),
        JunoModelSensor(device, config_entry),
    ]
    
    async_add_entities(sensors)


class JunoBaseSensor(SensorEntity):
    """Base class for Juno RB56SC sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        device: dr.DeviceEntry,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self._device = device
        self._attr_device_info = {
            "identifiers": device.identifiers,
            "name": device.name,
            "manufacturer": device.manufacturer or MANUFACTURER,
            "model": device.model or MODEL,
            "sw_version": device.sw_version,
        }


class JunoFirmwareSensor(JunoBaseSensor):
    """Sensor for Juno RB56SC firmware version."""

    _attr_name = "Firmware Version"
    _attr_icon = "mdi:chip"

    def __init__(
        self,
        device: dr.DeviceEntry,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the firmware sensor."""
        super().__init__(device, config_entry)
        self._attr_unique_id = f"{device.id}_firmware_version"
        self._attr_native_value = device.sw_version or "Unknown"

    async def async_update(self) -> None:
        """Update the sensor."""
        # Firmware version is updated from device registry
        device_registry = dr.async_get(self.hass)
        device = device_registry.async_get(self._device.id)
        if device:
            self._attr_native_value = device.sw_version or "Unknown"


class JunoManufacturerSensor(JunoBaseSensor):
    """Sensor for Juno RB56SC manufacturer."""

    _attr_name = "Manufacturer"
    _attr_icon = "mdi:factory"

    def __init__(
        self,
        device: dr.DeviceEntry,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the manufacturer sensor."""
        super().__init__(device, config_entry)
        self._attr_unique_id = f"{device.id}_manufacturer"
        self._attr_native_value = device.manufacturer or MANUFACTURER

    async def async_update(self) -> None:
        """Update the sensor."""
        device_registry = dr.async_get(self.hass)
        device = device_registry.async_get(self._device.id)
        if device:
            self._attr_native_value = device.manufacturer or MANUFACTURER


class JunoModelSensor(JunoBaseSensor):
    """Sensor for Juno RB56SC model."""

    _attr_name = "Model"
    _attr_icon = "mdi:information-outline"

    def __init__(
        self,
        device: dr.DeviceEntry,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the model sensor."""
        super().__init__(device, config_entry)
        self._attr_unique_id = f"{device.id}_model"
        self._attr_native_value = device.model or MODEL

    async def async_update(self) -> None:
        """Update the sensor."""
        device_registry = dr.async_get(self.hass)
        device = device_registry.async_get(self._device.id)
        if device:
            self._attr_native_value = device.model or MODEL

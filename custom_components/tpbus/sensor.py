"""Sensor platform for Taipei Bus Stop Monitor."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([
        TPBusStopSensor(coordinator, entry),
    ])


class TPBusStopSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Taipei Bus Stop sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = entry.data.get("name", DEFAULT_NAME)
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}"
        self._url = entry.data["url"]

    @property
    def state(self) -> str | None:
        """Return the state of the sensor (arrival time in seconds)."""
        if self.coordinator.data and "n1" in self.coordinator.data:
            try:
                n1_parts = self.coordinator.data["n1"].split(",")
                if len(n1_parts) >= 8:
                    arrival_time = n1_parts[7]
                    if arrival_time and arrival_time != "-1":
                        return arrival_time
            except Exception as e:
                _LOGGER.warning("Error parsing arrival time: %s", e)
        return "unavailable"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        data = self.coordinator.data
        attributes = {
            "url": self._url,
            "stop_id": data.get("id"),
            "update_time": data.get("UpdateTime"),
            "raw_data": data.get("n1"),
        }
        
        # Parse the n1 field if available
        if "n1" in data:
            try:
                n1_parts = data["n1"].split(",")
                if len(n1_parts) >= 8:
                    arrival_time = n1_parts[7]
                    attributes["arrival_time_seconds"] = arrival_time if arrival_time and arrival_time != "-1" else None
            except Exception as e:
                _LOGGER.warning("Error parsing n1 field: %s", e)
        
        return attributes

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:bus-stop"
    
    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return "s"
"""Sensor platform for knx_ets."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription


if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import KnxEtsConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="knx_ets",
        name="Integration Sensor",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: KnxEtsConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        KnxEtsSensor(
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class KnxEtsSensor(SensorEntity):
    """knx_ets Sensor class."""

    def __init__(
        self,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__()
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return "TestHello"

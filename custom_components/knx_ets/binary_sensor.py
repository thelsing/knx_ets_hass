"""Binary sensor platform for knx_ets."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)


if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import KnxEtsConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="knx_ets",
        name="Knx Ets Binary Sensor",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: KnxEtsConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        KnxEtsBinarySensor(
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class KnxEtsBinarySensor(BinarySensorEntity):
    """knx_ets binary_sensor class."""

    def __init__(
        self,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__()
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return True
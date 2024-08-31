"""Switch platform for knx_ets."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from homeassistant.const import (
    EntityCategory,
)
from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
import knx
import asyncio

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import KnxEtsConfigEntry
    from .device import KNXInterfaceDevice

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="program_mode",
        name="Enable Program Mode",
        entity_category = EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: KnxEtsConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""

    device: KNXInterfaceDevice = entry.runtime_data.device

    async_add_entities(
        KnxEtsSwitch(
            entity_description=entity_description, knx_device=device
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class KnxEtsSwitch(SwitchEntity):
    """knx_ets switch class."""

    def __init__(
        self,
        entity_description: SwitchEntityDescription, knx_device: KNXInterfaceDevice
    ) -> None:
        """Initialize the switch class."""
        super().__init__()
        self.entity_description = entity_description
        self._attr_device_info = knx_device.device_info

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return knx.ProgramMode()

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        knx.ProgramMode(True)
        await asyncio.sleep(0)

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        knx.ProgramMode(False)
        await asyncio.sleep(0)

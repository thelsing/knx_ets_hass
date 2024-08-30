"""Switch platform for knx_ets."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

import asyncio

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .data import KnxEtsConfigEntry

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="knx_ets",
        name="Integration Switch",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: KnxEtsConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        KnxEtsSwitch(
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class KnxEtsSwitch(SwitchEntity):
    """knx_ets switch class."""

    def __init__(
        self,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        super().__init__()
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return True

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        await asyncio.sleep(0)

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        await asyncio.sleep(0)

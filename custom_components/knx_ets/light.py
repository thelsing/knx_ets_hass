"""Support for KNX/IP lights."""

from __future__ import annotations

from typing import Any

from homeassistant.components.light import LightEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .module import KnxEtsConfigEntry, KnxModule, LightParams


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: KnxEtsConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up light(s) for KNX platform."""
    module: KnxModule = config_entry.runtime_data
    async_add_entities(KnxLight(module, param) for param in module.lights)

class KnxLight(LightEntity):
    """Representation of an Knx Light."""

    _attr_should_poll = False
    _params: LightParams

    def __init__(self, module: KnxModule, params:LightParams) -> None:
        """Initialize an KnxLight."""
        self._params = params
        self._state = None
        module.register(params.state_go, self)

    @property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._params.name

    @property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._params.state_go.value ==  b'\x01'

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on."""
        self._params.go.value = b'\x01'

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        self._params.go.value = b'\x00'

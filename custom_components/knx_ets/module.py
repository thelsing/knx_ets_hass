"""Custom types for knx_ets."""

from __future__ import annotations

from dataclasses import dataclass
from struct import unpack, unpack_from
from typing import TYPE_CHECKING

import debugpy
import knx
from knx import GroupObject

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

from homeassistant.helpers.entity import Entity

from .const import FUNCTION_LIGHT, FUNCTION_SENSOR
from .device import KNXInterfaceDevice

type KnxEtsConfigEntry = ConfigEntry[KnxModule]


@dataclass
class LightParams:
    """Holds data for a single light."""

    name: str
    go: GroupObject
    state_go: GroupObject


class KnxModule:
    """general module for the KnxEts integration."""

    integration: Integration
    device: KNXInterfaceDevice
    lights: list[LightParams] = []
    go_entity_map: dict[GroupObject, list[Entity]] = {}

    def parseDeviceParameters(self):
        parameters = knx.Parameters()
        channels = unpack(">h", parameters[:2])[0]
        offset = 2
        for channel in range(channels):
            (functiontype, functionparams) = unpack_from(
                ">bh", parameters, offset + channel * 3
            )
            match functiontype:
                case FUNCTION_LIGHT:
                    (first_go, name) = unpack_from(">h150s", parameters, functionparams)
                    self.lights.append(
                        LightParams(
                            name.decode().strip('\x00'),
                           # name.decode().strip('\x00'),
                            knx.GetGroupObject(first_go),
                            knx.GetGroupObject(first_go + 1),
                        )
                    )

    def register(self, go: GroupObject, entity:Entity):
        entities = self.go_entity_map.get(go)
        if entities is None:
            entities = []
        entities.append(entity)

        self.go_entity_map[go] = entities

    def updated(self, go: GroupObject):
       # debugpy.breakpoint()

        entities = self.go_entity_map.get(go)
        if entities is None:
            return

        for entity in self.go_entity_map[go]:
            entity.schedule_update_ha_state()


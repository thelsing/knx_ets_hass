"""
Custom integration to integrate knx_ets with Home Assistant.

For more details about this integration, please refer to
https://github.com/thelsing/knx_ets
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration
from homeassistant.helpers.storage import STORAGE_DIR

import debugpy
import knx

from .const import DOMAIN
from .data import KnxEtsData
from .device import KNXInterfaceDevice

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import KnxEtsConfigEntry

PLATFORMS: list[Platform] = [
 #   Platform.SENSOR,
 #   Platform.BINARY_SENSOR,
    Platform.SWITCH,
]

def updated(groupObject):
    debugpy.breakpoint()
    print(groupObject.asap())
    print(groupObject.value)

# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: KnxEtsConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    entry.runtime_data = KnxEtsData(
        integration=async_get_loaded_integration(hass, entry.domain),
        device=KNXInterfaceDevice(hass, entry),
    )
    path = Path(hass.config.path(STORAGE_DIR, DOMAIN), "flash.bin")
    knx.FlashFilePath(path.absolute().as_posix())
    knx.ReadMemory()
#   knx.ProgramMode(True)
    knx.Callback(updated)
#    if knx.Configured():
#        go = knx.GetGroupObject(1)
#        if go is not None:
#            go.callBack(updated)
    knx.Start()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: KnxEtsConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: KnxEtsConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)

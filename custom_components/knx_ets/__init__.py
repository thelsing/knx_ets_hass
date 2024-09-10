"""Custom integration to integrate knx_ets with Home Assistant.

For more details about this integration, please refer to
https://github.com/thelsing/knx_ets
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import knx

from homeassistant.const import Platform
from homeassistant.helpers.storage import STORAGE_DIR
from homeassistant.loader import async_get_loaded_integration

from .const import DOMAIN
from .device import KNXInterfaceDevice
from .module import KnxModule

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .module import KnxEtsConfigEntry

PLATFORMS: list[Platform] = [
 #   Platform.SENSOR,
 #   Platform.BINARY_SENSOR,
    Platform.SWITCH,
    Platform.LIGHT
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: KnxEtsConfigEntry,
) -> bool:
    """Set up this integration using UI."""

    module = KnxModule()
    module.integration=async_get_loaded_integration(hass, entry.domain)
    module.device=KNXInterfaceDevice(hass, entry)
    
    entry.runtime_data = module
    path = Path(hass.config.path(STORAGE_DIR, DOMAIN), "flash.bin")
    knx.FlashFilePath(path.absolute().as_posix())
    await hass.async_add_executor_job(knx.ReadMemory)
    knx.Callback(module.updated)
    if knx.Configured():
        module.parseDeviceParameters()
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

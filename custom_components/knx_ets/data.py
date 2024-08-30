"""Custom types for knx_ets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import KnxEtsApiClient
    from .coordinator import BlueprintDataUpdateCoordinator


type KnxEtsConfigEntry = ConfigEntry[KnxEtsData]


@dataclass
class KnxEtsData:
    """Data for the Blueprint integration."""

    client: KnxEtsApiClient
    coordinator: BlueprintDataUpdateCoordinator
    integration: Integration

"""Custom types for knx_ets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration


type KnxEtsConfigEntry = ConfigEntry[KnxEtsData]


@dataclass
class KnxEtsData:
    """Data for the KnxEts integration."""

    integration: Integration

# This file is part of Jeedom.
#
# Jeedom is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jeedom is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jeedom. If not, see <http://www.gnu.org/licenses/>.

"""Smart energy channels module for Zigbee Home Automation."""
import logging

import registries, zha_typing as zha_typing

import zigpy.zcl.clusters.smartenergy as smartenergy

from const import (
REPORT_CONFIG_DEFAULT,
TIME_MILLISECONDS,
TIME_SECONDS,
TIME_MINUTES,
TIME_HOURS,
TIME_DAYS,
TIME_WEEKS
)

@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.Calendar.cluster_id)
class Calendar():
    """Calendar channel."""
    pass


@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.DeviceManagement.cluster_id)
class DeviceManagement():
    """Device Management channel."""
    pass


@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.Drlc.cluster_id)
class Drlc():
    """Demand Response and Load Control channel."""
    pass


@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.EnergyManagement.cluster_id)
class EnergyManagement():
    """Energy Management channel."""
    pass


@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.Events.cluster_id)
class Events():
    """Event channel."""
    pass


@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.KeyEstablishment.cluster_id)
class KeyEstablishment():
    """Key Establishment channel."""
    pass


@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.MduPairing.cluster_id)
class MduPairing():
    """Pairing channel."""
    pass


@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.Messaging.cluster_id)
class Messaging():
    """Messaging channel."""
    pass


@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.Metering.cluster_id)
class Metering():
    """Metering channel."""
    REPORT_CONFIG = [{"attr": "instantaneous_demand", "config": REPORT_CONFIG_DEFAULT}]
    unit_of_measure_map = {
        0x00: "kW",
        0x01: f"m³/{TIME_HOURS}",
        0x02: f"ft³/{TIME_HOURS}",
        0x03: f"ccf/{TIME_HOURS}",
        0x04: f"US gal/{TIME_HOURS}",
        0x05: f"IMP gal/{TIME_HOURS}",
        0x06: f"BTU/{TIME_HOURS}",
        0x07: f"l/{TIME_HOURS}",
        0x08: "kPa",
        0x09: "kPa",
        0x0A: f"mcf/{TIME_HOURS}",
        0x0B: "unitless",
        0x0C: f"MJ/{TIME_SECONDS}",
    }


@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.Prepayment.cluster_id)
class Prepayment():
    """Prepayment channel."""
    pass


@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.Price.cluster_id)
class Price():
    """Price channel."""
    pass


@registries.ZIGBEE_CHANNEL_REGISTRY.register(smartenergy.Tunneling.cluster_id)
class Tunneling():
    """Tunneling channel."""
    pass

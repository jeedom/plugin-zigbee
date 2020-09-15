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

"""General channels module for Zigbee Home Automation."""
import asyncio
import logging
from typing import Any, List, Optional

import zigpy.exceptions
import zigpy.zcl.clusters.general as general

import registries, zha_typing as zha_typing
from const import (
    REPORT_CONFIG_ASAP,
    REPORT_CONFIG_BATTERY_SAVE,
    REPORT_CONFIG_DEFAULT,
    REPORT_CONFIG_IMMEDIATE,
    SIGNAL_ATTR_UPDATED,
    SIGNAL_MOVE_LEVEL,
    SIGNAL_SET_LEVEL,
    SIGNAL_STATE_ATTR,
    SIGNAL_UPDATE_DEVICE,
)


class Alarms():
    """Alarms channel."""

class AnalogInput():
    """Analog Input channel."""
    REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]

class AnalogOutput():
    """Analog Output channel."""
    REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.AnalogValue.cluster_id)
class AnalogValue():
    """Analog Value channel."""
    REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.ApplianceControl.cluster_id)
class ApplianceContorl():
    """Appliance Control channel."""

@registries.CHANNEL_ONLY_CLUSTERS.register(general.Basic.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Basic.cluster_id)
class BasicChannel():
    """Channel to interact with the basic cluster."""
    UNKNOWN = 0
    BATTERY = 3
    POWER_SOURCES = {
        UNKNOWN: "Unknown",
        1: "Mains (single phase)",
        2: "Mains (3 phase)",
        BATTERY: "Battery",
        4: "DC source",
        5: "Emergency mains constantly powered",
        6: "Emergency mains and transfer switch",
    }

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.BinaryInput.cluster_id)
class BinaryInput():
    """Binary Input channel."""
    REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.BinaryOutput.cluster_id)
class BinaryOutput():
    """Binary Output channel."""
    REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.BinaryValue.cluster_id)
class BinaryValue():
    """Binary Value channel."""
    REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Commissioning.cluster_id)
class Commissioning():
    """Commissioning channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.DeviceTemperature.cluster_id)
class DeviceTemperature():
    """Device Temperature channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.GreenPowerProxy.cluster_id)
class GreenPowerProxy():
    """Green Power Proxy channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Groups.cluster_id)
class Groups():
    """Groups channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Identify.cluster_id)
class Identify():
    """Identify channel."""

@registries.CLIENT_CHANNELS_REGISTRY.register(general.LevelControl.cluster_id)
class LevelControl():
    """LevelControl client cluster."""

@registries.BINDABLE_CLUSTERS.register(general.LevelControl.cluster_id)
@registries.LIGHT_CLUSTERS.register(general.LevelControl.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.LevelControl.cluster_id)
class LevelControlChannel():
    """Channel for the LevelControl Zigbee cluster."""
    CURRENT_LEVEL = 0
    REPORT_CONFIG = ({"attr": "current_level", "config": REPORT_CONFIG_ASAP},)


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.MultistateInput.cluster_id)
class MultistateInput():
    """Multistate Input channel."""
    REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.MultistateOutput.cluster_id)
class MultistateOutput():
    """Multistate Output channel."""
    REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.MultistateValue.cluster_id)
class MultistateValue():
    """Multistate Value channel."""
    REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.CLIENT_CHANNELS_REGISTRY.register(general.OnOff.cluster_id)
class OnOff():
    """OnOff client channel."""

@registries.BINARY_SENSOR_CLUSTERS.register(general.OnOff.cluster_id)
@registries.BINDABLE_CLUSTERS.register(general.OnOff.cluster_id)
@registries.LIGHT_CLUSTERS.register(general.OnOff.cluster_id)
@registries.SWITCH_CLUSTERS.register(general.OnOff.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.OnOff.cluster_id)
class OnOffChannel():
    """Channel for the OnOff Zigbee cluster."""
    ON_OFF = 0
    REPORT_CONFIG = ({"attr": "on_off", "config": REPORT_CONFIG_IMMEDIATE},)

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.OnOffConfiguration.cluster_id)
class OnOffConfiguration():
    """OnOff Configuration channel."""

@registries.CLIENT_CHANNELS_REGISTRY.register(general.Ota.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Ota.cluster_id)
class Ota():
    """OTA Channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Partition.cluster_id)
class Partition():
    """Partition channel."""

@registries.CHANNEL_ONLY_CLUSTERS.register(general.PollControl.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.PollControl.cluster_id)
class PollControl():
    """Poll Control channel."""
    CHECKIN_INTERVAL = 55 * 60 * 4  # 55min
    CHECKIN_FAST_POLL_TIMEOUT = 2 * 4  # 2s
    LONG_POLL = 6 * 4  # 6s

@registries.DEVICE_TRACKER_CLUSTERS.register(general.PowerConfiguration.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.PowerConfiguration.cluster_id)
class PowerConfigurationChannel():
    """Channel for the zigbee power configuration cluster."""
    REPORT_CONFIG = (
        {"attr": "battery_voltage", "config": REPORT_CONFIG_BATTERY_SAVE},
        {"attr": "battery_percentage_remaining", "config": REPORT_CONFIG_BATTERY_SAVE},
    )

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.PowerProfile.cluster_id)
class PowerProfile():
    """Power Profile channel."""

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.RSSILocation.cluster_id)
class RSSILocation():
    """RSSI Location channel."""

@registries.CLIENT_CHANNELS_REGISTRY.register(general.Scenes.cluster_id)
class Scenes():
    """Scenes channel."""

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Scenes.cluster_id)
class Scenes():
    """Scenes channel."""

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Time.cluster_id)
class Time():
    """Time channel."""

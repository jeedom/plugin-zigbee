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


"""
Security channels module for Zigbee Home Automation.
"""
import asyncio
import logging

from zigpy.exceptions import ZigbeeException
import zigpy.zcl.clusters.security as security

import registries
from const import (
    SIGNAL_ATTR_UPDATED,
    WARNING_DEVICE_MODE_EMERGENCY,
    WARNING_DEVICE_SOUND_HIGH,
    WARNING_DEVICE_SQUAWK_MODE_ARMED,
    WARNING_DEVICE_STROBE_HIGH,
    WARNING_DEVICE_STROBE_YES,
)

@registries.ZIGBEE_CHANNEL_REGISTRY.register(security.IasAce.cluster_id)
class IasAce():
    """IAS Ancillary Control Equipment channel."""

@registries.CHANNEL_ONLY_CLUSTERS.register(security.IasWd.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(security.IasWd.cluster_id)
class IasWd():
    """IAS Warning Device channel."""

@registries.BINARY_SENSOR_CLUSTERS.register(security.IasZone.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(security.IasZone.cluster_id)
class IASZoneChannel():
    """Channel for the IASZone Zigbee cluster."""

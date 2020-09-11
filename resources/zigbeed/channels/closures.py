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

"""Closures channels module for Zigbee Home Automation."""
import logging

import zigpy.zcl.clusters.closures as closures

import registries
from const import REPORT_CONFIG_IMMEDIATE, SIGNAL_ATTR_UPDATED

@registries.ZIGBEE_CHANNEL_REGISTRY.register(closures.DoorLock.cluster_id)
class DoorLockChannel():
    """Door lock channel."""

    _value_attribute = 0
    REPORT_CONFIG = ({"attr": "lock_state", "config": REPORT_CONFIG_IMMEDIATE},)

    async def async_update(self):
        """Retrieve latest state."""
        result = await self.get_attribute_value("lock_state", from_cache=True)
        if result is not None:
            self.async_send_signal(f"{self.unique_id}_{SIGNAL_ATTR_UPDATED}", 0, "lock_state", result)

    def attribute_updated(self, attrid, value):
        """Handle attribute update from lock cluster."""
        attr_name = self.cluster.attributes.get(attrid, [attrid])[0]
        self.debug("Attribute report '%s'[%s] = %s", self.cluster.name, attr_name, value)
        if attrid == self._value_attribute:
            self.async_send_signal(f"{self.unique_id}_{SIGNAL_ATTR_UPDATED}", attrid, attr_name, value)

    async def async_initialize(self, from_cache):
        """Initialize channel."""
        await self.get_attribute_value(self._value_attribute, from_cache=from_cache)
        await super().async_initialize(from_cache)


@registries.ZIGBEE_CHANNEL_REGISTRY.register(closures.Shade.cluster_id)
class Shade():
    """Shade channel."""


@registries.CLIENT_CHANNELS_REGISTRY.register(closures.WindowCovering.cluster_id)
class WindowCoveringClient():
    """Window client channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(closures.WindowCovering.cluster_id)
class WindowCovering():
    """Window channel."""

    _value_attribute = 8
    REPORT_CONFIG = ({"attr": "current_position_lift_percentage", "config": REPORT_CONFIG_IMMEDIATE},)

    async def async_update(self):
        """Retrieve latest state."""
        result = await self.get_attribute_value("current_position_lift_percentage", from_cache=False)
        self.debug("read current position: %s", result)
        if result is not None:
            self.async_send_signal(f"{self.unique_id}_{SIGNAL_ATTR_UPDATED}",8,"current_position_lift_percentage",result,)

    def attribute_updated(self, attrid, value):
        """Handle attribute update from window_covering cluster."""
        attr_name = self.cluster.attributes.get(attrid, [attrid])[0]
        self.debug("Attribute report '%s'[%s] = %s", self.cluster.name, attr_name, value)
        if attrid == self._value_attribute:
            self.async_send_signal(f"{self.unique_id}_{SIGNAL_ATTR_UPDATED}", attrid, attr_name, value)

    async def async_initialize(self, from_cache):
        """Initialize channel."""
        await self.get_attribute_value(self._value_attribute, from_cache=from_cache)
        await super().async_initialize(from_cache)

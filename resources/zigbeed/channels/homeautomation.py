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


"""Home automation channels module for Zigbee Home Automation."""
import logging
from typing import Optional

import zigpy.zcl.clusters.homeautomation as homeautomation

import registries
from const import (
    CHANNEL_ELECTRICAL_MEASUREMENT,
    REPORT_CONFIG_DEFAULT,
    SIGNAL_ATTR_UPDATED,
) 

@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.ApplianceEventAlerts.cluster_id)
class ApplianceEventAlerts():
    """Appliance Event Alerts channel."""

@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.ApplianceIdentification.cluster_id)
class ApplianceIdentification():
    """Appliance Identification channel."""

@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.ApplianceStatistics.cluster_id)
class ApplianceStatistics():
    """Appliance Statistics channel."""

@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.Diagnostic.cluster_id)
class Diagnostic():
    """Diagnostic channel."""

@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.ElectricalMeasurement.cluster_id)
class ElectricalMeasurementChannel():
    """Channel that polls active power level."""
    CHANNEL_NAME = CHANNEL_ELECTRICAL_MEASUREMENT
    REPORT_CONFIG = ({"attr": "active_power", "config": REPORT_CONFIG_DEFAULT},)

    async def async_update(self):
        """Retrieve latest state."""
        self.debug("async_update")

        # This is a polling channel. Don't allow cache.
        result = await self.get_attribute_value("active_power", from_cache=False)
        if result is not None:
            self.async_send_signal(f"{self.unique_id}_{SIGNAL_ATTR_UPDATED}",0x050B,"active_power",result,)

    async def async_initialize(self, from_cache):
        """Initialize channel."""
        await self.fetch_config(True)
        await super().async_initialize(from_cache)

    async def fetch_config(self, from_cache):
        """Fetch config from device and updates format specifier."""
        # prime the cache
        await self.get_attributes(["ac_power_divisor","power_divisor","ac_power_multiplier","power_multiplier",],from_cache=from_cache,)

    @property
    def divisor(self) -> Optional[int]:
        """Return active power divisor."""
        return self.cluster.get("ac_power_divisor", self.cluster.get("power_divisor", 1))

    @property
    def multiplier(self) -> Optional[int]:
        """Return active power divisor."""
        return self.cluster.get("ac_power_multiplier", self.cluster.get("power_multiplier", 1))


@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.MeterIdentification.cluster_id)
class MeterIdentification():
    """Metering Identification channel."""

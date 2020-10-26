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
import shared
import utils

@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.ApplianceEventAlerts.cluster_id)
class ApplianceEventAlerts():
	"""Appliance Event Alerts channel."""

	NO_BINDING=True

@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.ApplianceIdentification.cluster_id)
class ApplianceIdentification():
	"""Appliance Identification channel."""

	NO_BINDING=True

@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.ApplianceStatistics.cluster_id)
class ApplianceStatistics():
	"""Appliance Statistics channel."""

	NO_BINDING=True

@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.Diagnostic.cluster_id)
class Diagnostic():
	"""Diagnostic channel."""

	NO_BINDING=True

@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.ElectricalMeasurement.cluster_id)
class ElectricalMeasurementChannel():
	"""Channel that polls active power level."""
	CHANNEL_NAME = CHANNEL_ELECTRICAL_MEASUREMENT
	REPORT_CONFIG = ({"attr": "active_power", "config": REPORT_CONFIG_DEFAULT},)

@registries.ZIGBEE_CHANNEL_REGISTRY.register(homeautomation.MeterIdentification.cluster_id)
class MeterIdentification():
	"""Metering Identification channel."""

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

"""Manufacturer specific channels module for Zigbee Home Automation."""
import logging

import registries
from const import (
	ATTR_ATTRIBUTE_ID,
	ATTR_ATTRIBUTE_NAME,
	ATTR_VALUE,
	REPORT_CONFIG_ASAP,
	REPORT_CONFIG_MAX_INT,
	REPORT_CONFIG_MIN_INT,
	SIGNAL_ATTR_UPDATED,
	UNKNOWN,
)
import shared
import utils

@registries.ZIGBEE_CHANNEL_REGISTRY.register(registries.SMARTTHINGS_HUMIDITY_CLUSTER)
class SmartThingsHumidity():
	"""Smart Things Humidity channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]


@registries.CHANNEL_ONLY_CLUSTERS.register(0xFD00)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(0xFD00)
class OsramButton():
	"""Osram button channel."""
	REPORT_CONFIG = []


@registries.CHANNEL_ONLY_CLUSTERS.register(registries.PHILLIPS_REMOTE_CLUSTER)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(registries.PHILLIPS_REMOTE_CLUSTER)
class PhillipsRemote():
	"""Phillips remote channel."""
	REPORT_CONFIG = []


@registries.CHANNEL_ONLY_CLUSTERS.register(0xFCC0)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(0xFCC0)
class OppleRemote():
	"""Opple button channel."""
	REPORT_CONFIG = []

#@registries.ZIGBEE_CHANNEL_REGISTRY.register(registries.SMARTTHINGS_ACCELERATION_CLUSTER)
#class SmartThingsAcceleration():
#	"""Smart Things Acceleration channel."""
#
#	REPORT_CONFIG = [
#		{"attr": "acceleration", "config": REPORT_CONFIG_ASAP},
#		{"attr": "x_axis", "config": REPORT_CONFIG_ASAP},
#		{"attr": "y_axis", "config": REPORT_CONFIG_ASAP},
#		{"attr": "z_axis", "config": REPORT_CONFIG_ASAP},
#	]

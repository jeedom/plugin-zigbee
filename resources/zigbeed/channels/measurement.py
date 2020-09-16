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

"""Measurement channels module for Zigbee Home Automation."""
import logging
import zigpy.zcl.clusters.measurement as measurement

import registries
from const import (
	REPORT_CONFIG_DEFAULT,
	REPORT_CONFIG_IMMEDIATE,
	REPORT_CONFIG_MAX_INT,
	REPORT_CONFIG_MIN_INT,
)
import shared
import utils

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.FlowMeasurement.cluster_id)
class FlowMeasurement():
	"""Flow Measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value", "config": REPORT_CONFIG_DEFAULT}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.IlluminanceLevelSensing.cluster_id)
class IlluminanceLevelSensing():
	"""Illuminance Level Sensing channel."""
	REPORT_CONFIG = [{"attr": "level_status", "config": REPORT_CONFIG_DEFAULT}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.IlluminanceMeasurement.cluster_id)
class IlluminanceMeasurement():
	"""Illuminance Measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value", "config": REPORT_CONFIG_DEFAULT}]

@registries.BINARY_SENSOR_CLUSTERS.register(measurement.OccupancySensing.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.OccupancySensing.cluster_id)
class OccupancySensing():
	"""Occupancy Sensing channel."""
	REPORT_CONFIG = [{"attr": "occupancy", "config": REPORT_CONFIG_IMMEDIATE}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.PressureMeasurement.cluster_id)
class PressureMeasurement():
	"""Pressure measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value", "config": REPORT_CONFIG_DEFAULT}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.RelativeHumidity.cluster_id)
class RelativeHumidity():
	"""Relative Humidity measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.TemperatureMeasurement.cluster_id)
class TemperatureMeasurement():
	"""Temperature measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

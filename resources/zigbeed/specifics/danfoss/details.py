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

import logging
from zigpy.zcl.clusters.hvac import Thermostat
from zigpy.quirks import CustomCluster
import zigpy.types as types

REPORTING_SPECIFIC = {"0x0200" :
						{Thermostat.cluster_id:
							{1:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							2:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							3:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							4:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							5:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							6:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							7:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							8:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							9:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							10:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							11:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							12:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							13:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							14:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
							15:[{"attr":"output_status","min":1,"max":65534,"report": 1}]
							}
						}
					}

DANFOSS_WINDOWS_DETECTION = 0x4000
DANFOSS_EXTERNAL_OPEN_WINDOWS_DETECTION = 0x4003
DANFOSS_ORIENTATION = 0x4014
DANFOSS_ROOM_STATUS_CODE = 0x4100
DANFOSS_OUTPUT_STATUS = 0x4110
DANFOSS_ROOM_FLOOR_SENSOR_MODE = 0x4120
DANFOSS_FLOOR_MIN_SETPOINT = 0x4121
DANFOSS_FLOOR_MAX_SETPOINT = 0x4122
DANFOSS_SCHEDULED_TYPE_USED = 0x4130

DANFOSS_THERMOSTAT_MANUFACTURER_ATTRIBUTES = {
		DANFOSS_WINDOWS_DETECTION: ("etrv_open_windows_detection", types.enum8),
		DANFOSS_EXTERNAL_OPEN_WINDOWS_DETECTION: ("external_open_windows_detected", types.Bool),
		DANFOSS_ORIENTATION: ("orientation", types.Bool),
		DANFOSS_ROOM_STATUS_CODE: ("room_status_code", types.uint16_t),
		DANFOSS_OUTPUT_STATUS: ("output_status", types.int8s),
		DANFOSS_ROOM_FLOOR_SENSOR_MODE: ("room_floor_sensor_mode", types.int8s),
		DANFOSS_FLOOR_MIN_SETPOINT: ("floor_min_setpoint", types.int16s),
		DANFOSS_FLOOR_MAX_SETPOINT: ("floor_max_setpoint", types.int16s),
		DANFOSS_SCHEDULED_TYPE_USED: ("scheduled_type_used", types.int8s),
	}

class JeedomDanfossThermostatCluster(CustomCluster, Thermostat):
	"""Danfoss Thermostat cluster."""
	manufacturer_attributes = DANFOSS_THERMOSTAT_MANUFACTURER_ATTRIBUTES








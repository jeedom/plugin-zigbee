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
							{1:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							2:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							3:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							4:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							5:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							6:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							7:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							8:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							9:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							10:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							11:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							12:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							13:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							14:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}],
							15:[{"attr":"output_status","min":1,"max":65534,"report": 1},{"attr":"floor_min_setpoint","min":1,"max":65534,"report": 1},{"attr":"floor_max_setpoint","min":1,"max":65534,"report": 1},{"attr":"scheduled_type_used","min":1,"max":65534,"report": 1},{"attr":"room_status_code","min":1,"max":65534,"report": 1},{"attr":"room_floor_sensor_mode","min":1,"max":65534,"report": 1}]
							}
						},
					"eTRV0100" :
						{Thermostat.cluster_id:
							{1:[{"attr":"etrv_open_windows_detection","min":0,"max":4,"report": 1}],
							}
						}
					}

DANFOSS_THERMOSTAT_MANUFACTURER_ATTRIBUTES = {
		0x4000: ("etrv_open_windows_detection", types.enum8),
		0x4003: ("external_open_windows_detected", types.Bool),
		0x4014: ("orientation", types.Bool),
		0x4100: ("room_status_code", types.uint16_t),
		0x4110: ("output_status", types.int8s),
		0x4120: ("room_floor_sensor_mode", types.int8s),
		0x4121: ("floor_min_setpoint", types.int16s),
		0x4122: ("floor_max_setpoint", types.int16s),
		0x4130: ("scheduled_type_used", types.int8s),
	}

class JeedomDanfossThermostatCluster(CustomCluster, Thermostat):
	"""Danfoss Thermostat cluster."""
	attributes = dict(list(Thermostat.attributes.items()) + list(DANFOSS_THERMOSTAT_MANUFACTURER_ATTRIBUTES.items()))
	
	
DANFOSS_VALVE_MANUFACTURER_ATTRIBUTES = {
		0x4000: ("etrv_open_windows_detection", types.enum8),
		0x4003: ("external_open_windows_detected", types.Bool),
		0x4010: ("exercise_day_of_week", types.enum8),
		0x4011: ("exercise_trigger_time", types.uint16_t),
		0x4012: ("mounting_mode_active", types.Bool),
		0x4013: ("mounting_mode_control", types.Bool),
		0x4014: ("orientation", types.Bool),
		0x4015: ("external_measured_room_sensor", types.int16s),
		0x4016: ("radiator_overed", types.Bool),
		0x4020: ("control_algorithm_scale_factor", types.uint8_t),
		0x4030: ("heat_available", types.Bool),
		0x4031: ("heat_supply_request", types.Bool),
		0x4032: ("load_balancing_enable", types.Bool),
		0x4051: ("window_open_feature", types.Bool),
		0x404A: ("load_estimate_radiator", types.uint16_t),
		0x404B: ("regulation_setPoint_offset", types.int8s),
		0x404C: ("adaptation_run_control", types.enum8),
		0x404D: ("adaptation_run_status", types.bitmap8),
		0x404E: ("adaptation_run_settings", types.bitmap8),
		0xFFFD: ("cluster_revision", types.uint16_t),
	}
	
class JeedomDanfossValveCluster(CustomCluster, Thermostat):
	"""Danfoss Thermostat cluster."""
	attributes = dict(list(Thermostat.attributes.items()) + list(DANFOSS_VALVE_MANUFACTURER_ATTRIBUTES.items()))









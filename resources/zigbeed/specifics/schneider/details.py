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
from zigpy.zcl.clusters.general import Basic
from zigpy.zcl.clusters.smartenergy import Metering
from zigpy.zcl.clusters.hvac import Thermostat 
from zigpy.quirks import CustomCluster
import zigpy.types as types

REPORTING_SPECIFIC = {
	'CCTFR6700' :{
		Metering.cluster_id:{
			2:[
				{"attr":"current_summ_delivered","min":60,"max":60,"report": 1},
			 	{"attr":"instantaneous_demand","min":60,"max":60,"report": 1}
			]
		},
		Thermostat.cluster_id:{
			1:[	{"attr":"occupied_heating_setpoint","min":60,"max":60,"report": 1}]
		}
	}
}


class SchneiderBasicCluster(CustomCluster, Basic):
	"""Schneider basics cluster."""
	attributes = {
		0xE007: ("tb0", types.enum16),
		0xE009: ("tb1", types.CharacterString)
	}

class SchneiderPilotModeCluster(CustomCluster):
	"""Schneider Pilot mode cluster."""
	cluster_id = 0xFF23
	name = "Schneider Pilot Mode"
	ep_attribute = "pilot_mode"
	attributes = {
		0x0031: ("controller_pilot_mode", types.enum8)
	}
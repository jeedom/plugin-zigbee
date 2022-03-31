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
from zigpy.quirks import CustomCluster
import zigpy.types as types

REPORTING_SPECIFIC = {" Dimmer switch w/o neutral" :
						{64513:
							{38:[{"attr":"measured_value","min":60,"max":600,"report": 10}]
							}
						}
					},{" Dimmer switch with neutral" :
						{64513:
							{38:[{"attr":"measured_value","min":60,"max":600,"report": 10}]
							}
						}
					}	

class JeedomLegrandCluster(CustomCluster):
	cluster_id = 64513
	name = "Jeedom - Legrand Settings"
	ep_attribute = "legrand_cluster"
	attributes = {
      	0x0000: ("dimmer", types.data16),
        0x0001: ("led_dark", types.Bool),
        0x0002: ("led_on", types.Bool),
	}
    
class LegrandPilotModeCluster(CustomCluster):
	"""Legrand Pilot mode cluster."""
	cluster_id = 0xfc40
	name = "Legrand Pilot Mode"
	ep_attribute = "pilot_mode"
	attributes = {
		0x0000: ("pilot_mode", types.enum8)
	}
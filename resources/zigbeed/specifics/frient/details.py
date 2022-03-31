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

REPORTING_SPECIFIC = {"AQSZB-110" :
						{64515:
							{38:[{"attr":"measured_value","min":60,"max":600,"report": 10}]
							}
						}
					}

class JeedomFrientVOCCluster(CustomCluster):
	cluster_id = 64515
	name = "Jeedom - Frient Voc Measurement"
	ep_attribute = "voc"
	attributes = {
		0x0000: ("measured_value", types.uint16_t),
		0x0001: ("min_measured_value", types.uint16_t),
		0x0002: ("max_measured_value", types.uint16_t),
		0x0003: ("resolution", types.uint16_t),
	}








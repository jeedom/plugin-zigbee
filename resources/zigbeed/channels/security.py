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


"""
Security channels module for Zigbee Home Automation.
"""
import asyncio
import logging
import zigpy

from zigpy.exceptions import ZigbeeException
import zigpy.zcl.clusters.security as security

import registries
from const import (
	SIGNAL_ATTR_UPDATED,
	WARNING_DEVICE_MODE_EMERGENCY,
	WARNING_DEVICE_SOUND_HIGH,
	WARNING_DEVICE_SQUAWK_MODE_ARMED,
	WARNING_DEVICE_STROBE_HIGH,
	WARNING_DEVICE_STROBE_YES,
)
import shared
import utils
import traceback

@registries.ZIGBEE_CHANNEL_REGISTRY.register(security.IasAce.cluster_id)
class IasAce():
	"""IAS Ancillary Control Equipment channel."""

@registries.CHANNEL_ONLY_CLUSTERS.register(security.IasWd.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(security.IasWd.cluster_id)
class IasWd():
	"""IAS Warning Device channel."""

@registries.BINARY_SENSOR_CLUSTERS.register(security.IasZone.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(security.IasZone.cluster_id)
class IASZoneChannel():
	"""Channel for the IASZone Zigbee cluster."""

	async def initialize(cluster):
		ieee = cluster.endpoint.device.application.ieee
		logging.debug("["+str(ieee)+"][chanels.security.IASZoneChannel.initialize] Started IASZoneChannel specific configuration")
		try:
			res = await cluster.write_attributes({"cie_addr": ieee})
			logging.debug("["+str(ieee)+"][chanels.security.IASZoneChannel.initialize] Wrote cie_addr: %s to '%s' cluster: %s",str(ieee),cluster.ep_attribute,res[0],)
		except ZigbeeException as ex:
			logging.debug("["+str(ieee)+"][chanels.security.IASZoneChannel.initialize] Failed to write cie_addr: %s to '%s' cluster: %s",str(ieee),cluster.ep_attribute,str(ex),)
		logging.debug("["+str(ieee)+"][chanels.security.IASZoneChannel.initialize] Finished IASZoneChannel configuration")

	def cluster_command(cluster, command_id, *args):
		try:
			if command_id == 1:
				logging.debug("["+str(cluster.endpoint.device._ieee)+"][chanels.security.IASZoneChannel.cluster_command] Enroll requested")
				asyncio.ensure_future(cluster.enroll_response(0, 0))
			else:
				changes = {'devices' : {str(cluster.endpoint.device._ieee) : {str(cluster.endpoint._endpoint_id) : {str(cluster.cluster_id) : {'cmd' : {}}}}}}
				nb = 0
				for i in args :
					if hasattr(i, "__len__"):
						if len(i) == 0:
							continue
						i = i[0]
					changes['devices'][str(cluster.endpoint.device._ieee)][str(cluster.endpoint._endpoint_id)][str(cluster.cluster_id)]['cmd'][nb] = {"value" : str(i),"cluster_name" : cluster.name}
					nb += 1
				shared.JEEDOM_COM.send_change_immediate(changes);
				return True
		except Exception as e:
			logging.error(traceback.format_exc())

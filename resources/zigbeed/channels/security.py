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


	def set_bit(destination_value, destination_bit, source_value, source_bit):
		"""Set the specified bit in the value."""
		if IasWd.get_bit(source_value, source_bit):
			return destination_value | (1 << destination_bit)
		return destination_value

	def get_bit(value, bit):
		"""Get the specified bit from the value."""
		return (value & (1 << bit)) != 0

	async def start_warning(cluster,cmd):
		value = 0
		value = IasWd.set_bit(value, 0, int(cmd['args'][2]), 0) # mode
		value = IasWd.set_bit(value, 1, int(cmd['args'][2]), 1)
		value = IasWd.set_bit(value, 2, int(cmd['args'][1]), 0) # strobe
		value = IasWd.set_bit(value, 4, int(cmd['args'][0]), 0) # level
		value = IasWd.set_bit(value, 5, int(cmd['args'][0]), 1)
		value = IasWd.set_bit(value, 6, int(cmd['args'][0]), 2)
		value = IasWd.set_bit(value, 7, int(cmd['args'][0]), 3)
		await cluster.start_warning(value, int(cmd['args'][3]), int(cmd['args'][4]), int(cmd['args'][5]))

	async def squawk(cluster,cmd):
		value = 0
		value = IasWd.set_bit(value, 0, int(cmd['args'][2]), 0) # mode
		value = IasWd.set_bit(value, 1, int(cmd['args'][2]), 1)
		value = IasWd.set_bit(value, 3, int(cmd['args'][1]), 0) # strobe
		value = IasWd.set_bit(value, 4, int(cmd['args'][0]), 0) # level
		value = IasWd.set_bit(value, 5, int(cmd['args'][0]), 1)
		value = IasWd.set_bit(value, 6, int(cmd['args'][0]), 2)
		value = IasWd.set_bit(value, 7, int(cmd['args'][0]), 3)
		await cluster.squawk(value)

@registries.BINARY_SENSOR_CLUSTERS.register(security.IasZone.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(security.IasZone.cluster_id)
class IASZoneChannel():
	"""Channel for the IASZone Zigbee cluster."""

	async def initialize(cluster):
		ieee = cluster.endpoint.device.application.ieee
		logging.info("["+str(cluster.endpoint.device._ieee)+"][chanels.security.IASZoneChannel.initialize] Started IASZoneChannel specific configuration")
		try:
			res = await cluster.write_attributes({"cie_addr": ieee})
			logging.info("["+str(cluster.endpoint.device._ieee)+"][chanels.security.IASZoneChannel.initialize] Wrote cie_addr: %s to '%s' cluster: %s",str(ieee),cluster.ep_attribute,res[0],)
		except ZigbeeException as ex:
			logging.info("["+str(cluster.endpoint.device._ieee)+"][chanels.security.IASZoneChannel.initialize] Failed to write cie_addr: %s to '%s' cluster: %s",str(ieee),cluster.ep_attribute,str(ex),)
		logging.info("["+str(cluster.endpoint.device._ieee)+"][chanels.security.IASZoneChannel.initialize] Finished IASZoneChannel configuration")

	def cluster_command(cluster, tsn, *args):
		try:
			if args[0] == 1:
				logging.info("["+str(cluster.endpoint.device._ieee)+"][chanels.security.IASZoneChannel.cluster_command] Enroll requested")
				asyncio.ensure_future(cluster.enroll_response(0, 0))
				return True
			changes = {'devices' : {str(cluster.endpoint.device._ieee) : {str(cluster.endpoint._endpoint_id) : {str(cluster.cluster_id) : {'cmd' : {}}}}}}
			nb = 0
			for i in args :
				if hasattr(i, "__len__"):
					if len(i) == 0:
						continue
					nb2 = 0
					for j in i :
						key = nb
						if nb2 > 0:
							key = str(nb)+'.'+str(nb2)
						changes['devices'][str(cluster.endpoint.device._ieee)][str(cluster.endpoint._endpoint_id)][str(cluster.cluster_id)]['cmd'][key] = {"value" : str(j),"cluster_name" : cluster.name}
						nb2 += 1
				nb += 1
			shared.JEEDOM_COM.send_change_immediate(changes);
			return True
		except Exception as e:
			logging.error(traceback.format_exc())

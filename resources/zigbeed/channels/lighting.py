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

"""Lighting channels module for Zigbee Home Automation."""
import logging

import zigpy.zcl.clusters.lighting as lighting

import registries
from const import REPORT_CONFIG_DEFAULT
import shared
import utils

@registries.ZIGBEE_CHANNEL_REGISTRY.register(lighting.Ballast.cluster_id)
class Ballast():
	"""Ballast channel."""

@registries.CLIENT_CHANNELS_REGISTRY.register(lighting.Color.cluster_id)
class Color():
	"""Color client channel."""

@registries.BINDABLE_CLUSTERS.register(lighting.Color.cluster_id)
@registries.LIGHT_CLUSTERS.register(lighting.Color.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(lighting.Color.cluster_id)
class ColorChannel():
	"""Color channel."""

	CAPABILITIES_COLOR_XY = 0x08
	CAPABILITIES_COLOR_TEMP = 0x10
	UNSUPPORTED_ATTRIBUTE = 0x86
	REPORT_CONFIG = (
		{"attr": "current_x", "config": REPORT_CONFIG_DEFAULT},
		{"attr": "current_y", "config": REPORT_CONFIG_DEFAULT},
		{"attr": "color_temperature", "config": REPORT_CONFIG_DEFAULT},
	)
    
	

	async def color_loop_stop(cluster,cmd):
		await cluster.color_loop_set(0x1,0,0,0,0)

	async def color_loop_start(cluster,cmd):
		await cluster.color_loop_set(0x1,0x2,0x1,7,0)

	def attribute_updated(cluster, attribute_id, value):
		logging.info("["+str(cluster.endpoint.device._ieee)+"][channel.lighting.ColorChannel.attribute_updated] Attribut : "+str(attribute_id)+", value : "+str(value))
		if attribute_id != 3 and attribute_id != 4:
			return None
		if 3 in shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id] and 4 in shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id]:
			x_point = shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id][3]/65535
			y_point = shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id][4]/65535
			if y_point == 0:
				return True
			Y = 255
			if 8 in shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id] and 0 in shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][8]:
				Y = shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][8][0]
			logging.info("["+str(cluster.endpoint.device._ieee)+"][channel.lighting.ColorChannel.attribute_updated] Convertion to rgb  x_point : "+str(x_point)+", y_point : "+str(y_point)+", Y : "+str(Y))
			shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::color',{"value" : utils.convert_xy_to_rgb(x_point,y_point,Y),"cluster_name" : cluster.name})
			shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id] = {}
		return True

	def cluster_command(cluster, tsn, *args):
		logging.info("["+str(cluster.endpoint.device._ieee)+"][channel.lighting.ColorChannel.cluster_command] Args : "+str(args))
		if args[0] == 7 :
			shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::cmd::color',{"value" : utils.convert_xy_to_rgb(int(args[1][0]),int(args[1][1])),"cluster_name" : cluster.name})
		if args[0] == 10 :
			shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::cmd::colorTemperature',{"value" : args[1][0],"cluster_name" : cluster.name})
		return True

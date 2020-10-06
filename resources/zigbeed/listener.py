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
import shared,utils
import traceback
import registries
import asyncio
import zdevices
import time

class Listener:
	"""
	Contains callbacks that zigpy will call whenever something happens.	Look for `listener_event` in the Zigpy source or just look at the logged warnings.
	"""

	def __init__(self, application):
		self.application = application

	def unknown_cluster_message(self, cmd_id,*args):
		logging.info("************************* Unknown cluster message : %s" %(cmd_id))

	def device_joined(self, device):
		logging.info("************************* Device joined : %s" %(device))
		shared.JEEDOM_COM.send_change_immediate({'device_joined' : str(device._ieee)});

	def device_announce(self, device):
		logging.info("****************** device_announce Zigpy Device: %s" %(device))

	def device_removed(self, device):
		logging.info("****************** device_removed Zigpy Device: %s" %(device))
		shared.JEEDOM_COM.send_change_immediate({'device_removed' : str(device._ieee)});

	def device_left(self, device):
		logging.info("****************** device_left Zigpy Device: %s" %(device))
		shared.JEEDOM_COM.send_change_immediate({'device_left' : str(device._ieee)});

	def device_initialized(self, device, *, new=True):
		"""
		Called at runtime after a device's information has been queried.I also call it on startup to load existing devices from the DB.
		"""
		logging.info("******************** Device is ready: new=%s, device=%s", new, device._ieee)
		for ep_id, endpoint in device.endpoints.items():
			if ep_id == 0: # Ignore ZDO
				continue
			for cluster in endpoint.in_clusters.values(): # You need to attach a listener to every cluster to receive events
				cluster.add_context_listener(self) # The context listener passes its own object as the first argument to the callback
			for cluster in endpoint.out_clusters.values(): # You need to attach a listener to every cluster to receive events
				cluster.add_context_listener(self) # The context listener passes its own object as the first argument to the callback
		if new:
			time.sleep(5)
			asyncio.ensure_future(zdevices.initialize(device))
			shared.JEEDOM_COM.send_change_immediate({'device_initialized' : str(device._ieee)});

	def cluster_command(self, cluster, command_id, *args):
		try:
			logging.info("****************** cluster_command - Cluster: %s ClusterId: 0x%04x command_id: %s args: %s" %(cluster, cluster.cluster_id, command_id, args))
			utils.initSharedDeviceData(cluster,'cmd')
			shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id]['cmd'] = args
			if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'cluster_command'):
				logging.info("Use specific decode funtion")
				if registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].cluster_command(cluster, command_id, *args) is not None:
					return
			nb = 0
			for i in args :
				if hasattr(i, "__len__"):
					if len(i) == 0:
						continue
					i = i[0]
				infos = {"value" : str(i),"cluster_name" : cluster.name}
				shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::cmd::'+str(nb),infos)
				nb += 1
		except Exception as e:
			logging.error(traceback.format_exc())


	def device_announce(self, cluster, command_id, *args):
		device = cluster.endpoint.device
		logging.info("****************** device_announce - Cluster: %s ClusterId: 0x%04x command_id: %s args: %s" %(cluster, cluster.cluster_id, command_id, args))

	def general_command(self, cluster, command_id, *args):
		device = cluster.endpoint.device
		logging.info("****************** general_command - Cluster: %s ClusterId: 0x%04x command_id: %s args: %s" %(cluster, cluster.cluster_id, command_id, args))
		nb1=0
		nb2=0
		for i in args[0]:
			for j in i:
				if not hasattr(j,'attrid') or j.attrid == 0:
					continue;
				infos = {"value" : str(j.value.value),"cluster_name" : cluster.name}
				shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::gcmd::'+str(j.attrid)+'-'+str(nb1)+'-'+str(nb2),infos)
				nb2+=1
			nb1+=1


	def attribute_updated(self, cluster, attribute_id, value):
		try:
			logging.info("****************** Received an attribute update %s=%s on cluster %s from device %s",attribute_id, value, cluster.cluster_id, cluster.endpoint.device._ieee)
			utils.initSharedDeviceData(cluster,attribute_id)
			shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id][attribute_id] = value
			if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'attribute_updated'):
				if registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].attribute_updated(cluster, attribute_id, value) is not None:
					return
			shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::'+str(attribute_id),{"value" : str(value),"cluster_name" : cluster.name})
		except Exception as e:
			logging.error(traceback.format_exc())

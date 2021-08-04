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
import specifics
import zgp
import zigpy

class Listener:
	"""
	Contains callbacks that zigpy will call whenever something happens.	Look for `listener_event` in the Zigpy source or just look at the logged warnings.
	"""

	def __init__(self, application):
		self.application = application

	def unknown_cluster_message(self, cmd_id,*args):
		logging.info("[listener.unknown_cluster_message] %s" %(cmd_id))

	def device_joined(self, device):
		logging.info("["+str(device._ieee)+"][listener.device_joined]")
		shared.JEEDOM_COM.send_change_immediate({'device_joined' : str(device._ieee)});

	def device_announce(self, device):
		logging.info("["+str(device._ieee)+"][listener.device_announce]")

	def device_removed(self, device):
		logging.info("["+str(device._ieee)+"][listener.device_removed]")
		shared.JEEDOM_COM.send_change_immediate({'device_removed' : str(device._ieee)});

	def device_left(self, device):
		logging.info("["+str(device._ieee)+"][listener.device_left]")
		shared.JEEDOM_COM.send_change_immediate({'device_left' : str(device._ieee)});

	def device_initialized(self, device, *, new=True):
		"""
		Called at runtime after a device's information has been queried.I also call it on startup to load existing devices from the DB.
		"""
		specifics.init(device)
		logging.info("["+str(device._ieee)+"][listener.device_initialized] new=%s", new)
		for ep_id, endpoint in device.endpoints.items():
			if ep_id == 0: # Ignore ZDO
				continue
			for cluster in endpoint.in_clusters.values(): # You need to attach a listener to every cluster to receive events
				cluster.add_context_listener(self) # The context listener passes its own object as the first argument to the callback
			for cluster in endpoint.out_clusters.values(): # You need to attach a listener to every cluster to receive events
				cluster.add_context_listener(self) # The context listener passes its own object as the first argument to the callback
		if new:
			asyncio.ensure_future(zdevices.initialize(device))
			shared.JEEDOM_COM.send_change_immediate({'device_initialized' : str(device._ieee)});

	def cluster_command(self, cluster, tsn, *args):
		logging.info("["+str(cluster.endpoint.device._ieee)+"][listener.cluster_command] Cluster: %s ClusterId: 0x%04x tsn: %s args: %s" %(cluster, cluster.cluster_id, tsn, args))
		try:
			utils.initSharedDeviceData(cluster,'cmd')
			if 'tsn' in shared.DEVICES_DATA[cluster.endpoint.device._ieee] and shared.DEVICES_DATA[cluster.endpoint.device._ieee]['tsn'] == tsn:
				logging.info("["+str(cluster.endpoint.device._ieee)+"][listener.cluster_command] Ignoring already received this command last tsn="+str(shared.DEVICES_DATA[cluster.endpoint.device._ieee]['tsn'])+" received "+str(tsn))
				return
			shared.DEVICES_DATA[cluster.endpoint.device._ieee]['tsn'] = tsn
			shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id]['cmd'] = args
			if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'cluster_command'):
				logging.info("["+str(cluster.endpoint.device._ieee)+"][listener.cluster_command] Use specific decode funtion of cluster id "+str(cluster.cluster_id))
				if registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].cluster_command(cluster, tsn, *args) is not None:
					return
			changes = {'devices' : {str(cluster.endpoint.device._ieee) : {str(cluster.endpoint._endpoint_id) : {str(cluster.cluster_id) : {'cmd' : {}}}}}}
			nb = 0
			for i in args :
				if hasattr(i, "__len__") and len(i) != 0:
					nb2 = 0
					for j in i :
						key = nb
						if nb2 > 0:
							key = str(nb)+'.'+str(nb2)
						shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::cmd::'+str(key),{"value" : str(j),"cluster_name" : cluster.name})
						nb2 += 1
				else:
					shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::cmd::'+str(nb),{"value" : str(i),"cluster_name" : cluster.name})
				nb += 1
		except Exception as e:
			logging.error(traceback.format_exc())

	def device_announce(self, cluster, command_id, *args):
		device = cluster.endpoint.device
		logging.info("["+str(device._ieee)+"][listener.device_announce] Cluster: %s cluster_id: 0x%04x command_id: %s args: %s" %(cluster, cluster.cluster_id, command_id, args))

	def general_command(self, cluster, command_id, *args):
		device = cluster.endpoint.device
		logging.info("["+str(device._ieee)+"][listener.general_command] Cluster: %s cluster_id: 0x%04x command_id: %s args: %s" %(cluster, cluster.cluster_id, command_id, args))
		if cluster.endpoint.device._ieee not in shared.DEVICES_DATA:
			shared.DEVICES_DATA[cluster.endpoint.device._ieee] = {}
		if 'tsn' in shared.DEVICES_DATA[cluster.endpoint.device._ieee] and shared.DEVICES_DATA[cluster.endpoint.device._ieee]['tsn'] == command_id.tsn:
			logging.info("["+str(cluster.endpoint.device._ieee)+"][listener.general_command] Ignoring already received this command last tsn="+str(shared.DEVICES_DATA[cluster.endpoint.device._ieee]['tsn'])+" received "+str(command_id.tsn))
			return
		shared.DEVICES_DATA[cluster.endpoint.device._ieee]['tsn'] = command_id.tsn
		nb1=0
		nb2=0
		for i in args[0]:
			if not hasattr(i, "__len__") or len(i) != 0:
				continue
			for j in i:
				if not hasattr(j,'attrid') or j.attrid == 0 or not hasattr(j,'value') :
					continue;
				infos = {"value" : str(j.value.value),"cluster_name" : cluster.name}
				shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::gcmd::'+str(j.attrid)+'-'+str(nb1)+'-'+str(nb2),infos)
				nb2+=1
			nb1+=1

	def attribute_updated(self, cluster, attribute_id, value):
		try:
			logging.info("["+str(cluster.endpoint.device._ieee)+"][listener.attribute_updated] Received an attribute update %s=%s on cluster %s",attribute_id, value, cluster.cluster_id)
			utils.initSharedDeviceData(cluster,attribute_id)
			shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id][attribute_id] = value
			if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'attribute_updated'):
				if registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].attribute_updated(cluster, attribute_id, value) is not None:
					return
			shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::'+str(attribute_id),{"value" : str(value),"cluster_name" : cluster.name})
		except Exception as e:
			logging.error(traceback.format_exc())

	def zha_send_event(self, cluster, attribute_id, value):
		try:
			logging.info("["+str(cluster.endpoint.device._ieee)+"][listener.zha_send_event] Received an event update %s=%s on cluster %s",attribute_id, value, cluster.cluster_id)
			utils.initSharedDeviceData(cluster,attribute_id)
			shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id][attribute_id] = value
			if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'attribute_updated') and registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].attribute_updated(cluster, attribute_id, value) is not None:
				return
			#value['attribute'] = attribute_id
			shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::event::'+str(attribute_id),{"value" : value,"cluster_name" : cluster.name})
		except Exception as e:
			logging.error(traceback.format_exc())
			
	def zgp_frame(self,type,*args):
		try:
			logging.info("[listener.zgp_frame] Received zgp frame from %s  : %s",type,args)
			if type == 'bellows':
				gateway = shared.ZIGPY.get_device(nwk=0)
				if not zgp.endpoint_id in gateway.endpoints:
					ep = gateway.add_endpoint(zgp.endpoint_id)
					ep.status =  zigpy.endpoint.Status.ZDO_INIT
					ep.profile_id = zigpy.profiles.zha.PROFILE_ID
					ep.device_type = zgp.device_type
					ep.add_output_cluster(zgp.cluster_id)
				(status,gpdLink,sequenceNumber,unknown1,addr,gpdfSecurityLevel,gpdfSecurityKeyType,counter,command_id,mic,proxyTableIndex,payload) = args
				header = 0x308c
				if command_id == 0xe0 :
					logging.info("GreenPower autoCommissioning frame")
					zgp.create_device(addr)
				else:
					zgp.handle_notification(addr,header,counter,command_id,int.from_bytes(payload, byteorder="little"),len(payload),mic)
		except Exception as e:
			logging.error(traceback.format_exc())

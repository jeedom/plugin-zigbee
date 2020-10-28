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
import time
import json
import asyncio
import time
import sys
import os
import shared,utils
import traceback
import registries
import zqueue
import zigpy
from map import *

async def command(_data):
	device = find(_data['ieee'])
	if device == None :
		raise Exception("Device not found")
	for cmd in _data['cmd']:
		if not cmd['endpoint'] in device.endpoints:
			raise Exception("Endpoint not found : "+str(cmd['endpoint']))
		endpoint = device.endpoints[cmd['endpoint']]
		if not hasattr(endpoint,cmd['cluster']):
			raise Exception("Cluster not found : "+str(cmd['cluster']))
		cluster = getattr(endpoint, cmd['cluster'])
		if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],cmd['command']):
			logging.info("["+str(device._ieee)+"][zdevices.command] Use specific command action")
			command = getattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id], cmd['command'])
			if 'await' in cmd:
				await command(cluster,cmd)
			else:
				asyncio.ensure_future(command(cluster,cmd))
			continue
		if not hasattr(cluster,cmd['command']):
			raise Exception("Command not found : "+str(cmd['command']))
		command = getattr(cluster, cmd['command'])
		if 'args' in cmd:
			args = cmd['args']
			if 'await' in cmd:
				await command(*args)
			else:
				asyncio.ensure_future(command(*args))
		else:
			if 'await' in cmd:
				await command()
			else:
				asyncio.ensure_future(command())

async def write_attributes(_data):
	device = find(_data['ieee'])
	if device == None:
		raise Exception("Device not found")
	for attribute in _data['attributes']:
		if not attribute['endpoint'] in device.endpoints:
			raise Exception("Endpoint not found : "+str(attribute['endpoint']))
		endpoint = device.endpoints[attribute['endpoint']]
		if attribute['cluster_type'] == 'in':
			if not attribute['cluster'] in endpoint.in_clusters:
				raise Exception("Cluster not found : "+str(attribute['cluster']))
			cluster = endpoint.in_clusters[attribute['cluster']]
		else:
			if not attribute['cluster'] in endpoint.out_clusters:
				raise Exception("Cluster not found : "+str(attribute['cluster']))
			cluster = endpoint.out_clusters[attribute['cluster']]
		attributes = {}
		for i in attribute['attributes']:
			attributes[int(i)] = attribute['attributes'][i]
		manufacturer = None
		if 'manufacturer' in attribute:
			manufacturer = attribute['manufacturer']
		await cluster.write_attributes(attributes,manufacturer=manufacturer)
		asyncio.ensure_future(check_write_attributes(_data))

async def check_write_attributes(_data):
	await asyncio.sleep(120)
	device = find(_data['ieee'])
	logging.debug('['+str(device._ieee)+'][zdevices.check_write_attributes] Check write attribute for : '+str(_data))
	for attribute in _data['attributes']:
		if not attribute['endpoint'] in device.endpoints:
			return
		endpoint = device.endpoints[attribute['endpoint']]
		if attribute['cluster_type'] == 'in':
			if not attribute['cluster'] in endpoint.in_clusters:
				raise Exception("Cluster not found : "+str(attribute['cluster']))
			cluster = endpoint.in_clusters[attribute['cluster']]
		else:
			if not attribute['cluster'] in endpoint.out_clusters:
				return
			cluster = endpoint.out_clusters[attribute['cluster']]
		attributes = {}
		manufacturer = None
		if 'manufacturer' in attribute:
			manufacturer = attribute['manufacturer']
		for i in attribute['attributes']:
			values = await cluster.read_attributes([int(i)],True,manufacturer=manufacturer)
			if values[0][int(i)] != attribute['attributes'][i]:
				logging.debug('['+str(device._ieee)+'][zdevice.check_write_attributes] Attribute value issue for device : '+str(_data['ieee'])+' '+str(attribute['endpoint'])+'/'+str(attribute['cluster'])+'/'+str(int(i))+' expected value : '+str(attribute['attributes'][i])+' current value : '+str(values[0][int(i)]))
				attributes[int(i)] = attribute['attributes'][i]
		if len(attributes) == 0:
			logging.debug('['+str(device._ieee)+'][zdevices.check_write_attributes] All attribute write succefull do nothing')
			return;
		await cluster.write_attributes(attributes,manufacturer=manufacturer)

async def initialize(device):
	logging.debug("["+str(device._ieee)+"][zdevices.initialize] Begin device initialize")
	for ep_id, endpoint in device.endpoints.items():
		if ep_id == 0: # Ignore ZDO
			continue
		for cluster in endpoint.in_clusters.values():
			if not hasattr(cluster,'ep_attribute') or (cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'NO_BINDING') and registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].NO_BINDING):
				continue
			logging.debug("["+str(device._ieee)+"][zdevices.initialize] Begin configuration of input cluster '%s', is_server '%s'", cluster.ep_attribute,cluster.is_server)
			if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY :
				try:
					logging.debug("["+str(device._ieee)+"][zdevices.initialize] Bind input cluster '%s'", cluster.ep_attribute)
					await cluster.bind()
					logging.debug("["+str(device._ieee)+"][zdevices.initialize] Bound '%s' input cluster", cluster.ep_attribute)
				except (zigpy.exceptions.ZigbeeException, asyncio.TimeoutError) as ex:
					logging.debug("["+str(device._ieee)+"][zdevices.initialize] Failed to bind '%s' input cluster: %s", cluster.ep_attribute, str(ex))
				if cluster.is_server and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'REPORT_CONFIG') :
					logging.debug("["+str(device._ieee)+"][zdevices.initialize] This input cluster have REPORT_CONFIG, we need to configure it")
					kwargs = {}
					for report in registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].REPORT_CONFIG :
						attr = report["attr"]
						attr_name = cluster.attributes.get(attr, [attr])[0]
						min_report_int, max_report_int, reportable_change = report["config"]
						try:
							logging.debug("["+str(device._ieee)+"][zdevices.initialize] Reporting '%s' attr on '%s' input cluster: %d/%d/%d: For: '%s'",attr_name,cluster.ep_attribute,min_report_int,max_report_int,reportable_change,device.ieee)
							await cluster.configure_reporting(attr, min_report_int, max_report_int, reportable_change, **kwargs)
						except (zigpy.exceptions.ZigbeeException, asyncio.TimeoutError) as ex:
							logging.debug("["+str(device._ieee)+"][zdevices.initialize] Failed to set reporting for '%s' attr on '%s' input cluster: %s",attr_name,cluster.ep_attribute,str(ex),)
				try:
					if hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'initialize'):
						logging.debug('['+str(device._ieee)+'][zdevices.initialize] Intput cluster '+str(cluster.cluster_id)+ ' has specific function to initialize, I used it')
						await registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].initialize(cluster)
				except (zigpy.exceptions.ZigbeeException, asyncio.TimeoutError) as ex:
					logging.debug("["+str(device._ieee)+"][zdevices.initialize] Failed to initialize '%s' input cluster: %s", cluster.ep_attribute, str(ex))
			logging.debug("["+str(device._ieee)+"][zdevices.initialize] End configuration of input cluster '%s'", cluster.ep_attribute)
		for cluster in endpoint.out_clusters.values():
			if not hasattr(cluster,'ep_attribute') or (cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'NO_BINDING') and registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].NO_BINDING):
				continue
			logging.debug("["+str(device._ieee)+"][zdevices.initialize] Begin configuration of output cluster '%s', is_server '%s'", cluster.ep_attribute,cluster.is_server)
			if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY :
				try:
					logging.debug("["+str(device._ieee)+"][zdevices.initialize] Bind '%s' output cluster", cluster.ep_attribute)
					await cluster.bind()
					logging.debug("["+str(device._ieee)+"][zdevices.initialize] Bound '%s' output cluster", cluster.ep_attribute)
				except (zigpy.exceptions.ZigbeeException, asyncio.TimeoutError) as ex:
					logging.debug("["+str(device._ieee)+"][zdevices.initialize] Failed to bind '%s' output cluster: %s", cluster.ep_attribute, str(ex))
				if cluster.is_server and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'REPORT_CONFIG') :
					logging.debug("["+str(device._ieee)+"][zdevices.initialize] This output cluster have REPORT_CONFIG, we need to configure it")
					kwargs = {}
					for report in registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].REPORT_CONFIG :
						attr = report["attr"]
						attr_name = cluster.attributes.get(attr, [attr])[0]
						min_report_int, max_report_int, reportable_change = report["config"]
						try:
							logging.debug("["+str(device._ieee)+"][zdevices.initialize] reporting '%s' attr on '%s' output cluster: %d/%d/%d: For: '%s'",attr_name,cluster.ep_attribute,min_report_int,max_report_int,reportable_change,device.ieee)
							await cluster.configure_reporting(attr, min_report_int, max_report_int, reportable_change, **kwargs)
						except (zigpy.exceptions.ZigbeeException, asyncio.TimeoutError) as ex:
							logging.debug("["+str(device._ieee)+"][zdevices.initialize] failed to set reporting for '%s' attr on '%s' output cluster: %s",attr_name,cluster.ep_attribute,str(ex),)
				try:
					if hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'initialize'):
						logging.debug('['+str(device._ieee)+'][zdevices.initialize] Output cluster '+str(cluster.cluster_id)+ ' has specific function to initialize, I used it')
						await registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].initialize(cluster)
				except (zigpy.exceptions.ZigbeeException, asyncio.TimeoutError) as ex:
					logging.debug("["+str(device._ieee)+"][zdevices.initialize] Failed to initialize '%s' output cluster: %s", cluster.ep_attribute, str(ex))
			logging.debug("["+str(device._ieee)+"][zdevices.initialize] End configuration of output  cluster '%s'", cluster.ep_attribute)
	try:
		await get_basic_info(device)
	except Exception as e:
		logging.warning("["+str(device._ieee)+"][zdevices.initialize] Error on get_basic_info : "+str(e))
	if shared.CONTROLLER == 'deconz': # Force save neightbors on deconz after inclusion
		logging.debug("["+str(device._ieee)+"][zdevices.initialize] It's deconz key, force neightbors scan")
		await shared.ZIGPY.get_device(ieee=shared.ZIGPY.ieee).neighbors.scan()
	logging.debug("["+str(device._ieee)+"][zdevices.initialize] End device initialize")

async def get_basic_info(device):
		if 1 in device.endpoints and 0 in device.endpoints[1].in_clusters:
			try:
				await device.endpoints[1].in_clusters[0].read_attributes([4,5],True)
				await asyncio.sleep(1)
			except Exception as e:
				logging.warning("["+str(device._ieee)+"][zdevices.get_basic_info] Error on read attribute level 1 : "+str(e))
			try:
				await device.endpoints[1].in_clusters[0].read_attributes([0,1,2,3],True)
				await asyncio.sleep(1)
			except Exception as e:
				logging.warning("["+str(device._ieee)+"][zdevices.get_basic_info] Error on read attribute level 2 : "+str(e))
			try:
				await device.endpoints[1].in_clusters[0].read_attributes([7],True)
				await asyncio.sleep(1)
			except Exception as e:
				logging.warning("["+str(device._ieee)+"][zdevices.get_basic_info] Error on read attribute level 3 : "+str(e))
			try:
				await device.endpoints[1].in_clusters[0].read_attributes([6,16384],True)
			except Exception as e:
				logging.warning("["+str(device._ieee)+"][zdevices.get_basic_info] Error on read attribute level 4 : "+str(e))

async def serialize(device):
	obj = {
		'ieee': str(device.ieee),
		'nwk': device.nwk,
		'status': device.status,
		'lqi': str(device.lqi),
		'rssi':str(device.rssi),
		'last_seen':str(device.last_seen),
		'node_descriptor': None if not device.node_desc.is_valid else list(device.node_desc.serialize()),
		'endpoints': [],
	}
	if obj['node_descriptor'] is not None:
		obj['node_descriptor'] = ":".join("{:02x}".format(x) for x in obj['node_descriptor'])
	for endpoint_id, endpoint in device.endpoints.items():
		if endpoint_id == 0:
			continue
		endpoint_obj = {}
		endpoint_obj['id'] = endpoint_id
		endpoint_obj['status'] = endpoint.status
		endpoint_obj['device_type'] = getattr(endpoint, 'device_type', None)
		endpoint_obj['profile_id'] = getattr(endpoint, 'profile_id', None)
		endpoint_obj['output_clusters'] = []
		endpoint_obj['input_clusters'] = []
		endpoint_obj['output_clusters'] = []
		for cluster in endpoint.out_clusters.values():
			values = await serialize_cluster(cluster);
			endpoint_obj['output_clusters'].append(values)
		for cluster in endpoint.in_clusters.values():
			values = await serialize_cluster(cluster);
			endpoint_obj['input_clusters'].append(values)
		obj['endpoints'].append(endpoint_obj)
	return obj

async def serialize_cluster(cluster):
	obj = {
		'id' : cluster.cluster_id,
		'name' : cluster.name,
		'attributes' : []
	}
	for attribute in cluster.attributes:
		value = await cluster.read_attributes([attribute],True,True)
		if attribute in value[0]:
			value = value[0][attribute]
		else:
			continue
		obj['attributes'].append({'id' : attribute,'name' : cluster.attributes[attribute][0],'value':value})
	return obj

def find(ieee):
	for device in shared.ZIGPY.devices.values():
		if str(device.ieee) == ieee:
			return device
	return None

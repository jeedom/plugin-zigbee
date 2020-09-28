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
import shared
import json
import zigpy.exceptions
import registries
import asyncio

def format_json_result(success='ok', data='', log_level=None, code=0):
	if success == True or success == 'ok' :
		return json.dumps({'state': 'ok', 'result': data, 'code': code})
	else:
		return json.dumps({'state': 'error', 'result': data, 'code': code})

def check_apikey(apikey):
	if shared.APIKEY != apikey:
		raise Exception('Invalid apikey provided')

async def serialize_device(device):
	obj = {
		'ieee': str(device.ieee),
		'nwk': device.nwk,
		'status': device.status,
		'node_descriptor': None if not device.node_desc.is_valid else list(device.node_desc.serialize()),
		'endpoints': [],
	}
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

async def serialize_application():
	obj = {
		'ieee': str(shared.ZIGPY.ieee),
		'nwk': shared.ZIGPY.nwk,
		'config': shared.ZIGPY._config
	}
	try:
		obj['config']['network']['tc_link_key'] = ":".join("{:02x}".format(x) for x in obj['config']['network']['tc_link_key'])
	except Exception as e:
		pass

	if shared.CONTROLLER == 'ezsp':
		obj['ezsp'] = {}
		status, node_type, network_params = await shared.ZIGPY._ezsp.getNetworkParameters()
		version = await shared.ZIGPY._ezsp.get_board_info()
		obj['ezsp']['extendedPanId'] = ":".join("{:02x}".format(x) for x in network_params.extendedPanId)
		obj['ezsp']['panId'] = hex(network_params.panId)
		obj['ezsp']['radioTxPower'] = network_params.radioTxPower
		obj['ezsp']['radioChannel'] = network_params.radioChannel
		obj['ezsp']['nwkManagerId'] = hex(network_params.nwkManagerId)
		obj['ezsp']['nwkUpdateId'] = hex(network_params.nwkUpdateId)
		obj['ezsp']['version'] = str(version[2])
	if shared.CONTROLLER == 'deconz':
		obj['deconz'] = {}
		obj['deconz']['version'] = hex(shared.ZIGPY.version)
		obj['deconz']['extendedPanId'] = ":".join("{:02x}".format(x) for x in shared.ZIGPY._ext_pan_id)
		obj['deconz']['panId'] = hex(shared.ZIGPY._pan_id)
		obj['deconz']['radioChannel'] = shared.ZIGPY._channel
		obj['deconz']['nwkUpdateId'] = hex(shared.ZIGPY._nwk_update_id)
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

async def initialize_device_cluster(device):
	for ep_id, endpoint in device.endpoints.items():
		if ep_id == 0: # Ignore ZDO
			continue
		for cluster in endpoint.in_clusters.values(): # You need to attach a listener to every cluster to receive events
			try:
				await cluster.bind()
			except (zigpy.exceptions.ZigbeeException, asyncio.TimeoutError) as ex:
				logging.debug("Failed to bind '%s' cluster: %s", cluster.ep_attribute, str(ex))
			if cluster.is_server and cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'REPORT_CONFIG'):
				kwargs = {}
				for report in registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].REPORT_CONFIG:
					attr = report["attr"]
					attr_name = cluster.attributes.get(attr, [attr])[0]
					min_report_int, max_report_int, reportable_change = report["config"]
					try:
						await cluster.configure_reporting(attr, min_report_int, max_report_int, reportable_change, **kwargs)
						logging.debug("reporting '%s' attr on '%s' cluster: %d/%d/%d: For: '%s'",attr_name,cluster.ep_attribute,min_report_int,max_report_int,reportable_change,device.ieee)
					except (zigpy.exceptions.ZigbeeException, asyncio.TimeoutError) as ex:
						logging.debug("failed to set reporting for '%s' attr on '%s' cluster: %s",attr_name,cluster.ep_attribute,str(ex),)
		for cluster in endpoint.out_clusters.values(): # You need to attach a listener to every cluster to receive events
			try:
				await cluster.bind()
			except (zigpy.exceptions.ZigbeeException, asyncio.TimeoutError) as ex:
				logging.debug("Failed to bind '%s' cluster: %s", cluster.ep_attribute, str(ex))
			if cluster.is_server and cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],'REPORT_CONFIG'):
				kwargs = {}
				for report in registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].REPORT_CONFIG:
					attr = report["attr"]
					attr_name = cluster.attributes.get(attr, [attr])[0]
					min_report_int, max_report_int, reportable_change = report["config"]
					try:
						await cluster.configure_reporting(attr, min_report_int, max_report_int, reportable_change, **kwargs)
						logging.debug("reporting '%s' attr on '%s' cluster: %d/%d/%d: For: '%s'",attr_name,cluster.ep_attribute,min_report_int,max_report_int,reportable_change,device.ieee)
					except (zigpy.exceptions.ZigbeeException, asyncio.TimeoutError) as ex:
						logging.debug("failed to set reporting for '%s' attr on '%s' cluster: %s",attr_name,cluster.ep_attribute,str(ex),)
	if shared.CONTROLLER == 'deconz': # Force save neightbors on deconz after inclusion
		coord = shared.ZIGPY.get_device(ieee=self.ieee)
		coord.neighbors.scan()

def findDevice(ieee):
	for device in shared.ZIGPY.devices.values():
		if str(device.ieee) == ieee:
			return device
	return None

def initSharedDeviceData(cluster,attribute_id):
	if not cluster.endpoint.device._ieee in shared.DEVICES_DATA :
		shared.DEVICES_DATA[cluster.endpoint.device._ieee] = {}
	if not cluster.endpoint._endpoint_id in shared.DEVICES_DATA[cluster.endpoint.device._ieee] :
		shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id] = {}
	if not cluster.cluster_id in shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id] :
		shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id] = {}
	if not attribute_id in shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id] :
		shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id][attribute_id] = {}

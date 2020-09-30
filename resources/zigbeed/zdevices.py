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
from map import *

async def command(_data):
	device = utils.findDevice(_data['ieee'])
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
			logging.info("Use specific command action")
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
	device = utils.findDevice(_data['ieee'])
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

async def initialize(device):
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
	try:
		if 1 in device.endpoints and 0 in device.endpoints[1].in_clusters:
			await device.endpoints[1].in_clusters[0].read_attributes([4,5],True)
	except Exception as e:
		pass
	if shared.CONTROLLER == 'deconz': # Force save neightbors on deconz after inclusion
		await shared.ZIGPY.get_device(ieee=shared.ZIGPY.ieee).neighbors.scan()

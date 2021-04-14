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
import specifics
import zdevices
import zigpy.zdo.types as zdo_types
from zigpy import types

async def create_group(_name):
	id = 1
	for group in shared.ZIGPY.groups.values():
		id += 1
	shared.ZIGPY.groups.add_group(id,_name)

async def add_endpoint(_data):
	device = zdevices.find(_data['ieee'])
	endpoint = device.endpoints[_data['endpoint']]
	await endpoint.add_to_group(_data['id'])

async def add_device(_data):
	device = zdevices.find(_data['ieee'])
	await device.add_to_group(_data['id'])

async def delete_device(_data):
	device = zdevices.find(_data['ieee'])
	await device.remove_from_group(_data['id'])

def get_member(_data):
	group = find(_data['group_id'])
	logging.debug('group '+str(group.members))

async def command(_data):
	group = find(_data['ieee'])
	if group == None :
		raise Exception("Group not found")
	for cmd in _data['cmd']:
		cluster = group._endpoint.__getattr__(cmd['cluster'])
		if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],cmd['command']):
			logging.info("["+str(group._group_id)+"][zgroups.command] Use specific command action")
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

async def serialize(group):
	obj = {
		'id': group._group_id,
		'name': group._name,
	}
	members=[]
	for member in group.members:
		ieee,endpoint = member
		if (ieee not in members):
			members.append(str(ieee))
	obj['members'] = members
	return obj

def find(group_id):
	for group in shared.ZIGPY.groups.values():
		if group._group_id == int(group_id):
			return group
	return None
	
async def group_binding(device, group_id, operation, clusters):
		"""Create or remove a direct zigbee binding between a device and a group."""
		zdo = device.zdo
		op_msg = "0x%04x: %s %s, ep: %s, cluster: %s to group: 0x%04x"
		destination_address = zdo_types.MultiAddress()
		destination_address.addrmode = types.uint8_t(1)
		destination_address.nwk = types.uint16_t(group_id)
		tasks = []
		for cluster in clusters:
			if cluster.endpoint._endpoint_id == 0:
				continue
			op_params = (device.nwk,operation.name,str(device.ieee),cluster.endpoint._endpoint_id,cluster.cluster_id,group_id,)
			zdo.debug(f"processing {op_msg}", *op_params)
			tasks.append((zdo.request(operation,device.ieee,cluster.endpoint._endpoint_id,cluster.cluster_id,destination_address,),op_msg,op_params,))
		res = await asyncio.gather(*(t[0] for t in tasks), return_exceptions=True)
		for outcome, log_msg in zip(res, tasks):
			if isinstance(outcome, Exception):
				fmt = f"{log_msg[1]} failed: %s"
			else:
				fmt = f"{log_msg[1]} completed: %s"
			logging.debug(fmt, *(log_msg[2] + (outcome,)))

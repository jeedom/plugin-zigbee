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
	if shared.CONTROLLER == 'zigate':
		obj['zigate'] = {}
		obj['zigate']['version'] = str(shared.ZIGPY.version)
	return obj

def initSharedDeviceData(cluster,attribute_id):
	if not cluster.endpoint.device._ieee in shared.DEVICES_DATA :
		shared.DEVICES_DATA[cluster.endpoint.device._ieee] = {}
	if not cluster.endpoint._endpoint_id in shared.DEVICES_DATA[cluster.endpoint.device._ieee] :
		shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id] = {}
	if not cluster.cluster_id in shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id] :
		shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id] = {}
	if not attribute_id in shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id] :
		shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id][attribute_id] = {}

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
import zigpy.types as t
import registries
import asyncio
import pkg_resources

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
		'zigpy_version':zigpy.__version__,
		#'zha_version': pkg_resources.require("zha-quirks")[0].version,
		'nwk': shared.ZIGPY.nwk,
		'config': shared.ZIGPY._config
	}
	try:
		obj['config']['network']['tc_link_key'] = ":".join("{:02x}".format(x) for x in obj['config']['network']['tc_link_key'])
	except Exception as e:
		pass

	if shared.CONTROLLER == 'ezsp':
		import bellows
		obj['ezsp'] = {}
		obj['ezsp']['zigpy_bellows_version'] = bellows.__version__
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
		import zigpy_deconz
		obj['deconz'] = {}
		obj['deconz']['zigpy_deconz_version'] = zigpy_deconz.__version__
		obj['deconz']['version'] = hex(shared.ZIGPY.version)
		obj['deconz']['extendedPanId'] = ":".join("{:02x}".format(x) for x in shared.ZIGPY.state.network_information.extended_pan_id)
		obj['deconz']['panId'] = hex(shared.ZIGPY.state.network_information.pan_id)
		obj['deconz']['radioChannel'] = shared.ZIGPY.state.network_information.channel
		obj['deconz']['nwkUpdateId'] = hex(shared.ZIGPY.state.network_information.nwk_update_id)
	if shared.CONTROLLER == 'zigate':
		import zigpy_zigate
		obj['zigate'] = {}
		obj['zigate']['zigpy_zigate_version'] = zigpy_zigate.__version__
		obj['zigate']['version'] = str(shared.ZIGPY.version)
	if shared.CONTROLLER == 'znp':
		import zigpy_znp
		obj['znp'] = {}
		obj['znp']['zigpy_znp_version'] = zigpy_znp.__version__
		obj['znp']['z-stack version'] = str(shared.ZIGPY._znp.version)
		obj['znp']['z-stack build id'] = str(shared.ZIGPY._zstack_build_id)
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

def convertStrToIEU64(_ieee):
	ieee = []
	for i in _ieee.split(':'):
		ieee.append(int(i,16))
	if len(ieee) != 8:
		raise Exception("Invalid ieee size")
	ieee.reverse()
	return  t.EUI64(ieee)

def convert_xy_to_rgb(x_point,y_point,Y=255):
	X = (Y / y_point) * x_point
	Z = (Y / y_point) * (1 - x_point - y_point)
	r = X * 1.656492 - Y * 0.354851 - Z * 0.255038
	g = -X * 0.707196 + Y * 1.655397 + Z * 0.036152
	b = X * 0.051713 - Y * 0.121364 + Z * 1.011530
	r, g, b = map(lambda x: (12.92 * x) if (x <= 0.0031308) else ((1.0 + 0.055) * pow(x, (1.0 / 2.4)) - 0.055),[r, g, b])
	r, g, b = map(lambda x: max(0, x), [r, g, b])
	max_component = max(r, g, b)
	if max_component > 1:
		r, g, b = map(lambda x: x / max_component, [r, g, b])
		r, g, b = map(lambda x: int(x * 255), [r, g, b])
	return str('#%02x%02x%02x' % (r, g, b))
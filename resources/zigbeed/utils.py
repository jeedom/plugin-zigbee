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

def format_json_result(success='ok', data='', log_level=None, code=0):
	if success == True or success == 'ok' :
		return json.dumps({'state': 'ok', 'result': data, 'code': code})
	else:
		return json.dumps({'state': 'error', 'result': data, 'code': code})

def check_apikey(apikey):
	if shared.APIKEY != apikey:
		raise Exception('Invalid apikey provided')

def serialize_device(device):
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
		endpoint_obj['output_clusters'] = [cluster.cluster_id for cluster in endpoint.out_clusters.values()]
		endpoint_obj['input_clusters'] = [cluster.cluster_id for cluster in endpoint.in_clusters.values()]
		obj['endpoints'].append(endpoint_obj)
	return obj

def serialize_application(application):
	obj = {
		'ieee': str(application.ieee),
		'nwk': application.nwk,
		'config': application._config
	}
	return obj

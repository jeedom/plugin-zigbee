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

import sys
import logging
import os
import shared,utils
import json
import time
import zigpy
import zigpy.types as t
import zigpy.zdo as zdo


from Crypto.Cipher import AES
from Crypto.Util import Counter
from zigpy.zcl import Cluster, foundation

endpoint_id = 242
cluster_id = 0x0021
device_type = 0xA1E0

commands = {
	0x00: ("Identify", "CLUSTER_COMMAND", (), None, None, ()),
	0x10: ("Scene 0", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 0)),
	0x11: ("Scene 1","CLUSTER_COMMAND",(),0x0005,0x0001,(0,1,),),
	0x12: ("Scene 2", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 2)),
	0x13: ("Scene 3", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 3)),
	0x14: ("Scene 4", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 4)),
	0x15: ("Scene 5", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 5)),
	0x17: ("Scene 7", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 6)),
	0x16: ("Scene 6", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 7)),
	0x18: ("Scene 8", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 8)),
	0x19: ("Scene 9", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 9)),
	0x1A: ("Scene 10", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 10)),
	0x1B: ("Scene 11", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 11)),
	0x1C: ("Scene 12", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 12)),
	0x1D: ("Scene 13", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 13)),
	0x1E: ("Scene 14", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 14)),
	0x1F: ("Scene 15", "CLUSTER_COMMAND", (), 0x0005, 0x0001, (0, 15)),
	0x20: ("Off", "CLUSTER_COMMAND", (), 0x0006, 0x0000, ()),
	0x21: ("On", "CLUSTER_COMMAND", (), 0x0006, 0x0001, ()),
	0x22: ("Toggle", "CLUSTER_COMMAND", (), 0x0006, 0x0002, ()),
	0x23: ("Release", "CLUSTER_COMMAND", (), None, None, ()),
	0x30: ("Move Up", "CLUSTER_COMMAND", (t.uint8_t,), 0x0008, 0x0001, (1,)),
	0x31: ("Move Down", "CLUSTER_COMMAND", (t.uint8_t,), 0x0008, 0x0000, (0,)),
	0x32: ("Step Up","CLUSTER_COMMAND",(t.uint8_t, t.Optional(t.uint16_t)),0x0008,0x0002,(1,),),
	0x33: ("Step Down","CLUSTER_COMMAND",(t.uint8_t, t.Optional(t.uint16_t)),0x0008,0x0002,(0,),),
	0x34: ("Level Control/Stop", "CLUSTER_COMMAND", (), 0x0008, 0x0007, ()),
	0x35: ("Move Up (with On/Off)","CLUSTER_COMMAND",(t.uint8_t,),0x0008,0x0005,(1,),),
	0x36: ("Move Down (with On/Off)","CLUSTER_COMMAND",(t.uint8_t,),0x0008,0x0005,(0,),),
	0x37: ("Step Up (with On/Off)","CLUSTER_COMMAND",(t.uint8_t, t.Optional(t.uint16_t)),0x0008,0x0006,(1,),),
	0x38: ("Step Down (with On/Off)","CLUSTER_COMMAND",(t.uint8_t, t.Optional(t.uint16_t)),0x0008,0x0006,(0,),),
	0x40: ("Move Hue Stop", "CLUSTER_COMMAND", (), 0x0300, 0x0047, ()),
	0x41: ("Move Hue Up Color","CLUSTER_COMMAND",(t.uint8_t,),0x0300,0x0001,(1,),),
	0x42: ("Move Hue Down Color","CLUSTER_COMMAND",(t.uint8_t,),0x0300,0x0001,(0,),),
	0x43: ("Step Hue Up Color","CLUSTER_COMMAND",(t.uint8_t, t.Optional(t.uint16_t)),0x0300,0x0002,(1,),),
	0x44: ("Step Hue Down Color","CLUSTER_COMMAND",(t.uint8_t, t.Optional(t.uint16_t)),0x0300,0x0002,(0,),),
	0x46: ("Move Saturation Up","CLUSTER_COMMAND",(t.uint8_t,),0x0300,0x0004,(1,),),
	0x47: ("Move Saturation Down","CLUSTER_COMMAND",(t.uint8_t,),0x0300,0x0004,(0,),),
	0x48: ("Step Saturation Up","CLUSTER_COMMAND",(t.uint8_t,),0x0300,0x0005,(1,),),
	0x49: ("Step Saturation Down","CLUSTER_COMMAND",(t.uint8_t,),0x0300,0x0005,(0,),),
	0x4A: ("Move Color","CLUSTER_COMMAND",(t.uint16_t, t.uint16_t),0x0300,0x0008,(),),
	0x4B: ("Step Color","CLUSTER_COMMAND",(t.uint16_t, t.uint16_t, t.Optional(t.uint16_t)),0x0300,0x0009,(),),
	0x45: ("Move Saturation Stop", "CLUSTER_COMMAND", (), 0x0300, 0x0047, ()),
	0x50: ("Lock Door", "CLUSTER_COMMAND", (), 0x0101, 0x0000, ()),
	0x51: ("Unlock Door", "CLUSTER_COMMAND", (), 0x0101, 0x0001, ()),
	0x60: ("Press 1 of 1", "CLUSTER_COMMAND", (), None, None, ()),
	0x61: ("Release 1 of 1", "CLUSTER_COMMAND", (), None, None, ()),
	0x62: ("Press 1 of 2", "CLUSTER_COMMAND", (), None, None, ()),
	0x63: ("Release 1 of 2", "CLUSTER_COMMAND", (), None, None, ()),
	0x64: ("Press 2 of 2", "CLUSTER_COMMAND", (), None, None, ()),
	0x65: ("Release 2 of 2", "CLUSTER_COMMAND", (), None, None, ()),
	0x66: ("Short press 1 of 1", "CLUSTER_COMMAND", (), None, None, ()),
	0x67: ("Short press 1 of 2", "CLUSTER_COMMAND", (), None, None, ()),
	0x68: ("Short press 2 of 2", "CLUSTER_COMMAND", (), None, None, ()),
	0x69: ("Press", "CLUSTER_COMMAND", (t.uint8_t,), 0x0005, 0x0001, (0,)),
	0x6A: ("Release", "CLUSTER_COMMAND", (t.uint8_t,), None, None, ()),
}

devices = {
	0x00: ("Simple Generic 1-state Switch", [], [0x0006]),
	0x01: ("Simple Generic 2-state Switch", [], [0x0006]),
	0x02: ("On/Off Switch", [], [0x0005, 0x0006]),
	0x03: ("Level Control Switch", [], [0x0008]),
	0x04: ("Simple Sensor", [], []),
	0x05: ("Advanced Generic 1-state Switch", [], [0x0005, 0x0006]),
	0x06: ("Advanced Generic 2-state Switch", [], [0x0005, 0x0006]),
	0x07: ("On/Off Switch", [], [0x0005, 0x0006]),
	0x10: ("Color Dimmer Switch", [], [0x0300]),
	0x11: ("Light Sensor", [0x0400], []),
	0x12: ("Occupancy Sensor", [0x0406], []),
	0x20: ("Door Lock Controller", [], [0x0101]),
	0x30: ("Temperature Sensor", [0x0402], []),
	0x31: ("Pressure Sensor", [0x0403], []),
	0x32: ("Flow Sensor", [0x0404], []),
	0x33: ("Indoor Environment Sensor", [], []),
}

def create_device(ieee, type=None, remoteCommissioning=False):
	application = shared.ZIGPY
	if ieee in application.devices:
		return application.devices[ieee]
	gateway = shared.ZIGPY.get_device(nwk=0)
	if not endpoint_id in gateway.endpoints:
		ep = gateway.add_endpoint(endpoint_id)
		ep.status =  zigpy.endpoint.Status.ZDO_INIT
		ep.profile_id = zigpy.profiles.zha.PROFILE_ID
		ep.device_type = device_type
		ep.add_output_cluster(cluster_id)
	if not remoteCommissioning and (0x9997 not in gateway.endpoints[endpoint_id].out_clusters[cluster_id]._attr_cache or gateway.endpoints[endpoint_id].out_clusters[cluster_id]._attr_cache[0x9997] < time.time()):
		logging.info("[zgp.create_device] Not in permit joining mode and not in remoteCommissioning")
		return None
	logging.info("[zgp.create_device] Device %s not found, create it", ieee)
	nwk = 32766
	for i in range(32766, 65535):
		nwk = i 
		try:
			shared.ZIGPY.get_device(nwk=i)
		except KeyError:
			break
	dev = application.add_device(ieee, nwk)
	dev.status = zigpy.device.Status.ENDPOINTS_INIT
	dev._skip_configuration = True
	dev.node_desc = zdo.types.NodeDescriptor(2, 64, 128, 4174, 82, 82, 0, 82, 0)
	ep = dev.add_endpoint(1)
	ep.status = zigpy.endpoint.Status.ZDO_INIT
	ep.profile_id = zigpy.profiles.zha.PROFILE_ID
	ep.device_type = device_type
	application.device_initialized(dev)
	ep.add_input_cluster(zigpy.zcl.clusters.general.Basic.cluster_id)
	ep.in_clusters[zigpy.zcl.clusters.general.Basic.cluster_id]._update_attribute(0x0004, "GreenPower")
	in_clusters = None
	out_clusters = None
	if type is not None and type in devices:
		name, in_clusters, out_clusters = devices[type]
		ep.in_clusters[zigpy.zcl.clusters.general.Basic.cluster_id]._update_attribute(0x0005, name)
		for id in in_clusters:
			logging.info("[zgp.create_device] Add input cluster id %s on device %s", id, ieee)
			ep.add_input_cluster(id)
		for id in out_clusters:
			logging.info("[zgp.create_device] Add output cluster id %s on device %s", id, ieee)
			ep.add_output_cluster(id)
	else:
		ep.in_clusters[zigpy.zcl.clusters.general.Basic.cluster_id]._update_attribute(0x0005, "GreenPowerDevice")
	ep = dev.add_endpoint(endpoint_id)
	ep.status = zigpy.endpoint.Status.ZDO_INIT
	ep.profile_id = zigpy.profiles.zha.PROFILE_ID
	ep.device_type = device_type
	ep.add_input_cluster(cluster_id)
	return dev

def handle_notification(ieee, header, counter, command_id, payload, payload_length, mic):
	application = shared.ZIGPY
	if ieee not in application.devices:
		logging.info("[zgp.handle_notification] Unkwonw device : %s try to create it if allow", ieee)
		if create_device(ieee) is None:
			return
	if command_id not in commands:
		logging.info("[zgp.handle_notification] Unhandled command_id : %s", command_id)
		return
	expected_mic = calcul_mic(ieee,header,counter,command_id.to_bytes(1, "little")+ payload.to_bytes(payload_length, "little"),payload_length + 1,)
	if expected_mic is not None :
		logging.info("[zgp.handle_notification] Mic : %s, expected mic %s : OK", hex(mic), hex(expected_mic))
	if expected_mic is not None and expected_mic != mic:
		logging.info("[zgp.handle_notification] Wrong mic : %s, expected mic %s, ignore frame", hex(mic), hex(expected_mic))
		return
	(command,type,schema,clusterid,zcl_command_id,value) = commands[command_id]
	try:
		payload, _ = t.deserialize(payload.to_bytes(payload_length, "little"), schema)
	except Exception as e:
		payload = ()
		pass
	logging.info("[zgp.handle_notification] Green power frame ieee : %s, command_id : %s, payload : %s,counter : %s",ieee,command_id,payload,counter)
	value = value + tuple(payload)
	dev = application.devices[ieee]
	if counter is not None:
		attributes = dev.endpoints[endpoint_id].in_clusters[cluster_id]._attr_cache
		if 0x9999 in attributes and attributes[0x9999] >= counter:
			logging.info("[zgp.handle_notification] Already get this frame counter,I ignoring it")
			return
		attributes[0x9999] = counter
	if clusterid is not None and type == "CLUSTER_COMMAND":
		if clusterid not in dev.endpoints[1].out_clusters:
			dev.endpoints[1].add_output_cluster(clusterid)
			application.device_initialized(dev)
		dev.endpoints[1].out_clusters[clusterid].handle_message(foundation.ZCLHeader.cluster(application.get_sequence(), zcl_command_id),value)

def handle_message(data):
	application = shared.ZIGPY
	data = data[0]
	if data[0] == 12 and data[5] == 224:
		ieee = t.EUI64(data[1:5] + data[1:5])
		type = data[6]
		create_device(application,ieee, type)
		return
	payload = ()
	ieee = t.EUI64(data[2:6] + data[2:6])
	counter = int.from_bytes(data[6:10], byteorder="little")
	command_id = data[10]
	payload_length = len(data[11:-4])
	payload = int.from_bytes(data[11:-4], byteorder="little")
	mic = int.from_bytes(data[-4:], byteorder="little")
	header = int.from_bytes(data[0:2], byteorder="little")
	handle_notification(application,ieee, header, counter, command_id, payload, payload_length, mic)

def calcul_mic(ieee, header, counter, payload, payload_length):
	application = shared.ZIGPY
	if ieee not in application.devices:
		return None
	dev = application.devices[ieee]
	if (0x9998 not in dev.endpoints[endpoint_id].in_clusters[cluster_id]._attr_cache):
		return None
	src_id = bytearray(ieee[0:4])
	if not isinstance(header, (bytes)):
		header = header.to_bytes(2, "little")
	if not isinstance(counter, (bytes)):
		counter = counter.to_bytes(4, "little")
	if not isinstance(payload, (bytes)):
		payload = payload.to_bytes(payload_length, "little")
	logging.info("[zgp.calcul_mic] Calcul mic of green power frame for %s on header : 0x%s, src_id : 0x%s, counter : 0x%s, payload : 0x%s, payload length : %s",ieee,header.hex(),src_id.hex(),counter.hex(),payload.hex(),payload_length,)
	key = dev.endpoints[endpoint_id].in_clusters[cluster_id]._attr_cache[0x9998]
	nonce = src_id + src_id + counter + (0x05).to_bytes(1, "little")
	header = header + src_id + counter
	a = header + payload
	La = len(a).to_bytes(2, "big")
	AddAuthData = La + a
	AddAuthData += (0x00).to_bytes(1, "little") * (16 - len(AddAuthData))
	B0 = (0x49).to_bytes(1, "little") + nonce
	B0 += (0x00).to_bytes(1, "little") * (16 - len(B0))
	B1 = AddAuthData
	X0 = (0x00000000000000000000000000000000).to_bytes(16, "big")
	cipher = AES.new(key, AES.MODE_CBC, B0)
	X1 = cipher.encrypt(X0)
	cipher = AES.new(key, AES.MODE_CBC, B1)
	X2 = cipher.encrypt(X1)
	A0 = (0x01).to_bytes(1, "little") + nonce + (0x0000).to_bytes(2, "big")
	cipher = AES.new(key,AES.MODE_CTR,counter=Counter.new(128, initial_value=int.from_bytes(A0, byteorder="big")))
	return int.from_bytes(cipher.encrypt(X2[0:4]), byteorder="little")
	
def setKey(device, key):
	if key is None:
		logging.info("[zgp.setKey] Remove key for device "+str(device.ieee))
		del device.endpoints[endpoint_id].in_clusters[cluster_id]._attr_cache[0x9998]
		return
	if not isinstance(key, (bytes)):
		key = key.to_bytes(16, "big")
	logging.info("[zgp.setKey] Set key for device "+str(device.ieee)+' to '+str(key))
	device.endpoints[endpoint_id].in_clusters[cluster_id]._update_attribute(0x9998, key)
	
async def permit(time_s=60):
	assert 0 <= time_s <= 254
	gateway = shared.ZIGPY.get_device(nwk=0)
	logging.info("[zgp.permit] Permit green power pairing for %s s", time_s)
	gateway.endpoints[endpoint_id].out_clusters[cluster_id]._attr_cache[0x9997] = int(time.time() + time_s)
	return
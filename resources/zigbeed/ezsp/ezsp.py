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
import shared
import time

try:
	from jeedom.jeedom import *
except ImportError:
	print("Error: importing module jeedom.jeedom")
	sys.exit(1)

from ezsp.command import *
from ezsp.value import *
from ezsp.uart import *

class ezsp():

	def validateReturn(_data,raiseExeption=True,_success=[0]):
		if 'command' not in _data :
			return _data
		command = _data['command']
		if command in EZSP_COMMANDS and 'resultClass' in EZSP_COMMANDS[command]:
			result = ezsp.convertFromValue(EZSP_COMMANDS[command]['resultClass'],_data['data'][0])
			if 'noExeption' not in EZSP_COMMANDS[command] and raiseExeption and _data['data'][0] not in _success :
				raise Exception('Error on return '+str(command)+ ' code '+str(_data['data'][0])+' => '+str(result))
			logging.debug('Return for '+str(command)+ ' code '+str(_data['data'][0])+' => '+str(result))
		return _data

	def convertFromValue(_class,_value):
		if _class in globals():
			obj = globals()[_class];
			attrs = dir(obj)
			for i in attrs:
				if getattr(obj,i) == _value:
					return i
		return _value

	def convertTovalue(_str):
		values = _str.split('.')
		if values[0] in globals():
			if hasattr(globals()[values[0]], values[1]):
				return getattr(globals()[values[0]],values[1])
		return _str

	def getCommandFromId(_id):
		for i in EZSP_COMMANDS:
			if EZSP_COMMANDS[i]['value'] == _id :
				return i
		return 'unknown'

	def read(timeout=9):
		startTime=time.time()
		message = b''
		while 1:
			time.sleep(0.02)
			byte = shared.JEEDOM_SERIAL.read()
			if byte != None :
				message += byte
				if byte == shared.FLAG:
					return message
			if timeout != None and (time.time()-startTime) > timeout :
				return None

	def decode(data):
		result = uart.decode_frame(data)
		if result['type'] != 'DATA' :
			return result
		logging.debug('Decode frame : '+str(jeedom_utils.printHex(result['frame_ezsp'].hex()))+' with EZSP_VRSION '+str(shared.EZSP_VERSION))
		if shared.EZSP_VERSION >= 8:
			result['seq_ezsp'] = result['frame_ezsp'][0]
			result['frame_id'] = ((result['frame_ezsp'][4] << 8) | result['frame_ezsp'][3])
			result['data'] = result['frame_ezsp'][5:]
		else:
			result['seq_ezsp'] = result['frame_ezsp'][0]
			result['frame_id'] =result['frame_ezsp'][2]
			result['data'] = result['frame_ezsp'][3:]
		if 'frame_id' in result :
			result['command'] = ezsp.getCommandFromId(result['frame_id']);
		if 'data' in result :
			data = result['data']
			result['data'] = []
			for i in data :
				result['data'].append(i)
		if 'handle_'+result['command'] in dir(globals()['ezsp']):
			result['handle_result'] = getattr(globals()['ezsp'],'handle_'+result['command'])(result)
		logging.debug('Decode result : '+str(result))
		return result

	def make(cmd,data=None):
		logging.debug('**********************MAKE : '+str(cmd)+' ***********************')
		if shared.EZSP_VERSION >= 8:
			result = bytes([shared.SEQUENCE])+bytes([0x00])+bytes([0x01])
			result += bytes([EZSP_COMMANDS[cmd]['value'] & 0x00FF])
			result += bytes([(EZSP_COMMANDS[cmd]['value'] & 0xFF00) >> 8])
			if data != None:
				result += bytes(data)
		else :
			result = bytes([shared.SEQUENCE])+bytes([0x00])+bytes([EZSP_COMMANDS[cmd]['value']])+bytes(data)
		shared.SEQUENCE += 1
		if shared.SEQUENCE > 256 :
			shared.SEQUENCE = 0
		return result;

	def init():
		logging.info('Begin init ezsp')
		shared.JEEDOM_SERIAL.write(uart.make_rst_frame())
		time.sleep(1)
		resp = ezsp.decode(ezsp.read())
		if resp['type'] != 'RSTACK':
			raise Exception("No RSTACK received after RST")
		shared.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('version',[0x08])))
		time.sleep(1)
		resp = ezsp.decode(ezsp.read())
		if resp['type'] != 'DATA' or resp['frame_id'] != EZSP_COMMANDS['version']['value']:
			raise Exception("Invalid EZSP version")
		shared.EZSP_VERSION=resp['data'][0]
		logging.info('EZSP version : '+str(resp['data'][0])+'.'+str(resp['data'][1])+'.'+str(resp['data'][2]+resp['data'][3]))

		logging.info('Init network')
		shared.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('networkInit',[0,0])))
		try:
			ezsp.validateReturn(ezsp.decode(ezsp.read()))
			time.sleep(1)
			resp = ezsp.decode(ezsp.read())
		except Exception as e:
			ezsp.formNetwork()

		shared.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('getNetworkParameters')))
		resp = ezsp.validateReturn(ezsp.decode(ezsp.read()))

		needReformNetwork = False

		if resp['data'][1] != EmberNodeType.COORDINATOR:
			logging.debug('Node not coordinator, need reforming network')
			needReformNetwork = True
		if resp['handle_result']['extendedPanId'] != shared.CONFIG['network']['parameters']['extendedPanId']:
			logging.debug('extendedPanId nok : '+str(resp['handle_result']['extendedPanId'])+' != '+str(shared.CONFIG['network']['parameters']['extendedPanId']))
			needReformNetwork = True
		if resp['handle_result']['panId'] != shared.CONFIG['network']['parameters']['panId']:
			logging.debug('panId nok : '+str(resp['handle_result']['panId'])+' != '+str(shared.CONFIG['network']['parameters']['panId']))
			needReformNetwork = True
		if resp['handle_result']['radioTxPower'] != shared.CONFIG['network']['parameters']['radioTxPower']:
			logging.debug('radioTxPower nok : '+str(resp['handle_result']['radioTxPower'])+' != '+str(shared.CONFIG['network']['parameters']['radioTxPower']))
			needReformNetwork = True
		if resp['handle_result']['nwkManagerId'] != shared.CONFIG['network']['parameters']['nwkManagerId']:
			logging.debug('nwkManagerId nok : '+str(resp['handle_result']['nwkManagerId'])+' != '+str(shared.CONFIG['network']['parameters']['nwkManagerId']))
			needReformNetwork = True
		if resp['handle_result']['nwkUpdateId'] != shared.CONFIG['network']['parameters']['nwkUpdateId']:
			logging.debug('nwkUpdateId nok : '+str(resp['handle_result']['nwkUpdateId'])+' != '+str(shared.CONFIG['network']['parameters']['nwkUpdateId']))
			needReformNetwork = True

		if needReformNetwork:
			shared.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('leaveNetwork')))
			ezsp.validateReturn(ezsp.decode(ezsp.read()))
			time.sleep(2)
			ezsp.formNetwork()

		logging.info('End init ezsp successfull')

	def handle_getNetworkParameters(_data):
		result = {}
		result['nodeType'] = _data['data'][1]
		result['nodeType_str'] = ezsp.convertFromValue('EmberNodeType',_data['data'][1])
		result['extendedPanId'] = _data['data'][2:10]
		result['panId'] = _data['data'][10:12]
		result['radioTxPower'] = _data['data'][12]
		result['joinMethod'] = _data['data'][13]
		result['nwkManagerId'] = _data['data'][14]
		result['nwkUpdateId'] = _data['data'][15]
		result['channels'] = _data['data'][16:]
		return result

	def formNetwork():
		logging.info('FORMING NETWORK')
		parameters = []
		parameters +=  (EmberInitialSecurityBitmask.HAVE_PRECONFIGURED_KEY| EmberInitialSecurityBitmask.REQUIRE_ENCRYPTED_KEY).to_bytes(2, 'little')
		parameters += shared.CONFIG['network']['security']['preconfiguredKey']
		parameters += shared.CONFIG['network']['security']['networkKey']
		parameters.append(shared.CONFIG['network']['security']['networkKeySequenceNumber'])
		parameters += shared.CONFIG['network']['security']['preconfiguredTrustCenterEui64']
		shared.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('setInitialSecurityState',parameters)))
		resp = ezsp.validateReturn(ezsp.decode(ezsp.read()))

		if resp['command'] == 'stackStatusHandler':
			resp = ezsp.validateReturn(ezsp.decode(ezsp.read()))

		parameters = []
		parameters += shared.CONFIG['network']['parameters']['extendedPanId']
		parameters += shared.CONFIG['network']['parameters']['panId']
		parameters.append(shared.CONFIG['network']['parameters']['radioTxPower'])
		parameters.append(shared.CONFIG['network']['parameters']['radioChannel'])
		parameters.append(ezsp.convertTovalue(shared.CONFIG['network']['parameters']['joinMethod']))
		parameters.append(shared.CONFIG['network']['parameters']['nwkManagerId'])
		parameters.append(shared.CONFIG['network']['parameters']['nwkUpdateId'])
		parameters += shared.CONFIG['network']['parameters']['channels']
		shared.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('formNetwork',parameters)))
		ezsp.validateReturn(ezsp.decode(ezsp.read()))

		if resp['command'] == 'stackStatusHandler':
			resp = ezsp.validateReturn(ezsp.decode(ezsp.read()))

	def version_info():
		logging.info('Begin version info')
		shared.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('getValue',[0x11])))
		time.sleep(1)
		resp = ezsp.decode(ezsp.read())
		ezsp.validateReturn(resp);
		logging.info('_____Stack version : '+str(resp['data'][6])+'.'+str(resp['data'][5])+'.'+str(resp['data'][4]))

	def permitJoining(_second):
		logging.info('Permit joining for '+str(_second))
		shared.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('permitJoining',[_second])))

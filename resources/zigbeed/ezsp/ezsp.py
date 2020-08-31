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

try:
	from jeedom.jeedom import *
except ImportError:
	print("Error: importing module jeedom.jeedom")
	sys.exit(1)

from ezsp.command import *
from ezsp.value import *
from ezsp.uart import *

class ezsp():

	def convertTovalue(_value):
		values = _value.split('.')
		if values[0] in globals():
			if hasattr(globals()[values[0]], values[1]):
				return getattr(globals()[values[0]],values[1])
		return _value

	def getCommandFromId(_id):
		for i in EZSP_COMMANDS:
			if EZSP_COMMANDS[i] == _id :
				return i
		return 'unknown'

	def read():
		message = b''
		while 1:
			time.sleep(0.02)
			byte = shared.JEEDOM_SERIAL.read()
			if byte != None :
				message += byte
				if byte == shared.FLAG:
					return message

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
		logging.debug('Decode result : '+str(result))
		return result

	def make(cmd,data):
		if shared.EZSP_VERSION >= 8:
			result = bytes([shared.SEQUENCE])+bytes([0x00])+bytes([0x01])
			result += bytes([EZSP_COMMANDS[cmd] & 0x00FF])
			result += bytes([(EZSP_COMMANDS[cmd] & 0xFF00) >> 8])
			result += bytes(data)
		else :
			result = bytes([shared.SEQUENCE])+bytes([0x00])+bytes([EZSP_COMMANDS[cmd]])+bytes(data)
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
		if resp['type'] != 'DATA' or resp['frame_id'] != EZSP_COMMANDS['version']:
			raise Exception("Invalid EZSP version")
		shared.EZSP_VERSION=resp['data'][0]
		logging.info('EZSP version : '+str(resp['data'][0])+'.'+str(resp['data'][1])+'.'+str(resp['data'][2]+resp['data'][3]))

		parameters = []
		parameters += shared.CONFIG['network']['parameters']['extendedPanId']
		parameters += shared.CONFIG['network']['parameters']['panId']
		parameters.append(shared.CONFIG['network']['parameters']['radioTxPower']) #Power setting
		parameters.append(shared.CONFIG['network']['parameters']['radioChannel']) #Channel
		parameters.append(ezsp.convertTovalue(shared.CONFIG['network']['parameters']['joinMethod'])) #Join method
		parameters.append(shared.CONFIG['network']['parameters']['nwkManagerId']) #NWK Manager ID
		parameters.append(shared.CONFIG['network']['parameters']['nwkUpdateId']) #NWP Update ID
		parameters += shared.CONFIG['network']['parameters']['channels'] #Channels Mask
		logging.info('Configure network : '+str(parameters))
		shared.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('formNetwork',parameters)))
		resp = ezsp.decode(ezsp.read())
		logging.info('End init ezsp successfull')

	def version_info():
		logging.info('Begin version info')
		shared.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('getValue',[0x11])))
		time.sleep(1)
		resp = ezsp.decode(ezsp.read())
		logging.info('Stack version : '+str(resp['data'][6])+'.'+str(resp['data'][5])+'.'+str(resp['data'][4]))

	def permitJoining(_second):
		logging.info('Permit joining for '+str(_second))
		shared.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('permitJoining',[_second])))

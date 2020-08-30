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
import globals

try:
	from jeedom.jeedom import *
except ImportError:
	print("Error: importing module jeedom.jeedom")
	sys.exit(1)

from ezsp.command import *
from ezsp.uart import *

class ezsp():

	def getCommandFromId(_id):
		for i in EZSP_COMMANDS:
			if EZSP_COMMANDS[i] == _id :
				return i
		return 'unknown'

	def read():
		message = b''
		while 1:
			time.sleep(0.02)
			byte = globals.JEEDOM_SERIAL.read()
			if byte != None :
				message += byte
				if byte == globals.FLAG:
					return message

	def decode(data):
		result = uart.decode_frame(data)
		if result['type'] != 'DATA' :
			return result
		logging.debug('Decode frame : '+str(result['frame_ezsp'].hex())+' with EZSP_VRSION '+str(globals.EZSP_VERSION))
		if globals.EZSP_VERSION >= 8:
			result['seq_ezsp'] = result['frame_ezsp'][0]
			result['frame_id'] = result['frame_ezsp'][3]
			result['data'] = result['frame_ezsp'][4:]
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
		result = bytes([globals.SEQUENCE])+bytes([0x00])+bytes([EZSP_COMMANDS[cmd]])+bytes(data)
		globals.SEQUENCE += 1
		if globals.SEQUENCE > 256 :
			globals.SEQUENCE = 0
		return result;

	def init():
		logging.info('Begin init ezsp')
		globals.JEEDOM_SERIAL.write(uart.make_rst_frame())
		time.sleep(1)
		resp = ezsp.decode(ezsp.read())
		if resp['type'] != 'RSTACK':
			raise Exception("No RSTACK received after RST")
		globals.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('version',[0x08])))
		time.sleep(1)
		resp = ezsp.decode(ezsp.read())
		if resp['type'] != 'DATA' or resp['frame_id'] != EZSP_COMMANDS['version']:
			raise Exception("Invalid EZSP version")
		globals.EZSP_VERSION=resp['data'][0]
		logging.info('EZSP version : '+str(resp['data'][0])+'.'+str(resp['data'][1])+'.'+str(resp['data'][2]+resp['data'][3]))

		if globals.PAN_ID == None :
			globals.PAN_ID = []
			for i in range(2):
			   globals.PAN_ID.append(int.from_bytes(os.urandom(1), byteorder="little"))
		if globals.EXT_PAN_ID == None :
			globals.EXT_PAN_ID = []
			for i in range(8):
			   globals.EXT_PAN_ID.append(int.from_bytes(os.urandom(1), byteorder="little"))
		parameters = []
		parameters += globals.EXT_PAN_ID
		parameters += globals.PAN_ID
		parameters.append(19) #Power setting
		parameters.append(24) #Channel
		parameters.append(0) #Join method
		parameters.append(0) #NWK Manager ID
		parameters.append(00) #NWP Update ID
		parameters += [15,20,25] #Channels Mask
		logging.info('Configure network : '+str(parameters))
		globals.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('formNetwork',parameters)))
		resp = ezsp.decode(ezsp.read())
		logging.info('End init ezsp successfull')

	def version_info():
		logging.info('Begin version info')
		globals.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('getValue',[0x11])))
		time.sleep(1)
		resp = ezsp.decode(ezsp.read())
		logging.info('Stack version : '+str(resp['data'][3])+'.'+str(resp['data'][4])+'.'+str(resp['data'][5]))

	def permitJoining(_second):
		logging.info('Permit joining for '+str(_second))
		globals.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('permitJoining',[_second])))

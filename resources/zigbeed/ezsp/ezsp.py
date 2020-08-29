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

    def decode(data):
        result = uart.decode_frame(data)
        logging.info('Raw ezsp frame : '+str(result))
        if 'frame_id' in result :
            result['command'] = ezsp.getCommandFromId(result['frame_id']);
        if 'data' in result :
            data = result['data']
            result['data'] = []
            for i in data :
                result['data'].append(i)

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
        resp = ezsp.decode(globals.JEEDOM_SERIAL.readbytes(7))
        logging.debug('Read : '+str(resp))
        if resp['type'] != 'RSTACK':
            raise Exception("No RSTACK received after RST")
        globals.JEEDOM_SERIAL.write(uart.make_ack_frame())
        globals.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('version',[0x08])))
        time.sleep(1)
        resp = ezsp.decode(globals.JEEDOM_SERIAL.readbytes(11))
        logging.debug('Read : '+str(resp))
        globals.JEEDOM_SERIAL.write(uart.make_ack_frame())
        if resp['type'] != 'DATA' or resp['frame_id'] != EZSP_COMMANDS['version']:
            raise Exception("Invalid EZSP version")
        globals.EZSP_VERSION=resp['data'][0]
        logging.info('EZSP version : '+str(resp['data'][0])+'.'+str(resp['data'][1])+'.'+str(resp['data'][2]+resp['data'][3]))
        logging.info('End init ezsp successfull')

    def version_info():
        logging.info('Begin version info')
        globals.JEEDOM_SERIAL.write(uart.make_data_frame(ezsp.make('getValue',[0x11])))
        time.sleep(1)
        resp = ezsp.decode(globals.JEEDOM_SERIAL.readbytes(16))
        globals.JEEDOM_SERIAL.write(uart.make_ack_frame())
        logging.debug('Read : '+str(resp))

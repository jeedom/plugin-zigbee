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

import shared
import logging
import string
import sys
import os
import time
import argparse
import datetime
import binascii
import re
import signal
import traceback
from optparse import OptionParser
from os.path import join
import json

try:
	from jeedom.jeedom import *
except ImportError:
	print("Error: importing module jeedom.jeedom")
	sys.exit(1)

try:
	from jeedom.jeedom import *
except ImportError:
	print("Error: importing module jeedom.jeedom")
	sys.exit(1)

def decodePacket(message):

	return

# ----------------------------------------------------------------------------

def read_socket(name):
	while 1:
		time.sleep(0.02)
		try:
			global JEEDOM_SOCKET_MESSAGE
			if not JEEDOM_SOCKET_MESSAGE.empty():
				logging.debug("Message received in socket JEEDOM_SOCKET_MESSAGE")
				message = json.loads(JEEDOM_SOCKET_MESSAGE.get())
				if message['apikey'] != _apikey:
					logging.error("Invalid apikey from socket : " + str(message))
					return
				if message['apikey'] != _apikey:
						logging.error("Invalid apikey from socket : " + str(message))
						return
				if message['cmd'] == 'add':
					logging.debug('Add device : '+str(message['device']))
					if 'id' in message['device'] :
						shared.KNOWN_DEVICES[message['device']['id']] = message['device']['id']
				elif message['cmd'] == 'remove':
					logging.debug('Remove device : '+str(message['device']))
					if 'id' in message['device'] and message['device']['id'] in shared.KNOWN_DEVICES :
						del shared.KNOWN_DEVICES[message['device']['id']]
				elif message['cmd'] == 'include_mode':
					if int(message['state']) == 1:
						logging.debug('Enter in include mode')
						shared.INCLUDE_MODE = True
					else :
						logging.debug('Leave in include mode')
						shared.INCLUDE_MODE = False
					shared.JEEDOM_COM.send_change_immediate({'include_mode' : message['state']});
				elif message['cmd'] == 'send':
					if isinstance(message['data'], list):
						for data in message['data']:
							try:
								send_zigbee(data)
							except Exception as e:
								logging.error('Send command to zigbee error : '+str(e))
					else:
						try:
							send_zigbee(message['data'])
						except Exception as e:
							logging.error('Send command to zigbee error : '+str(e))
		except Exception as e:
			logging.error('Error on read socket : '+str(e))

# ----------------------------------------------------------------------------

def send_zigbee(message):
	if test_zigbee(message):
		shared.JEEDOM_SERIAL.flushOutput()
		shared.JEEDOM_SERIAL.flushInput()
	else:
		logging.error("Invalid message from socket.")

# ----------------------------------------------------------------------------

def read_zigbee(name):
	message = b''
	while 1:
		try:
			resp = ezsp.decode(ezsp.read(None))
		except Exception as e:
			logging.error("Error in read_zigbee: " + str(e))
			logging.debug(traceback.format_exc())
			if str(e) == '[Errno 5] Input/output error':
				logging.error("Exit 1 because this exeption is fatal")
				shutdown()

# ----------------------------------------------------------------------------

def listen():
	logging.debug("Start listening...")
	jeedom_socket.open()
	shared.JEEDOM_SERIAL.open()
	shared.JEEDOM_SERIAL.flushOutput()
	shared.JEEDOM_SERIAL.flushInput()
	try:
		threading.Thread(target=read_socket,args=('socket',)).start()
		logging.debug('Read Socket Thread Launched')
	except KeyboardInterrupt:
		logging.error("KeyboardInterrupt, shutdown")
		shutdown()

	ezsp.init()
	shared.JEEDOM_SERIAL.flushInput()
	ezsp.version_info()

	try:
		threading.Thread(target=read_zigbee,args=('read',)).start()
		logging.debug('Read Device Thread Launched')
	except KeyboardInterrupt:
		logging.error("KeyboardInterrupt, shutdown")
		shutdown()
	ezsp.permitJoining(60)

# ----------------------------------------------------------------------------

def handler(signum=None, frame=None):
	logging.debug("Signal %i caught, exiting..." % int(signum))
	shutdown()

def shutdown():
	logging.debug("Shutdown")
	logging.debug("Removing PID file " + str(_pidfile))
	try:
		os.remove(_pidfile)
	except:
		pass
	try:
		jeedom_socket.close()
	except:
		pass
	try:
		shared.JEEDOM_SERIAL.close()
	except:
		pass
	logging.debug("Exit 0")
	sys.stdout.flush()
	os._exit(0)

# ----------------------------------------------------------------------------

_log_level = "error"
_socket_port = 55009
_socket_host = '127.0.0.1'
_device = 'auto'
_pidfile = '/tmp/zigbeed.pid'
_apikey = ''
_callback = ''
_serial_rate = 115200
_serial_timeout = 9
_cycle = 0.3
_config_file_path = '/var/www/html/plugins/zigbee/data/config.json'

parser = argparse.ArgumentParser(description='Zigbee Daemon for Jeedom plugin')
parser.add_argument("--device", help="Device", type=str)
parser.add_argument("--socketport", help="Socketport for server", type=str)
parser.add_argument("--loglevel", help="Log Level for the daemon", type=str)
parser.add_argument("--callback", help="Callback", type=str)
parser.add_argument("--apikey", help="Apikey", type=str)
parser.add_argument("--cycle", help="Cycle to send event", type=str)
parser.add_argument("--serialrate", help="Device serial rate", type=str)
parser.add_argument("--pid", help="Pid file", type=str)
args = parser.parse_args()

if args.device:
	_device = args.device
if args.socketport:
	_socket_port = int(args.socketport)
if args.loglevel:
	_log_level = args.loglevel
if args.callback:
	_callback = args.callback
if args.apikey:
	_apikey = args.apikey
if args.pid:
	_pidfile = args.pid
if args.serialrate:
	_serial_rate = int(args.serialrate)
if args.cycle:
	_cycle = float(args.cycle)

jeedom_utils.set_log_level(_log_level)

logging.info('Start zigbeed')
logging.info('Log level : '+str(_log_level))
logging.info('Socket port : '+str(_socket_port))
logging.info('Socket host : '+str(_socket_host))
logging.info('PID file : '+str(_pidfile))
logging.info('Device : '+str(_device))
logging.info('Apikey : '+str(_apikey))
logging.info('Callback : '+str(_callback))
logging.info('Cycle : '+str(_cycle))
logging.info('Serial rate : '+str(_serial_rate))
logging.info('Serial timeout : '+str(_serial_timeout))

if _device == 'auto':
	_device = jeedom_utils.find_tty_usb('1366','0105')

if _device is None:
	logging.error('No device found')
	shutdown()

logging.info('Find device : '+str(_device))

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

from ezsp.uart import *
from ezsp.ezsp import *


logging.info('Load config file path : '+str(_config_file_path))
with open(_config_file_path) as f:
	shared.CONFIG = json.load(f)

try:
	jeedom_utils.write_pid(str(_pidfile))
	shared.JEEDOM_COM = jeedom_com(apikey = _apikey,url = _callback,cycle=_cycle)
	if not shared.JEEDOM_COM.test():
		logging.error('Network communication issues. Please fixe your Jeedom network configuration.')
		shutdown()
	shared.JEEDOM_SERIAL = jeedom_serial(device=_device,rate=_serial_rate,timeout=_serial_timeout)
	jeedom_socket = jeedom_socket(port=_socket_port,address=_socket_host)
	listen()
except Exception as e:
	logging.error('Fatal error : '+str(e))
	logging.debug(traceback.format_exc())
	shutdown()

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

import globals
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
						globals.KNOWN_DEVICES[message['device']['id']] = message['device']['id']
				elif message['cmd'] == 'remove':
					logging.debug('Remove device : '+str(message['device']))
					if 'id' in message['device'] and message['device']['id'] in globals.KNOWN_DEVICES :
						del globals.KNOWN_DEVICES[message['device']['id']]
				elif message['cmd'] == 'include_mode':
					if int(message['state']) == 1:
						logging.debug('Enter in include mode')
						globals.INCLUDE_MODE = True
					else :
						logging.debug('Leave in include mode')
						globals.INCLUDE_MODE = False
					globals.JEEDOM_COM.send_change_immediate({'include_mode' : message['state']});
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
		globals.JEEDOM_SERIAL.flushOutput()
		globals.JEEDOM_SERIAL.flushInput()

	else:
		logging.error("Invalid message from socket.")

# ----------------------------------------------------------------------------

def read_zigbee(name):
	while 1:
		time.sleep(0.02)
		message = None
		try:
			byte = globals.JEEDOM_SERIAL.read()
		except Exception as e:
			logging.error("Error in read_zigbee: " + str(e))
			if str(e) == '[Errno 5] Input/output error':
				logging.error("Exit 1 because this exeption is fatal")
				shutdown()
		try:
			if byte != 0 and  byte != None :
				message = byte + globals.JEEDOM_SERIAL.readbytes(int.from_bytes(byte,'big'))
				logging.debug("Message: " + str(jeedom_utils.ByteToHex(message)))

		except OSError as e:
			logging.error("Error in read_zigbee on decode message : " + str(jeedom_utils.ByteToHex(message))+" => "+str(e))

# ----------------------------------------------------------------------------

def zigbee_init():
	globals.JEEDOM_SERIAL.write(b'\x1A\xC0\x38\xBC\x7E')
    # Wait for RSTACK FRAME (Reset ACK)
	time.sleep(1)
	resp = globals.JEEDOM_SERIAL.readbytes(7)
	logging.debug('Read : '+str(resp))
    # If we get an invalid RSTACK FRAME, fail detection
	if resp != b'\x1A\xC1\x02\x0B\x0A\x52\x7E':
		logging.error("Invalid ack")
		shutdown()
	globals.JEEDOM_SERIAL.write(b'\x80\x70\x78\x7E') #ack
    # EZSP Configuration Frame: version ID: 0x00
    # Note: Must be sent before any other EZSP commands
    # { FRAME CTR + EZSP [0x00 0x00 0x00 0x07] + CRC + FRAME END }
	globals.JEEDOM_SERIAL.write(b'\x00\x42\x21\xA8\x5C\x2C\xA0\x7E')
    # Wait for Data Response { protocolVersion, stackType, stackVersion }
    # this must be ACK'd
	time.sleep(1)
	resp = globals.JEEDOM_SERIAL.readbytes(11)
	logging.debug('Read : '+str(resp))
    # DATA ACK response frame
	globals.JEEDOM_SERIAL.write(b'\x81\x60\x59\x7E')
    # Check ncp data response:
    # 7.0.0 ncp example: { 01 42 a1 a8 5c 28 75 d5 3e 39 7e  }
	if resp[1:5] != b'\x42\xA1\xA8\x5C':
		logging.error("Invalid EZSP version")
		shutdown()

def zigbee_version():
	globals.JEEDOM_SERIAL.write(b'\x7D\x31\x43\x21\x02\x45\x85\xB2\x7E')
	time.sleep(1)
	resp = globals.JEEDOM_SERIAL.readbytes(16)
	logging.debug('Read : '+str(resp))
	versioninfo = trans(resp[1:])[5:]
	logging.debug('StackVersion : '+str(versioninfo[2]) + '.' + str(versioninfo[3]) + '.' + str(versioninfo[4]) + '-' + str(versioninfo[0]))

def listen():
	logging.debug("Start listening...")
	jeedom_socket.open()
	globals.JEEDOM_SERIAL.open()
	globals.JEEDOM_SERIAL.flushOutput()
	globals.JEEDOM_SERIAL.flushInput()
	try:
		threading.Thread(target=read_socket,args=('socket',)).start()
		logging.debug('Read Socket Thread Launched')
	except KeyboardInterrupt:
		logging.error("KeyboardInterrupt, shutdown")
		shutdown()

	zigbee_init()
	globals.JEEDOM_SERIAL.flushInput()
	zigbee_version()

	try:
		threading.Thread(target=read_zigbee,args=('read',)).start()
		logging.debug('Read Device Thread Launched')
	except KeyboardInterrupt:
		logging.error("KeyboardInterrupt, shutdown")
		shutdown()

def trans(s):
    seq = randSeqUpTo(len(s))
    out = []
    for i in range(len(s)):
        out.append(s[i] ^ seq[i])
    return out

def randSeqUpTo(n):
    curr = 0x42
    out = []
    while len(out) < n:
        out.append(curr)
        if bin(curr)[-1] == '0':
            curr = curr >> 1
        else:
            curr = (curr >> 1) ^ 0xB8
    return out
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
		globals.JEEDOM_SERIAL.close()
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

try:
	jeedom_utils.write_pid(str(_pidfile))
	globals.JEEDOM_COM = jeedom_com(apikey = _apikey,url = _callback,cycle=_cycle)
	if not globals.JEEDOM_COM.test():
		logging.error('Network communication issues. Please fixe your Jeedom network configuration.')
		shutdown()
	globals.JEEDOM_SERIAL = jeedom_serial(device=_device,rate=_serial_rate,timeout=_serial_timeout)
	jeedom_socket = jeedom_socket(port=_socket_port,address=_socket_host)
	listen()
except Exception as e:
	logging.error('Fatal error : '+str(e))
	logging.debug(traceback.format_exc())
	shutdown()

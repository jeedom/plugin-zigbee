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
import asyncio
import logging
import zhaquirks

import zigpy.types
from zigpy.zdo import types as zdo_t

try:
	from jeedom.jeedom import *
except ImportError:
	print("Error: importing module jeedom.jeedom")
	sys.exit(1)

from jsonPersisting import *
from mainListenner import *

try:
	from tornado.httpserver import HTTPServer
	from tornado.ioloop import IOLoop
except Exception as e:
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

from rest_server import *

# ----------------------------------------------------------------------------

async def start():
	zigpy_config={
		"json_database_path": _data_folder+"/network.json",
		"device": {
			"path": _device,
		},
		"network" : {
			"channel" : 15
		}
	}
	if shared.ZIGBEE_CONFIG != None:
		zigpy_config.network.channel = shared.ZIGBEE_CONFIG.channel
		if not _controler == 'zigate':
			zigpy_config.network.pan_id = shared.ZIGBEE_CONFIG.pan_id
			zigpy_config.network.extended_pan_id = shared.ZIGBEE_CONFIG.extended_pan_id
			zigpy_config.network.key = shared.ZIGBEE_CONFIG.key
		
	shared.ZIGPY = await JSONControllerApplication.new(
		config=JSONControllerApplication.SCHEMA(zigpy_config),
		auto_form=True,
		start_radio=True,
	)
	listener = MainListener(shared.ZIGPY)
	shared.ZIGPY.add_listener(listener)
	# Have every device in the database fire the same event so you can attach listeners
	for device in shared.ZIGPY.devices.values():
		listener.device_initialized(device, new=False)
	# Run forever
	await asyncio.get_running_loop().create_future()

def handler(signum=None, frame=None):
	logging.debug("Signal %i caught, exiting..." % int(signum))
	shutdown()

def shutdown():
	logging.debug("Shutdown")
	if shared.ZIGPY != None:
		shared.ZIGPY.shutdown()
	logging.debug("Removing PID file " + str(_pidfile))
	try:
		os.remove(_pidfile)
	except:
		pass
	logging.debug("Exit 0")
	sys.stdout.flush()
	os._exit(0)

# ----------------------------------------------------------------------------

_log_level = "error"
_port_server = 8089
_device = 'auto'
_pidfile = '/tmp/zigbeed.pid'
_apikey = ''
_callback = ''
_cycle = 0.3
_controler = 'ezsp'
_data_folder = '/tmp'
_socket_host='127.0.0.1'

parser = argparse.ArgumentParser(description='Zigbee Daemon for Jeedom plugin')
parser.add_argument("--device", help="Device", type=str)
parser.add_argument("--loglevel", help="Log Level for the daemon", type=str)
parser.add_argument("--callback", help="Callback", type=str)
parser.add_argument("--apikey", help="Apikey", type=str)
parser.add_argument("--cycle", help="Cycle to send event", type=str)
parser.add_argument("--pid", help="Pid file", type=str)
parser.add_argument("--controler", help="Controler type (ezsp,deconz,zigate,cc...)", type=str)
parser.add_argument("--data_folder", help="Data folder", type=str)
parser.add_argument("--port", help="Port for Zigbee server", type=str)
args = parser.parse_args()

if args.device:
	_device = args.device
if args.loglevel:
	_log_level = args.loglevel
if args.callback:
	_callback = args.callback
if args.apikey:
	_apikey = args.apikey
if args.pid:
	_pidfile = args.pid
if args.cycle:
	_cycle = float(args.cycle)
if args.controler:
	_controler = args.controler
if args.cycle:
	_data_folder = args.data_folder
if args.port:
	_port_server = args.port

jeedom_utils.set_log_level(_log_level)

logging.info('Start zigbeed')
logging.info('Log level : '+str(_log_level))
logging.info('PID file : '+str(_pidfile))
logging.info('Device : '+str(_device))
logging.info('Apikey : '+str(_apikey))
logging.info('Callback : '+str(_callback))
logging.info('Cycle : '+str(_cycle))
logging.info('Controler : '+str(_controler))
logging.info('Data folder : '+str(_data_folder))

shared.APIKEY = _apikey
if path.exists(_data_folder+'/config.json'):
	with open(_data_folder+'/config.json') as config_file:
		shared.ZIGBEE_CONFIG = json.load(config_file)

if _controler == 'ezsp' :
	from bellows.zigbee.application import ControllerApplication
elif _controler == 'deconz' :
	from zigpydeconz.zigbee.application import ControllerApplication
elif _controler == 'zigate' :
	from zigpyzigate.zigbee.application import ControllerApplication
elif _controler == 'cc' :
	from zigpycc.zigbee.application import ControllerApplication
elif _controler == 'xbee' :
	from zigpyxbee.zigbee.application import ControllerApplication


if _device == 'auto':
	if _controler == 'ezsp' :
		_device = jeedom_utils.find_tty_usb('1366','0105')
	if _controler == 'deconz' :
		_device = jeedom_utils.find_tty_usb('1cf1','0030')

if _device is None:
	logging.error('No device found')
	shutdown()

logging.info('Find device : '+str(_device))

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

try:
	jeedom_utils.write_pid(str(_pidfile))
	shared.JEEDOM_COM = jeedom_com(apikey = _apikey,url = _callback,cycle=_cycle)
	if not shared.JEEDOM_COM.test():
		logging.error('Network communication issues. Please fixe your Jeedom network configuration.')
		shutdown()
	http_server = HTTPServer(shared.REST_SERVER)
	http_server.listen(_port_server, address=_socket_host)
	IOLoop.instance().start()
	asyncio.run(start())
except Exception as e:
	logging.error('Fatal error : '+str(e))
	logging.debug(traceback.format_exc())
	shutdown()

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
import zqueue
import zigpy.config

try:
	from jeedom.jeedom import *
except ImportError:
	print("Error: importing module jeedom.jeedom")
	sys.exit(1)

from listener import *

try:
	from tornado.httpserver import HTTPServer
	from tornado.ioloop import IOLoop
except Exception as e:
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

from restServer import *

# ----------------------------------------------------------------------------

async def start_zigbee():
	try:
		zigpy_config={
			zigpy.config.CONF_DATABASE : _data_folder+"/network_"+_controller+".db",
			zigpy.config.CONF_DEVICE : {
				"path": _device,
			},
			zigpy.config.CONF_NWK : {
				zigpy.config.CONF_NWK_CHANNEL : _channel
			}
		}
		if shared.CONTROLLER == 'ezsp' and shared.SUB_CONTROLLER == 'elelabs' :
			zigpy_config[zigpy.config.CONF_DEVICE]['baudrate'] = 115200
			zigpy_config['ezsp'] = {
				"CONFIG_APS_UNICAST_MESSAGE_COUNT": 12,
				"CONFIG_SOURCE_ROUTE_TABLE_SIZE": 16,
				"CONFIG_ADDRESS_TABLE_SIZE": 8
			}
		logging.debug('[start_zigbee] Init zigbee network with config : '+str(zigpy_config))
		shared.ZIGPY = await ControllerApplication.new(
			config=ControllerApplication.SCHEMA(zigpy_config),
			auto_form=True,
			start_radio=True,
		)
		listener = Listener(shared.ZIGPY)
		shared.ZIGPY.add_listener(listener)
		for device in shared.ZIGPY.devices.values():
			listener.device_initialized(device, new=False)

		logging.debug('[start_zigbee] Init and start http server : '+str(zigpy_config))
		http_server = HTTPServer(shared.REST_SERVER)
		http_server.listen(_socketport, address=_socket_host)
		asyncio.create_task(zqueue.handle())
		logging.debug('[start_zigbee] Start zigbee network')
		await asyncio.get_running_loop().create_future()
	except Exception as e:
		logging.error('[start_zigbee] Fatal error : '+str(e))
		logging.debug(traceback.format_exc())
		shutdown()

def handler(signum=None, frame=None):
	logging.debug("Signal %i caught, exiting..." % int(signum))
	shutdown()

def shutdown():
	logging.debug("Shutdown")
	if shared.ZIGPY != None:
		shared.ZIGPY.shutdown()
		time.sleep(2)
	IOLoop.instance().stop()
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
_controller = 'ezsp'
_sub_controller = None
_data_folder = '/tmp'
_socket_host='127.0.0.1'
_channel=15
_instance=1

parser = argparse.ArgumentParser(description='Zigbee Daemon for Jeedom plugin')
parser.add_argument("--device", help="Device", type=str)
parser.add_argument("--loglevel", help="Log Level for the daemon", type=str)
parser.add_argument("--callback", help="Callback", type=str)
parser.add_argument("--apikey", help="Apikey", type=str)
parser.add_argument("--cycle", help="Cycle to send event", type=str)
parser.add_argument("--pid", help="Pid file", type=str)
parser.add_argument("--controller", help="Controller type (ezsp,deconz,zigate,cc...)", type=str)
parser.add_argument("--sub_controller", help="Sub-controller type (elelabs...)", type=str)
parser.add_argument("--data_folder", help="Data folder", type=str)
parser.add_argument("--socketport", help="Port for Zigbee server", type=str)
parser.add_argument("--channel", help="Channel for Zigbee network", type=str)
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
if args.channel:
	_channel = int(args.channel)
if args.controller:
	_controller = args.controller
if args.sub_controller:
	_sub_controller = args.sub_controller
if args.cycle:
	_data_folder = args.data_folder
if args.socketport:
	_socketport = args.socketport

jeedom_utils.set_log_level(_log_level)

logging.info('Start zigbeed')
logging.info('Log level : '+str(_log_level))
logging.info('PID file : '+str(_pidfile))
logging.info('Device : '+str(_device))
logging.info('Apikey : '+str(_apikey))
logging.info('Callback : '+str(_callback))
logging.info('Cycle : '+str(_cycle))
logging.info('Controller : '+str(_controller))
logging.info('Channel : '+str(_channel))
logging.info('Data folder : '+str(_data_folder))

shared.APIKEY = _apikey
if os.path.exists(_data_folder+'/config.json'):
	with open(_data_folder+'/config.json') as config_file:
		shared.ZIGBEE_CONFIG = json.load(config_file)

if _controller == 'ezsp' :
	from bellows.zigbee.application import ControllerApplication
elif _controller == 'deconz' :
	from zigpy_deconz.zigbee.application import ControllerApplication
elif _controller == 'zigate' :
	from zigpy_zigate.zigbee.application import ControllerApplication
elif _controller == 'cc' :
	from zigpy_cc.zigbee.application import ControllerApplication
elif _controller == 'xbee' :
	from zigpy_xbee.zigbee.application import ControllerApplication
elif _controller == 'znp' :
	from zigpy_znp.zigbee.application import ControllerApplication

shared.CONTROLLER = _controller
shared.SUB_CONTROLLER = _sub_controller

if _device == 'auto':
	if _controller == 'ezsp' :
		_device = jeedom_utils.find_tty_usb('1366','0105')
		if _device == None:
			_device = jeedom_utils.find_tty_usb('1a86','7523') # Elelabs USB key
	if _controller == 'deconz' :
		_device = jeedom_utils.find_tty_usb('1cf1','0030')
	if _controller == 'zigate' :
		_device = jeedom_utils.find_tty_usb('067b','2303')

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
	asyncio.run(start_zigbee())
except Exception as e:
	logging.error('Fatal error : '+str(e))
	logging.debug(traceback.format_exc())
	shutdown()

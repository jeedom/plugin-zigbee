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
import json

try:
	from jeedom.jeedom import *
except ImportError as error :
	print("Error: importing module jeedom.jeedom : " + str(error))
	sys.exit(1)

try:
	from tornado.httpserver import HTTPServer
	from tornado.ioloop import IOLoop
except Exception as e:
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

# ----------------------------------------------------------------------------

def merge_dict(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a

async def start_zigbee():
	try:
		zhaquirks.setup({
			zhaquirks.const.CUSTOM_QUIRKS_PATH : os.path.dirname(os.path.realpath(__file__))+'/quirks'
		})
		zigpy_config={
			zigpy.config.CONF_DATABASE : _data_folder+"/network_"+_controller+".db",
			zigpy.config.CONF_DEVICE : {
				"path": _device,
			},
			zigpy.config.CONF_NWK : {
				zigpy.config.CONF_NWK_CHANNEL : _channel
			}
		}
		if _folder_OTA is not None :
			zigpy_config[zigpy.config.CONF_OTA] = {
				zigpy.config.CONF_OTA_DIR  : _folder_OTA,
				zigpy.config.CONF_OTA_IKEA : True,
				zigpy.config.CONF_OTA_IKEA_URL : "http://fw.ota.homesmart.ikea.net/feed/version_info.json",
				zigpy.config.CONF_OTA_LEDVANCE : True
			}
		if shared.CONTROLLER == 'ezsp' :
			if shared.SUB_CONTROLLER == 'elelabs' :
				zigpy_config[zigpy.config.CONF_DEVICE]['baudrate'] = 115200
				zigpy_config['ezsp'] = {
					"CONFIG_APS_UNICAST_MESSAGE_COUNT": 12,
					"CONFIG_SOURCE_ROUTE_TABLE_SIZE": 16,
					"CONFIG_ADDRESS_TABLE_SIZE": 8
				}
		if _zigpy_advance_config is not None:
			with open(_zigpy_advance_config) as f:
  				advance_config = json.load(f)
			zigpy_config = merge_dict(zigpy_config,advance_config)	
		logging.info('[start_zigbee] Init zigbee network with config : '+str(zigpy_config))
		shared.ZIGPY = await ControllerApplication.new(
			config=ControllerApplication.SCHEMA(zigpy_config),
			auto_form=True,
			start_radio=True,
		)
		if shared.CONTROLLER == 'ezsp' :
			try:
				asyncio.ensure_future(shared.ZIGPY._ezsp.setRadioChannel(_channel))
			except Exception as e:
				pass

		listener = Listener(shared.ZIGPY)
		shared.ZIGPY.add_listener(listener)
		for device in shared.ZIGPY.devices.values():
			listener.device_initialized(device, new=False)

		logging.info('[start_zigbee] Init and start http server : '+str(zigpy_config))
		http_server = HTTPServer(shared.REST_SERVER)
		http_server.listen(_socketport, address=_socket_host)
		asyncio.create_task(zqueue.handle())
		logging.info('[start_zigbee] Start zigbee network')
		await asyncio.get_running_loop().create_future()
	except Exception as e:
		logging.error('[start_zigbee] Fatal error : '+str(e))
		logging.info(traceback.format_exc())
		shutdown()

def handler(signum=None, frame=None):
	logging.info("Signal %i caught, exiting..." % int(signum))
	shutdown()

def shutdown():
	logging.info("Shutdown")
	if shared.ZIGPY != None:
		shared.ZIGPY.shutdown()
		time.sleep(2)
	IOLoop.instance().stop()
	logging.info("Removing PID file " + str(_pidfile))
	try:
		os.remove(_pidfile)
	except:
		pass
	logging.info("Exit 0")
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
_device_folder = '/tmp'
_socket_host ='127.0.0.1'
_channel = 15
_instance = 1
_folder_OTA = None
_zigpy_advance_config = None

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
parser.add_argument("--device_folder", help="Data folder", type=str)
parser.add_argument("--socketport", help="Port for Zigbee server", type=str)
parser.add_argument("--channel", help="Channel for Zigbee network", type=str)
parser.add_argument("--folder_OTA", help="Allow device OTA update", type=str)
parser.add_argument("--zigpy_advance_config", help="Allow to override zigpy initial configuration (json format file)", type=str)
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
if args.data_folder:
	_data_folder = args.data_folder
if args.device_folder:
	_device_folder = args.device_folder
if args.socketport:
	_socketport = args.socketport
if args.folder_OTA:
	_folder_OTA = args.folder_OTA
if args.zigpy_advance_config:
	_zigpy_advance_config = args.zigpy_advance_config
	if not os.path.isfile(_zigpy_advance_config):
		logging.info('Advance config file path invalid : '+str(_zigpy_advance_config))
		_zigpy_advance_config = None

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
logging.info('Device folder : '+str(_device_folder))
logging.info('Folder OTA : '+str(_folder_OTA))
logging.info('Zigpy advance configuration file : '+str(_zigpy_advance_config))

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
shared.DEVICE_FOLDER=_device_folder

if os.path.exists(shared.DEVICE_FOLDER):
	for file in os.listdir(shared.DEVICE_FOLDER):
		if file.endswith(".json"):
			ieee = file.replace('.json','')
			with open(shared.DEVICE_FOLDER+'/'+file) as specific_file:
				try:
					shared.DEVICE_SPECIFIC[ieee] = json.load(specific_file)
					logging.info('Add specific configuration for '+str(ieee)+' to '+str(shared.DEVICE_SPECIFIC[ieee]))
				except Exception as e:
					pass

if _device == 'auto':
	if _controller == 'ezsp' :
		_device = jeedom_utils.find_tty_usb('1366','0105')
		if _device == None:
			_device = jeedom_utils.find_tty_usb('1a86','7523') # Elelabs USB key
	if _controller == 'deconz' :
		_device = jeedom_utils.find_tty_usb('1cf1','0030')
		if _device == None:
			_device = jeedom_utils.find_tty_usb('0403','6015')
	if _controller == 'zigate' :
		_device = jeedom_utils.find_tty_usb('067b','2303')
		if _device is None:
			_device = jeedom_utils.find_tty_usb('0403','6015')

if _device is None:
	logging.error('No device found')
	shutdown()

logging.info('Find device : '+str(_device))

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)
import zhaquirks
import zqueue
import zigpy.config
from listener import *
from restServer import *
try:
	jeedom_utils.write_pid(str(_pidfile))
	shared.JEEDOM_COM = jeedom_com(apikey = _apikey,url = _callback,cycle=_cycle)
	if not shared.JEEDOM_COM.test():
		logging.error('Network communication issues. Please fixe your Jeedom network configuration.')
		shutdown()
	asyncio.run(start_zigbee())
except Exception as e:
	logging.error('Fatal error : '+str(e))
	logging.info(traceback.format_exc())
	shutdown()

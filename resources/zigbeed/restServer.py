#!flask/bin/python

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
import binascii
import logging
import os
import shared,utils
import json
import traceback
import asyncio
import registries
from map import *
try:
	from tornado.web import RequestHandler,Application,HTTPError
except Exception as e:
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

class ApplicationHandler(RequestHandler):
	def prepare(self):
		utils.check_apikey(self.request.headers.get("autorization", ""))
		self.json_args = None
		try:
			if self.request.headers.get("Content-Type", "").startswith("application/json"):
				self.json_args = json.loads(self.request.body)
		except Exception as e:
			self.json_args = None
		logging.debug('Json arg : '+str(self.json_args))

	async def get(self,arg1):
		try:
			if arg1 == 'info':
				info = await utils.serialize_application()
				return self.write(utils.format_json_result(success=True,data=info))
			raise Exception("No method found")
		except Exception as e:
			logging.debug(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def put(self,arg1):
		try:
			if arg1 == 'include':
				await shared.ZIGPY.permit(self.json_args['duration'])
				return self.write(utils.format_json_result(success=True))
			raise Exception("No method found")
		except Exception as e:
			logging.debug(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

class NetworkHandler(RequestHandler):
	def prepare(self):
		utils.check_apikey(self.request.headers.get("autorization", ""))
		self.json_args = None
		try:
			if self.request.headers.get("Content-Type", "").startswith("application/json"):
				self.json_args = json.loads(self.request.body)
		except Exception as e:
			self.json_args = None
		logging.debug('Json arg : '+str(self.json_args))

	async def get(self,arg1):
		try:
			if arg1 == 'map':
				tb = TopologyBuilder(shared.ZIGPY)
				map = await tb.build()
				result = [];
				for i in map:
					result.append(map[i].json())
				return self.write(utils.format_json_result(success=True,data=result))
			raise Exception("No method found")
		except Exception as e:
			logging.debug(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

class DeviceHandler(RequestHandler):
	def prepare(self):
		utils.check_apikey(self.request.headers.get("autorization", ""))
		self.json_args = None
		try:
			if self.request.headers.get("Content-Type", "").startswith("application/json"):
				self.json_args = json.loads(self.request.body)
		except Exception as e:
			self.json_args = None
		logging.debug('Json arg : '+str(self.json_args))

	async def get(self,arg1):
		try:
			if arg1 == 'all':
				result = []
				for device in shared.ZIGPY.devices.values():
					values = await utils.serialize_device(device)
					result.append(values)
				return self.write(utils.format_json_result(success=True,data=result))
			if arg1 == 'info':
				device = utils.findDevice(self.get_argument('ieee',''))
				if device == None:
					raise Exception("Device not found")
				values = await utils.serialize_device(device)
				return self.write(utils.format_json_result(success=True,data=values))
			raise Exception("No method found")
		except Exception as e:
			logging.debug(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def post(self,arg1):
		try:
			if arg1 == 'attributes':
				device = utils.findDevice(self.json_args['ieee'])
				if device == None:
					raise Exception("Device not found")
				if not self.json_args['endpoint'] in device.endpoints:
					raise Exception("Endpoint not found : "+str(self.json_args['endpoint']))
				endpoint = device.endpoints[self.json_args['endpoint']]
				if self.json_args['cluster_type'] == 'in':
					if not self.json_args['cluster'] in endpoint.in_clusters:
						raise Exception("Cluster not found : "+str(self.json_args['cluster']))
					cluster = endpoint.in_clusters[self.json_args['cluster']]
				else:
					if not self.json_args['cluster'] in endpoint.out_clusters:
						raise Exception("Cluster not found : "+str(self.json_args['cluster']))
					cluster = endpoint.out_clusters[self.json_args['cluster']]
				if self.json_args['allowCache'] == 1:
					values = await cluster.read_attributes(self.json_args['attributes'],True)
				else:
					values = await cluster.read_attributes(self.json_args['attributes'])
				return self.write(utils.format_json_result(success=True,data=values))
		except Exception as e:
			logging.debug(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def put(self,arg1):
		try:
			if arg1 == 'attributes':
				device = utils.findDevice(self.json_args['ieee'])
				if device == None:
					raise Exception("Device not found")
				if not self.json_args['endpoint'] in device.endpoints:
					raise Exception("Endpoint not found : "+str(self.json_args['endpoint']))
				endpoint = device.endpoints[self.json_args['endpoint']]
				if self.json_args['cluster_type'] == 'in':
					if not self.json_args['cluster'] in endpoint.in_clusters:
						raise Exception("Cluster not found : "+str(self.json_args['cluster']))
					cluster = endpoint.in_clusters[self.json_args['cluster']]
				else:
					if not self.json_args['cluster'] in endpoint.out_clusters:
						raise Exception("Cluster not found : "+str(self.json_args['cluster']))
					cluster = endpoint.out_clusters[self.json_args['cluster']]
				attributes = {}
				for i in self.json_args['attributes']:
					attributes[int(i)] = self.json_args['attributes'][i]
				await cluster.write_attributes(attributes)
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'initialize':
				device = utils.findDevice(self.json_args['ieee'])
				if device == None :
					raise Exception("Device not found")
				await utils.initialize_device_cluster(device)
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'command':
				device = utils.findDevice(self.json_args['ieee'])
				if device == None :
					raise Exception("Device not found")
				for cmd in self.json_args['cmd']:
					if not cmd['endpoint'] in device.endpoints:
						raise Exception("Endpoint not found : "+str(cmd['endpoint']))
					endpoint = device.endpoints[cmd['endpoint']]
					if not hasattr(endpoint,cmd['cluster']):
						raise Exception("Cluster not found : "+str(cmd['cluster']))
					cluster = getattr(endpoint, cmd['cluster'])
					if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id],cmd['command']):
						logging.info("Use specific command action")
						command = getattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id], cmd['command'])
						if 'await' in cmd:
							await command(cluster,cmd)
						else:
							asyncio.ensure_future(command(cluster,cmd))
						continue
					if not hasattr(cluster,cmd['command']):
						raise Exception("Command not found : "+str(cmd['command']))
					command = getattr(cluster, cmd['command'])
					if 'args' in cmd:
						args = cmd['args']
						if 'await' in cmd:
							await command(*args)
						else:
							asyncio.ensure_future(command(*args))
					else:
						if 'await' in cmd:
							await command()
						else:
							asyncio.ensure_future(command())
				return self.write(utils.format_json_result(success=True))
			raise Exception("No method found")
		except Exception as e:
			logging.debug(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def delete(self):
		try:
			device = utils.findDevice(self.json_args['ieee'])
			if device == None :
				raise Exception("Device not found")
			await shared.ZIGPY.remove(device.ieee)
			return self.write(utils.format_json_result(success=True))
		except Exception as e:
			logging.debug(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))


shared.REST_SERVER = Application([
		(r"/application/([^/]+)?", ApplicationHandler),
		(r"/network/([^/]+)?", NetworkHandler),
		(r"/device/([^/]+)?", DeviceHandler),
		(r"/device", DeviceHandler)
	])

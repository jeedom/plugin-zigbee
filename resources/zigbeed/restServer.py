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
import logging
import os
import shared,utils
import json
import time
import traceback
import asyncio
import registries
import zdevices
import zqueue
import zigpy
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
		logging.debug('[ApplicationHandler.prepare] Json arg : '+str(self.json_args))

	async def get(self,arg1):
		try:
			if arg1 == 'info':
				info = await utils.serialize_application()
				return self.write(utils.format_json_result(success=True,data=info))
			raise Exception("No method found for "+str(arg1))
		except Exception as e:
			logging.debug(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def put(self,arg1):
		try:
			if arg1 == 'include':
				await shared.ZIGPY.permit(self.json_args['duration'])
				gateway = shared.ZIGPY.get_device(nwk=0)
				try:
					if zigpy.zcl.clusters.general.GreenPowerProxy.enpoint_id in gateway.endpoints and zigpy.zcl.clusters.general.GreenPowerProxy.cluster_id in gateway.endpoints[zigpy.zcl.clusters.general.GreenPowerProxy.enpoint_id].out_clusters:
						await gateway.endpoints[zigpy.zcl.clusters.general.GreenPowerProxy.enpoint_id].out_clusters[zigpy.zcl.clusters.general.GreenPowerProxy.cluster_id].permit(self.json_args['duration'])
				except:
					pass
				return self.write(utils.format_json_result(success=True))
			raise Exception("No method found for "+str(arg1))
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
		logging.debug('[NetworkHandler.prepare] Json arg : '+str(self.json_args))

	async def get(self,arg1):
		try:
			if arg1 == 'map':
				tb = TopologyBuilder(shared.ZIGPY)
				map = await tb.build()
				result = [];
				for i in map:
					result.append(map[i].json())
				return self.write(utils.format_json_result(success=True,data=result))
			raise Exception("No method found for "+str(arg1))
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
		logging.debug('[DeviceHandler.prepare] Json arg : '+str(self.json_args))

	async def get(self,arg1):
		try:
			if arg1 == 'all':
				result = []
				for device in shared.ZIGPY.devices.values():
					values = await zdevices.serialize(device)
					result.append(values)
				return self.write(utils.format_json_result(success=True,data=result))
			if arg1 == 'info':
				device = zdevices.find(self.get_argument('ieee',''))
				if device == None:
					raise Exception("Device not found")
				values = await zdevices.serialize(device)
				return self.write(utils.format_json_result(success=True,data=values))
			raise Exception("No method found for "+str(arg1))
		except Exception as e:
			logging.debug(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def post(self,arg1):
		try:
			if arg1 == 'attributes':
				device = zdevices.find(self.json_args['ieee'])
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
				manufacturer = None
				if 'manufacturer' in self.json_args and self.json_args['manufacturer'] != '' :
					manufacturer = self.json_args['manufacturer']
				if self.json_args['allowCache'] == 1:
					values = await cluster.read_attributes(self.json_args['attributes'],True,manufacturer=manufacturer)
				else:
					values = await cluster.read_attributes(self.json_args['attributes'],manufacturer=manufacturer)
				logging.debug('[DeviceHandler.post] Attribute Value received : '+str(values))
				return self.write(utils.format_json_result(success=True,data=values))
		except Exception as e:
			logging.debug(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def put(self,arg1):
		try:
			if arg1 == 'attributes':
				try:
					await zdevices.write_attributes(self.json_args)
				except Exception as e:
					if 'allowQueue' in self.json_args and self.json_args['allowQueue'] :
						logging.debug('[DeviceHandler.put] Failed on write attribute'+str(self.json_args)+' => '+str(e))
						logging.debug('[DeviceHandler.put] Replan write attribut later')
						zqueue.add('write_attributes',10,self.json_args,3)
					else:
						raise
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'gpDevice':
				device = zdevices.find(self.json_args['ieee'])
				if device == None :
					if not 'type' in self.json_args or self.json_args['type'] == '' :
						self.json_args['type'] = None
					device = shared.ZIGPY.devices[shared.ZIGPY].endpoints[zigpy.zcl.clusters.general.GreenPowerProxy.endpoint_id].out_clusters[zigpy.zcl.clusters.general.GreenPowerProxy.cluster_id].create_device(utils.convertStrToIEU64(self.json_args['ieee']),self.json_args['type'])
				if self.json_args['key'] == '':
					device.endpoints[zigpy.zcl.clusters.general.GreenPowerProxy.endpoint_id].in_clusters[zigpy.zcl.clusters.general.GreenPowerProxy.cluster_id].setKey(None)
				else:
					device.endpoints[zigpy.zcl.clusters.general.GreenPowerProxy.endpoint_id].in_clusters[zigpy.zcl.clusters.general.GreenPowerProxy.cluster_id].setKey(int(self.json_args['key'], 16))
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'initialize':
				device = zdevices.find(self.json_args['ieee'])
				if device == None :
					raise Exception("Device not found")
				await zdevices.initialize(device)
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'get_basic_info':
				device = zdevices.find(self.json_args['ieee'])
				if device == None :
					raise Exception("Device not found")
				await zdevices.get_basic_info(device)
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'command':
				try:
					await zdevices.command(self.json_args)
				except Exception as e:
					if 'allowQueue' in self.json_args and self.json_args['allowQueue']:
						logging.debug('[DeviceHandler.put] Failed on command'+str(self.json_args)+' => '+str(e))
						logging.debug('[DeviceHandler.put] Replan command later')
						zqueue.add('command',5,self.json_args,1)
					else:
						raise
				return self.write(utils.format_json_result(success=True))
			raise Exception("No method found for "+str(arg1))
		except Exception as e:
			logging.debug(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def delete(self):
		try:
			device = zdevices.find(self.json_args['ieee'])
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

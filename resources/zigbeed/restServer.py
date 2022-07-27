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
import zgroups
import zqueue
import zigpy
import zigpy.zdo.types as zdo_types
import zgp

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
		logging.info('[ApplicationHandler.prepare] Json arg : '+str(self.json_args))

	async def get(self,arg1):
		try:
			if arg1 == 'info':
				info = await utils.serialize_application()
				return self.write(utils.format_json_result(success=True,data=info))
			raise Exception("[ApplicationHandler.get] No method found for "+str(arg1))
		except Exception as e:
			logging.info(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def put(self,arg1):
		try:
			if arg1 == 'include':
				await shared.ZIGPY.permit(self.json_args['duration'])
				gateway = shared.ZIGPY.get_device(nwk=0)
				try:
					if not zgp.endpoint_id in gateway.endpoints:
						logging.info('[ApplicationHandler.put.include] No ZGP endpoint found, create it')
						ep = gateway.add_endpoint(zgp.endpoint_id)
						ep.status =  zigpy.endpoint.Status.ZDO_INIT
						ep.profile_id = zigpy.profiles.zha.PROFILE_ID
						ep.device_type = zgp.device_type
						ep.add_output_cluster(zgp.cluster_id)
					logging.info('[ApplicationHandler.put.include] Permit ZGP include')
					await zgp.permit(self.json_args['duration'])
				except Exception as e:
					logging.info(traceback.format_exc())
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'neighbors_scan':
				await shared.ZIGPY.get_device(ieee=shared.ZIGPY.ieee).neighbors.scan()
				return self.write(utils.format_json_result(success=True))
			raise Exception("[ApplicationHandler.put] No method found for "+str(arg1))
		except Exception as e:
			logging.info(traceback.format_exc())
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
		logging.info('[NetworkHandler.prepare] Json arg : '+str(self.json_args))

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
			logging.info(traceback.format_exc())
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
		logging.info('[DeviceHandler.prepare] Json arg : '+str(self.json_args))

	async def get(self,arg1):
		try:
			if arg1 == 'all':
				result = []
				with_attributes = self.get_argument('with_attributes',1)
				for device in shared.ZIGPY.devices.values():
					values = await zdevices.serialize(device,with_attributes)
					result.append(values)
				return self.write(utils.format_json_result(success=True,data=result))
			if arg1 == 'info':
				device = zdevices.find(self.get_argument('ieee',''))
				if device == None:
					raise Exception("Device not found")
				values = await zdevices.serialize(device)
				return self.write(utils.format_json_result(success=True,data=values))
			if arg1 == 'groupable':
				result = []
				for device in shared.ZIGPY.devices.values():
					if zdevices.is_groupable(device):
						values = await zdevices.serialize(device)
						result.append(values)
				return self.write(utils.format_json_result(success=True,data=result))
			raise Exception("No method found for "+str(arg1))
		except Exception as e:
			logging.info(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def post(self,arg1):
		try:
			if arg1 == 'attributes':
				if self.json_args == None :
					raise Exception("No arg for post "+str(arg1))
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
				for i in range(len(values)):
					for j in values[i]:
						if isinstance(values[i][j], (bytes)):
							values[i][j] = values[i][j].hex()
				logging.info('[DeviceHandler.post] Attribute Value received : '+str(values))
				return self.write(utils.format_json_result(success=True,data=values))
		except Exception as e:
			logging.info(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def put(self,arg1):
		try:
			if arg1 == 'attributes':
				if self.json_args == None :
					raise Exception("No arg for put "+str(arg1))
				try:
					await zdevices.write_attributes(self.json_args)
				except Exception as e:
					if 'allowQueue' in self.json_args and self.json_args['allowQueue'] :
						logging.info('[DeviceHandler.put/attributes] Failed on write attribute'+str(self.json_args)+' => '+str(e)+'. Replan write attribut later')
						zqueue.add('write_attributes',10,self.json_args,3)
					else:
						raise
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'reportConfig':
				if self.json_args == None :
					raise Exception("No arg for put "+str(arg1))
				device = zdevices.find(self.json_args['ieee'])
				if device == None:
					raise Exception("Device not found")
				for attribute in self.json_args['attributes']:
					if not attribute['endpoint'] in device.endpoints:
						raise Exception("Endpoint not found : "+str(attribute['endpoint']))
					endpoint = device.endpoints[attribute['endpoint']]
					if attribute['cluster_type'] == 'in':
						if not attribute['cluster'] in endpoint.in_clusters:
							raise Exception("Cluster not found : "+str(attribute['cluster']))
						cluster = endpoint.in_clusters[attribute['cluster']]
					else:
						if not attribute['cluster'] in endpoint.out_clusters:
							raise Exception("Cluster not found : "+str(attribute['cluster']))
						cluster = endpoint.out_clusters[attribute['cluster']]
					kwargs = {}
					for attr in attribute['attributes']:
						await cluster.configure_reporting(attr['name'],attr['min_report_int'],attr['max_report_int'],attr['reportable_change'], **kwargs)
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'gpDevice':
				if self.json_args == None :
					raise Exception("No arg for put "+str(arg1))
				deviceAdded = False
				device = zdevices.find(self.json_args['ieee'])
				if device == None :
					if not 'type' in self.json_args or self.json_args['type'] == '' :
						self.json_args['type'] = None
					device = zgp.create_device(utils.convertStrToIEU64(self.json_args['ieee']),self.json_args['type'],True)
					deviceAdded = True
				if device is None:
					raise Exception("Can not create device")
				if self.json_args['key'] == '':
					zgp.setKey(device,None)
				else:
					zgp.setKey(device,int(self.json_args['key'], 16))
				if deviceAdded:
					shared.JEEDOM_COM.send_change_immediate({'device_initialized' : self.json_args['ieee']});
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'initialize':
				if self.json_args == None :
					raise Exception("No arg for put "+str(arg1))
				device = zdevices.find(self.json_args['ieee'])
				if device == None :
					raise Exception("Device not found")
				await zdevices.initialize(device)
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'rediscover':
				if self.json_args == None :
					raise Exception("No arg for put "+str(arg1))
				device = zdevices.find(self.json_args['ieee'])
				if device == None :
					raise Exception("Device not found")
				device.status = 0
				await device._initialize()
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'get_basic_info':
				if self.json_args == None :
					raise Exception("No arg for put "+str(arg1))
				device = zdevices.find(self.json_args['ieee'])
				if device == None :
					raise Exception("Device not found")
				await zdevices.get_basic_info(device)
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'command':
				if self.json_args == None :
					raise Exception("No arg for put "+str(arg1))
				try:
					await zdevices.command(self.json_args)
				except Exception as e:
					if 'allowQueue' in self.json_args and self.json_args['allowQueue']:
						logging.info('[DeviceHandler.put/command] Failed on command'+str(self.json_args)+' => '+str(e)+'. Replan command later')
						zqueue.add('command',5,self.json_args,1)
					else:
						raise
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'update_specific':
				if self.json_args == None :
					raise Exception("No arg for put "+str(arg1))
				ieee = self.json_args['ieee']
				if not os.path.exists(shared.DEVICE_FOLDER+'/'+ieee+'.json'):
					raise Exception("File not found "+str(shared.DEVICE_FOLDER+'/'+ieee+'.json'))
				with open(shared.DEVICE_FOLDER+'/'+ieee+'.json') as specific_file:
					shared.DEVICE_SPECIFIC[ieee] = json.load(specific_file)
				logging.info('[DeviceHandler.put/update_specific] Update specific configuration for '+str(ieee)+' to '+str(shared.DEVICE_SPECIFIC[ieee]))
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'delete_specific':
				if self.json_args == None :
					raise Exception("No arg for put "+str(arg1))
				ieee = self.json_args['ieee']
				shared.DEVICE_SPECIFIC.pop(ieee, None)
				logging.info('[DeviceHandler.put/delete_specific] Delete specific configuration for '+str(ieee))
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'bind' or arg1 == 'unbind':
				if self.json_args == None :
					raise Exception("No arg for put "+str(arg1))
				logging.info('[DeviceHandler.bind/unbind] '+str(arg1)+' device '+str(self.json_args['src']['ieee'])+' endpoint '+str(self.json_args['src']['endpoint'])+' cluster '+str(self.json_args['src']['cluster']))
				src_device = zdevices.find(self.json_args['src']['ieee'])
				if src_device == None :
					raise Exception("Device source not found")
				if not self.json_args['src']['endpoint'] in src_device.endpoints:
					raise Exception("Endpoint not found : "+str(self.json_args['src']['endpoint']))
				src_endpoint = src_device.endpoints[self.json_args['src']['endpoint']]
				if not self.json_args['src']['cluster'] in src_endpoint.out_clusters:
					raise Exception("Cluster not found : "+str(self.json_args['src']['cluster']))
				src_cluster = src_endpoint.out_clusters[self.json_args['src']['cluster']]
				if 'type' in self.json_args['dest'] and self.json_args['dest']['type'] == 'group':
					if arg1 == 'unbind':
						logging.info('[DeviceHandler.bind/unbind] Unbind group '+str(self.json_args['dest']['group_id']))
						await zgroups.binding(src_device,self.json_args['dest']['group_id'],zdo_types.ZDOCmd.Unbind_req,[src_cluster]);
					else:
						logging.info('[DeviceHandler.bind/unbind] Bind group '+self.json_args['dest']['group_id'])
						await zgroups.binding(src_device,self.json_args['dest']['group_id'],zdo_types.ZDOCmd.Bind_req,[src_cluster]);
				else:
					dest_device = zdevices.find(self.json_args['dest']['ieee'])
					if dest_device == None :
						raise Exception("Device destination not found")
					if not self.json_args['dest']['endpoint'] in dest_device.endpoints:
						raise Exception("Endpoint not found : "+str(self.json_args['dest']['endpoint']))
					dest_endpoint = dest_device.endpoints[self.json_args['dest']['endpoint']]
					dstaddr = zdo_types.MultiAddress()
					dstaddr.addrmode = 3
					dstaddr.ieee = dest_device.ieee
					dstaddr.endpoint = dest_endpoint.endpoint_id
					if arg1 == 'unbind':
						logging.info('[DeviceHandler.bind/unbind] Unbind device src '+str(src_device.ieee)+' endpoint '+str(src_cluster.endpoint.endpoint_id)+' cluster '+str(src_cluster.cluster_id)+' to '+str(dstaddr))
						await src_device.zdo.Unbind_req(src_device.ieee,src_cluster.endpoint.endpoint_id,src_cluster.cluster_id,dstaddr)
					else:
						logging.info('[DeviceHandler.bind/unbind] Bind device src '+str(src_device.ieee)+' endpoint '+str(src_cluster.endpoint.endpoint_id)+' cluster '+str(src_cluster.cluster_id)+' to '+str(dstaddr))
						await src_device.zdo.Bind_req(src_device.ieee,src_cluster.endpoint.endpoint_id,src_cluster.cluster_id,dstaddr)
				return self.write(utils.format_json_result(success=True))
		except Exception as e:
			logging.info(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def delete(self):
		if self.json_args == None :
			raise Exception("No arg for delete")
		try:
			device = zdevices.find(self.json_args['ieee'])
			if device == None :
				raise Exception("Device not found")
			await shared.ZIGPY.remove(device.ieee)
			return self.write(utils.format_json_result(success=True))
		except Exception as e:
			logging.info(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

class GroupHandler(RequestHandler):
	def prepare(self):
		utils.check_apikey(self.request.headers.get("autorization", ""))
		self.json_args = None
		try:
			if self.request.headers.get("Content-Type", "").startswith("application/json"):
				self.json_args = json.loads(self.request.body)
		except Exception as e:
			self.json_args = None
		logging.info('[GroupHandler.prepare] Json arg : '+str(self.json_args))

	async def get(self,arg1):
		try:
			if arg1 == 'all':
				result = []
				for group in shared.ZIGPY.groups.values():
					values = await zgroups.serialize(group)
					result.append(values)
				return self.write(utils.format_json_result(success=True,data=result))
			if arg1 == 'info':
				result = []
				group = zgroups.find(self.get_argument('id',''))
				if group == None:
					raise Exception("Group not found")
				values = await zgroups.serialize(group)
				return self.write(utils.format_json_result(success=True,data=values))
			raise Exception("No method found for "+str(arg1))
		except Exception as e:
			logging.info(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def post(self,arg1):
		try:
			True
		except Exception as e:
			logging.info(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))

	async def put(self,arg1):
		try:
			if arg1 == 'command':
				try:
					await zgroups.command(self.json_args)
				except Exception as e:
					if 'allowQueue' in self.json_args and self.json_args['allowQueue']:
						logging.info('[GroupHandler.put] Failed on command'+str(self.json_args)+' => '+str(e)+'. Replan group command later')
						zqueue.add('command',5,self.json_args,1)
					else:
						raise
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'create':
				try:
					await zgroups.create_group(self.json_args['name'])
					return self.write(utils.format_json_result(success=True))
				except:
					raise
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'add_device':
				try:
					await zgroups.add_device(self.json_args)
				except Exception as e:
					raise
				return self.write(utils.format_json_result(success=True))
			if arg1 == 'delete_device':
				try:
					await zgroups.delete_device(self.json_args)
				except Exception as e:
					raise
				return self.write(utils.format_json_result(success=True))
			raise Exception("No method found for "+str(arg1))

		except Exception as e:
			logging.info(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))
	
	async def delete(self):
		try:
			group = zgroups.find(self.json_args['id'])
			if group == None :
				raise Exception("Group not found")
			shared.ZIGPY.groups.pop(group._group_id)
			return self.write(utils.format_json_result(success=True))
		except Exception as e:
			logging.info(traceback.format_exc())
			return self.write(utils.format_json_result(success="error",data=str(e)))


shared.REST_SERVER = Application([
		(r"/application/([^/]+)?", ApplicationHandler),
		(r"/network/([^/]+)?", NetworkHandler),
		(r"/device/([^/]+)?", DeviceHandler),
		(r"/device", DeviceHandler),
		(r"/group/([^/]+)?", GroupHandler),
		(r"/group", GroupHandler)
	])

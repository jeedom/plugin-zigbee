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
from zigpy.zcl.clusters.hvac import Thermostat
from . import details
import shared



class DanfossSpecific():
	def __init__(self):
		self.manuf = 'Danfoss'
		self.specific = ['init','reporting']

	def isvalid(self,manufacturer):
		if manufacturer == self.manuf:
			return True

	def init(self,device):
		if (device.model in ['eTRV0100']):
			endpoints = device.endpoints.items()
			logging.info('Found danfoss valve')
			for endpoint_id, ep in device.endpoints.items():
				if endpoint_id == 1:
					cluster = details.JeedomDanfossValveCluster(ep, is_server=True)
					for oldcluster in ep.in_clusters.values():
						if oldcluster.cluster_id == cluster.cluster_id:
							cluster._attr_cache=oldcluster._attr_cache
							break
					ep.add_input_cluster(cluster.cluster_id, cluster)
			
		if (device.model in ['0x8020','0x8021','0x8030','0x8031','0x8034','0x8035','0x0200']):
			endpoints = device.endpoints.items()
			logging.info('Found endpoints : ' + str(endpoints))
			for endpoint_id, ep in device.endpoints.items():
				if endpoint_id == 232:
					logging.info('Found endpoint 232')
					logging.info('Setting Device Model')
					device.model = '0x0200'
					shared.ZIGPY.devices[device.ieee] = device
				if endpoint_id in range(1,15):
					cluster = details.JeedomDanfossThermostatCluster(ep, is_server=True)
					for oldcluster in ep.in_clusters.values():
						if oldcluster.cluster_id == cluster.cluster_id:
							cluster._attr_cache=oldcluster._attr_cache
							break
					ep.add_input_cluster(cluster.cluster_id, cluster)

	async def reporting(self,model , cluster_id ,ep_id,cluster):
		logging.info('Checking specific reporting for device '+str(model)+' '+str(cluster_id)+' '+str(ep_id))
		if model in details.REPORTING_SPECIFIC and cluster_id in details.REPORTING_SPECIFIC[model] and ep_id in details.REPORTING_SPECIFIC[model][cluster_id]:
			logging.info('Found specific reporting ' + str(details.REPORTING_SPECIFIC[model][cluster_id][ep_id]))
			for reporting in details.REPORTING_SPECIFIC[model][cluster_id][ep_id]:
				logging.info('Setting specific reporting ' + str(reporting))
				await cluster.configure_reporting(reporting["attr"], reporting["min"],reporting["max"], reporting["report"])
		else:
			logging.info('No specific reporting found')


shared.JEEDOM_SPECIFIC.append(DanfossSpecific)









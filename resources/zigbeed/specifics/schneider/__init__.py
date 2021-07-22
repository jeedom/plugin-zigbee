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
from . import details
import shared

class SchneiderSpecifics():
	def __init__(self):
		self.manuf = 'Schneider Electric'
		self.specific = ['init','reporting']

	def isvalid(self,manufacturer):
		if manufacturer == self.manuf:
			return True

	def init(self,device):
		if (device.model in ['CCTFR6700','PUCK\/SHUTTER\/1']):
			endpoints = device.endpoints.items()
			logging.debug('Found Schneider heater controller Specifics')
			for endpoint_id, ep in device.endpoints.items():
				if device.model == 'PUCK\/SHUTTER\/1' and endpoint_id == 5:
					cluster = details.SchneiderShutterCluster(ep, is_server=True)
					for oldcluster in ep.in_clusters.values():
						if oldcluster.cluster_id == cluster.cluster_id:
							cluster._attr_cache=oldcluster._attr_cache
							break
					ep.add_input_cluster(cluster.cluster_id, cluster)
				if device.model == 'CCTFR6700' and endpoint_id == 1:
					cluster = details.SchneiderPilotModeCluster(ep, is_server=True)
					for oldcluster in ep.in_clusters.values():
						if oldcluster.cluster_id == cluster.cluster_id:
							cluster._attr_cache=oldcluster._attr_cache
							break
					ep.add_input_cluster(cluster.cluster_id, cluster)

					cluster = details.SchneiderBasicCluster(ep, is_server=True)
					for oldcluster in ep.out_clusters.values():
						if oldcluster.cluster_id == cluster.cluster_id:
							cluster._attr_cache=oldcluster._attr_cache
							break
					ep.add_output_cluster(cluster.cluster_id, cluster)


	async def reporting(self, model, cluster_id, ep_id, cluster):
		logging.debug('Checking specific reporting for device '+str(model)+' '+str(cluster_id)+' '+str(ep_id))
		if model in details.REPORTING_SPECIFIC and cluster_id in details.REPORTING_SPECIFIC[model] and ep_id in details.REPORTING_SPECIFIC[model][cluster_id]:
			logging.debug('Found specific reporting ' + str(details.REPORTING_SPECIFIC[model][cluster_id][ep_id]))
			for reporting in details.REPORTING_SPECIFIC[model][cluster_id][ep_id]:
				logging.debug('Setting specific reporting ' + str(reporting))
				await cluster.configure_reporting(reporting["attr"], reporting["min"],reporting["max"], reporting["report"])
		else:
			logging.debug('No specific reporting found')

shared.JEEDOM_SPECIFIC.append(SchneiderSpecifics)
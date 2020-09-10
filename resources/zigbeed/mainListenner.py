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
import shared,utils
import traceback

LOGGER = logging.getLogger(__name__)

class MainListener:
	"""
	Contains callbacks that zigpy will call whenever something happens.	Look for `listener_event` in the Zigpy source or just look at the logged warnings.
	"""

	def __init__(self, application):
		self.application = application

	def device_joined(self, device):
		LOGGER.info("************************* Device joined : %s" %(device))
		shared.JEEDOM_COM.send_change_immediate({'device_joined' : str(device._ieee)});

	def device_announce(self, device):
		LOGGER.info("****************** device_announce Zigpy Device: %s" %(device))

	def device_removed(self, device):
		LOGGER.info("****************** device_removed Zigpy Device: %s" %(device))
		shared.JEEDOM_COM.send_change_immediate({'device_removed' : str(device._ieee)});

	def device_left(self, device):
		LOGGER.info("****************** device_left Zigpy Device: %s" %(device))
		shared.JEEDOM_COM.send_change_immediate({'device_left' : str(device._ieee)});

	def device_initialized(self, device, *, new=True):
		"""
		Called at runtime after a device's information has been queried.I also call it on startup to load existing devices from the DB.
		"""
		LOGGER.info("******************** Device is ready: new=%s, device=%s", new, device._ieee)
		for ep_id, endpoint in device.endpoints.items():
			if ep_id == 0: # Ignore ZDO
				continue
			for cluster in endpoint.in_clusters.values(): # You need to attach a listener to every cluster to receive events
				cluster.add_context_listener(self) # The context listener passes its own object as the first argument to the callback
		if new:
			shared.JEEDOM_COM.send_change_immediate({'device_initialized' : str(device._ieee)});

	def cluster_command(self, cluster, command_id, *args):
		device = cluster.endpoint.device
		LOGGER.info("****************** cluster_command - Cluster: %s ClusterId: 0x%04x command_id: %s args: %s" %(cluster, cluster.cluster_id, command_id, args))

	def attribute_updated(self, cluster, attribute_id, value):
		try:
			LOGGER.info("****************** Received an attribute update %s=%s on cluster %s from device %s",attribute_id, value, cluster.cluster_id, cluster.endpoint.device._ieee)
			infos = {
				"value" : str(value),
				"cluster_name" : cluster.name,
			}
			shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::'+str(attribute_id),infos)
		except Exception as e:
			logging.error(traceback.format_exc())

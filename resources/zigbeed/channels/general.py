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

"""General channels module for Zigbee Home Automation."""
import asyncio
import logging
from typing import Any, List, Optional

import zigpy.exceptions
import zigpy.zcl.clusters.general as general

import registries
from const import (
	REPORT_CONFIG_ASAP,
	REPORT_CONFIG_BATTERY_SAVE,
	REPORT_CONFIG_DEFAULT,
	REPORT_CONFIG_IMMEDIATE,
	SIGNAL_ATTR_UPDATED,
	SIGNAL_MOVE_LEVEL,
	SIGNAL_SET_LEVEL,
	SIGNAL_STATE_ATTR,
	SIGNAL_UPDATE_DEVICE,
)
import shared
import utils

class Alarms():
	"""Alarms channel."""

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.AnalogInput.cluster_id)
class AnalogInput():
	"""Analog Input channel."""
	REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.AnalogOutput.cluster_id)
class AnalogOutput():
	"""Analog Output channel."""
	REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.AnalogValue.cluster_id)
class AnalogValue():
	"""Analog Value channel."""
	REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.ApplianceControl.cluster_id)
class ApplianceContorl():
	"""Appliance Control channel."""

@registries.CHANNEL_ONLY_CLUSTERS.register(general.Basic.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Basic.cluster_id)
class BasicChannel():
	"""Channel to interact with the basic cluster."""
	UNKNOWN = 0
	BATTERY = 3
	POWER_SOURCES = {
		UNKNOWN: "Unknown",
		1: "Mains (single phase)",
		2: "Mains (3 phase)",
		BATTERY: "Battery",
		4: "DC source",
		5: "Emergency mains constantly powered",
		6: "Emergency mains and transfer switch",
	}

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.BinaryInput.cluster_id)
class BinaryInput():
	"""Binary Input channel."""
	REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.BinaryOutput.cluster_id)
class BinaryOutput():
	"""Binary Output channel."""
	REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.BinaryValue.cluster_id)
class BinaryValue():
	"""Binary Value channel."""
	REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Commissioning.cluster_id)
class Commissioning():
	"""Commissioning channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.DeviceTemperature.cluster_id)
class DeviceTemperature():
	"""Device Temperature channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.GreenPowerProxy.cluster_id)
class GreenPowerProxy():
	"""Green Power Proxy channel."""

	NO_BINDING=True


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Groups.cluster_id)
class Groups():
	"""Groups channel."""

	NO_BINDING=True


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Identify.cluster_id)
class Identify():
	"""Identify channel."""

	NO_BINDING=True

@registries.CLIENT_CHANNELS_REGISTRY.register(general.LevelControl.cluster_id)
class LevelControl():
	"""LevelControl client cluster."""

@registries.BINDABLE_CLUSTERS.register(general.LevelControl.cluster_id)
@registries.LIGHT_CLUSTERS.register(general.LevelControl.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.LevelControl.cluster_id)
class LevelControlChannel():
	"""Channel for the LevelControl Zigbee cluster."""
	CURRENT_LEVEL = 0
	REPORT_CONFIG = ({"attr": "current_level", "config": REPORT_CONFIG_ASAP},)


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.MultistateInput.cluster_id)
class MultistateInput():
	"""Multistate Input channel."""
	REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.MultistateOutput.cluster_id)
class MultistateOutput():
	"""Multistate Output channel."""
	REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.MultistateValue.cluster_id)
class MultistateValue():
	"""Multistate Value channel."""
	REPORT_CONFIG = [{"attr": "present_value", "config": REPORT_CONFIG_DEFAULT}]


@registries.CLIENT_CHANNELS_REGISTRY.register(general.OnOff.cluster_id)
class OnOff():
	"""OnOff client channel."""

@registries.BINARY_SENSOR_CLUSTERS.register(general.OnOff.cluster_id)
@registries.BINDABLE_CLUSTERS.register(general.OnOff.cluster_id)
@registries.LIGHT_CLUSTERS.register(general.OnOff.cluster_id)
@registries.SWITCH_CLUSTERS.register(general.OnOff.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.OnOff.cluster_id)
class OnOffChannel():
	"""Channel for the OnOff Zigbee cluster."""
	ON_OFF = 0
	REPORT_CONFIG = ({"attr": "on_off", "config": REPORT_CONFIG_IMMEDIATE},)

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.OnOffConfiguration.cluster_id)
class OnOffConfiguration():
	"""OnOff Configuration channel."""

@registries.CLIENT_CHANNELS_REGISTRY.register(general.Ota.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Ota.cluster_id)
class Ota():
	"""OTA Channel."""

	NO_BINDING=True

	def attribute_updated(cluster, attribute_id, value):
		return False

	def cluster_command(cluster, tsn,command_id, *args):
		cmd_name = cluster.server_commands.get(command_id, [command_id])[0]
		logging.info("["+str(cluster.endpoint.device._ieee)+"][chanels.general.Ota.cluster_command] Received command "+str(cmd_name))
		return False


@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Partition.cluster_id)
class Partition():
	"""Partition channel."""

@registries.CHANNEL_ONLY_CLUSTERS.register(general.PollControl.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.PollControl.cluster_id)
class PollControl():
	"""Poll Control channel."""
	CHECKIN_INTERVAL = 60 * 60 * 4  # 60min
	CHECKIN_FAST_POLL_TIMEOUT = 10 * 4  # 10s
	LONG_POLL = 5 * 4  # 5s

	async def initialize(cluster):
		 try:
			 res = await cluster.write_attributes({"checkin_interval": PollControl.CHECKIN_INTERVAL})
			 logging.info("["+str(cluster.endpoint.device._ieee)+"][chanels.general.PollControl.initialize] %ss check-in interval set: %s", PollControl.CHECKIN_INTERVAL / 4, res)
		 except (asyncio.TimeoutError, zigpy.exceptions.ZigbeeException) as ex:
			 logging.info("["+str(cluster.endpoint.device._ieee)+"][chanels.general.PollControl.initialize] Couldn't set check-in interval: %s", ex)

	def attribute_updated(cluster, attribute_id, value):
		return False

	def cluster_command(cluster, tsn, *args):
		"""Handle commands received to this cluster."""
		logging.info("["+str(cluster.endpoint.device._ieee)+"][chanels.general.PollControl.cluster_command] Received %s tsn : %s", tsn, args)
		cmd_name = cluster.client_commands.get(args[0], [])[0]
		logging.info("["+str(cluster.endpoint.device._ieee)+"][chanels.general.PollControl.cluster_command] Command %s", cmd_name)
		if cmd_name == "checkin":
			fast_poll_timeout = PollControl.CHECKIN_FAST_POLL_TIMEOUT
			long_poll = PollControl.LONG_POLL
			ieee = str(cluster.endpoint.device._ieee)
			if ieee in shared.DEVICE_SPECIFIC and 'poll_control' in shared.DEVICE_SPECIFIC[ieee]:
				if 'long_poll' in shared.DEVICE_SPECIFIC[ieee]['poll_control'] and shared.DEVICE_SPECIFIC[ieee]['poll_control']['long_poll'] != '' :
					long_poll = int(shared.DEVICE_SPECIFIC[ieee]['poll_control']['long_poll'])
				if 'fast_poll_timeout' in shared.DEVICE_SPECIFIC[ieee]['poll_control'] and shared.DEVICE_SPECIFIC[ieee]['poll_control']['fast_poll_timeout'] != '' :
					fast_poll_timeout = int(shared.DEVICE_SPECIFIC[ieee]['poll_control']['fast_poll_timeout'])
			utils.initSharedDeviceData(cluster,'long_poll')	
			if long_poll == -1 or shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id]['long_poll'] == long_poll:
				logging.info("["+ieee+"][chanels.general.PollControl.cluster_command] No checkin update needed")
				asyncio.ensure_future(cluster.checkin_response(False, fast_poll_timeout, tsn=tsn))
				return True
			shared.DEVICES_DATA[cluster.endpoint.device._ieee][cluster.endpoint._endpoint_id][cluster.cluster_id]['long_poll'] = long_poll
			asyncio.ensure_future(PollControl.set_poll_parameters(cluster,tsn,fast_poll_timeout,long_poll))
			return True
		return False
		
	async def set_poll_parameters(cluster,tsn,fast_poll_timeout,long_poll):
		ieee = str(cluster.endpoint.device._ieee)
		logging.info("["+ieee+"][chanels.general.PollControl.set_poll_parameters] Send checkin response. Fastpoll timeout : %s s, long poll %s s",(fast_poll_timeout/4),(long_poll/4))
		await cluster.checkin_response(True, fast_poll_timeout, tsn=tsn)
		await cluster.set_long_poll_interval(long_poll)
		await cluster.fast_poll_stop()
		logging.info("["+ieee+"][chanels.general.PollControl.set_poll_parameters] End of checkin response")

@registries.DEVICE_TRACKER_CLUSTERS.register(general.PowerConfiguration.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.PowerConfiguration.cluster_id)
class PowerConfigurationChannel():
	"""Channel for the zigbee power configuration cluster."""
	REPORT_CONFIG = (
		{"attr": "battery_voltage", "config": REPORT_CONFIG_BATTERY_SAVE},
		{"attr": "battery_percentage_remaining", "config": REPORT_CONFIG_BATTERY_SAVE},
	)

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.PowerProfile.cluster_id)
class PowerProfile():
	"""Power Profile channel."""

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.RSSILocation.cluster_id)
class RSSILocation():
	"""RSSI Location channel."""

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Scenes.cluster_id)
class Scenes():
	"""Scenes channel."""

	def cluster_command(cluster, tsn, *args):
		if len(args) < 2 or len(args[1]) < 1:
			return True
		value = args[1][0]*10
		if len(args[1]) > 1:
			value += args[1][1]
		shared.JEEDOM_COM.add_changes('devices::'+str(cluster.endpoint.device._ieee)+'::'+str(cluster.endpoint._endpoint_id)+'::'+str(cluster.cluster_id)+'::cmd::'+str(args[0]),{"value" : value,"cluster_name" : cluster.name})
		return True

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.Time.cluster_id)
class Time():
	"""Time channel."""

	NO_BINDING=True

@registries.ZIGBEE_CHANNEL_REGISTRY.register(general.GreenPowerProxy.cluster_id)
class GreenPowerProxy():
	"""GreenPowerProxy channel."""

	NO_BINDING=True

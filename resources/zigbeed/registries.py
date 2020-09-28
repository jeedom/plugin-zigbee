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


"""Mapping registries for Zigbee Home Automation."""
import collections
from typing import Callable, Dict, List, Set, Tuple, Union
from decorators import DictRegistry, SetRegistry
import zigpy.profiles.zha
import zigpy.profiles.zll
import zigpy.zcl as zcl

SMARTTHINGS_ACCELERATION_CLUSTER = 0xFC02
SMARTTHINGS_ARRIVAL_SENSOR_DEVICE_TYPE = 0x8000
SMARTTHINGS_HUMIDITY_CLUSTER = 0xFC45


REMOTE_DEVICE_TYPES = {
	zigpy.profiles.zha.PROFILE_ID: [
		zigpy.profiles.zha.DeviceType.COLOR_CONTROLLER,
		zigpy.profiles.zha.DeviceType.COLOR_DIMMER_SWITCH,
		zigpy.profiles.zha.DeviceType.COLOR_SCENE_CONTROLLER,
		zigpy.profiles.zha.DeviceType.DIMMER_SWITCH,
		zigpy.profiles.zha.DeviceType.LEVEL_CONTROL_SWITCH,
		zigpy.profiles.zha.DeviceType.NON_COLOR_CONTROLLER,
		zigpy.profiles.zha.DeviceType.NON_COLOR_SCENE_CONTROLLER,
		zigpy.profiles.zha.DeviceType.ON_OFF_SWITCH,
		zigpy.profiles.zha.DeviceType.ON_OFF_LIGHT_SWITCH,
		zigpy.profiles.zha.DeviceType.REMOTE_CONTROL,
		zigpy.profiles.zha.DeviceType.SCENE_SELECTOR,
	],
	zigpy.profiles.zll.PROFILE_ID: [
		zigpy.profiles.zll.DeviceType.COLOR_CONTROLLER,
		zigpy.profiles.zll.DeviceType.COLOR_SCENE_CONTROLLER,
		zigpy.profiles.zll.DeviceType.CONTROL_BRIDGE,
		zigpy.profiles.zll.DeviceType.CONTROLLER,
		zigpy.profiles.zll.DeviceType.SCENE_CONTROLLER,
	],
}


PHILLIPS_REMOTE_CLUSTER = 0xFC00

SMARTTHINGS_ACCELERATION_CLUSTER = 0xFC02
SMARTTHINGS_ARRIVAL_SENSOR_DEVICE_TYPE = 0x8000
SMARTTHINGS_HUMIDITY_CLUSTER = 0xFC45

REMOTE_DEVICE_TYPES = collections.defaultdict(list, REMOTE_DEVICE_TYPES)


SWITCH_CLUSTERS = SetRegistry()

BINARY_SENSOR_CLUSTERS = SetRegistry()
BINARY_SENSOR_CLUSTERS.add(SMARTTHINGS_ACCELERATION_CLUSTER)

BINDABLE_CLUSTERS = SetRegistry()
CHANNEL_ONLY_CLUSTERS = SetRegistry()
CLIMATE_CLUSTERS = SetRegistry()
CUSTOM_CLUSTER_MAPPINGS = {}

DEVICE_TRACKER_CLUSTERS = SetRegistry()
LIGHT_CLUSTERS = SetRegistry()
OUTPUT_CHANNEL_ONLY_CLUSTERS = SetRegistry()
CLIENT_CHANNELS_REGISTRY = DictRegistry()

ZIGBEE_CHANNEL_REGISTRY = DictRegistry()

from channels import general
from channels import closures
from channels import homeautomation
from channels import smartenergy
from channels import measurement
from channels import hvac
from channels import lighting
from channels import lightlink
from channels import manufacturerspecific
from channels import protocol
from channels import security

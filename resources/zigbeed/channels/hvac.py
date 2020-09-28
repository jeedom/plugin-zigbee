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

"""
HVAC channels module for Zigbee Home Automation.
"""
import time
import asyncio
from collections import namedtuple
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from zigpy.exceptions import ZigbeeException
import zigpy.zcl.clusters.hvac as hvac
from zigpy.zcl.foundation import Status

import registries
from const import (
	REPORT_CONFIG_MAX_INT,
	REPORT_CONFIG_MIN_INT,
	REPORT_CONFIG_OP,
	SIGNAL_ATTR_UPDATED,
)
from helpers import retryable_req
import shared
import utils

AttributeUpdateRecord = namedtuple("AttributeUpdateRecord", "attr_id, attr_name, value")
REPORT_CONFIG_CLIMATE = (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 25)
REPORT_CONFIG_CLIMATE_DEMAND = (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 5)
REPORT_CONFIG_CLIMATE_DISCRETE = (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 1)

@registries.ZIGBEE_CHANNEL_REGISTRY.register(hvac.Dehumidification.cluster_id)
class Dehumidification():
	"""Dehumidification channel."""

@registries.ZIGBEE_CHANNEL_REGISTRY.register(hvac.Fan.cluster_id)
class FanChannel():
	"""Fan channel."""

	_value_attribute = 0

	REPORT_CONFIG = ({"attr": "fan_mode", "config": REPORT_CONFIG_OP},)

@registries.ZIGBEE_CHANNEL_REGISTRY.register(hvac.Pump.cluster_id)
class Pump():
	"""Pump channel."""

@registries.CLIMATE_CLUSTERS.register(hvac.Thermostat.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(hvac.Thermostat.cluster_id)
class ThermostatChannel():
	"""Thermostat channel."""

	REPORT_CONFIG = (
	{"attr": "local_temp", "config": REPORT_CONFIG_CLIMATE},
	{"attr": "occupied_cooling_setpoint", "config": REPORT_CONFIG_CLIMATE},
	{"attr": "occupied_heating_setpoint", "config": REPORT_CONFIG_CLIMATE},
	{"attr": "unoccupied_cooling_setpoint", "config": REPORT_CONFIG_CLIMATE},
	{"attr": "unoccupied_heating_setpoint", "config": REPORT_CONFIG_CLIMATE},
	{"attr": "running_mode", "config": REPORT_CONFIG_CLIMATE},
	{"attr": "running_state", "config": REPORT_CONFIG_CLIMATE_DEMAND},
	{"attr": "system_mode", "config": REPORT_CONFIG_CLIMATE},
	{"attr": "occupancy", "config": REPORT_CONFIG_CLIMATE_DISCRETE},
	{"attr": "pi_cooling_demand", "config": REPORT_CONFIG_CLIMATE_DEMAND},
	{"attr": "pi_heating_demand", "config": REPORT_CONFIG_CLIMATE_DEMAND},
	)

@registries.ZIGBEE_CHANNEL_REGISTRY.register(hvac.UserInterface.cluster_id)
class UserInterface():
	"""User interface (thermostat) channel."""

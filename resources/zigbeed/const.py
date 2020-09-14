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

import enum
import logging
from typing import List

TIME_MILLISECONDS = "ms"
TIME_SECONDS = "s"
TIME_MINUTES = "min"
TIME_HOURS = "h"
TIME_DAYS = "d"
TIME_WEEKS = "w"

ATTR_ARGS = "args"
ATTR_ATTRIBUTE = "attribute"
ATTR_ATTRIBUTE_ID = "attribute_id"
ATTR_ATTRIBUTE_NAME = "attribute_name"
ATTR_AVAILABLE = "available"
ATTR_CLUSTER_ID = "cluster_id"
ATTR_CLUSTER_TYPE = "cluster_type"
ATTR_COMMAND = "command"
ATTR_COMMAND_TYPE = "command_type"
ATTR_DEVICE_IEEE = "device_ieee"
ATTR_DEVICE_TYPE = "device_type"
ATTR_ENDPOINTS = "endpoints"
ATTR_ENDPOINT_ID = "endpoint_id"
ATTR_IEEE = "ieee"
ATTR_IN_CLUSTERS = "in_clusters"
ATTR_LAST_SEEN = "last_seen"
ATTR_LEVEL = "level"
ATTR_LQI = "lqi"
ATTR_MANUFACTURER = "manufacturer"
ATTR_MANUFACTURER_CODE = "manufacturer_code"
ATTR_MEMBERS = "members"
ATTR_MODEL = "model"
ATTR_NAME = "name"
ATTR_NODE_DESCRIPTOR = "node_descriptor"
ATTR_NWK = "nwk"
ATTR_OUT_CLUSTERS = "out_clusters"
ATTR_POWER_SOURCE = "power_source"
ATTR_PROFILE_ID = "profile_id"
ATTR_QUIRK_APPLIED = "quirk_applied"
ATTR_QUIRK_CLASS = "quirk_class"
ATTR_RSSI = "rssi"
ATTR_SIGNATURE = "signature"
ATTR_TYPE = "type"
ATTR_UNIQUE_ID = "unique_id"
ATTR_VALUE = "value"
ATTR_WARNING_DEVICE_DURATION = "duration"
ATTR_WARNING_DEVICE_MODE = "mode"
ATTR_WARNING_DEVICE_STROBE = "strobe"
ATTR_WARNING_DEVICE_STROBE_DUTY_CYCLE = "duty_cycle"
ATTR_WARNING_DEVICE_STROBE_INTENSITY = "intensity"

BAUD_RATES = [2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000, 256000]
BINDINGS = "bindings"

CHANNEL_ACCELEROMETER = "accelerometer"
CHANNEL_ANALOG_INPUT = "analog_input"
CHANNEL_ATTRIBUTE = "attribute"
CHANNEL_BASIC = "basic"
CHANNEL_COLOR = "light_color"
CHANNEL_COVER = "window_covering"
CHANNEL_DOORLOCK = "door_lock"
CHANNEL_ELECTRICAL_MEASUREMENT = "electrical_measurement"
CHANNEL_EVENT_RELAY = "event_relay"
CHANNEL_FAN = "fan"
CHANNEL_HUMIDITY = "humidity"
CHANNEL_IAS_WD = "ias_wd"
CHANNEL_IDENTIFY = "identify"
CHANNEL_ILLUMINANCE = "illuminance"
CHANNEL_LEVEL = ATTR_LEVEL
CHANNEL_MULTISTATE_INPUT = "multistate_input"
CHANNEL_OCCUPANCY = "occupancy"
CHANNEL_ON_OFF = "on_off"
CHANNEL_POWER_CONFIGURATION = "power"
CHANNEL_PRESSURE = "pressure"
CHANNEL_SHADE = "shade"
CHANNEL_SMARTENERGY_METERING = "smartenergy_metering"
CHANNEL_TEMPERATURE = "temperature"
CHANNEL_THERMOSTAT = "thermostat"
CHANNEL_ZDO = "zdo"
CHANNEL_ZONE = ZONE = "ias_zone"

CLUSTER_COMMAND_SERVER = "server"
CLUSTER_COMMANDS_CLIENT = "client_commands"
CLUSTER_COMMANDS_SERVER = "server_commands"
CLUSTER_TYPE_IN = "in"
CLUSTER_TYPE_OUT = "out"

DEFAULT_RADIO_TYPE = "ezsp"
DEFAULT_BAUDRATE = 57600
DEFAULT_DATABASE_NAME = "zigbee.db"
DISCOVERY_KEY = "zha_discovery_info"

DOMAIN = "zha"

GROUP_ID = "group_id"
GROUP_IDS = "group_ids"
GROUP_NAME = "group_name"

MFG_CLUSTER_ID_START = 0xFC00

POWER_MAINS_POWERED = "Mains"
POWER_BATTERY_OR_UNKNOWN = "Battery or Unknown"

REPORT_CONFIG_MAX_INT = 900
REPORT_CONFIG_MAX_INT_BATTERY_SAVE = 10800
REPORT_CONFIG_MIN_INT = 30
REPORT_CONFIG_MIN_INT_ASAP = 1
REPORT_CONFIG_MIN_INT_IMMEDIATE = 0
REPORT_CONFIG_MIN_INT_OP = 5
REPORT_CONFIG_MIN_INT_BATTERY_SAVE = 3600
REPORT_CONFIG_RPT_CHANGE = 1
REPORT_CONFIG_DEFAULT = (
    REPORT_CONFIG_MIN_INT,
    REPORT_CONFIG_MAX_INT,
    REPORT_CONFIG_RPT_CHANGE,
)
REPORT_CONFIG_ASAP = (
    REPORT_CONFIG_MIN_INT_ASAP,
    REPORT_CONFIG_MAX_INT,
    REPORT_CONFIG_RPT_CHANGE,
)
REPORT_CONFIG_BATTERY_SAVE = (
    REPORT_CONFIG_MIN_INT_BATTERY_SAVE,
    REPORT_CONFIG_MAX_INT_BATTERY_SAVE,
    REPORT_CONFIG_RPT_CHANGE,
)
REPORT_CONFIG_IMMEDIATE = (
    REPORT_CONFIG_MIN_INT_IMMEDIATE,
    REPORT_CONFIG_MAX_INT,
    REPORT_CONFIG_RPT_CHANGE,
)
REPORT_CONFIG_OP = (
    REPORT_CONFIG_MIN_INT_OP,
    REPORT_CONFIG_MAX_INT,
    REPORT_CONFIG_RPT_CHANGE,
)

SENSOR_ACCELERATION = "acceleration"
SENSOR_BATTERY = "battery"
SENSOR_ELECTRICAL_MEASUREMENT = CHANNEL_ELECTRICAL_MEASUREMENT
SENSOR_GENERIC = "generic"
SENSOR_HUMIDITY = CHANNEL_HUMIDITY
SENSOR_ILLUMINANCE = CHANNEL_ILLUMINANCE
SENSOR_METERING = "metering"
SENSOR_OCCUPANCY = CHANNEL_OCCUPANCY
SENSOR_OPENING = "opening"
SENSOR_PRESSURE = CHANNEL_PRESSURE
SENSOR_TEMPERATURE = CHANNEL_TEMPERATURE
SENSOR_TYPE = "sensor_type"

SIGNAL_ADD_ENTITIES = "zha_add_new_entities"
SIGNAL_ATTR_UPDATED = "attribute_updated"
SIGNAL_AVAILABLE = "available"
SIGNAL_MOVE_LEVEL = "move_level"
SIGNAL_REMOVE = "remove"
SIGNAL_SET_LEVEL = "set_level"
SIGNAL_STATE_ATTR = "update_state_attribute"
SIGNAL_UPDATE_DEVICE = "{}_zha_update_device"
SIGNAL_GROUP_ENTITY_REMOVED = "group_entity_removed"
SIGNAL_GROUP_MEMBERSHIP_CHANGE = "group_membership_change"

UNKNOWN = "unknown"
UNKNOWN_MANUFACTURER = "unk_manufacturer"
UNKNOWN_MODEL = "unk_model"

WARNING_DEVICE_MODE_STOP = 0
WARNING_DEVICE_MODE_BURGLAR = 1
WARNING_DEVICE_MODE_FIRE = 2
WARNING_DEVICE_MODE_EMERGENCY = 3
WARNING_DEVICE_MODE_POLICE_PANIC = 4
WARNING_DEVICE_MODE_FIRE_PANIC = 5
WARNING_DEVICE_MODE_EMERGENCY_PANIC = 6

WARNING_DEVICE_STROBE_NO = 0
WARNING_DEVICE_STROBE_YES = 1

WARNING_DEVICE_SOUND_LOW = 0
WARNING_DEVICE_SOUND_MEDIUM = 1
WARNING_DEVICE_SOUND_HIGH = 2
WARNING_DEVICE_SOUND_VERY_HIGH = 3

WARNING_DEVICE_STROBE_LOW = 0x00
WARNING_DEVICE_STROBE_MEDIUM = 0x01
WARNING_DEVICE_STROBE_HIGH = 0x02
WARNING_DEVICE_STROBE_VERY_HIGH = 0x03

WARNING_DEVICE_SQUAWK_MODE_ARMED = 0
WARNING_DEVICE_SQUAWK_MODE_DISARMED = 1

ZHA_DISCOVERY_NEW = "zha_discovery_new_{}"
ZHA_GW_MSG = "zha_gateway_message"
ZHA_GW_MSG_DEVICE_FULL_INIT = "device_fully_initialized"
ZHA_GW_MSG_DEVICE_INFO = "device_info"
ZHA_GW_MSG_DEVICE_JOINED = "device_joined"
ZHA_GW_MSG_DEVICE_REMOVED = "device_removed"
ZHA_GW_MSG_GROUP_ADDED = "group_added"
ZHA_GW_MSG_GROUP_INFO = "group_info"
ZHA_GW_MSG_GROUP_MEMBER_ADDED = "group_member_added"
ZHA_GW_MSG_GROUP_MEMBER_REMOVED = "group_member_removed"
ZHA_GW_MSG_GROUP_REMOVED = "group_removed"
ZHA_GW_MSG_LOG_ENTRY = "log_entry"
ZHA_GW_MSG_LOG_OUTPUT = "log_output"
ZHA_GW_MSG_RAW_INIT = "raw_device_initialized"

EFFECT_BLINK = 0x00
EFFECT_BREATHE = 0x01
EFFECT_OKAY = 0x02

EFFECT_DEFAULT_VARIANT = 0x00
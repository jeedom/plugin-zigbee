"""Map from manufacturer to standard clusters for thermostatic valves."""
import logging
from typing import Optional, Union

from zigpy.profiles import zha
import zigpy.types as t
from zigpy.zcl import foundation
from zigpy.zcl.clusters.general import (
    AnalogOutput,
    Basic,
    BinaryInput,
    Groups,
    Identify,
    OnOff,
    Ota,
    Scenes,
    Time,
)
from zigpy.zcl.clusters.hvac import Thermostat

from zhaquirks import Bus, LocalDataCluster
from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks.tuya import (
    TuyaManufClusterAttributes,
    TuyaPowerConfigurationCluster2AA,
    TuyaThermostat,
    TuyaThermostatCluster,
    TuyaUserInterfaceCluster,
)

ZONNSMART_MODE_ATTR = (
    0x0402  # [0] Scheduled/auto [1] manual [2] Holiday [3] HolidayTempShow
)
ZONNSMART_WINDOW_DETECT_ATTR = 0x0108  # window is opened [0] false [1] true
ZONNSMART_FROST_PROTECT_ATTR = 0x010A  # [0] inactive [1] active
ZONNSMART_TARGET_TEMP_ATTR = 0x0210  # [0,0,0,210] target room temp (decidegree)
ZONNSMART_TEMPERATURE_ATTR = 0x0218  # [0,0,0,200] current room temp (decidegree)
ZONNSMART_TEMPERATURE_CALIBRATION_ATTR = 0x021B  # temperature calibration (decidegree)
ZONNSMART_WEEK_FORMAT_ATTR = 0x041F  # # [0] 5+2 days [1] 6+1 days, [2] 7 days
ZONNSMART_HOLIDAY_TEMP_ATTR = (
    0x0220  # [0, 0, 0, 170] temp in holiday mode (decidegreee)
)
ZONNSMART_BATTERY_ATTR = 0x0223  # [0,0,0,98] battery charge
ZONNSMART_UPTIME_TIME_ATTR = (
    0x0024  # Seems to be the uptime attribute (sent hourly, increases) [0,200]
)
ZONNSMART_CHILD_LOCK_ATTR = 0x0128  # [0] unlocked [1] child-locked
ZONNSMART_FAULT_DETECTION_ATTR = 0x052D  # [0] no fault [1] fault detected
ZONNSMART_HOLIDAY_DATETIME_ATTR = 0x032E  # holiday mode datetime of begin and end
ZONNSMART_BOOST_TIME_ATTR = 0x0265  # BOOST mode operating time in (sec) [0, 0, 1, 44]
ZONNSMART_OPENED_WINDOW_TEMP = 0x0266  # [0, 0, 0, 210] opened window detected temp
ZONNSMART_COMFORT_TEMP_ATTR = 0x0268  # [0, 0, 0, 210] comfort temp in auto (decidegree)
ZONNSMART_ECO_TEMP_ATTR = 0x0269  # [0, 0, 0, 170] eco temp in auto (decidegree)
ZONNSMART_HEATING_STOPPING_ATTR = 0x016B  # [0] inactive [1] active
# In online mode TRV publishes all values, expires automatically after ca. 1 min
# TRV uses different datatype for send and receive, we need both
ZONNSMART_ONLINE_MODE_ENUM_ATTR = 0x0473  # device publises value as enum datatype
ZONNSMART_ONLINE_MODE_BOOL_ATTR = 0x0173  # but expects to receive bool datatype

ZONNSMART_MAX_TEMPERATURE_VAL = 3000
ZONNSMART_MIN_TEMPERATURE_VAL = 500
ZonnsmartManuClusterSelf = None


class ZONNSMARTManufCluster(TuyaManufClusterAttributes):
    """Manufacturer Specific Cluster of some thermostatic valves."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        global ZonnsmartManuClusterSelf
        ZonnsmartManuClusterSelf = self

    attributes = TuyaManufClusterAttributes.attributes.copy()
    attributes = {
        ZONNSMART_MODE_ATTR: ("mode", t.uint8_t, True),
        ZONNSMART_WINDOW_DETECT_ATTR: ("window_detection", t.uint8_t, True),
        ZONNSMART_FROST_PROTECT_ATTR: ("frost_protection", t.uint8_t, True),
        ZONNSMART_TARGET_TEMP_ATTR: ("target_temperature", t.uint32_t, True),
        ZONNSMART_TEMPERATURE_ATTR: ("temperature", t.uint32_t, True),
        ZONNSMART_TEMPERATURE_CALIBRATION_ATTR: (
            "temperature_calibration",
            t.int32s,
            True,
        ),
        ZONNSMART_WEEK_FORMAT_ATTR: ("week_format", t.uint8_t, True),
        ZONNSMART_HOLIDAY_TEMP_ATTR: ("holiday_temperature", t.uint32_t, True),
        ZONNSMART_BATTERY_ATTR: ("battery", t.uint32_t, True),
        ZONNSMART_UPTIME_TIME_ATTR: ("uptime", t.uint32_t, True),
        ZONNSMART_CHILD_LOCK_ATTR: ("child_lock", t.uint8_t, True),
        ZONNSMART_FAULT_DETECTION_ATTR: ("fault_detected", t.uint8_t, True),
        ZONNSMART_BOOST_TIME_ATTR: ("boost_duration_seconds", t.uint32_t, True),
        ZONNSMART_OPENED_WINDOW_TEMP: ("opened_window_temperature", t.uint32_t, True),
        ZONNSMART_COMFORT_TEMP_ATTR: ("comfort_mode_temperature", t.uint32_t, True),
        ZONNSMART_ECO_TEMP_ATTR: ("eco_mode_temperature", t.uint32_t, True),
        ZONNSMART_HEATING_STOPPING_ATTR: ("heating_stop", t.uint8_t, True),
        ZONNSMART_ONLINE_MODE_BOOL_ATTR: ("online_set", t.uint8_t, True),
        ZONNSMART_ONLINE_MODE_ENUM_ATTR: ("online", t.uint8_t, True),
    }

    DIRECT_MAPPED_ATTRS = {
        ZONNSMART_TEMPERATURE_ATTR: ("local_temperature", lambda value: value * 10),
        ZONNSMART_TEMPERATURE_CALIBRATION_ATTR: (
            "local_temperature_calibration",
            lambda value: value * 10,
        ),
        ZONNSMART_TARGET_TEMP_ATTR: (
            "occupied_heating_setpoint",
            lambda value: value * 10,
        ),
        ZONNSMART_HOLIDAY_TEMP_ATTR: (
            "unoccupied_heating_setpoint",
            lambda value: value * 10,
        ),
        ZONNSMART_FAULT_DETECTION_ATTR: (
            "alarm_mask",
            lambda value: 0x02 if value else 0x00,
        ),
    }

    def _update_attribute(self, attrid, value):
        super()._update_attribute(attrid, value)
        if attrid in self.DIRECT_MAPPED_ATTRS:
            self.endpoint.device.thermostat_bus.listener_event(
                "temperature_change",
                self.DIRECT_MAPPED_ATTRS[attrid][0],
                value
                if self.DIRECT_MAPPED_ATTRS[attrid][1] is None
                else self.DIRECT_MAPPED_ATTRS[attrid][1](value),
            )
        elif attrid == ZONNSMART_WINDOW_DETECT_ATTR:
            self.endpoint.device.window_detection_bus.listener_event("set_value", value)
        elif attrid == ZONNSMART_OPENED_WINDOW_TEMP:
            self.endpoint.device.window_temperature_bus.listener_event(
                "set_value", value
            )
        elif attrid in (ZONNSMART_MODE_ATTR, ZONNSMART_FROST_PROTECT_ATTR):
            self.endpoint.device.thermostat_bus.listener_event(
                "mode_change", attrid, value
            )
        elif attrid == ZONNSMART_HEATING_STOPPING_ATTR:
            self.endpoint.device.thermostat_bus.listener_event(
                "system_mode_change", value == 0
            )
        elif attrid == ZONNSMART_CHILD_LOCK_ATTR:
            self.endpoint.device.ui_bus.listener_event("child_lock_change", value)
            self.endpoint.device.child_lock_bus.listener_event("set_change", value)
        elif attrid == ZONNSMART_BATTERY_ATTR:
            self.endpoint.device.battery_bus.listener_event("battery_change", value)
        elif attrid == ZONNSMART_ONLINE_MODE_ENUM_ATTR:
            self.endpoint.device.online_mode_bus.listener_event("set_change", value)
        elif attrid == ZONNSMART_BOOST_TIME_ATTR:
            self.endpoint.device.boost_bus.listener_event(
                "set_change", 1 if value > 0 else 0
            )

        if attrid == ZONNSMART_TEMPERATURE_CALIBRATION_ATTR:
            self.endpoint.device.temperature_calibration_bus.listener_event(
                "set_value", value / 10
            )
        elif attrid in (ZONNSMART_TEMPERATURE_ATTR, ZONNSMART_TARGET_TEMP_ATTR):
            self.endpoint.device.thermostat_bus.listener_event(
                "state_temp_change", attrid, value
            )


class ZONNSMARTThermostat(TuyaThermostatCluster):
    """Thermostat cluster for some thermostatic valves."""

    class Preset(t.enum8):
        """Working modes of the thermostat."""

        Schedule = 0x00
        Manual = 0x01
        Holiday = 0x02
        HolidayTemp = 0x03
        FrostProtect = 0x04

    attributes = TuyaThermostatCluster.attributes.copy()
    attributes.update(
        {
            0x4002: ("operation_preset", Preset, True),
        }
    )

    DIRECT_MAPPING_ATTRS = {
        "occupied_heating_setpoint": (
            ZONNSMART_TARGET_TEMP_ATTR,
            lambda value: round(value / 10),
        ),
    }

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.endpoint.device.thermostat_bus.listener_event(
            "temperature_change",
            "min_heat_setpoint_limit",
            ZONNSMART_MIN_TEMPERATURE_VAL,
        )
        self.endpoint.device.thermostat_bus.listener_event(
            "temperature_change",
            "max_heat_setpoint_limit",
            ZONNSMART_MAX_TEMPERATURE_VAL,
        )

    def map_attribute(self, attribute, value):
        """Map standardized attribute value to dict of manufacturer values."""
        if attribute in self.DIRECT_MAPPING_ATTRS:
            return {
                self.DIRECT_MAPPING_ATTRS[attribute][0]: value
                if self.DIRECT_MAPPING_ATTRS[attribute][1] is None
                else self.DIRECT_MAPPING_ATTRS[attribute][1](value)
            }
        elif attribute in ("system_mode", "programing_oper_mode"):
            if attribute == "system_mode":
                system_mode = value
                oper_mode = self._attr_cache.get(
                    self.attributes_by_name["programing_oper_mode"].id,
                    self.ProgrammingOperationMode.Simple,
                )
            else:
                system_mode = self._attr_cache.get(
                    self.attributes_by_name["system_mode"].id, self.SystemMode.Heat
                )
                oper_mode = value
            if system_mode == self.SystemMode.Off:
                return {ZONNSMART_HEATING_STOPPING_ATTR: 1}
            if system_mode == self.SystemMode.Heat:
                if oper_mode == self.ProgrammingOperationMode.Schedule_programming_mode:
                    return {ZONNSMART_MODE_ATTR: 0}
                if oper_mode == self.ProgrammingOperationMode.Simple:
                    return {ZONNSMART_MODE_ATTR: 1}
                self.error("Unsupported value for ProgrammingOperationMode")
            else:
                self.error("Unsupported value for SystemMode")
        elif attribute == "operation_preset":
            if value == 0:
                return {ZONNSMART_MODE_ATTR: 0}
            elif value == 1:
                return {ZONNSMART_MODE_ATTR: 1}
            elif value == 3:
                return {ZONNSMART_MODE_ATTR: 3}
            elif value == 4:
                return {ZONNSMART_FROST_PROTECT_ATTR: 1}
            else:
                self.error("Unsupported value for OperationPreset")

    def mode_change(self, attrid, value):
        """Mode change."""
        operation_preset = None

        if attrid == ZONNSMART_MODE_ATTR:
            prog_mode = None
            if value == 0:
                prog_mode = self.ProgrammingOperationMode.Schedule_programming_mode
                operation_preset = self.Preset.Schedule
            elif value == 1:
                prog_mode = self.ProgrammingOperationMode.Simple
                operation_preset = self.Preset.Manual
            elif value == 2:
                prog_mode = self.ProgrammingOperationMode.Simple
                operation_preset = self.Preset.Holiday
            elif value == 3:
                prog_mode = self.ProgrammingOperationMode.Schedule_programming_mode
                operation_preset = self.Preset.HolidayTemp
            else:
                self.error("Unsupported value for Mode")

            if prog_mode is not None:
                self._update_attribute(
                    self.attributes_by_name["programing_oper_mode"].id, prog_mode
                )
        elif attrid == ZONNSMART_FROST_PROTECT_ATTR:
            if value == 1:
                operation_preset = self.Preset.FrostProtect

        if operation_preset is not None:
            self._update_attribute(
                self.attributes_by_name["operation_preset"].id, operation_preset
            )

    def system_mode_change(self, value):
        """System Mode change."""
        self._update_attribute(
            self.attributes_by_name["system_mode"].id,
            self.SystemMode.Heat if value else self.SystemMode.Off,
        )

    def state_temp_change(self, attrid, value):
        """Set heating state based on current and set temperature."""
        if attrid == ZONNSMART_TEMPERATURE_ATTR:
            temp_current = value * 10
            temp_set = self._attr_cache.get(
                self.attributes_by_name["occupied_heating_setpoint"].id
            )
        elif attrid == ZONNSMART_TARGET_TEMP_ATTR:
            temp_current = self._attr_cache.get(
                self.attributes_by_name["local_temperature"].id
            )
            temp_set = value * 10
        else:
            return

        state = 0 if (int(temp_current) >= int(temp_set)) else 1
        self.endpoint.device.thermostat_bus.listener_event("state_change", state)


class ZONNSMARTUserInterface(TuyaUserInterfaceCluster):
    """HVAC User interface cluster for tuya electric heating thermostats."""

    _CHILD_LOCK_ATTR = ZONNSMART_CHILD_LOCK_ATTR


class ZONNSMARTWindowDetection(LocalDataCluster, BinaryInput):
    """Binary cluster for the window detection function of the heating thermostats."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.endpoint.device.window_detection_bus.add_listener(self)
        self._update_attribute(
            self.attributes_by_name["description"].id, "Open Window Detected"
        )

    def set_value(self, value):
        """Set opened window value."""
        self._update_attribute(self.attributes_by_name["present_value"].id, value)


class ZONNSMARTHelperOnOff(LocalDataCluster, OnOff):
    """Helper OnOff cluster for various functions controlled by switch."""

    def set_change(self, value):
        """Set new OnOff value."""
        self._update_attribute(self.attributes_by_name["on_off"].id, value)

    def get_attr_val_to_write(self, value):
        """Return dict with attribute and value for thermostat."""
        return None

    async def write_attributes(self, attributes, manufacturer=None):
        """Defer attributes writing to the set_data tuya command."""
        records = self._write_attr_records(attributes)
        if not records:
            return [[foundation.WriteAttributesStatusRecord(foundation.Status.SUCCESS)]]

        has_change = False
        for record in records:
            attr_name = self.attributes[record.attrid].name
            if attr_name == "on_off":
                value = record.value.value
                has_change = True

        if has_change:
            attr_val = self.get_attr_val_to_write(value)
            if attr_val is not None:
                # global self in case when different endpoint has to exist
                return await ZonnsmartManuClusterSelf.endpoint.tuya_manufacturer.write_attributes(
                    attr_val, manufacturer=manufacturer
                )

        return [
            [
                foundation.WriteAttributesStatusRecord(
                    foundation.Status.FAILURE, r.attrid
                )
                for r in records
            ]
        ]

    async def command(
        self,
        command_id: Union[foundation.GeneralCommand, int, t.uint8_t],
        *args,
        manufacturer: Optional[Union[int, t.uint16_t]] = None,
        expect_reply: bool = True,
        tsn: Optional[Union[int, t.uint8_t]] = None,
    ):
        """Override the default Cluster command."""

        if command_id in (0x0000, 0x0001, 0x0002):

            if command_id == 0x0000:
                value = False
            elif command_id == 0x0001:
                value = True
            else:
                attrid = self.attributes_by_name["on_off"].id
                success, _ = await self.read_attributes(
                    (attrid,), manufacturer=manufacturer
                )
                try:
                    value = success[attrid]
                except KeyError:
                    return foundation.GENERAL_COMMANDS[
                        foundation.GeneralCommand.Default_Response
                    ].schema(command_id=command_id, status=foundation.Status.FAILURE)
                value = not value
            _LOGGER.debug("CALLING WRITE FROM COMMAND")
            (res,) = await self.write_attributes(
                {"on_off": value},
                manufacturer=manufacturer,
            )
            return foundation.GENERAL_COMMANDS[
                foundation.GeneralCommand.Default_Response
            ].schema(command_id=command_id, status=res[0].status)

        return foundation.GENERAL_COMMANDS[
            foundation.GeneralCommand.Default_Response
        ].schema(command_id=command_id, status=foundation.Status.UNSUP_CLUSTER_COMMAND)


class ZONNSMARTBoost(ZONNSMARTHelperOnOff):
    """On/Off cluster for the boost function of the heating thermostats."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.endpoint.device.boost_bus.add_listener(self)

    def get_attr_val_to_write(self, value):
        """Return dict with attribute and value for boot mode."""
        return {ZONNSMART_BOOST_TIME_ATTR: 299 if value else 0}


class ZONNSMARTChildLock(ZONNSMARTHelperOnOff):
    """On/Off cluster for the child lock of the heating thermostats."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.endpoint.device.child_lock_bus.add_listener(self)

    def get_attr_val_to_write(self, value):
        """Return dict with attribute and value for child lock."""
        return {ZONNSMART_CHILD_LOCK_ATTR: value}


class ZONNSMARTOnlineMode(ZONNSMARTHelperOnOff):
    """On/Off cluster for the online mode of the heating thermostats."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.endpoint.device.online_mode_bus.add_listener(self)

    def get_attr_val_to_write(self, value):
        """Return dict with attribute and value for online mode."""
        return {ZONNSMART_ONLINE_MODE_BOOL_ATTR: value}


class ZONNSMARTTemperatureOffset(LocalDataCluster, AnalogOutput):
    """AnalogOutput cluster for setting temperature offset."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.endpoint.device.temperature_calibration_bus.add_listener(self)
        self._update_attribute(
            self.attributes_by_name["description"].id, "Temperature Offset"
        )
        self._update_attribute(self.attributes_by_name["max_present_value"].id, 5)
        self._update_attribute(self.attributes_by_name["min_present_value"].id, -5)
        self._update_attribute(self.attributes_by_name["resolution"].id, 0.1)
        self._update_attribute(self.attributes_by_name["application_type"].id, 0x0009)
        self._update_attribute(self.attributes_by_name["engineering_units"].id, 62)

    def set_value(self, value):
        """Set new temperature offset value."""
        self._update_attribute(self.attributes_by_name["present_value"].id, value)

    def get_value(self):
        """Get current temperature offset value."""
        return self._attr_cache.get(self.attributes_by_name["present_value"].id)

    async def write_attributes(self, attributes, manufacturer=None):
        """Modify value before passing it to the set_data tuya command."""
        for attrid, value in attributes.items():
            if isinstance(attrid, str):
                attrid = self.attributes_by_name[attrid].id
            if attrid not in self.attributes:
                self.error("%d is not a valid attribute id", attrid)
                continue
            self._update_attribute(attrid, value)

            await self.endpoint.tuya_manufacturer.write_attributes(
                {ZONNSMART_TEMPERATURE_CALIBRATION_ATTR: value * 10}, manufacturer=None
            )
        return ([foundation.WriteAttributesStatusRecord(foundation.Status.SUCCESS)],)


class ZONNSMARTWindowOpenedTemp(LocalDataCluster, AnalogOutput):
    """AnalogOutput cluster for temperature when opened window detected."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.endpoint.device.window_temperature_bus.add_listener(self)
        self._update_attribute(
            self.attributes_by_name["description"].id, "Opened Window Temperature"
        )
        self._update_attribute(
            self.attributes_by_name["max_present_value"].id,
            ZONNSMART_MAX_TEMPERATURE_VAL / 100,
        )
        self._update_attribute(
            self.attributes_by_name["min_present_value"].id,
            ZONNSMART_MIN_TEMPERATURE_VAL / 100,
        )
        self._update_attribute(self.attributes_by_name["resolution"].id, 0.5)
        self._update_attribute(self.attributes_by_name["application_type"].id, 0 << 16)
        self._update_attribute(self.attributes_by_name["engineering_units"].id, 62)

    def set_value(self, value):
        """Set temperature value when opened window detected."""
        self._update_attribute(self.attributes_by_name["present_value"].id, value / 10)

    def get_value(self):
        """Get temperature value when opened window detected."""
        return self._attr_cache.get(self.attributes_by_name["present_value"].id)

    async def write_attributes(self, attributes, manufacturer=None):
        """Modify value before passing it to the set_data tuya command."""
        for attrid, value in attributes.items():
            if isinstance(attrid, str):
                attrid = self.attributes_by_name[attrid].id
            if attrid not in self.attributes:
                self.error("%d is not a valid attribute id", attrid)
                continue
            self._update_attribute(attrid, value)

            # different Endpoint for compatibility issue
            await ZonnsmartManuClusterSelf.endpoint.tuya_manufacturer.write_attributes(
                {ZONNSMART_OPENED_WINDOW_TEMP: value * 10}, manufacturer=None
            )
        return ([foundation.WriteAttributesStatusRecord(foundation.Status.SUCCESS)],)

class ZonnsmartTV01_ZG(TuyaThermostat):
    """ZONNSMART TV01-ZG Thermostatic radiator valve."""

    def __init__(self, *args, **kwargs):
        """Init device."""
        self.boost_bus = Bus()
        self.child_lock_bus = Bus()
        self.online_mode_bus = Bus()
        self.temperature_calibration_bus = Bus()
        self.window_detection_bus = Bus()
        self.window_temperature_bus = Bus()
        super().__init__(*args, **kwargs)

    signature = {
        #  endpoint=1 profile=260 device_type=81 device_version=0 input_clusters=[0, 4, 5, 61184]
        #  output_clusters=[10, 25]>
        MODELS_INFO: [
            ("_TZE200_kds0pmmv", "TS0601"),
        ],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.SMART_PLUG,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    TuyaManufClusterAttributes.cluster_id,
                ],
                OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.THERMOSTAT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    ZONNSMARTBoost,
                    ZONNSMARTManufCluster,
                    ZONNSMARTTemperatureOffset,
                    ZONNSMARTThermostat,
                    ZONNSMARTUserInterface,
                    ZONNSMARTWindowDetection,
                    TuyaPowerConfigurationCluster2AA,
                ],
                OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id],
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.COMBINED_INTERFACE,
                INPUT_CLUSTERS: [
                    ZONNSMARTChildLock,
                    ZONNSMARTWindowOpenedTemp,
                ],
                OUTPUT_CLUSTERS: [],
            },
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.COMBINED_INTERFACE,
                INPUT_CLUSTERS: [
                    ZONNSMARTOnlineMode,
                ],
                OUTPUT_CLUSTERS: [],
            },
        }
    }
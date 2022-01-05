"""Module to handle quirks of the  Fanfoss thermostat.
manufacturer specific attributes to control displaying and specific configuration.
"""

import zigpy.profiles.zha as zha_p
from zigpy.quirks import CustomCluster, CustomDevice
from zigpy.zcl.clusters.manufacturer_specific import ManufacturerSpecificCluster
from zigpy.zcl.clusters.general import Basic, Groups, Scenes, Identify, Time, Ota
from zigpy.zcl.clusters.hvac import Thermostat, UserInterface
from zigpy.zcl.clusters.measurement import TemperatureMeasurement
from zigpy.zcl.clusters.smartenergy import Metering
from zigpy.zcl.clusters.homeautomation import ElectricalMeasurement,Diagnostic
import zigpy.types as t

from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)

class OTH3600GAZBCluster(CustomCluster,ManufacturerSpecificCluster):
    """OTH3600GAZB custom cluster."""
    cluster_id = 65281
    name = "OTH3600GAZBCluster"
    ep_attribute = "OTH3600GAZBCluster"
    manufacturer_attributes = {
        0x0010: ("outdoorTempearature", t.int16s),
		0x0011: ("OutdoorTempearatureTimeout", t.uint16_t)
    }

class OTH3600GAZB(CustomDevice):
    """OTH3600GAZB custom device."""
    signature = {
        MODELS_INFO: [('Sinope Technologies', "OTH3600-GA-ZB")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: 260,
                DEVICE_TYPE: 769,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    Thermostat.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    ElectricalMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    65281
                ],
                OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id,65281],
            }
        }
    }

    replacement = {
         ENDPOINTS: {
            1: {
                PROFILE_ID: 260,
                DEVICE_TYPE: 769,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    Thermostat.cluster_id,
                    UserInterface.cluster_id,
                    TemperatureMeasurement.cluster_id,
                    Metering.cluster_id,
                    ElectricalMeasurement.cluster_id,
                    Diagnostic.cluster_id,
                    OTH3600GAZBCluster
                ],
                OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id,65281],
            }
        }
    }
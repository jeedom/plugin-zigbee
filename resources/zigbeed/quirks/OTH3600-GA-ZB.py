"""Module to handle quirks of the  Fanfoss thermostat.
manufacturer specific attributes to control displaying and specific configuration.
"""

import zigpy.profiles.zha as zha_p
from zigpy.quirks import CustomCluster, CustomDevice
from zigpy.zcl.clusters.manufacturer_specific import ManufacturerSpecificCluster
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
        0x0010: ("outdoorTempearature", t.uint16_t),
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
                    0,
                    3,
                    4,
                    5,
                    513,
                    516,
                    1026,
                    1794,
                    2820,
                    2821,
                    65281
                ],
                OUTPUT_CLUSTERS: [10,65281,25],
            }
        }
    }

    replacement = {
         ENDPOINTS: {
            1: {
                PROFILE_ID: 260,
                DEVICE_TYPE: 769,
                INPUT_CLUSTERS: [
                    0,
                    3,
                    4,
                    5,
                    513,
                    516,
                    1026,
                    1794,
                    2820,
                    2821,
                    OTH3600GAZBCluster
                ],
                OUTPUT_CLUSTERS: [10,65281,25],
            }
        }
    }
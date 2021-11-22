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

"""Measurement channels module for Zigbee Home Automation."""
import logging
import zigpy.zcl.clusters.measurement as measurement

import registries
from const import (
	REPORT_CONFIG_DEFAULT,
	REPORT_CONFIG_IMMEDIATE,
	REPORT_CONFIG_MAX_INT,
	REPORT_CONFIG_MIN_INT,
)
import shared
import utils

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.FlowMeasurement.cluster_id)
class FlowMeasurement():
	"""Flow Measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value", "config": REPORT_CONFIG_DEFAULT}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.IlluminanceLevelSensing.cluster_id)
class IlluminanceLevelSensing():
	"""Illuminance Level Sensing channel."""
	REPORT_CONFIG = [{"attr": "level_status", "config": REPORT_CONFIG_DEFAULT}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.IlluminanceMeasurement.cluster_id)
class IlluminanceMeasurement():
	"""Illuminance Measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value", "config": REPORT_CONFIG_DEFAULT}]

@registries.BINARY_SENSOR_CLUSTERS.register(measurement.OccupancySensing.cluster_id)
@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.OccupancySensing.cluster_id)
class OccupancySensing():
	"""Occupancy Sensing channel."""
	REPORT_CONFIG = [{"attr": "occupancy", "config": REPORT_CONFIG_IMMEDIATE}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.PressureMeasurement.cluster_id)
class PressureMeasurement():
	"""Pressure measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value", "config": REPORT_CONFIG_DEFAULT}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.RelativeHumidity.cluster_id)
class RelativeHumidity():
	"""Relative Humidity measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.TemperatureMeasurement.cluster_id)
class TemperatureMeasurement():
	"""Temperature measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.CarbonDioxideConcentration.cluster_id)
class CarbonDioxideConcentration():
	"""CarbonDioxideConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.CarbonMonoxideConcentration.cluster_id)
class CarbonMonoxideConcentration():
	"""CarbonMonoxideConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.EthyleneConcentration.cluster_id)
class EthyleneConcentration():
	"""EthyleneConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.EthyleneOxideConcentration.cluster_id)
class EthyleneOxideConcentration():
	"""EthyleneOxideConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.HydrogenConcentration.cluster_id)
class HydrogenConcentration():
	"""HydrogenConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.NitricOxideConcentration.cluster_id)
class NitricOxideConcentration():
	"""NitricOxideConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.HydrogenSulfideConcentration.cluster_id)
class HydrogenSulfideConcentration():
	"""HydrogenSulfideConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.NitrogenDioxideConcentration.cluster_id)
class NitrogenDioxideConcentration():
	"""NitrogenDioxideConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.OxygenConcentration.cluster_id)
class OxygenConcentration():
	"""OxygenConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.OzoneConcentration.cluster_id)
class OzoneConcentration():
	"""OzoneConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.SulfurDioxideConcentration.cluster_id)
class SulfurDioxideConcentration():
	"""SulfurDioxideConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.DissolvedOxygenConcentration.cluster_id)
class DissolvedOxygenConcentration():
	"""DissolvedOxygenConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.BromateConcentration.cluster_id)
class BromateConcentration():
	"""BromateConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.BromateConcentration.cluster_id)
class BromateConcentration():
	"""BromateConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.ChloraminesConcentration.cluster_id)
class ChloraminesConcentration():
	"""ChloraminesConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.ChlorineConcentration.cluster_id)
class ChlorineConcentration():
	"""ChlorineConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.FecalColiformAndEColiFraction.cluster_id)
class FecalColiformAndEColiFraction():
	"""FecalColiformAndEColiFraction measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.FluorideConcentration.cluster_id)
class FluorideConcentration():
	"""FluorideConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.HaloaceticAcidsConcentration.cluster_id)
class HaloaceticAcidsConcentration():
	"""HaloaceticAcidsConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.TotalTrihalomethanesConcentration.cluster_id)
class TotalTrihalomethanesConcentration():
	"""TotalTrihalomethanesConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.TotalColiformBacteriaFraction.cluster_id)
class TotalColiformBacteriaFraction():
	"""TotalColiformBacteriaFraction measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.Turbidity.cluster_id)
class Turbidity():
	"""Turbidity measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.CopperConcentration.cluster_id)
class CopperConcentration():
	"""CopperConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.LeadConcentration.cluster_id)
class LeadConcentration():
	"""LeadConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.ManganeseConcentration.cluster_id)
class ManganeseConcentration():
	"""ManganeseConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.SulfateConcentration.cluster_id)
class SulfateConcentration():
	"""SulfateConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.BromodichloromethaneConcentration.cluster_id)
class BromodichloromethaneConcentration():
	"""BromodichloromethaneConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.BromoformConcentration.cluster_id)
class BromoformConcentration():
	"""BromoformConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.ChlorodibromomethaneConcentration.cluster_id)
class ChlorodibromomethaneConcentration():
	"""ChlorodibromomethaneConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.ChloroformConcentration.cluster_id)
class ChloroformConcentration():
	"""ChloroformConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.SodiumConcentration.cluster_id)
class SodiumConcentration():
	"""SodiumConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.SodiumConcentration.cluster_id)
class SodiumConcentration():
	"""SodiumConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.FormaldehydeConcentration.cluster_id)
class FormaldehydeConcentration():
	"""FormaldehydeConcentration measurement channel."""
	REPORT_CONFIG = [{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.LeafWetness.cluster_id)
class LeafWetness():
	"""LeafWetness measurement channel."""
	REPORT_CONFIG = [
		{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),},
		{"attr": "min_measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),},
		{"attr": "max_measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}
	]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.SoilMoisture.cluster_id)
class SoilMoisture():
	"""SoilMoisture measurement channel."""
	REPORT_CONFIG = [
		{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),},
		{"attr": "min_measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),},
		{"attr": "max_measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}
	]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.PH.cluster_id)
class PH():
	"""PH measurement channel."""
	REPORT_CONFIG = [
		{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),},
		{"attr": "min_measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),},
		{"attr": "max_measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}
	]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.ElectricalConductivity.cluster_id)
class ElectricalConductivity():
	"""ElectricalConductivity measurement channel."""
	REPORT_CONFIG = [
		{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),},
		{"attr": "min_measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),},
		{"attr": "max_measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}
	]

@registries.ZIGBEE_CHANNEL_REGISTRY.register(measurement.WindSpeed.cluster_id)
class WindSpeed():
	"""WindSpeed measurement channel."""
	REPORT_CONFIG = [
		{"attr": "measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),},
		{"attr": "min_measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),},
		{"attr": "max_measured_value","config": (REPORT_CONFIG_MIN_INT, REPORT_CONFIG_MAX_INT, 50),}
	]
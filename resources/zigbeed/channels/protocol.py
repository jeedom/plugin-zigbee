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

"""Protocol channels module for Zigbee Home Automation."""
import logging

import zigpy.zcl.clusters.protocol as protocol

import registries
import shared
import utils

@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.AnalogInputExtended.cluster_id)
class AnalogInputExtended():
	"""Analog Input Extended channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.AnalogInputRegular.cluster_id)
class AnalogInputRegular():
	"""Analog Input Regular channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.AnalogOutputExtended.cluster_id)
class AnalogOutputExtended():
	"""Analog Output Regular channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.AnalogOutputRegular.cluster_id)
class AnalogOutputRegular():
	"""Analog Output Regular channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.AnalogValueExtended.cluster_id)
class AnalogValueExtended():
	"""Analog Value Extended edition channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.AnalogValueRegular.cluster_id)
class AnalogValueRegular():
	"""Analog Value Regular channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.BacnetProtocolTunnel.cluster_id)
class BacnetProtocolTunnel():
	"""Bacnet Protocol Tunnel channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.BinaryInputExtended.cluster_id)
class BinaryInputExtended():
	"""Binary Input Extended channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.BinaryInputRegular.cluster_id)
class BinaryInputRegular():
	"""Binary Input Regular channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.BinaryOutputExtended.cluster_id)
class BinaryOutputExtended():
	"""Binary Output Extended channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.BinaryOutputRegular.cluster_id)
class BinaryOutputRegular():
	"""Binary Output Regular channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.BinaryValueExtended.cluster_id)
class BinaryValueExtended():
	"""Binary Value Extended channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.BinaryValueRegular.cluster_id)
class BinaryValueRegular():
	"""Binary Value Regular channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.GenericTunnel.cluster_id)
class GenericTunnel():
	"""Generic Tunnel channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.MultistateInputExtended.cluster_id)
class MultiStateInputExtended():
	"""Multistate Input Extended channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.MultistateInputRegular.cluster_id)
class MultiStateInputRegular():
	"""Multistate Input Regular channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.MultistateOutputExtended.cluster_id)
class MultiStateOutputExtended():
	"""Multistate Output Extended channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.MultistateOutputRegular.cluster_id)
class MultiStateOutputRegular():
	"""Multistate Output Regular channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.MultistateValueExtended.cluster_id)
class MultiStateValueExtended():
	"""Multistate Value Extended channel."""


@registries.ZIGBEE_CHANNEL_REGISTRY.register(protocol.MultistateValueRegular.cluster_id)
class MultiStateValueRegular():
	"""Multistate Value Regular channel."""

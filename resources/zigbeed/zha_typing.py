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

from typing import TYPE_CHECKING, Callable, TypeVar

import zigpy.device
import zigpy.endpoint
import zigpy.group
import zigpy.zcl
import zigpy.zdo

ChannelType = "ZigbeeChannel"
ChannelsType = "Channels"
ChannelPoolType = "ChannelPool"
ClientChannelType = "ClientChannel"
ZDOChannelType = "ZDOChannel"
ZhaDeviceType = "ZHADevice"
ZhaEntityType = "ZHAEntity"
ZhaGatewayType = "ZHAGateway"
ZhaGroupType = "ZHAGroupType"
ZigpyClusterType = zigpy.zcl.Cluster
ZigpyDeviceType = zigpy.device.Device
ZigpyEndpointType = zigpy.endpoint.Endpoint
ZigpyGroupType = zigpy.group.Group
ZigpyZdoType = zigpy.zdo.ZDO

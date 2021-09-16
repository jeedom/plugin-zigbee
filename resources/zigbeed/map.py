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


import asyncio
import enum
import logging
import random
import time

import attr
import zigpy.zdo.types as zdo_t
from zigpy.exceptions import DeliveryError
from zigpy.util import retryable
import zigpy.exceptions as zigpy_exc


class NeighbourType(enum.IntEnum):
    Coordinator = 0x0
    Router = 0x1
    End_Device = 0x2
    Unknown = 0x3


class RxOnIdle(enum.IntEnum):
    Off = 0x0
    On = 0x1
    Unknown = 0x2


class Relation(enum.IntEnum):
    Parent = 0x0
    Child = 0x1
    Sibling = 0x2
    None_of_the_above = 0x3
    Previous_Child = 0x4


class PermitJoins(enum.IntEnum):
    Not_Accepting = 0x0
    Accepting = 0x1
    Unknown = 0x2


class TopologyBuilder():
    def __init__(self, app):
        """Init instance."""
        self._app = app
        self._in_process = None
        self._seen = {}

    async def build(self):
        self._seen.clear()
        for device in self._app.devices.values():
            nei = await Neighbour.scan_device(device)
            self._seen[nei.ieee] = nei
        await self.sanity_check()
        self._current = {**self._seen}
        self._timestamp = time.time()
        return self._seen

    async def sanity_check(self):
        """Check discovered neighbours vs Zigpy database."""
        # do we have extra neighbours
        for nei in self._seen.values():
            if nei.ieee not in self._app.devices:
                logging.info(
                    "["+str(nei.ieee)+"][map.sanity_check] Neighbour not in 'zigbee.db': %s - %s", nei.ieee, nei.device_type)
        # are we missing neighbours
        for dev in self._app.devices.values():
            if dev.ieee in self._seen:
                continue
            logging.info("["+str(dev.ieee)+"][map.sanity_check] %s (%s %s) was not found in the neighbours tables",
                         dev.ieee, dev.manufacturer, dev.model,)
            nei = Neighbour(dev.ieee, f"0x{dev.nwk:04x}", "unk")
            nei.device = dev
            nei.model = dev.model
            nei.manufacturer = dev.manufacturer
            nei.offline = True
            if dev.node_desc.logical_type is not None:
                nei.device_type = dev.node_desc.logical_type.name
            self._seen[dev.ieee] = nei


@attr.s
class Neighbour():
    ieee = attr.ib(default=None)
    nwk = attr.ib(default=None)
    lqi = attr.ib(default=None)
    rssi = attr.ib(default=None)
    pan_id = attr.ib(default=None)
    device_type = attr.ib(default="unk")
    rx_on_when_idle = attr.ib(default=None)
    relation = attr.ib(default=None)
    new_joins_accepted = attr.ib(default=None)
    depth = attr.ib(default=None)
    device = attr.ib(default=None)
    model = attr.ib(default=None)
    manufacturer = attr.ib(default=None)
    neighbours = attr.ib(factory=list)
    offline = attr.ib(factory=bool)
    supported = attr.ib(default=True)

    @classmethod
    def new_from_record(cls, record):
        """Create new neighbour from a neighbour record."""
        r = Neighbour()
        r.offline = False
        r.pan_id = str(record.extended_pan_id)
        r.ieee = record.ieee
        r.device_type = record.device_type.name
        r.rx_on_when_idle = record.rx_on_when_idle.name
        if record.relationship == zdo_t.Neighbor.RelationShip.NoneOfTheAbove:
            r.relation = "None_of_the_above"
        else:
            r.relation = record.relationship.name
        r.new_joins_accepted = record.permit_joining.name
        r.depth = record.depth
        r.lqi = record.lqi
        return r

    def _update_info(self):
        """Update info based on device information."""
        if self.device is None:
            return
        self.nwk = "0x{:04x}".format(self.device.nwk)
        self.model = self.device.model
        self.rssi = self.device.rssi
        self.manufacturer = self.device.manufacturer
        if self.device.node_desc is not None:
            self.device_type = self.device.node_desc.logical_type.name
        else:
            self.device_type = "unknown"
        if self.lqi is None:
            self.lqi = self.device.lqi

    async def scan_device(device):
        """New neighbour from a scan."""
        r = Neighbour()
        r.offline = False
        r.device = device
        r.ieee = device.ieee
        r._update_info()
        await r.scan()
        return r

    async def scan(self):
        """Scan for neighbours."""
        for neighbor in self.device.neighbors:
            new = self.new_from_record(neighbor.neighbor)
            try:
                new.device = self.device.application.get_device(new.ieee)
                new._update_info()
            except KeyError:
                logging.warning(
                    "["+str(new.ieee)+"][map.scan] neighbour %s is not in 'zigbee.db'", new.ieee)
            self.neighbours.append(new)
        logging.info(
            "[map.scan] Done scanning. Total %s neighbours", len(self.neighbours))

    def json(self):
        """Return JSON representation of the neighbours table."""
        res = []
        for nei in sorted(self.neighbours, key=lambda x: x.ieee):
            if nei.device is not None:
                assert nei.ieee == nei.device.ieee
            dict_nei = attr.asdict(
                nei,
                filter=lambda a, v: a.name not in ("device", "neighbours"),
                retain_collection_types=True,
            )
            dict_nei["ieee"] = str(dict_nei["ieee"])
            res.append(dict_nei)
        return {
            "ieee": str(self.ieee),
            "nwk": self.nwk,
            "lqi": self.lqi,
            "rssi": self.rssi,
            "device_type": self.device_type,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "offline": self.offline,
            "neighbours": res,
        }

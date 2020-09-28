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
	def __init__(self,app):
		"""Init instance."""
		self._app = app
		self._in_process = None
		self._seen = {}
		self._failed = {}

	async def build(self):
		self._seen.clear()
		self._failed.clear()

		seed = self._app.get_device(nwk=0x0000)
		logging.debug("Building topology starting from coordinator")
		try:
			await self.scan_device(seed)
		except zigpy_exc.ZigbeeException as exc:
			logging.error("failed to scan %s device: %s", seed.ieee, exc)
			return

		pending = self._pending()
		while pending:
			for nei in pending:
				try:
					await nei.scan()
				except (zigpy_exc.ZigbeeException, asyncio.TimeoutError):
					logging.warning("Couldn't scan %s neighbours", nei.ieee)
					self._failed[nei.ieee] = nei
					nei.offline = True
					continue
				await self.process_neighbour_table(nei)
			pending = self._pending()

		await self.sanity_check()
		return self._seen

	def _pending(self):
	   """Return neighbours still pending a scan."""
	   pending = [
		   n
		   for n in self._seen.values()
		   if not n.neighbours
		   and n.supported
		   and n.device is not None
		   and n.device_type
		   in (NeighbourType.Coordinator.name, NeighbourType.Router.name)
		   and n.ieee not in self._failed
	   ]

	   if pending:
		   logging.debug( "continuing neighbour scan. Neighbours discovered: %s",[n.ieee for n in pending],)
	   else:
		   logging.debug("Finished neighbour scan pass. Failed: %s",[k for k in self._failed.keys()],)
	   return pending

	async def sanity_check(self):
		"""Check discovered neighbours vs Zigpy database."""
		# do we have extra neighbours
		for nei in self._seen.values():
			if nei.ieee not in self._app.devices:
				logging.debug("Neighbour not in 'zigbee.db': %s - %s", nei.ieee, nei.device_type)

		# are we missing neighbours
		for dev in self._app.devices.values():
			if dev.ieee in self._seen:
				continue
			if dev.ieee in self._failed:
				logging.debug(("%s (%s %s) was discovered in the neighbours ""tables, but did not respond"),dev.ieee,dev.manufacturer,dev.model,)
			else:
				logging.debug("%s (%s %s) was not found in the neighbours tables",dev.ieee,dev.manufacturer,dev.model,)
				nei = Neighbour(dev.ieee, f"0x{dev.nwk:04x}", "unk")
				nei.device = dev
				nei.model = dev.model
				nei.manufacturer = dev.manufacturer
				nei.offline = True
				if dev.node_desc.logical_type is not None:
					nei.device_type = dev.node_desc.logical_type.name
				self._seen[dev.ieee] = nei

	async def scan_device(self, device):
		"""Scan device neigbours."""
		nei = await Neighbour.scan_device(device)
		await self.process_neighbour_table(nei)

	async def process_neighbour_table(self, nei):
		for entry in nei.neighbours:
			if entry.ieee in self._seen:
				continue
			logging.debug("Adding %s to all neighbours", entry.ieee)
			self._seen[entry.ieee] = entry

@attr.s
class Neighbour():
	ieee = attr.ib(default=None)
	nwk = attr.ib(default=None)
	lqi = attr.ib(default=None)
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
	def new_from_record(cls,record):
		"""Create new neighbour from a neighbour record."""
		r = cls()
		r.offline = False
		r.pan_id = str(record.PanId)
		r.ieee = record.IEEEAddr
		raw = record.NeighborType & 0x03
		try:
			r.device_type = NeighbourType(raw).name
		except ValueError:
			r.device_type = "undefined_0x{:02x}".format(raw)
		raw = (record.NeighborType >> 2) & 0x03
		try:
			r.rx_on_when_idle = RxOnIdle(raw).name
		except ValueError:
			r.rx_on_when_idle = "undefined_0x{:02x}".format(raw)
		raw = (record.NeighborType >> 4) & 0x07
		try:
			r.relation = Relation(raw).name
		except ValueError:
			r.relation = "undefined_0x{:02x}".format(raw)

		raw = record.PermitJoining & 0x02
		try:
			r.new_joins_accepted = PermitJoins(raw).name
		except ValueError:
			r.new_joins_accepted = "undefined_0x{:02x}".format(raw)
		r.depth = record.Depth
		if hasattr(record, 'LQI'):
			r.lqi = record.LQI
		return r

	def _update_info(self):
		"""Update info based on device information."""
		if self.device is None:
			return
		self.nwk = "0x{:04x}".format(self.device.nwk)
		self.model = self.device.model
		self.manufacturer = self.device.manufacturer

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
		idx = 0
		while True:
			status, val = await self.device.zdo.request(zdo_t.ZDOCmd.Mgmt_Lqi_req, idx, tries=3, delay=1)
			logging.debug("neighbor request Status: %s. Response: %r", status, val)
			if zdo_t.Status.SUCCESS != status:
				self.supported = False
				logging.debug("device does not support 'Mgmt_Lqi_req'")
				return

			neighbors = val.NeighborTableList
			logging.debug("******************Neighbors of "+str(self.device.ieee)+' => '+str(neighbors))
			for neighbor in neighbors:
				new = self.new_from_record(neighbor)
				if repr(new.ieee) in ("00:00:00:00:00:00:00:00","ff:ff:ff:ff:ff:ff:ff:ff",):
					logging.debug("Ignoring invalid neighbour: %s", new.ieee)
					idx += 1
					continue

				try:
					new.device = self.device.application.get_device(new.ieee)
					new._update_info()
				except KeyError:
					logging.warning("neighbour %s is not in 'zigbee.db'", new.ieee)
				self.neighbours.append(new)
				idx += 1
			if idx >= val.Entries:
				break
			if len(neighbors) <= 0:
				idx += 1
				logging.debug("Neighbor count is 0 (idx : %d)", idx)

			await asyncio.sleep(random.uniform(1.0, 1.5))
			logging.debug("Querying next starting at %s", idx)

		logging.debug("Done scanning. Total %s neighbours", len(self.neighbours))

	def json(self):
		"""Return JSON representation of the neighbours table."""
		res = []
		for nei in sorted(self.neighbours, key=lambda x: x.ieee):
			if nei.device is not None:
				assert nei.ieee == nei.device.ieee
			dict_nei = attr.asdict(nei,filter=lambda a, v: a.name not in ("device", "neighbours"),retain_collection_types=True,)
			dict_nei["ieee"] = str(dict_nei["ieee"])
			res.append(dict_nei)
		return {
			"ieee": str(self.ieee),
			"nwk": self.nwk,
			"lqi": self.lqi,
			"device_type": self.device_type,
			"manufacturer": self.manufacturer,
			"model": self.model,
			"offline": self.offline,
			"neighbours": res,
		}

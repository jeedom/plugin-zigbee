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

import json
import pathlib
import logging
import zigpy.types
from zigpy.zdo import types as zdo_t
from bellows.zigbee.application import ControllerApplication

LOGGER = logging.getLogger(__name__)

class JSONPersistingListener:
    def __init__(self, database_file, application):
        self._database_file = pathlib.Path(database_file)
        self._application = application

        self._db = {'devices': {}}

    def device_joined(self, device):
        self.raw_device_initialized(device)

    def device_initialized(self, device):
        # This is passed in a quirks device
        pass

    def device_left(self, device):
        self._db['devices'].pop(str(device.ieee))
        self._dump()

    def raw_device_initialized(self, device):
        self._db['devices'][str(device.ieee)] = self._serialize_device(device)
        self._dump()

    def device_removed(self, device):
        self._db['devices'].pop(str(device.ieee))
        self._dump()

    def attribute_updated(self, cluster, attrid, value):
        self._dump()

    def _serialize_device(self, device):
        obj = {
            'ieee': str(device.ieee),
            'nwk': device.nwk,
            'status': device.status,
            'node_descriptor': None if not device.node_desc.is_valid else list(device.node_desc.serialize()),
            'endpoints': [],
        }

        for endpoint_id, endpoint in device.endpoints.items():
            if endpoint_id == 0:
                continue  # Skip zdo

            endpoint_obj = {}
            endpoint_obj['id'] = endpoint_id
            endpoint_obj['status'] = endpoint.status
            endpoint_obj['device_type'] = getattr(endpoint, 'device_type', None)
            endpoint_obj['profile_id'] = getattr(endpoint, 'profile_id', None)
            endpoint_obj['output_clusters'] = [cluster.cluster_id for cluster in endpoint.out_clusters.values()]
            endpoint_obj['input_clusters'] = [cluster.cluster_id for cluster in endpoint.in_clusters.values()]

            obj['endpoints'].append(endpoint_obj)

        return obj

    def _dump(self):
        devices = []

        for device in self._application.devices.values():
            devices.append(self._serialize_device(device))

        existing = self._database_file.read_text()
        new = json.dumps({'devices': devices}, separators=(', ', ': '), indent=4)

        # Don't waste writes
        if existing == new:
            return

        self._database_file.write_text(new)

    def load(self):
        try:
            state_obj = json.loads(self._database_file.read_text())
        except FileNotFoundError:
            LOGGER.warning('Database is empty! Creating an empty one...')
            self._database_file.write_text('')

            state_obj = {'devices': []}

        for obj in state_obj['devices']:
            ieee = zigpy.types.named.EUI64([zigpy.types.uint8_t(int(c, 16)) for c in obj['ieee'].split(':')][::-1])

            assert obj['ieee'] in repr(ieee)

            device = self._application.add_device(ieee, obj['nwk'])
            device.status = zigpy.device.Status(obj['status'])

            if 'node_descriptor' in obj and obj['node_descriptor'] is not None:
                device.node_desc = zdo_t.NodeDescriptor.deserialize(bytearray(obj['node_descriptor']))[0]

            for endpoint_obj in obj['endpoints']:
                endpoint = device.add_endpoint(endpoint_obj['id'])
                endpoint.profile_id = endpoint_obj['profile_id']
                device_type = endpoint_obj['device_type']

                try:
                    if endpoint.profile_id == 260:
                        device_type = zigpy.profiles.zha.DeviceType(device_type)
                    elif endpoint.profile_id == 49246:
                        device_type = zigpy.profiles.zll.DeviceType(device_type)
                except ValueError:
                    pass

                endpoint.device_type = device_type
                endpoint.status = zigpy.endpoint.Status(endpoint_obj['status'])

                for output_cluster in endpoint_obj['output_clusters']:
                    endpoint.add_output_cluster(output_cluster)

                for input_cluster in endpoint_obj['input_clusters']:
                    cluster = endpoint.add_input_cluster(input_cluster)


# Use this in place of your radio's ControllerApplication
class JSONControllerApplication(ControllerApplication):
    def __init__(self, config):
        super().__init__(self.SCHEMA(config))
        # Replace the internal SQLite DB listener with our own
        self._dblistener = JSONPersistingListener(self.config['json_database_path'], self)
        self.add_listener(self._dblistener)
        self._dblistener.load()
        self._dblistener._dump()

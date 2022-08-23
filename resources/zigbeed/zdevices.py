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

import logging
import time
import json
import asyncio
import time
import sys
import os
import shared
import utils
import traceback
import registries
import zqueue
import zigpy
from map import *
import specifics
from zigpy.zcl.clusters.general import Groups
import zgp


async def command(_data):
    device = find(_data['ieee'])
    if device == None:
        raise Exception("Device not found")
    for cmd in _data['cmd']:
        if not cmd['endpoint'] in device.endpoints:
            raise Exception("["+str(device._ieee)+"][zdevices.command] Endpoint not found : "+str(cmd['endpoint']))
        endpoint = device.endpoints[cmd['endpoint']]
        cluster = None
        if 'cluster_type' in cmd:
            if cmd['cluster_type'] == 'out' and cmd['cluster'] in endpoint.out_clusters:
                cluster = endpoint.out_clusters[cmd['cluster']]
            elif cmd['cluster'] in endpoint.in_clusters:
                cluster = endpoint.in_clusters[cmd['cluster']]
        elif hasattr(endpoint, cmd['cluster']):
            cluster = getattr(endpoint, cmd['cluster'])
        if cluster is None:
            raise Exception("["+str(device._ieee)+"][zdevices.command] Cluster not found : "+str(cmd['cluster']))
        if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id], cmd['command']):
            command = getattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id], cmd['command'])
            if 'await' in cmd:
                logging.info("["+str(device._ieee)+"][zdevices.command] Use specific command action in await mode for"+str(cmd['command']))
                await command(cluster, cmd)
            else:
                logging.info("["+str(device._ieee)+"][zdevices.command] Use specific command action for "+str(cmd['command']))
                asyncio.create_task(command(cluster, cmd))
            continue
        if not hasattr(cluster, cmd['command']):
            raise Exception("Command not found : "+str(cmd['command']))
        command = getattr(cluster, cmd['command'])
        if 'args' in cmd:
            args = cmd['args']
            if cmd['command'] == 'image_notify' :
                command(*args)
                return
            if 'await' in cmd and cmd['await'] == 1 :
                try:
                    logging.debug("["+str(device._ieee)+"][zdevices.command] Execution await of "+str(cmd['command'])+" args : "+str(cmd['args']))
                    await command(*args)
                except Exception as e:
                    logging.error(
                        "["+str(device._ieee)+"][zdevices.command] Command failed retry in 1s : "+str(e))
                    await asyncio.sleep(1)
                    await command(*args)
            else:
                logging.debug("["+str(device._ieee)+"][zdevices.command] Execution of "+str(cmd['command'])+" args : "+str(cmd['args']))
                asyncio.create_task(command(*args))
        else:
            if 'await' in cmd:
                try:
                    logging.debug("["+str(device._ieee)+"][zdevices.command] Execution await of "+str(cmd['command']))
                    await command()
                except Exception as e:
                    logging.error(
                        "["+str(device._ieee)+"][zdevices.command] Command failed retry in 1s : "+str(e))
                    await asyncio.sleep(1)
                    await command()
            else:
                logging.debug("["+str(device._ieee)+"][zdevices.command] Execution of "+str(cmd['command']))
                asyncio.create_task(command())


async def write_attributes(_data):
    device = find(_data['ieee'])
    if device == None:
        raise Exception("Device not found")
    for attribute in _data['attributes']:
        if not attribute['endpoint'] in device.endpoints:
            raise Exception(
                "["+str(device._ieee)+"][zdevices.write_attributes] Endpoint not found : "+str(attribute['endpoint']))
        endpoint = device.endpoints[attribute['endpoint']]
        if attribute['cluster_type'] == 'in':
            if not attribute['cluster'] in endpoint.in_clusters:
                raise Exception(
                    "["+str(device._ieee)+"][zdevices.write_attributes] Cluster not found : "+str(attribute['cluster']))
            cluster = endpoint.in_clusters[attribute['cluster']]
        else:
            if not attribute['cluster'] in endpoint.out_clusters:
                raise Exception(
                    "["+str(device._ieee)+"][zdevices.write_attributes] Cluster not found : "+str(attribute['cluster']))
            cluster = endpoint.out_clusters[attribute['cluster']]
        attributes = {}
        for i in attribute['attributes']:
            attributes[int(i)] = attribute['attributes'][i]
        manufacturer = None
        if 'manufacturer' in attribute and attribute['manufacturer'] != '':
            manufacturer = attribute['manufacturer']
        try:
            await cluster.write_attributes(attributes, manufacturer=manufacturer)
        except Exception as e:
            logging.error(
                "["+str(device._ieee)+"][zdevices.write_attributes] Write attribut retry in 1s : "+str(e))
            await asyncio.sleep(1)
            await cluster.write_attributes(attributes, manufacturer=manufacturer)
        asyncio.ensure_future(check_write_attributes(_data))


async def check_write_attributes(_data):
    await asyncio.sleep(15)
    device = find(_data['ieee'])
    logging.info('['+str(device._ieee) +
                 '][zdevices.check_write_attributes] Check write attribute for : '+str(_data))
    for attribute in _data['attributes']:
        if not attribute['endpoint'] in device.endpoints:
            return
        endpoint = device.endpoints[attribute['endpoint']]
        if attribute['cluster_type'] == 'in':
            if not attribute['cluster'] in endpoint.in_clusters:
                raise Exception("Cluster not found : " +
                                str(attribute['cluster']))
            cluster = endpoint.in_clusters[attribute['cluster']]
        else:
            if not attribute['cluster'] in endpoint.out_clusters:
                return
            cluster = endpoint.out_clusters[attribute['cluster']]
        attributes = {}
        manufacturer = None
        if 'manufacturer' in attribute and attribute['manufacturer'] != '':
            manufacturer = attribute['manufacturer']
        for i in attribute['attributes']:
            values = await cluster.read_attributes([int(i)], True, manufacturer=manufacturer)
            if not 0 in values:
                continue
            if values[0][int(i)] != attribute['attributes'][i]:
                logging.info('['+str(device._ieee)+'][zdevice.check_write_attributes] Attribute value issue for device : '+str(_data['ieee'])+' '+str(attribute['endpoint']) +
                             '/'+str(attribute['cluster'])+'/'+str(int(i))+' expected value : '+str(attribute['attributes'][i])+' current value : '+str(values[0][int(i)]))
                attributes[int(i)] = attribute['attributes'][i]
        if len(attributes) == 0:
            logging.info(
                '['+str(device._ieee)+'][zdevices.check_write_attributes] All attribute write succefull do nothing')
            return
        await cluster.write_attributes(attributes, manufacturer=manufacturer)


async def initialize(device):
    logging.info(
        "["+str(device._ieee)+"][zdevices.initialize] Begin device initialize")
    for ep_id, endpoint in device.endpoints.items():
        if ep_id == 0 or ep_id == zgp.endpoint_id:  # Ignore ZDO and green power
            continue
        if endpoint.device_type == zgp.device_type:  # No binding for GreenPower device
            continue
        for cluster in endpoint.in_clusters.values():
            if not hasattr(cluster, 'ep_attribute') or (cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id], 'NO_BINDING') and registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].NO_BINDING):
                continue
            logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(ep_id) +
                         "] Begin configuration of input cluster '%s', is_server '%s'", cluster.ep_attribute, cluster.is_server)
            if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY:
                try:
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] Bind input cluster '%s'", cluster.ep_attribute)
                    await cluster.bind()
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] Bound '%s' input cluster", cluster.ep_attribute)
                except Exception as ex:
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] Failed to bind '%s' input cluster: %s", cluster.ep_attribute, str(ex))
                if cluster.is_server and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id], 'REPORT_CONFIG'):
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] This input cluster have REPORT_CONFIG, we need to configure it")
                    kwargs = {}
                    for report in registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].REPORT_CONFIG:
                        attr = report["attr"]
                        attr_name = cluster.attributes.get(attr, [attr])[0]
                        min_report_int, max_report_int, reportable_change = report["config"]
                        try:
                            logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(ep_id)+"] Reporting '%s' attr on '%s' input cluster: %d/%d/%d: For: '%s'",
                                         attr_name, cluster.ep_attribute, min_report_int, max_report_int, reportable_change, device.ieee)
                            await cluster.configure_reporting(attr, min_report_int, max_report_int, reportable_change, **kwargs)
                        except Exception as ex:
                            logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                                ep_id)+"] Failed to set reporting for '%s' attr on '%s' input cluster: %s", attr_name, cluster.ep_attribute, str(ex),)
                try:
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] Set specific reporting for '%s' attr on '%s' input cluster: %s", device._manufacturer, device._model, cluster.cluster_id)
                    await specifics.reporting(device._manufacturer, device._model, cluster.cluster_id, ep_id, cluster)
                except Exception as ex:
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] Failed to set specific reporting for '%s' attr on '%s' input cluster: %s", device._manufacturer, device._model, str(ex),)
                try:
                    if hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id], 'initialize'):
                        logging.info('['+str(device._ieee)+'][zdevices.initialize][Endpoint '+str(ep_id)+'] Intput cluster '+str(
                            cluster.cluster_id) + ' has specific function to initialize, I used it')
                        await registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].initialize(cluster)
                except Exception as ex:
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] Failed to initialize '%s' input cluster: %s", cluster.ep_attribute, str(ex))
            logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                ep_id)+"] End configuration of input cluster '%s'", cluster.ep_attribute)
        for cluster in endpoint.out_clusters.values():
            if not hasattr(cluster, 'ep_attribute') or (cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id], 'NO_BINDING') and registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].NO_BINDING):
                continue
            logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(ep_id) +
                         "] Begin configuration of output cluster '%s', is_server '%s'", cluster.ep_attribute, cluster.is_server)
            if cluster.cluster_id in registries.ZIGBEE_CHANNEL_REGISTRY:
                try:
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] Bind '%s' output cluster", cluster.ep_attribute)
                    await cluster.bind()
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] Bound '%s' output cluster", cluster.ep_attribute)
                except Exception as ex:
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] Failed to bind '%s' output cluster: %s", cluster.ep_attribute, str(ex))
                if cluster.is_server and hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id], 'REPORT_CONFIG'):
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] This output cluster have REPORT_CONFIG, we need to configure it")
                    kwargs = {}
                    for report in registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].REPORT_CONFIG:
                        attr = report["attr"]
                        attr_name = cluster.attributes.get(attr, [attr])[0]
                        min_report_int, max_report_int, reportable_change = report["config"]
                        try:
                            logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(ep_id)+"] reporting '%s' attr on '%s' output cluster: %d/%d/%d: For: '%s'",
                                         attr_name, cluster.ep_attribute, min_report_int, max_report_int, reportable_change, device.ieee)
                            await cluster.configure_reporting(attr, min_report_int, max_report_int, reportable_change, **kwargs)
                        except Exception as ex:
                            logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                                ep_id)+"] failed to set reporting for '%s' attr on '%s' output cluster: %s", attr_name, cluster.ep_attribute, str(ex),)
                try:
                    if hasattr(registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id], 'initialize'):
                        logging.info('['+str(device._ieee)+'][zdevices.initialize][Endpoint '+str(ep_id)+'] Output cluster '+str(
                            cluster.cluster_id) + ' has specific function to initialize, I used it')
                        await registries.ZIGBEE_CHANNEL_REGISTRY[cluster.cluster_id].initialize(cluster)
                except Exception as ex:
                    logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                        ep_id)+"] Failed to initialize '%s' output cluster: %s", cluster.ep_attribute, str(ex))
            logging.info("["+str(device._ieee)+"][zdevices.initialize][Endpoint "+str(
                ep_id)+"] End configuration of output cluster '%s'", cluster.ep_attribute)
    try:
        await get_basic_info(device)
    except Exception as e:
        logging.warning(
            "["+str(device._ieee)+"][zdevices.initialize] Error on get_basic_info : "+str(e))
    if shared.CONTROLLER == 'deconz':  # Force save neightbors on deconz after inclusion
        logging.info(
            "["+str(device._ieee)+"][zdevices.initialize] It's deconz key, force neightbors scan")
        await shared.ZIGPY.get_device(ieee=shared.ZIGPY.ieee).neighbors.scan()
    logging.info(
        "["+str(device._ieee)+"][zdevices.initialize] End device initialize")


async def get_basic_info(device):
    logging.warning(
        "["+str(device._ieee)+"][zdevices.get_basic_info] Begin get basic info from device")
    for ep_id, endpoint in device.endpoints.items():
        if ep_id == 0 or ep_id == zgp.endpoint_id:  # Ignore ZDO and green power
            continue
        if endpoint.device_type == zgp.device_type:  # No binding for GreenPower device
            continue
        for cluster in endpoint.in_clusters.values():
            if cluster.cluster_id != 0:
                continue
            logging.warning(
                "["+str(device._ieee)+"][zdevices.get_basic_info] Endpoint found")
            try:
                await cluster.read_attributes([4, 5], True)
                await asyncio.sleep(1)
            except Exception as e:
                logging.warning(
                    "["+str(device._ieee)+"][zdevices.get_basic_info] Error on read attribute level 1 : "+str(e))
            try:
                await cluster.read_attributes([0, 1, 2, 3], True)
                await asyncio.sleep(1)
            except Exception as e:
                logging.warning(
                    "["+str(device._ieee)+"][zdevices.get_basic_info] Error on read attribute level 2 : "+str(e))
            try:
                await cluster.read_attributes([7], True)
                await asyncio.sleep(1)
            except Exception as e:
                logging.warning(
                    "["+str(device._ieee)+"][zdevices.get_basic_info] Error on read attribute level 3 : "+str(e))
            try:
                await cluster.read_attributes([6, 16384], True)
            except Exception as e:
                logging.warning(
                    "["+str(device._ieee)+"][zdevices.get_basic_info] Error on read attribute level 4 : "+str(e))
    logging.warning(
        "["+str(device._ieee)+"][zdevices.get_basic_info] End get basic info from device")


def is_groupable(device):
    for ep_id, endpoint in device.endpoints.items():
        if ep_id == 0:
            continue
        for cluster in endpoint.in_clusters.values():
            if Groups.cluster_id == cluster.cluster_id:
                return True
    return False


async def serialize(device, with_attributes=1):
    logging.info("["+str(device._ieee) +
                 '][zdevices.serialize] Serialize device with attributes : '+str(with_attributes))
    obj = {
        'ieee': str(device.ieee),
        'nwk': device.nwk,
        'status': device.status,
        'lqi': str(device.lqi),
        'rssi': str(device.rssi),
        'last_seen': str(device.last_seen),
        'node_descriptor': None if device.node_desc is None else list(device.node_desc.serialize()),
        'endpoints': [],
        'signature': device.get_signature(),
        'class': device.__module__,
    }
    if obj['node_descriptor'] is not None:
        obj['node_descriptor'] = ":".join(
            "{:02x}".format(x) for x in obj['node_descriptor'])
    for endpoint_id, endpoint in device.endpoints.items():
        if endpoint_id == 0:
            continue
        endpoint_obj = {}
        endpoint_obj['id'] = endpoint_id
        endpoint_obj['status'] = endpoint.status
        endpoint_obj['device_type'] = getattr(endpoint, 'device_type', None)
        endpoint_obj['profile_id'] = getattr(endpoint, 'profile_id', None)
        manufacturer = None
        model = None
        try:
            model, manufacturer = await asyncio.wait_for(endpoint.get_model_info(), timeout=2.0)
        except:
            pass
        endpoint_obj['manufacturer'] = manufacturer
        endpoint_obj['model'] = model
        endpoint_obj['output_clusters'] = []
        endpoint_obj['input_clusters'] = []
        endpoint_obj['output_clusters'] = []
        for cluster in endpoint.out_clusters.values():
            values = await serialize_cluster(cluster, with_attributes)
            endpoint_obj['output_clusters'].append(values)
        for cluster in endpoint.in_clusters.values():
            values = await serialize_cluster(cluster, with_attributes)
            endpoint_obj['input_clusters'].append(values)
        obj['endpoints'].append(endpoint_obj)
    return obj


async def serialize_cluster(cluster, with_attributes=1):
    obj = {
        'id': cluster.cluster_id,
        'name': cluster.name,
        'attributes': []
    }
    if with_attributes == 0:
        return obj
    if with_attributes == 2 and cluster.cluster_id not in [0, 1]:
        return obj
    if cluster.cluster_id == 33:
        value = await cluster.read_attributes([39320], True, True)
        if 39320 in value[0]:
            value = value[0][39320]
            if isinstance(value, (bytes, bytearray)):
                value = value.hex()
            obj['attributes'].append(
                {'id': 39320, 'name': 'ZGP_key', 'value': value})
    for attribute in cluster.attributes:
        value = await cluster.read_attributes([attribute], True, True)
        if attribute in value[0]:
            value = value[0][attribute]
        else:
            continue
        if isinstance(value, (bytes, bytearray)):
            value = value.hex()
        if isinstance(cluster.attributes[attribute], (set)):
            name = str(cluster.attributes[attribute])
        else:
            name = cluster.attributes[attribute][0]
        obj['attributes'].append(
            {'id': attribute, 'name': name, 'value': value})
    return obj


def find(ieee):
    for device in shared.ZIGPY.devices.values():
        if str(device.ieee).lower() == ieee.lower():
            return device
    return None

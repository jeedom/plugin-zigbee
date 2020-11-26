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
from zigpy.zcl.clusters.hvac import Thermostat
import zigpy.quirks
import shared

ROUTING_SPECIFIC = {"Danfoss" :
                        {"0x0200" :
                            {Thermostat.cluster_id:
                                {1:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                2:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                3:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                4:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                5:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                6:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                7:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                8:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                9:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                10:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                11:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                12:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                13:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                14:[{"attr":"output_status","min":1,"max":65534,"report": 1}],
                                15:[{"attr":"output_status","min":1,"max":65534,"report": 1}]
                                }
                            }
                        }
                    }


async def routing(manufacturer, model , cluster_id ,ep_id,cluster):
    logging.debug('Checking specific routing for device ' +str(manufacturer)+' '+str(model)+' '+str(cluster_id)+' '+str(ep_id))
    if manufacturer in ROUTING_SPECIFIC and model in ROUTING_SPECIFIC[manufacturer] and cluster_id in ROUTING_SPECIFIC[manufacturer][model] and ep_id in ROUTING_SPECIFIC[manufacturer][model][cluster_id]:
        logging.debug('Found specific routing ' + str(ROUTING_SPECIFIC[manufacturer][model][cluster_id][ep_id]))
        for routing in ROUTING_SPECIFIC[manufacturer][model][cluster_id][ep_id]:
            logging.debug('Setting specific routing ' + str(routing))
            await cluster.configure_reporting(routing["attr"], routing["min"],routing["max"], routing["report"])
    else:
        logging.debug('No specific routing found')

async def init(device):
    if (device.manufacturer == 'Danfoss' and device.model in ['0x8030','0x0200']):
        endpoints = device.endpoints.items()
        logging.debug('Found endpoints : ' + str(endpoints))
        for endpoint_id, ep in device.endpoints.items():
            if endpoint_id == 232:
                logging.debug('Found endpoint 232')
                try:
                    await ep.initialize()
                except Exception as exc:
                    self.warning("Endpoint %s initialization failure: %s", endpoint_id, exc)
                    break
                logging.debug('Setting Device Model and Manufacturer')
                device.model, device.manufacturer = await ep.get_model_info()
                device = zigpy.quirks.get_device(device)
                shared.ZIGPY.devices[device.ieee] = device

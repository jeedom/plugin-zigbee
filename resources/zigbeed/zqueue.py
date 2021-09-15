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
import shared
import json
import asyncio
import time
import threading
import zdevices

def add(_type,_interval,_data,_repeat = 1):
	shared.ZQUEUE.append({'data' : _data, 'timestamp' : time.time(),'type' : _type,'interval' : _interval,'repeat' :  _repeat})

async def handle():
	while True:
		for zqueue in shared.ZQUEUE:
			if not 'type' in zqueue or not 'timestamp' in zqueue or not 'data' in zqueue or not 'repeat' in zqueue or not 'interval' in zqueue :
				shared.ZQUEUE.remove(zqueue)
				continue
			if zqueue['repeat'] < 1:
				shared.ZQUEUE.remove(zqueue)
				continue
			if (zqueue['timestamp'] + zqueue['interval']) > time.time():
				continue
			logging.info('[zqueue.handle] Handle queue item : '+str(zqueue))
			try:
				if zqueue['type'] == 'write_attributes':
					await zdevices.write_attributes(zqueue['data'])
				elif zqueue['type'] == 'command':
					await zdevices.command(zqueue['data'])
				shared.ZQUEUE.remove(zqueue)
			except Exception as e:
				logging.info('[zqueue.handle] Error on queue for '+str(zqueue)+' => '+str(e))
				if zqueue['repeat'] < 1:
					shared.ZQUEUE.remove(zqueue)
					continue
				zqueue['repeat'] = zqueue['repeat'] - 1
				pass
		await asyncio.sleep(10)

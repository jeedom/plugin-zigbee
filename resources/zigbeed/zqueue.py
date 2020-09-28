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
		for i in range(len(shared.ZQUEUE)):
			if not 'type' in shared.ZQUEUE[i] or not 'timestamp' in shared.ZQUEUE[i] or not 'data' in shared.ZQUEUE[i] or not 'repeat' in shared.ZQUEUE[i] or not 'interval' in shared.ZQUEUE[i] :
				shared.ZQUEUE.pop(i)
				continue
			if shared.ZQUEUE[i]['repeat'] < 1:
				shared.ZQUEUE.pop(i)
				continue
			if (shared.ZQUEUE[i]['timestamp'] + shared.ZQUEUE[i]['interval']) > time.time():
				continue
			logging.debug('Handle queue item : '+str(shared.ZQUEUE[i]))
			try:
				if shared.ZQUEUE[i]['type'] == 'write_attributes':
					await zdevices.write_attributes(shared.ZQUEUE[i]['data'])
				elif shared.ZQUEUE[i]['type'] == 'command':
					await zdevices.command(shared.ZQUEUE[i]['data'])
				shared.ZQUEUE.pop(i)
			except Exception as e:
				logging.debug('Error on queue for '+str(shared.ZQUEUE[i])+' => '+str(e))
				if shared.ZQUEUE[i]['repeat'] < 1:
					shared.ZQUEUE.pop(i)
					continue
				shared.ZQUEUE[i]['repeat'] = shared.ZQUEUE[i]['repeat'] - 1
				pass
		await asyncio.sleep(10)

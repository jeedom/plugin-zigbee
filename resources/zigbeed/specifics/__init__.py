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
import pkgutil
import importlib
import shared

async def reporting(manufacturer, model , cluster_id ,ep_id,cluster):
	for specific in shared.JEEDOM_SPECIFIC:
		if specific().isvalid(manufacturer) and 'reporting' in specific().specific:
			logging.info('Found specific Reporting')
			await specific().reporting(model,cluster_id,ep_id,cluster)
			break

def init(device):
	for specific in shared.JEEDOM_SPECIFIC:
		if specific().isvalid(device.manufacturer) and 'init' in specific().specific:
			logging.info('Found specific init')
			specific().init(device)
			break

__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
	logging.info("LOADER------Import de la configuration " + modname)
	try:
		importlib.import_module(modname)
	except Exception as e:
		logging.info('Impossible d\'importer ' + modname + ' : ' + str(e))

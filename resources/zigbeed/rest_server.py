#!flask/bin/python

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

import sys
import binascii
import logging
import os
import shared,utils
try:
	from tornado.web import RequestHandler,Application,HTTPError
except Exception as e:
	print("Error: %s" % str(e), 'error')
	sys.exit(1)

class ControllerHandler(RequestHandler):
	def get(self):
		try:
			utils.check_apikey(self.get_argument('apikey',''))
			self.write(utils.format_json_result())
			type = self.get_argument('type','')
			if type == 'include':
				shared.ZIGPY.permit(self.get_argument('duration',60))
		except Exception as e:
			self.write(utils.format_json_result(success="error",data=str(e)))

class NetworkHandler(RequestHandler):
	def get(self):
		try:
			utils.check_apikey(self.get_argument('apikey',''))
			self.write(utils.format_json_result())
		except Exception as e:
			self.write(utils.format_json_result(success="error",data=str(e)))

class NodeHandler(RequestHandler):
	def get(self):
		try:
			utils.check_apikey(self.get_argument('apikey',''))
			self.write(utils.format_json_result())
		except Exception as e:
			self.write(utils.format_json_result(success="error",data=str(e)))

shared.REST_SERVER = Application([
		(r"/controller", ControllerHandler),
		(r"/network", NetworkHandler),
		(r"/node", NodeHandler),
	])

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

class ApplicationHandler(RequestHandler):
	def prepare(self):
		utils.check_apikey(self.request.headers.get("autorization", ""))
		if self.request.headers.get("Content-Type", "").startswith("application/json"):
			self.json_args = json.loads(self.request.body)
		else:
			self.json_args = None
	
	def get(self,arg1):
		try:
			if arg1 == 'info':
				return self.write(utils.format_json_result(success=True,data=shared.ZIGPY.__dict__))
			return self.write(utils.format_json_result(success="error",data="No method found"))
		except Exception as e:
			return self.write(utils.format_json_result(success="error",data=str(e)))
			
	def put(self,arg1):
		try:
			if arg1 == 'include':
				shared.ZIGPY.permit(self.json_args.duration)
				return self.write(utils.format_json_result(success=True))
			return self.write(utils.format_json_result(success="error",data="No method found"))
		except Exception as e:
			return self.write(utils.format_json_result(success="error",data=str(e)))


shared.REST_SERVER = Application([
		(r"/application/([^/]+)?", ApplicationHandler)
	])

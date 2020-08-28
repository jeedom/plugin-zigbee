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
import globals
import binascii

try:
	from jeedom.jeedom import *
except ImportError:
	print("Error: importing module jeedom.jeedom")
	sys.exit(1)

class uart():

	def make_frame_control(_type):
		result = None
		globals.FRAME_NUMBER += 1
		if globals.FRAME_NUMBER > 7 :
			globals.FRAME_NUMBER = 0
		if globals.ACK_NUMBER <= globals.FRAME_NUMBER :
			globals.ACK_NUMBER = globals.FRAME_NUMBER + 1
		if globals.ACK_NUMBER > 7 :
			globals.ACK_NUMBER = 0
		if _type == 'DATA' :
			result = '0'+bin(globals.FRAME_NUMBER)[2:].zfill(3)+'0'+bin(globals.ACK_NUMBER)[2:].zfill(3)
		return bytes(int(result[i : i + 8], 2) for i in range(0, len(result), 8))
		return hex(int(result, 2))

	def make_crc(frame):
		crc = binascii.crc_hqx(frame, 0xFFFF)
		return bytes([crc >> 8, crc % 256])

	def make_data_frame(_data):
	    logging.debug('Encode data frame : '+str(_data))
	    frame = uart.make_frame_control('DATA')+uart.randomize(_data)
	    frame = uart.escape(frame+uart.make_crc(frame))+globals.FLAG
	    logging.debug('Result frame : '+str(frame.hex()))
	    return frame

	def randomize(_data):
	    rand = globals.RANDOMIZE_START
	    out = b""
	    for c in _data:
		    out += bytes([c ^ rand])
		    if rand % 2:
		        rand = (rand >> 1) ^ globals.RANDOMIZE_SEQ
		    else:
		        rand = rand >> 1
	    return out

	def escape(s):
	    out = b""
	    for c in s:
	       if c in globals.RESERVED:
                out += globals.ESCAPE + bytes([c ^ globals.STUFF])
	       else:
                out += bytes([c])
	    return out

	def unescape(s):
	    out = b""
	    escaped = False
	    for c in s:
	       if escaped:
	            out += bytes([c ^ globals.STUFF])
	            escaped = False
	       elif c in globals.ESCAPE:
	            escaped = True
	       else:
	            out += bytes([c])
	    return out

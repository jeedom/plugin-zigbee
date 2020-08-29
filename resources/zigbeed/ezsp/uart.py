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

	def decode_frame(frame):
		logging.debug('Decode frame : '+str(frame.hex()))
		if globals.CANCEL in frame:
			frame = frame[frame.rfind(globals.CANCEL) + 1 :]
		if globals.SUBSTITUTE in frame:
			frame = frame[frame.find(globals.FLAG) + 1 :]
		if globals.FLAG not in frame:
			raise Exception("No end flag")
		place = frame.find(globals.FLAG)
		if place+1 < len(frame):
			frame = frame[place+1:]
		logging.debug('Corrected frame : '+str(frame.hex()))
		result  = {}
		crc = uart.make_crc(frame[:-3])
		if crc != frame[-3:-1]:
			raise Exception("Invalid CRC, found : "+str(frame[-3:-1].hex())+' attemp : '+str(crc.hex()))
		frame = uart.unescape(frame);
		if (frame[0] & 0b10000000) == 0:
			logging.debug('Received data frame')
			result['type'] = 'DATA'
			result['seq'] = (frame[0] & 0b01110000) >> 4
			globals.ACK_NUMBER = result['seq']+1
			frame_ezsp = uart.randomize(frame[1:-3])
			logging.debug('Decode frame ezsp : '+str(frame_ezsp.hex())+' with EZSP_VRSION '+str(globals.EZSP_VERSION))
			if globals.EZSP_VERSION >= 8:
				result['seq_ezsp'] = frame_ezsp[0]
				result['frame_id'] = ((frame_ezsp[4] << 8) | frame_ezsp[3])
				result['data'] = frame_ezsp[5:]
			else:
			    result['seq_ezsp'] = frame_ezsp[0]
			    result['frame_id'] =frame_ezsp[2]
			    result['data'] = frame_ezsp[3:]
		elif (frame[0] & 0b11100000) == 0b10000000:
			logging.debug('Received ack frame')
			result['type'] = 'ACK'
		elif (frame[0] & 0b11100000) == 0b10100000:
			logging.debug('Received nak frame')
			result['type'] = 'NACK'
		elif frame[0] == 0b11000001:
			logging.debug('Received rstack frame')
			result['type'] = 'RSTACK'
		elif frame[0] == 0b11000010:
			logging.debug('Received error frame')
			result['type'] = 'ERROR'
		else:
			raise Exception("Unknown frame")

		return result;

	def make_frame_control(_type):
		result = None
		if globals.FRAME_NUMBER > 7 :
			globals.FRAME_NUMBER = 0
		#if globals.ACK_NUMBER < globals.FRAME_NUMBER :
		#	globals.ACK_NUMBER = globals.FRAME_NUMBER + 1
		if globals.ACK_NUMBER > 7 :
			globals.ACK_NUMBER = 0
		logging.debug('Ack number : '+str(globals.ACK_NUMBER))
		if _type == 'DATA' :
			logging.debug('Frame number : '+str(globals.FRAME_NUMBER))
			result = '0'+bin(globals.FRAME_NUMBER)[2:].zfill(3)+'0'+bin(globals.ACK_NUMBER)[2:].zfill(3)
			globals.FRAME_NUMBER += 1
		if _type == 'ACK' :
			result = '10000'+bin(globals.ACK_NUMBER)[2:].zfill(3)
		if _type == 'NACK' :
			result = '10100'+bin(globals.ACK_NUMBER)[2:].zfill(3)
		if _type == 'RST' :
			result = '11000000'
		return bytes(int(result[i : i + 8], 2) for i in range(0, len(result), 8))

	def make_crc(frame):
		logging.debug('Calcul CRC on : '+str(frame.hex()))
		crc = binascii.crc_hqx(frame, 0xFFFF)
		return bytes([crc >> 8, crc % 256])

	def make_data_frame(_data):
	    logging.debug('Encode data frame : '+str(_data))
	    frame = uart.make_frame_control('DATA')+uart.randomize(_data)
	    frame = uart.escape(frame+uart.make_crc(frame))+globals.FLAG
	    logging.debug('Result frame : '+str(frame.hex()))
	    return frame

	def make_ack_frame():
		frame = uart.make_frame_control('ACK')
		frame = uart.escape(frame+uart.make_crc(frame))+globals.FLAG
		logging.debug('ACK frame : '+str(frame.hex()))
		return frame

	def make_nack_frame():
		frame = uart.make_frame_control('NACK')
		frame = uart.escape(frame+uart.make_crc(frame))+globals.FLAG
		logging.debug('NACK frame : '+str(frame.hex()))
		return frame

	def make_rst_frame():
		frame = uart.make_frame_control('RST')
		frame = bytes([0x1A])+uart.escape(frame+uart.make_crc(frame))+globals.FLAG
		logging.debug('RST : '+str(frame.hex()))
		globals.ACK_NUMBER = 0
		globals.FRAME_NUMBER = 0
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

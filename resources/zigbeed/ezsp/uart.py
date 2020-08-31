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
import shared
import binascii

try:
	from jeedom.jeedom import *
except ImportError:
	print("Error: importing module jeedom.jeedom")
	sys.exit(1)

class uart():

	def decode_frame(frame):
		if shared.CANCEL in frame:
			frame = frame[frame.rfind(shared.CANCEL) + 1 :]
		if shared.SUBSTITUTE in frame:
			frame = frame[frame.find(shared.FLAG) + 1 :]
		if shared.FLAG not in frame:
			raise Exception("No end flag")
		place = frame.find(shared.FLAG)
		if place+1 < len(frame):
			frame = frame[place+1:]
		logging.debug('Received frame : '+str(frame.hex()))
		result  = {}
		#crc = uart.make_crc(frame[:-3])
		#if crc != frame[-3:-1]:
		#	raise Exception("Invalid CRC, found : "+str(frame[-3:-1].hex())+' attemp : '+str(crc.hex()))
		frame = uart.unescape(frame);
		if (frame[0] & 0b10000000) == 0:
			logging.debug('Received data frame, send ack')
			result['type'] = 'DATA'
			result['seq'] = (frame[0] & 0b01110000) >> 4
			shared.ACK_NUMBER = result['seq']+1
			shared.JEEDOM_SERIAL.write(uart.make_ack_frame())
			result['frame_ezsp'] = uart.randomize(frame[1:-3])
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
		if shared.FRAME_NUMBER > 7 :
			shared.FRAME_NUMBER = 0
		if shared.ACK_NUMBER < shared.FRAME_NUMBER :
			shared.FRAME_NUMBER = shared.ACK_NUMBER + 1
		if shared.ACK_NUMBER > 7 :
			shared.ACK_NUMBER = 0
		logging.debug('Ack number : '+str(shared.ACK_NUMBER))
		if _type == 'DATA' :
			logging.debug('Frame number : '+str(shared.FRAME_NUMBER))
			result = '0'+bin(shared.FRAME_NUMBER)[2:].zfill(3)+'0'+bin(shared.ACK_NUMBER)[2:].zfill(3)
			shared.FRAME_NUMBER += 1
		if _type == 'ACK' :
			result = '10000'+bin(shared.ACK_NUMBER)[2:].zfill(3)
		if _type == 'NACK' :
			result = '10100'+bin(shared.ACK_NUMBER)[2:].zfill(3)
		if _type == 'RST' :
			result = '11000000'
		return bytes(int(result[i : i + 8], 2) for i in range(0, len(result), 8))

	def make_crc(frame):
		crc = binascii.crc_hqx(frame, 0xFFFF)
		return bytes([crc >> 8, crc % 256])

	def make_data_frame(_data):
		logging.debug('Encode data frame : '+str(_data))
		frame = uart.make_frame_control('DATA')+uart.randomize(_data)
		frame = uart.escape(frame+uart.make_crc(frame))+shared.FLAG
		logging.debug('Result frame : '+jeedom_utils.printHex(str(frame.hex())))
		return frame

	def make_ack_frame():
		frame = uart.make_frame_control('ACK')
		frame = uart.escape(frame+uart.make_crc(frame))+shared.FLAG
		logging.debug('ACK frame : '+str(frame.hex()))
		return frame

	def make_nack_frame():
		frame = uart.make_frame_control('NACK')
		frame = uart.escape(frame+uart.make_crc(frame))+shared.FLAG
		logging.debug('NACK frame : '+str(frame.hex()))
		return frame

	def make_rst_frame():
		frame = uart.make_frame_control('RST')
		frame = bytes([0x1A])+uart.escape(frame+uart.make_crc(frame))+shared.FLAG
		logging.debug('RST : '+str(frame.hex()))
		shared.ACK_NUMBER = 0
		shared.FRAME_NUMBER = 0
		return frame

	def randomize(_data):
		rand = shared.RANDOMIZE_START
		out = b""
		for c in _data:
			out += bytes([c ^ rand])
			if rand % 2:
				rand = (rand >> 1) ^ shared.RANDOMIZE_SEQ
			else:
				rand = rand >> 1
		return out

	def escape(s):
		out = b""
		for c in s:
			if c in shared.RESERVED:
				out += shared.ESCAPE + bytes([c ^ shared.STUFF])
			else:
				out += bytes([c])
		return out

	def unescape(s):
		out = b""
		escaped = False
		for c in s:
			if escaped:
				out += bytes([c ^ shared.STUFF])
				escaped = False
			elif c in shared.ESCAPE:
				escaped = True
			else:
				out += bytes([c])
		return out

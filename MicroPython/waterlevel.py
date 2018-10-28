from machine import Pin, UART
from ringbuffer import RingBuffer

import re

class WaterLevel:

	def __init__(self, port):
		self.uart = UART(port, 9600)
		self.uart.init(9600, timeout=10)	# 9600, 1byte about 1ms, wait for 10ms
		self.buffer = RingBuffer(6)

	# return
	# False: no change
	# True: change, need read value
	def Check(self):
		count = self.uart.any()
		if count < 3:
			return False
			# At lease 3 bytes in buffer (For example:0mm)
		
		value_change = None

		while 1:		# maybe too many data in UART RX buffer
			data = self.uart.readline()
			if data:
				number_string = re.search(b'^\d+', data)
				if number_string:
					number = int(number_string.group(0))
					value_change = self.buffer.InsertData(number, True)

			else:
				break
		
		return value_change


	def GetValue(self):
		return self.buffer.GetAverage()

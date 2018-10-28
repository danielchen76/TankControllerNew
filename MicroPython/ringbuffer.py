import array
import sys

# Ring buffer for water level, temperature etc.

class RingBuffer:
	def __init__(self, count):
		self.count = count
		self.index = 0
		self.last_avg = 0
		self.wrong_data_count = 0	#wrong data continue counter

		self.buffer = array.array('i')
		for i in range(0, self.count):
			self.buffer.append(-1)

	def InsertData(self, data, changeCheck = False):
		self.buffer[self.index] = data
		self.index += 1
		if self.index == self.count :
			self.index = 0

		#wrong data check
		if data < 0:
			self.wrong_data_count += 1
		else:
			self.wrong_data_count = 0		#reset wrong data counter
		
		if changeCheck:
			# Calculate average, and compare with last on
			# Total and remove -1
			data_count = 0
			data_total = 0
			data_max = 0
			data_min = sys.maxsize			# TODO:

			for data in self.buffer:
				if data > 0:
					data_total += data
					data_count += 1
					#look for max, min, then will remove
					if data > data_max:
						data_max = data
					if data < data_min:
						data_min = data
				
			if data_count < 3:
				return None

			if data_count <= (self.count / 2):
				return None			# too many wrong data

			# remove max, min data
			data_count -= 2
			data_total -= data_max
			data_total -= data_min

			# calculate average
			data_avg = int(data_total / data_count)
			if data_avg != self.last_avg:
				self.last_avg = data_avg
				return True		# Change
			else:
				return False	# Not change
		else:
			return None			# buffer average is unavailable.
				
				
	def GetAverage(self):
		return self.last_avg

	def OutputData(self):
		for item in self.buffer:
			print(item)


		


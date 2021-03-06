from micropython import const
from machine import Pin, UART
import time

from ringbuffer import RingBuffer
from ds18x20 import DS18X20
from onewire import OneWire

from ui import *

DS_IDEL = const(0)
DS_START = const(1)

class TempSensor:
	def __init__(self, pin):
		self.check_ticks_ms = 0
		self.ds = DS18X20(OneWire(Pin(pin)))
		self.rom = None
		self.buffer = RingBuffer(6)
		self.state = DS_IDEL

		roms = self.ds.scan()
		if roms:
			self.rom = roms[0]
			UI.LogOut(str(self.rom))

	def Start(self):
		# Wait for 1000ms(1s) to start
		if self.state != DS_IDEL:
			return

		if time.ticks_diff(time.ticks_ms(), self.check_ticks_ms) < 1000:
			return

		if self.rom:
			self.ds.convert_temp()
			self.state = DS_START
			self.check_ticks_ms = time.ticks_ms()

	def Check(self):
		if self.rom is None:
			return None

		# Need wait for 750ms(800ms) after start
		if self.state != DS_START:
			return False

		if time.ticks_diff(time.ticks_ms(), self.check_ticks_ms) < 800:
			return False
		
		try:
			value = int(self.ds.read_temp(self.rom) * 100)
		except:
			UI.LogOut("Read DS18B20 failed!")
			return False
		else:
			value_change = self.buffer.InsertData(value, True)
			
			self.state = DS_IDEL

			return value_change

	def GetValue(self):
		return self.buffer.GetAverage()


class Sensors:
	Ro_ext_sensor = None
	Ro_ext_sensor_exist = None
	Ro_emergen_sensor = None
	Sub_emergen_sensor = None
	Green_Button = None

	Ro_ext_have_water = False

	def Init():
		Sensors.Ro_ext_sensor = Pin('X22', Pin.IN, Pin.PULL_UP)
		Sensors.Ro_ext_sensor_exist = Pin('X2', Pin.IN, Pin.PULL_UP)
		Sensors.Ro_emergen_sensor = Pin('X19', Pin.IN, Pin.PULL_UP)
		Sensors.Sub_emergen_sensor = Pin('X21', Pin.IN, Pin.PULL_UP)
		Sensors.Green_Button = Pin('X1', Pin.IN, Pin.PULL_UP)

	# Update the sensor state
	def check():
		# TODO
		Ro_ext_have_water = True if (Sensors.Ro_ext_sensor.value() == 1) and (Sensors.Ro_ext_sensor_exist.value() == 0) else False
		Ro_emergen = True if Sensors.Ro_emergen_sensor.value() == 0 else False
		Sub_emergen = True if Sensors.Sub_emergen_sensor.value() == 0 else False

		data = {}
		data['ROEW'] = Ro_ext_have_water
		data['ROEM'] = Ro_emergen
		data['SUBEM'] = Sub_emergen
		return data




	

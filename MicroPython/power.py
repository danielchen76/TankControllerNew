from machine import Pin
from pyb import ADC, ADCAll

from ui import *

import time

class Power:
	def Init():
		# Power
		Power.bat24v = Pin('Y11', Pin.OUT)
		Power.dc24_bat24 = Pin('Y12', Pin.OUT)

		Power.dc_v = ADC('X3')
		Power.battery_v = ADC('X4')
		Power.dc_c = ADC('X5')
		Power.main_pump_c = ADC('X7')
		Power.skim_pump_c = ADC('X6')

		# ADC all object
		Power.adc = ADCAll(12, 0x70000)

		Power.check_ticks_ms = 0

	def SwitchToBattery(On):
		Power.dc24_bat24.value(On)

	def TurnOnBat24V(On):
		Power.bat24v.value(On)

	def Check():
		t = time.ticks_ms()
		if time.ticks_diff(t, Power.check_ticks_ms) < 1000:
			return

		v33 = Power.adc.read_vref()

		data_dc_v = Power.dc_v.read()
		data_bat_v = Power.battery_v.read()
		data_dc_c = Power.dc_c.read()
		data_main_pump_c = Power.main_pump_c.read()
		data_skim_pump_c = Power.skim_pump_c.read()

		data = {}
		data['DC'] = int(data_dc_v * v33 * 1000 * 9 / 4096)
		data['BAT'] = int(data_bat_v * v33 * 1000 * 5 / 4096)
		data['DC_C'] = int(data_dc_c * v33 * 1000 / 4096)
		data['MP_C'] = int(data_main_pump_c * v33 * 1000 / 4096)
		data['SP_C'] = int(data_skim_pump_c * v33 * 1000 / 4096)

		data['bat24'] = Power.bat24v.value()
		data['dc24bat'] = Power.dc24_bat24.value()

		Power.check_ticks_ms = time.ticks_ms()
		return data






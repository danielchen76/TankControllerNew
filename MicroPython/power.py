from machine import Pin
from pyb import ADC, ADCAll

class Power:
	def Init():
		# Power
		Power.bat24v = Pin('Y11', Pin.OUT)
		Power.dc24_bat24 = Pin('Y12', Pin.OUT)

		Power.dc_v = ADC('X3')
		Power.battery_v = Pin('X4')
		Power.dc_c = ADC('X5')
		Power.main_pump_c = ADC('X7')
		Power.Skim_pump_c = ADC('X6')

		# ADC all object
		Power.adc = ADCAll(12, 0x70000)

	def SwitchToBattery(On):
		return



from pyb import Pin, UART, ADC

from devices import *
from ui import *
from waterlevel import WaterLevel

# Initialize 
Ro_level = WaterLevel(3)		# UART3
Sub_level = WaterLevel(6)		# UART6

# Main loop
while 1:
	# Ro tank water level
	value_change = Ro_level.Check()
	if value_change:
		SetRoLevel(Ro_level.GetValue())

	# Sub tank water level
	value_change = Sub_level.Check()
	if value_change:
		SetSubLevel(Sub_level.GetValue())

	# Temperature

	# Sensors

	# Main process
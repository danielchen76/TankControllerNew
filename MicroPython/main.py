from pyb import Pin, UART, ADC

from devices import *
from ui import *
from waterlevel import WaterLevel
from sensors import *
from power import *

from pyb import LED

# Initialize 
UI.Init()

Ro_level = WaterLevel(3)		# UART3
Sub_level = WaterLevel(6)		# UART6
Temperature = TempSensor('X20')

Devices.Init()
Sensors.Init()
Power.Init()

# Main loop
while 1:
	# Ro tank water level
	value_change = Ro_level.Check()
	if value_change:
		UI.SetRoLevel(Ro_level.GetValue())

	# Sub tank water level
	value_change = Sub_level.Check()
	if value_change:
		UI.SetSubLevel(Sub_level.GetValue())

	# Temperature
	Temperature.Start()
	value_change = Temperature.Check()
	if value_change:
		UI.SetTemperature(Temperature.GetValue())

	# Sensors
	Sensors.check()

	# UI uart
	if UI.Check():
		UI.LogOut("have request from Pi Zero W")

	UI.Report()

	# Main process


# lost connect with Pi Zero, need stop some pump
def lostConnection():
	Devices.Ro_pump_switch(False)
	Devices.Ro_ext_pump_switch(False)
	Devices.Sea_pump_switch(False)
	# Sync to UI


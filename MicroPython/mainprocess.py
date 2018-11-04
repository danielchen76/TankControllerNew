from ui import *
from sensors import *
from devices import *

class MainProcess:
	# Config 
	# TODO:need config by function
	Ro_full_water_level = 270
	Sub_full_water_level = 235

	Ro_low_water_level = 30

	# State
	Ro_ext_have_water = False

	Ro_low_water = False
	Ro_full_water = True
	Ro_can_refill = False

	Sub_full_water = True
	Sub_can_refill = False

	State = State_idle


	def Process():
		# Check state
		value = GetRoLevel()
		
		MainProcess.Ro_full_water = True if (value >= MainProcess.Ro_full_water_level) else False
		MainProcess.Ro_low_water = True if (value <= MainProcess.Ro_low_water_level) else False
		MainProcess.Ro_can_refill = True if (value <= MainProcess.Ro_full_water_level - 10) else False

		value = GetSubLevel()

		MainProcess.Sub_full_water = True if (value >= MainProcess.Sub_full_water_level) else False
		MainProcess.Sub_can_refill = True if (value <= MainProcess.Sub_full_water_level - 10) else False

		MainProcess.Ro_ext_have_water = Sensors.IsRoExtHaveWater()

		# Auto run

		# Message Queue

	def State_idle():
		# normal check
		# Sub tank
		if MainProcess.Sub_can_refill and (not MainProcess.Ro_low_water):
			Ro_pump_switch(True)
			state = 
			return

		# Ro ext
		if MainProcess.Ro_ext_have_water and MainProcess.Ro_can_refill:
			Ro_ext_pump_switch(True)
			state = 
			return


	def State_sub_refill():
		# Ro refill into sub tank

	def State_ro_refill():
		# Ro ext refill into Ro tank
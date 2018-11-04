from machine import Pin


class Devices:
	def Init():
	# Devices
		Devices.Sea_pump 		= Pin('Y3', Pin.OUT)
		Devices.Ro_ext_pump 	= Pin('Y4', Pin.OUT)
		Devices.Ro_pump 		= Pin('Y5', Pin.OUT)
		Devices.Rever_dc 		= Pin('Y6', Pin.OUT)
		Devices.Main_pump		= Pin('Y7', Pin.OUT)
		Devices.Skim_pump		= Pin('Y8', Pin.OUT)
		Devices.Main_wave		= Pin('X11', Pin.OUT)
		Devices.Main_wave_bak 	= Pin('X12', Pin.OUT)


	def Sea_pump_switch(on):
		Devices.Sea_pump.value(on)

	def Ro_ext_pump_switch(on):
		Devices.Ro_ext_pump.value(on)

	def Ro_pump_switch(on):
		Devices.Ro_pump.value(on)

	def Main_pump_switch(on):
		Devices.Main_pump.value(on)

	def Skim_pump_switch(on):
		Devices.Skim_pump.value(on)

	def Main_wave_switch(on, bak_on):
		Devices.Main_wave.value(on)
		Devices.Main_wave_bak.value(bak_on)

	def Main_wave_NightMode(on):
		if on:
			Devices.Main_wave.off()
			Devices.Main_wave_bak.on()
		else:
			Devices.Main_wave.on()
			Devices.Main_wave_bak.on()


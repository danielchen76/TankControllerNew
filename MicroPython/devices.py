from machine import Pin


# Beep
beep = Pin('X8', Pin.OUT)

# Power
bat24v = Pin('Y11', Pin.OUT)
dc24_bat24 = Pin('Y12', Pin.OUT)

# Devices
Sea_pump 	= Pin('Y3', Pin.OUT)
Ro_ext_pump = Pin('Y4', Pin.OUT)
Ro_pump 	= Pin('Y5', Pin.OUT)
Rever_dc 	= Pin('Y6', Pin.OUT)
Main_pump	= Pin('Y7', Pin.OUT)
Skim_pump	= Pin('Y8', Pin.OUT)
Main_wave	= Pin('X11', Pin.OUT)
Main_wave_bak = Pin('X12', Pin.OUT)


def Sea_pump_switch(on):
	Sea_pump.value(on)

def Ro_ext_pump_switch(on):
	Ro_ext_pump.value(on)

def Ro_pump_switch(on):
	Ro_pump.value(on)

def Main_pump_switch(on):
	Main_pump.value(on)

def Skim_pump_switch(on):
	Skim_pump.value(on)

def Main_wave_switch(on, bak_on):
	Main_wave.value(on)
	Main_wave_bak.value(bak_on)

def Main_wave_NightMode(on):
	if on:
		Main_wave.off()
		Main_wave_bak.on()
	else:
		Main_wave.on()
		Main_wave_bak.on()


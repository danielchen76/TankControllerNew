from pyb import Pin, UART, ADC

from devices import *
from ui import *
from waterlevel import WaterLevel
from sensors import *
from power import *
from json_string import CMD

from pyb import LED

# Initialize 
UI.Init()

Ro_level = WaterLevel(3)		# UART3
Sub_level = WaterLevel(6)		# UART6
Temperature = TempSensor('X20')

Devices.Init()
Sensors.Init()
Power.Init()


def Cmd_Sea_pump_switch(msg):
	Devices.Sea_pump_switch(msg)
	UI.SetSeaPump(msg)

def Cmd_Ro_ext_pump_switch(msg):
	Devices.Ro_ext_pump_switch(msg)
	UI.SetRoExtPump(msg)

def Cmd_Ro_pump_switch(msg):
	Devices.Ro_pump_switch(msg)
	UI.SetRoPump(msg)

def Cmd_Main_pump_switch(msg):
	Devices.Main_pump_switch(msg)
	UI.SetMainPump(msg)

def Cmd_Skim_pump_switch(msg):
	Devices.Skim_pump_switch(msg)
	UI.SetSkimPump(msg)

def Cmd_Main_wave_switch(msg):
	Devices.Main_wave_switch(msg)
	UI.SetMainWave(msg)

def Cmd_Main_wave_bak_switch(msg):
	Devices.Main_wave_bak_switch(msg)
	UI.SetMainWaveBak(msg)

def Cmd_SwitchToBattery(msg):
	Power.SwitchToBattery(msg)

def Cmd_TurnOnBat24V(msg):
	Power.TurnOnBat24V(msg)

	# lost connect with Pi Zero, need stop some pump
def lostConnection():
	UI.LogOut("Stop special pumps.")
	Cmd_Ro_pump_switch(False)
	Cmd_Ro_ext_pump_switch(False)
	Cmd_Sea_pump_switch(False)


Cmd_entries = {
	CMD.JSON_MAIN_PUMP		: Cmd_Sea_pump_switch,
	CMD.JSON_SKIM_PUMP		: Cmd_Skim_pump_switch,
	CMD.JSON_RO_PUMP		: Cmd_Ro_pump_switch,
	CMD.JSON_RO_EXT_PUMP	: Cmd_Ro_ext_pump_switch,
	CMD.JSON_SEA_PUMP		: Cmd_Sea_pump_switch,
	CMD.JSON_WAVE_PUMP		: Cmd_Main_wave_switch,
	CMD.JSON_WAVE_BAK		: Cmd_Main_wave_bak_switch,

	CMD.JSON_BAT_24V		: Cmd_SwitchToBattery,
	CMD.JSON_DC_BAT			: Cmd_TurnOnBat24V,
}

def Cmd_Set(id, data):
	UI.LogOut("set id " + str(id) + str(data))
	for k, v in data.items():
		msg_entry = Cmd_entries.get(k)
		if msg_entry:
			msg_entry(v)

	UI.Response(id, 0)

def Cmd_Disconnect():
	# Stop some pump for safty
	lostConnection()

	# Alarm

	return

def Cmd_Connect():
	# Cancel Alarm
	
	return

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
	data = Sensors.check()
	if data:
		UI.SetSensors(data)

	# Power
	data = Power.Check()
	if data:
		UI.SetPower(data)

	# UI uart
	msg_count = UI.Check()
	if msg_count > 0:
		while 1:
			try:
				msg = UI.cmds.popleft()
				UI.LogOut(str(msg))
				action = msg.get(CMD.JSON_ACTION)
				if action == CMD.JSON_A_SET:
					UI.LogOut(msg.get(CMD.JSON_ACTION))
					UI.LogOut(str(msg.get(CMD.JSON_A_ID)))
					UI.LogOut(str(msg.get(CMD.JSON_DATA)))
					Cmd_Set(msg.get(CMD.JSON_A_ID), msg.get(CMD.JSON_DATA))
				elif action == CMD.JSON_A_DISCON:
					Cmd_Disconnect()
				elif action == CMD.JSON_A_CONN:
					Cmd_Connect()
				else:
					UI.Response(msg.get(CMD.JSON_A_ID), 1)

			except:
				break

	UI.Report()

	# Main process



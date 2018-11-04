from machine import Pin, UART
from tm1637 import TM1637
from pyb import Timer
from micropython import const

import json
import time

from json_string import CMD

# total depth
RO_TANK_TOTAL_LEVEL = const(320)
SUB_TANK_TOTAL_LEVEL = const(410)

class UI:
	report_ticks_ms = 0

	def Init():
		UI.SubLevel = 0
		UI.RoLevel = 0
		UI.Temperature = 0

		# Power controller
		UI.Sea_pump 		= False
		UI.Ro_ext_pump 		= False
		UI.Ro_pump 			= False
		UI.Rever_dc 		= False
		UI.Main_pump		= False
		UI.Skim_pump		= False
		UI.Main_wave		= False
		UI.Main_wave_bak 	= False

		# Switch type sensors
		UI.Ro_emergen_sensor	= False
		UI.Sub_emergen_sensor 	= False

		UI.Ro_ext_have_water 	= False

		# Power
		UI.bat24v 		= False
		UI.dc24_bat24 	= False

		UI.dc_v 		= 0
		UI.battery_v	= 0
		UI.dc_c 		= 0
		UI.main_pump_c 	= 0
		UI.Skim_pump_c 	= 0

		UI.WorkMode = 0

		# Init
		UI.tm = TM1637(Pin('X18'), Pin('X17'))
		UI.tm.brightness(0)		# darkest
		UI.tm.write([0, 0, 0, 0])

		UI.pi_uart = UART(1, 115200)
		UI.pi_uart.init(115200, timeout = 100)

	def Check():
		count = UI.pi_uart.any()
		if count < 3 :
			return False

		while 1:
			data = UI.pi_uart.readline()
			if data:
				try:
					decode_data = json.loads(data)
				except:
					decode_data = None
				else:
					# TODO: put data input queuc
					UI.LogOut(str(decode_data))
			return True

	def Report():
		if time.ticks_diff(time.ticks_ms(), UI.report_ticks_ms) < 1000:
			return

		# report all data
		data = {}
		data[CMD.JSON_RO_LEVEL] = UI.RoLevel
		data[CMD.JSON_SUB_LEVEL] = UI.SubLevel
		data[CMD.JSON_TEMPERATURE] = UI.Temperature

		data[CMD.JSON_MAIN_PUMP] = int(UI.Main_pump)
		data[CMD.JSON_SKIM_PUMP] = int(UI.Skim_pump)
		data[CMD.JSON_WAVE_PUMP] = int(UI.Main_wave)
		data[CMD.JSON_WAVE_BAK] = int(UI.Main_wave_bak)
		data[CMD.JSON_RO_PUMP] = int(UI.Ro_pump)
		data[CMD.JSON_RO_EXT_PUMP] = int(UI.Ro_ext_pump)
		data[CMD.JSON_SEA_PUMP] = int(UI.Sea_pump)

		data[CMD.JSON_RO_EMERGEN] = int(UI.Ro_emergen_sensor)
		data[CMD.JSON_SUB_EMERGEN] = int(UI.Sub_emergen_sensor)
		data[CMD.JSON_RO_EXT_WATER] = int(UI.Ro_ext_have_water)

		data[CMD.JSON_MAIN_VOLTAGE] = UI.dc_v
		data[CMD.JSON_BATTERY_VOL] = UI.battery_v
		data[CMD.JSON_MAIN_CURRENT] = UI.dc_c
		data[CMD.JSON_MAIN_PUMP_C] = UI.main_pump_c
		data[CMD.JSON_SKIM_PUMP_C] = UI.Skim_pump_c

		data[CMD.JSON_BAT_24V] = int(UI.bat24v)
		data[CMD.JSON_DC_BAT] = int(UI.dc24_bat24)

		UI.StatusReport(data)
		UI.report_ticks_ms = time.ticks_ms()

	#  Sub Tank water level
	def SetSubLevel(value):
		UI.SubLevel = SUB_TANK_TOTAL_LEVEL - value

	def GetSubLevel():
		return UI.SubLevel

	# Ro Tank water level
	def SetRoLevel(value):
		UI.RoLevel = RO_TANK_TOTAL_LEVEL - value

	def GetRoLevel():
		return UI.RoLevel

	# Water Temperature
	def SetTemperature(value):
		UI.Temperature = value
		UI.tm.number(UI.Temperature)

	def GetTemperature():
		return UI.Temperature

	def StatusReport(data):
		report_data = {}
		report_data[CMD.JSON_ACTION] = CMD.JSON_A_REPORT
		report_data[CMD.JSON_DATA] = data
		output = json.dumps(report_data) + '\r\n'
		UI.pi_uart.write(output)

	def LogOut(data):
		UI.pi_uart.write('###')
		UI.pi_uart.write(data)
		UI.pi_uart.write('\r\n')



# =============== Beep ================
class Beep:
	timer = None

	def Init():
		Beep.pin = Pin('X8', Pin.OUT)
		Beep.timer = Timer(1)

	def Begin():
		Beep.timer.init(freq = 10, callback = Beep.callback)

	def End():
		Beep.timer.deinit()

	def callback(timer):
		return
		
from machine import Pin, UART
from tm1637 import TM1637
from pyb import Timer
from micropython import const

import json
import time
from collections import deque

from json_string import CMD

# total depth
RO_TANK_TOTAL_LEVEL = const(318)
SUB_TANK_TOTAL_LEVEL = const(410)

# UART buffer length
UI_UART_BUF_LEN = const(256)

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

		UI.id = 0
		UI.last_handshake_tick = 0
		UI.uart_connection = False

		# Init
		UI.tm = TM1637(Pin('X18'), Pin('X17'))
		UI.tm.brightness(0)		# darkest
		UI.tm.write([0, 0, 0, 0])

		UI.pi_uart = UART(1, 115200)
		UI.pi_uart.init(115200, timeout = 100)

		# Buffer
		UI.uart_buf = memoryview(bytearray(UI_UART_BUF_LEN))
		UI.uart_buf_len = 0

		UI.cmds = deque((), 5)

	def ProcessReportMsg(msg):
		UI.last_handshake_tick = time.ticks_ms()
		if UI.uart_connection == False:
			msg_local = {}
			msg_local[CMD.JSON_ACTION] = CMD.JSON_A_CONN
			UI.cmds.append(msg_local)
			UI.uart_connection = True
			UI.LogOut("Pi connection is ok")

	def ProcessGetMsg(msg):
		UI.LogOut("Get Msg" + str(msg['data']))

	def ProcessMsg(msg):
		try:
			data = json.loads(msg)
		except:
			data = None
		else:
			# put data input queue
			action = data[CMD.JSON_ACTION]
			if action is not None:
				if action == CMD.JSON_A_REPORT:
					UI.ProcessReportMsg(data)
				elif action == CMD.JSON_A_GET:
					UI.ProcessGetMsg(data)
				else:
					UI.cmds.append(data)

		UI.uart_buf_len = 0

	def Check():
		while 1:
			count = UI.pi_uart.any()
			if count == 0:
				break

			data = UI.pi_uart.read(count)
			if data:
				for e in data:
					if e == 0x0D or e == 0x0A:
						# decode buffer
						if UI.uart_buf_len == 0:
							continue
						else:
							UI.ProcessMsg(bytes(UI.uart_buf[0:UI.uart_buf_len]))
					else:
						UI.uart_buf[UI.uart_buf_len] = e
						UI.uart_buf_len += 1
		
		# Check connection
		if UI.uart_connection:
			if time.ticks_diff(time.ticks_ms(), UI.last_handshake_tick) > 5000:
				# lost connection, add a msg
				msg = {}
				msg[CMD.JSON_ACTION] = CMD.JSON_A_DISCON
				UI.cmds.append(msg)
				UI.uart_connection = False
				UI.LogOut("Pi connection disconnect.")

		return len(UI.cmds)

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
		UI.tm.number(UI.SubLevel)

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
		# UI.tm.number(UI.Temperature)

	def GetTemperature():
		return UI.Temperature

	# Power
	def SetPower(data):
		UI.dc_v 		= data['DC']
		UI.battery_v	= data['BAT']
		UI.dc_c 		= data['DC_C']
		UI.main_pump_c 	= data['MP_C']
		UI.Skim_pump_c 	= data['SP_C']

		UI.bat24v 		= data['bat24']
		UI.dc24_bat24 	= data['dc24bat']

	# Sensors
	def SetSensors(data):
		UI.Ro_ext_have_water = data['ROEW']
		UI.Ro_emergen_sensor = data['ROEM']
		UI.Sub_emergen_sensor = data['SUBEM']

	# Pump
	def SetSeaPump(on):
		UI.Sea_pump 		= on

	def SetRoExtPump(on):
		UI.Ro_ext_pump 		= on

	def SetRoPump(on):
		UI.Ro_pump 			= on

	def SetReverDc(on):
		UI.Rever_dc 		= on
	
	def SetMainPump(on):
		UI.Main_pump		= on

	def SetSkimPump(on):
		UI.Skim_pump		= on

	def SetMainWave(on):
		UI.Main_wave		= on

	def SetMainWaveBak(on):
		UI.Main_wave_bak 	= on

	def StatusReport(data):
		report_data = {}
		report_data[CMD.JSON_ACTION] = CMD.JSON_A_REPORT
		report_data[CMD.JSON_A_ID] = UI.id
		report_data[CMD.JSON_DATA] = data
		output = json.dumps(report_data) + '\r\n'
		UI.pi_uart.write(output)
		UI.id += 1

	def Response(id, err, data = None):
		resp_data = {}
		resp_data[CMD.JSON_ACTION] = CMD.JSON_A_RESPONSE
		resp_data[CMD.JSON_A_ID] = id
		resp_data[CMD.JSON_A_ERR] = err
		resp_data[CMD.JSON_DATA] = data
		output = json.dumps(resp_data) + '\r\n'
		UI.pi_uart.write(output)

	def LogOut(data):
		UI.pi_uart.write('###')
		UI.pi_uart.write(data)
		UI.pi_uart.write('\r\n')



# =============== Beep ================
class Beep:
	timer = None
	count = 0
	on_count = 0
	off_count = 0
	max_count = 0

	BEEP_MODE_NONE = const(0)
	BEEP_MODE_WARN = const(1)		# Warnning mode()
	BEEP_MODE_ERROR = const(2)		# Error mode()

	Beep_errors = None
	Beep_warns = None

	def Init():
		Beep.pin = Pin('X8', Pin.OUT)
		Beep.timer = Timer(1)
		Beep_errors = deque((), 5)
		Beep_warns = deuque((), 5)

	def Mode(mode):
		if mode == Beep.BEEP_MODE_NONE:
			return
		elif mode == Beep.BEEP_MODE_WARN:
			Beep.on_count = 3
			Beep.off_count = 500
	
		elif mode == Beep.BEEP_MODE_ERROR:
			Beep.on_count = 10
			Beep.off_count = 25

		Beep.max_count = Beep.on_count + Beep.off_count

	def Begin():
		Beep.timer.init(freq = 100, callback = Beep.beepCallback)

	def End():
		Beep.timer.deinit()
		Beep.pin.off()
		Beep.count = 0

	def SwitchMode(mode):
		Beep.End()
		Beep.Mode(mode)
		Beep.Begin()


	def beepCallback(timer):
		if Beep.count == 0:
			Beep.pin.on()
		if Beep.count == Beep.on_count:
			Beep.pin.off()
		Beep.count = 0 if Beep.count == Beep.max_count else Beep.count + 1
		
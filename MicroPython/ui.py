from machine import Pin, UART
from tm1637 import TM1637

import json

SubLevel = 0
RoLevel = 0
Temperature = 0
WorkMode = 0

# Init
tm = TM1637(Pin('X18'), Pin('X17'))
tm.brightness(0)		# darkest
tm.write([0, 0, 0, 0])

pi_uart = UART(1, 115200)
pi_uart.init(115200, timeout = 100)

def SetSubLevel(value):
	SubLevel = value
	data = {}
	data['Sub'] = SubLevel
	StatusReport(data)
	tm.number(SubLevel)

def GetSubLevel():
	return SubLevel

def SetRoLevel(value):
	RoLevel = value
	data = {}
	data['Ro'] = RoLevel
	StatusReport(data)

def GetRoLevel():
	return RoLevel

def StatusReport(data):
	output = json.dumps(data) + '\r\n'
	pi_uart.write(output)


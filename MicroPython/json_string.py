
class CMD:
	# const form json encode & decode
	JSON_ACTION			= 'a'
	JSON_A_ID			= 'id'		# get/set/resp id
	JSON_A_ERR			= 'err'		# for response
	JSON_DATA			= 'data'

	# Action
	JSON_A_REPORT		= 'rep'
	JSON_A_SET			= 'set'
	JSON_A_GET			= 'get'
	JSON_A_RESPONSE		= 'resp'

	# Internal use
	JSON_A_DISCON		= 'discon'
	JSON_A_CONN			= 'conn'

	# Internal command
	JSON_COMMAND		= 'cmd'

	JSON_COMMAND_CONN	= 'conn'
	JSON_CONN_STATUS	= 'status'

	JSON_RO_LEVEL		= 'ro'
	JSON_SUB_LEVEL		= 'sub'
	JSON_TEMPERATURE	= 'temp'

	JSON_MAIN_PUMP		= 'mp'
	JSON_SKIM_PUMP		= 'sp'
	JSON_WAVE_PUMP		= 'wp'
	JSON_WAVE_BAK		= 'wpb'
	JSON_RO_PUMP		= 'rp'
	JSON_RO_EXT_PUMP	= 'rep'
	JSON_SEA_PUMP		= 'seap'

	JSON_RO_EXT_WATER	= 'roew'
	JSON_RO_EMERGEN		= 'roem'
	JSON_SUB_EMERGEN	= 'subem'

	JSON_MAIN_VOLTAGE	= 'mv'
	JSON_BATTERY_VOL	= 'bv'
	JSON_MAIN_CURRENT	= 'mc'
	JSON_MAIN_PUMP_C	= 'mpc'
	JSON_SKIM_PUMP_C	= 'smc'

	JSON_BAT_24V		= 'bat24'
	JSON_DC_BAT			= 'dcbat'
	


	# Others
	JSON_ALARM_MODE		= 'alarm'

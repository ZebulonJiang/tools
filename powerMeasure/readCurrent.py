#! usr/bin/python
#coding=utf-8   //这句是使用utf8编码方式方法
import os
import sys
import ctypes

def readCurrent():
	debug 			= 0;
	src_path		= '';
	for i in range(0,len(sys.argv)):
		if(sys.argv[i]=="-d"):
			debug		= 1;
		if(sys.argv[i]=="-f"):
			src_path	= sys.argv[i+1];
	if(os.path.isfile(src_path)==False):	
		if(debug==1):	print("\'%s\'  is not exist"%(src_path))
		return -1
	

	f = open(src_path,'r')

	lines = f.readlines()
	count = len(lines)-4
	tmp = 15
	dataTmp = 2047
	powerTotal = 0
	powerList = {'VCCINT': '0x13', 
				'VCCBRAM': '0x14',
				'VCCAUX': '0x15',
				'VCC1V2': '0x16',
				'VCC3V3': '0x17',
				'VADJ_FMC': '0x18',
				'MGTAVCC': '0x72',
				'MGTAVTT': '0x73',
				'VCCPSINTFP': '0xa',
				'VCCPSINTLP': '0xb',
				'DDR4_DIMM_VDDQ': '0x1d',
				'VCCOPS': '0x10',
				'UTIL_3V3': '0x1a',
				'UTIL_5V0': '0x1b'
				}
	#参数排列顺序  RL(K) CL(uF) L(uH) IOUT_CAL_GAIN  IOUT_CAL_OFFSET
	dcrList={
		'0x13':(9.09,0.1,0.25,0.179931640625,2.3984375),
		'0x14':(0.549,0.1,0.68,20,0),
		'0x15':(0.360,0.1,2.2,44,0),
		'0x16':(1.960,0.1,3.9,16,0),
		'0x17':(1.40,0.1,2.0,14.203125,0.169921875),
		'0x18':(1.69,0.1,0.47,3,0),
		'0x72':(0.360,0.1,2.2,0,0),
		'0x73':(0.360,0.1,2.2,0,0),
		'0xa':(1.18,0.1,0.47,3.75,0),
		'0xb':(0.392,0.1,2.2,47,0),
		'0x1d':(1.33,0.1,1.15,7.8984375,0),
		'0x10':(1.33,0.1,1.15,7.5,-0.029998779296875),
		'0x1a':(4.99,0.1,0.68,1.099609375,0.7998046875),
		'0x1b':(1.74,0.1,1.5,8.40625,-0.139892578125)
	}

	def getDCR(addr):
		return dcrList[addr][2]/(dcrList[addr][0]*dcrList[addr][1])

	def getIoutCalGain(addr):
		return dcrList[addr][3]
		
	def getIoutOffset(addr):
		return dcrList[addr][4]
	print("powerNet    addr    voltage(V)    current(A)    power(W)")
	for i in range(1,count,4):
		cmd1 = lines[i][14:16]
		cmd2 = lines[i+2][14:16]
		if((cmd1 != '8B') or (cmd2 != '8C')):
			print("@Line:%d PmBus cmd is error.Please check it!"%(i+1))
			return -1
		##电压参数
		string = lines[i+1]
		addr = hex(int(string[0:2],16)/2)
		powerNet = list(powerList.keys())[list(powerList.values()).index(addr)]
		dataH = int(string[17:19],16)
		dataL = int(string[14:16],16)
		complement = 20
		complement = 16-((complement&tmp))
		data = float((dataH << 8) + dataL)	
		voltage = data/(2**complement)

		####电流参数
		string = lines[i+3]
		addr = hex(int(string[0:2],16)/2)
		DCR=getDCR(addr)
		dataH = int(string[17:19],16)
		dataL = int(string[14:16],16)
		complement = dataH/8
		if ((dataH & 0x80 ) == 0x80):
			complement = 16-((complement&tmp))
		else:
			complement = complement;
			
		data = (dataH << 8) + dataL
		#print("data  %d  %d"%(data,(data & 1024)))
		
		if ((data & 1024) == 1024):
			data = 1024 - (data & 1023)
			#print("data****%d"%(data))
		else:
			data = data
		
		data = float(data&dataTmp)
		readIout = data/(2**complement)
		IoutCalGain= getIoutCalGain(addr)
		IoutOffset = getIoutOffset(addr)
		current = (readIout ) * IoutCalGain/DCR
		#current = readIout
		power = voltage*current
		powerTotal = powerTotal + power
		print("%s    %s    %f    %f    %f    %f  %f"%(powerNet,addr,voltage,current,power,DCR,readIout))
	print("****** powerTotal=%f W ******"%(powerTotal))
	#print count

	f.close

readCurrent()

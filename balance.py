# Program for automatically balancing the capacitance bridge to obtain Vs for null voltage at balance point (or obtain list of Vs values that fit the same requirement)

import time
import visa
import serial
from check_length import check_length

rm = visa.ResourceManager()
lockin = rm.open_resource('GPIB0::5::INSTR') # should be lock-in amp's address, always check though

clock = 300e3 # clock frequency in Hz
n = 48 # bits of FTW
output = 100e3 # desired output frequency in Hz

ftw = int(output * (2**n / clock)) # calculate frequency tuning word
ftw_hex_str = string(hex(ftw_hex)) # convert to hex string
ftw_hex_str = check_length(ftw_hex_str[2:-1]) #eliminate 0x at beginning, make into two's complement hex string

#Vnode_vals0 = lockin.query_ascii_values('SNAP? 1,2') obtain x and y values from lockin

board = serial.Serial('/dev/cu.wchusbserial145410') # for my USB input ONLY; figure out how to generalize
frequency_command = '$WR02' +



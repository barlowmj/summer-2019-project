# Program for automatically balancing the capacitance bridge to obtain Vs for null voltage at balance point (or obtain list of Vs values that fit the same requirement)

import time
import visa
import serial

rm = visa.ResourceManager()
lockin = rm.open_resource('GPIB0::5::INSTR') # should be lock-in amp's address, always check though

clock = 300e3 # clock frequency in Hz
n = 48 # bits of FTW
output = 100e3 # desired output frequency in Hz

ftw = int(output * (2**n / clock)) # calculate frequency tuning word
ftw_hex_str = str(hex(ftw)) # convert to hex string
ftw_hex_str = ftw_hex_str[2:-1] #eliminate 0x at beginning

if len(ftw_hex_str) % 2 != 0:
    ftw_hex_str = '0' + ftw_hex_str

#Vnode_vals0 = lockin.query_ascii_values('SNAP? 1,2') obtain x and y values from lockin

# need to generalize locations
board1_location = '/dev/cu.wchusbserial145410'
board2_location = '/dev/cu.wchusbserial145420' # change end 10, 20, 30 depending on where in usb hub they are connected
board1 = serial.Serial(board1_location)
board2 = serial.Serial(board2_location)






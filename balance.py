# Program for automatically balancing the capacitance bridge to obtain Vs for null voltage at balance point (or obtain list of Vs values that fit the same requirement)

import time
import visa
from AD9854_DDS_Signal_Generator import Board

rm = visa.ResourceManager()
lockin = rm.open_resource('GPIB0::5::INSTR') # should be lock-in amp's address, always check though

#Vnode_vals0 = lockin.query_ascii_values('SNAP? 1,2') obtain x and y values from lockin

# need to generalize locations
board1_location = '/dev/cu.wchusbserial145410'
board2_location = '/dev/cu.wchusbserial145420' # change end 10, 20, 30 depending on where in usb hub they are connected
board1 = Board(board1_location)
board2 = Board(board2_location)








# Program for automatically balancing the capacitance bridge to obtain Vs for null voltage at balance point (or obtain list of Vs values that fit the same requirement)

import time
import visa
from AD9854_AC_board import Board

board2_gain = 3000
error = 1e-7
max_iterations = 20
known_cap = 100e-12

rm = visa.ResourceManager()
lockin = rm.open_resource('GPIB0::5::INSTR') # should be lock-in amp's address, always check though

# need to generalize locations – how??
board1_location = '/dev/cu.wchusbserial145410'
board2_location = '/dev/cu.wchusbserial145420' # change end to 10, 20, 30 depending on where in usb hub they are connected
board1 = Board(board1_location)
board2 = Board(board2_location)

# turns on OSK_EN and sets frequency multiplier to x10 (see class & documentation for reasoning)
board1.init_control_chip()
board2.init_control_chip()

# make board 2's gain a constant
board2.set_q_gain(board2_gain)

# Newton's method implementation
gain0, gain1 = 4095, 4075

board1.set_q_gain(gain0)
time.sleep(0.0005)
v0 = lockin.query_ascii_values('SNAP? 1,2')

board1.set_q_gain(gain1)
time.sleep(0.0005)
v1 = lockin.query_ascii_values('SNAP? 1,2')

slope = (v1[0]-v0[0])/(gain1-gain0)

gain2 = gain1 - v1/slope

i = 0
while (v1-0) < error and i < max_iterations:
    gain0 = gain1
    gain1 = gain2
    v0 = v1
    board1.set_q_gain(round(gain1))
    time.sleep(0.0005)
    v1 = lockin.query_ascii_values('SNAP? 1,2')
    slope = (v1-v0)/(gain1-gain0)
    gain2 = gain1 - v1/slope # theoretically more accurate than the previous gain value?
    i += 1

cap = round(gain2)*known_cap/board2_gain



# Program for automatically balancing the capacitance bridge to obtain Vs for null voltage at balance point (or obtain list of Vs values that fit the same requirement)

import time
import visa
#from AD9854 import Board
import sys
from serial import Serial

# check syntax for gain setting, etc: think it's "SET {channel} {gain} \r" but unclear from arduino code

def newtons_method(serial, lockin, gain0, gain1):
    max_iterations = 20
    #board1.q(gain0)
    serial.write(f'SET {gain0}\r')
    serial.read()
    time.sleep(0.0005) # adjust time based on tau – use the function already written?
    v0 = lockin.query_ascii_values('SNAP? 1,2')
    #board1.q(gain1)
    serial.write(f'SET {gain1}')
    serial.read()
    time.sleep(0.0005)
    v1 = lockin.query_ascii_values('SNAP? 1,2')
    slope = (v1[0]-v0[0])/(gain1-gain0)
    gain2 = gain1-v1/slope
    i = 0
    error = 1e-7
    while abs(v1) < error and i < max_iterations:
        gain0 = gain1
        gain1 = gain2
        v0 = v1
        #board1.q(round(gain1))
        serial.write(f'SET {gain1}\r')
        time.sleep(0.0005)
        v1 = lockin.query_ascii_values('SNAP? 1,2')
        slope = (v1-v0)/(gain1-gain0)
        gain2 = gain1-v1/slope  # theoretically more accurate than the previous gain value?
        i += 1

    return gain2

def main():

    board2_gain = 1500  # test various values, for now set to something reltively in the middle
    frequency = 100000  # 100kHz
    known_cap = 100e-12  # capacitance of the known capacitor

    # input the locations in command line; argv[0] is the script name
    board1_location = sys.argv[1]
    board2_location = sys.argv[2]

    gain0, gain1 = 4095, 4075

    # establish communication with the lock-in amplifier
    rm = visa.ResourceManager()
    lockin = rm.open_resource('GPIB0::5::INSTR')  # should be lock-in amp's address, always check though

    # need to generalize locations – how??
    # should be able to get general name for usb hub that goes in box once it arrives, might need to alter based on
    # OS though?
    # change end to 10, 20, 30 depending on where in usb hub they are
    # connected
    '''
    board1 = Board(board1_location)
    board2 = Board(board2_location)
    '''
    serial = Serial('board1_location')
    '''
    # turns on OSK_EN and sets frequency multiplier to x10 (see class & documentation for reasoning)
    board1.init_control_chip()
    board2.init_control_chip()
    '''
    # set frequency of the boards
    '''
    board1.f1(frequency)
    board2.f1(frequency)
    '''
    serial.write('INIT \r')
    serial.read()

    serial.write('*RDY?\r')
    serial.read()

    serial.write(f'FRQ {frequency}\r')
    serial.read()

    # set board 2's gain to a constant
    #board2.q(board2_gain)

    #null_gain = newtons_method(serial, lockin, gain0, gain1)

if __name__ == '__main__':
    main()



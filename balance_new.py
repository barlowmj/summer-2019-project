# version 2.0 of 'balance.py'
# program for automatically balancing the capacitance bridge

from time import sleep
import visa
from serial import Serial
import sys

def newtons_method(s, lockin, gain0, gain1): # returns gain value at which lockin reads ~0V
    # s is instance of serial class, lockin is instance of rm.open_resource('...'), gain0 and gain1 are two pre-determined test values of the gain for newton's method
    max_iterations = 20
    error = 1e-7 # maximum acceptable error
    s.write(f'SET, X1, {gain0}\r')
    s.read() # read to clear buffer
    sleep(0.0005)
    v0 = lockin.query_ascii_values('SNAP? 1,2')[0] # obtain voltage reading from lockin - returns list of two values, so index
    s.write(f'SET, X1, {gain1}\r')
    s.read()
    sleep(0.0005)
    v1 = lockin.query_ascii_values('SNAP? 1,2')[0]
    slope = (v1-v0)/(gain1-gain0)
    gain2 = gain1 - v1/slope
    i = 0
    while abs(v1) < error and i < max_iterations:
        gain0 = gain1
        gain1 = gain2
        v0 = v1
        s.write(f'SET, X1, {gain1}\r')
        s.read()
        sleep(0.0005)
        v1 = lockin.query_ascii_values('SNAP? 1,2')[0]
        slope = (v1-v0)/(gain1-gain0)
        gain2 = gain1 - v1/slope
        i += 1
    return gain2

def main():
    freq = 10e3 # Hz
    ve_gain = 1500/4095 # constant gain for V_e
    cx = 10e-12 # known capacitance
    gain0, gain1 = 4095/4095, 4075/4095 # test different values, inital gain values for newton's method

    # establish communication with lockin amplifier
    rm = visa.ResourceManager()
    lockin = rm.open_resoirce('GPIB0::5::INSTR')

    # use python -m serial.tools.list_ports or something similar to obtain serial port location of box,
    # input as command line argument
    location = sys.argv[1]

    # establish communicationb with ac box
    box = Serial('location')

    box.write('INIT \r') # initialize box
    box.read() # clear buffer

    box.write('*RDY? \r') # check if ready
    box.read()

    box.write(f'FRQ, {freq} \r') # set frequency
    box.read()

    box.write(f'SET, X2, {ve_gain} \r') # set constant excitation voltage gain
    box.read()

    null_gain = newtons_method(box, lockin, gain0, gain1) # obtain appropriate gain value from newtons method

    cs = cx * null_gain / ve_gain # calculate sample capacitance

    print(cs)

if __name__ == '__main__':
    main()
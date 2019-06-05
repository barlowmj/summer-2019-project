# Program for automatically balancing the capacitance bridge to obtain Vs for null voltage at balance point (or obtain list of Vs values that fit the same requirement)

import time
import sh
import visa
from numpy import sqrt

acc = 1e-6 # set accuracy req
Vs_values = [] # make empty list to store Vs values? decide if this is the way to output the data or if txt file is better
gpp = sh.Command('g++') # call gpp('filename.c/pp', '-o', 'filename'), then call Command('./filename') to run the C/++ program that controls the board
rm = visa.ResourceManager()
lockin = rm.open_resource('GPIB0::5::INSTR') # should be lock-in amp's address, always check though – also commands to reset it?


# need to initialize amplitude of Vs (run c/cpp file through sh)

Vs0 = 25 # come up with better numbers when boards arrive and can test, also see about units

# obtain node voltage from lockin (after delay – see how long)

time.sleep(1) # set to 1 second for now, probably insufficient – look into time constant to see if settle time gets better

# time constant: increasing makes output more steady, but also takes 5 time constants to settle, have to determine st trade-off is good

Vnode_x0 = lockin.query_ascii_values('OUTP? 1')[0]
Vnode_y0 = lockin.query_ascii_values('OUTP? 2')[0]
Vnode0 = sqrt(Vnode_x0**2 + Vnode_y0**2)

# repeat for slightly lower Vs to obtain next data point for loop

# set voltage amplitude (sh)

Vs1 = 20 # ditto comment from Vs0

# obtain node voltage from lockin

time.sleep(1)

Vnode_x1 = lockin.query_ascii_values('OUTP? 1')[0]
Vnode_y1 = lockin.query_ascii_values('OUTP? 2')[0]
Vnode1 = sqrt(Vnode_x1**2 + Vnode_y1**2)

# set next Vs from Newton's method algorithm

Vs2 = Vs1 - Vnode1*(Vs1 - Vs0)/(Vnode1 - Vnode0)

# obtain node voltage from lockin

time.sleep(1)

Vnode_x2 = lockin.query_ascii_values('OUTP? 1')[0]
Vnode_y2 = lockin.query_ascii_values('OUTP? 2')[0]
Vnode2 = sqrt(Vnode_x1**2 + Vnode_y1**2)

while abs(Vnode2) > acc:
    # reset parameters
    Vnode0 = Vnode1
    Vnode1 = Vnode2
    Vs0 = Vs1
    Vs1 = Vs2
    # Newton's method
    Vs2 = Vs1 - Vnode1*(Vs1 - Vs0)/(Vnode1 - Vnode0)
    # delay
    time.sleep(1)
    # obtain node voltage, at end runs accuracy check
    Vnode_x2 = lockin.query_ascii_values('OUTP? 1')[0]
    Vnode_y2 = lockin.query_ascii_values('OUTP? 2')[0]
    Vnode2 = sqrt(Vnode_x1**2 + Vnode_y1**2)

# add Vs to a list? or export to file?

Vs_list.append(Vs2)

# should repeat this process to obtain and output Vs values, can then process to determine Cx from known Cs, Ve amplitudes


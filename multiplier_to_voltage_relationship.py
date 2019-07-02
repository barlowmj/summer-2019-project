from AD9854_DDS_Signal_Generator import Board
from numpy import arange, array
from numpy.linalg import norm
from pylab import plot, xlabel, ylabel, title, figure, show
import time
import serial
import visa

board = Board('/dev/cu.wchusbserial145410')
board.set_control_chip()
board.set_i_gain(1)

rm = visa.ResourceManager()
lockin = rm.open_resource('GPIB0::5::INSTR')

f = open('trial_x.txt', 'w+')

mult_vals = arange(1, 4096, 1)

vx_vals = []
vy_vals = []
voltage_vals = []
for m in mult_vals:
    board.set_i_gain(m)
    time.sleep(0.0005) # change depending on time constant of lock-in
    voltage = lockin.query_ascii_values('SNAP? 1,2', container=array)
    vx_vals.append(voltage[0])
    vy_vals.append(voltage[1])
    voltage_vals.append(norm(voltage))
    f.write(f'{voltage[0]}\n')

f.close()

figure(1)
plot(mult_vals, voltage_vals)
xlabel('Multiplier value')
ylabel('Voltage amplitude')
title('Voltage vs Multiplier value')

figure(2)
plot(mult_vals, vx_vals)
xlabel('Multiplier value')
ylabel('x-component of voltage amplitude')
title(f'V_x vs Multiplier value')

figure(3)
plot(mult_vals, vy_vals)
xlabel('Multiplier value')
ylabel('y-component of voltage amplitude')
title(f'V_y vs Multiplier value')

show()